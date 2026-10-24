# DEP-14: Attestation Verification Service

## Abstract

This document specifies an optional opt-in verifier role that issues durable Nostr attestations linking a public key to one of several externally-attestable identities — a lightning-address domain (NIP-05, lightning-challenge), a manual proclamation by an already-trusted account, or anonymous web-of-trust ring-signature membership (DEP-15). Operators MAY require a valid attestation to authorize `deposit_open` (DEP-08), enabling per-domain or per-graph access control without the operator itself running any non-Nostr infrastructure.

The protocol is deliberately scoped: a verifier issues *cryptographically-signed claims about identity*, and an operator decides what to do with them. Reputation, rate-limiting, and policy live with the operator and are out of scope here.

## Motivation

DEP-08 defines the deposit lifecycle and references "access control" without specifying how an operator decides whether a `deposit_open` request comes from a trustworthy sender. Three concrete signals are relevant:

1. **Pubkey allowlist** — a static list of npubs the operator manually trusts. Already specified in DEP-08; needs no protocol surface.
2. **Subkey delegation** — DEP-04 already lets an allowlisted account delegate its trust to an ephemeral key.
3. **External identity attestation** — the operator wants evidence that the requester controls a particular lightning address, has been vouched for by an allowlisted account, or is a member of a curated social graph. This is the gap DEP-14 closes.

A verifier is run as a separate service (the reference implementation is `lnaddr-attest` in this repository). Operators publish a single environment variable — `ATTESTATION_VERIFIER_PUBKEY` — pointing at the verifier they trust; the verifier's signed attestations then become the access-control credential.

## Roles

- **Verifier** — a Nostr identity that issues attestations. Holds a long-term BIP-340 keypair; signs both ephemeral verify responses (Kind 25501) and durable attestations (Kind 55502). Connected to the durable ledgers relay and the ephemeral messaging relay (DEP-04).
- **Subject** — the npub the attestation describes. Often the same key that originated the verification request, except in the `proclaim` flow.
- **Requester** — the npub that signs the verification request. Equal to the subject in all flows except `proclaim`.
- **Operator** — the deposits-node operator whose `deposit_open` is being gated. Configures `ATTESTATION_VERIFIER_PUBKEY` and access lists; calls `check_attestation` on each request.

## Verification Methods

A verifier MUST implement at least one method and MAY implement any subset of those listed below. Each method produces an attestation distinguishable by the `method` field on the Kind 55502 content (see "Attestation Event").

### 1. NIP-05 Domain Attestation

The subject claims a lightning-address `<user>@<domain>`. The verifier:

1. Fetches `https://<domain>/.well-known/nostr.json?name=<user>` (NIP-05).
2. Confirms the resulting `pubkey` field equals the subject's xonly hex.
3. Issues a Kind 55502 attestation carrying `method: "nip05"`, `lightning_address: "<user>@<domain>"`.

The verifier SHOULD cache `nostr.json` per-domain with a short TTL (default 5–60 seconds for tests, longer for production). Operators consuming this attestation match `<domain>` against their `deposit_domain_allowlist.txt`.

### 2. Lightning Challenge Attestation

The subject claims a lightning-address `<user>@<domain>`. The verifier:

1. On request `action: "link"`: emits a BOLT-11 invoice for `challenge_sats + num_payments × fee_fallback_sats`, returns `{ session_id, invoice, amount_sats }`.
2. On request `action: "challenge"` (after the user pays the invoice): pays `num_payments` random amounts summing to `challenge_sats` *to* the subject's lightning address.
3. On request `action: "verify"` carrying the list of amounts the subject observed: confirms the amounts match (set equality) and issues a Kind 55502 attestation with `method: "challenge"`, `lightning_address: "<user>@<domain>"`.

A verifier MUST reject `verify` events submitted outside `timeout_secs` of session creation, MUST reject more than `max_attempts` `verify` failures per session, and SHOULD reject any `challenge` request whose paid invoice the verifier did not previously emit.

The challenge flow is sound under the assumption that an attacker cannot intercept lightning payments to the claimed address. A subject who genuinely controls the address sees the random amounts; an impostor does not.

### 3. Proclaim Attestation

An already-trusted requester (one whose xonly appears in the verifier's `VERIFY_ALLOWLIST_FILE`, typically a bind-mount of the operator's `deposit_allowlist.txt`) vouches for an arbitrary subject by submitting `action: "proclaim", attest_pubkey: "<subject xonly>"`. The verifier:

1. Reads `VERIFY_ALLOWLIST_FILE` fresh each request.
2. Rejects if the requester's xonly is not present.
3. Issues a Kind 55502 attestation tagged `#p` with the *subject*'s xonly, content carrying `method: "proclaim"`, `allowlist_npub: "<requester xonly>"`.

This lets a manually-allowlisted account onboard an ephemeral key for one-shot operations — for example, a user holding a hardware wallet may proclaim their daily-driver phone key without copying the hardware key onto the phone.

### 4. Ring-Signature Attestation

The subject proves membership in one of the verifier's published anonymity rings, without revealing which ring member they are, by submitting a Kind 25502 first-contact event. The wire format and verification procedure are specified in DEP-15. On a valid first-contact event, the verifier issues a Kind 55502 attestation tagged `#p` with the subject's *bound* pubkey (not their underlying ring-member key), content carrying `method: "ringsig"`, `nullifier: "<32-byte hex>"`.

A wallet using ringsig attestation MUST sign subsequent `deposit_open` requests under the bound pubkey, since that is the npub the operator's `check_attestation` will look up. The attestation does not record `lightning_address` or `allowlist_npub` — anonymity-set membership *is* the access criterion.

## Wire Format

### Kind 25500 — Verify Request (ephemeral, gift-wrapped)

Wallets MUST send verify requests as NIP-59 gift-wraps. The wrap envelope is:

- Outer event: `kind: 1059`, encrypted with NIP-44 to the verifier's pubkey, `pubkey` set to a one-shot ephemeral key.
- Seal: `kind: 13`, encrypted with NIP-44 by the wallet's real signing key.
- Rumor: `kind: 25500`, content is a JSON object with at least an `action` field selecting the method.

The rumor schema is method-specific; the union accepted by the reference verifier is:

```json
{
  "action": "link" | "challenge" | "verify" | "nip05" | "proclaim",
  "lightning_address": "user@domain",     // link / challenge / verify / nip05
  "session_id": "...",                    // challenge / verify
  "amounts": [123, 456, 421],             // verify
  "attest_pubkey": "<xonly hex>"          // proclaim (subject npub)
}
```

A verifier MUST reject any rumor whose `action` is not on its supported-methods list, and SHOULD reject any field combination not consistent with the specified action.

### Kind 25501 — Verify Response (ephemeral, gift-wrapped)

The verifier replies by gift-wrapping a Kind 25501 rumor back to the original requester, addressed via the `#p` tag on the outer wrap. The rumor body is:

```json
{ "status": "verified" | "rejected" | "challenge_pending" | "invoice",
  "method": "nip05" | "challenge" | "proclaim",
  "attestation_event_id": "<hex>",         // verified
  "lightning_address": "user@domain",      // verified (nip05/challenge)
  "allowlist_npub": "<xonly hex>",         // verified (proclaim)
  "invoice": "lnbc...",                    // invoice
  "session_id": "...",                     // challenge_pending / invoice
  "message": "..." }                       // rejected
```

The response is correlated with the request via the gift-wrap envelope's outer `#p` and the rumor's `session_id` (when relevant). The 25501 reply is for synchronous UX feedback only — the durable record is the Kind 55502 below.

### Kind 25502 / 25503 — Ringsig Request / Response (ephemeral, plain-signed)

Specified in DEP-15. Unlike Kind 25500, ringsig events are not gift-wrapped: the bound pubkey is the *purpose* of the event and is signed in the clear.

### Kind 55502 — Attestation (durable)

The persistent record. Published by the verifier on the durable ledgers relay; consumed by the operator's `check_attestation` (see below).

Kind 55502 is a regular event, outside both replaceable ranges of NIP-01, so relays keep every attestation a verifier publishes. That is intended: an attestation is never overwritten. A verifier withdraws one by publishing a revocation (see "Revocation"), and a correction is a new attestation.

```json
{
  "kind": 55502,
  "pubkey": "<verifier xonly>",
  "tags": [
    ["p", "<subject xonly>"]           // the npub being attested for
  ],
  "content": "{...AttestationContent...}",
  "sig": "<verifier BIP-340 sig>"
}
```

The `#p` tag is the index operators query on. A subject may hold any number of attestations, for the same or different methods; none replaces another.

`AttestationContent`:

```json
{
  "npub": "<subject xonly>",
  "method": "nip05" | "challenge" | "proclaim" | "ringsig" | "revoked",
  "verified_at": "<ISO-8601 timestamp>",
  "lightning_address": "user@domain",   // nip05 / challenge only
  "allowlist_npub": "<xonly hex>",      // proclaim only
  "nullifier": "<32-byte hex>",         // ringsig only, diagnostic
  "revokes": "<event id hex>",           // revoked only
  "reason": "..."                        // revoked only, optional
}
```

A consumer MUST verify the event signature against the configured verifier xonly, MUST confirm the `#p` tag matches the subject of interest, MUST disregard any attestation the same verifier has revoked (see "Revocation"), and MUST dispatch on `method` to apply the matching access-control rule.

### Revocation

A verifier withdraws an attestation by publishing another Kind 55502 event with `method: "revoked"`, the same `#p` subject, and an `#e` tag naming the attestation it withdraws:

```json
{
  "kind": 55502,
  "pubkey": "<verifier xonly>",
  "tags": [
    ["p", "<subject xonly>"],
    ["e", "<id of the attestation being revoked>"]
  ],
  "content": "{\"npub\": \"<subject xonly>\", \"method\": \"revoked\", \"revokes\": \"<same id>\", \"verified_at\": \"...\"}",
  "sig": "<verifier BIP-340 sig>"
}
```

The content's `revokes` MUST equal the `#e` tag. A revocation with no `#e` tag, more than one, or a `revokes` that differs from it is malformed, and a consumer MUST ignore it, so one event can't say two different things.

Revocation is terminal. A consumer that has seen a valid revocation, signed by the attestation's own verifier, MUST treat the revoked attestation as void, whatever either event's `created_at` or `verified_at` says. A revocation cannot itself be revoked; to restore access, the verifier issues a new attestation.

Ordering comes from the reference, never from timestamps. A revocation names exactly the event it voids, so it does not matter which was published first or what dates either carries. Because the operator's single query on `#p` returns attestations and revocations together, no second lookup is needed.

### Time

`created_at` and `verified_at` are values the verifier chose. A consumer MUST NOT treat them as evidence of when anything happened, and MUST NOT use them to order attestations or to decide between an attestation and its revocation. They are informational: useful in logs and to a human, not to policy.

Nostr has no trusted clock, and depending on one would reintroduce the central party this protocol avoids. Where a deployment genuinely needs a bound in time, it anchors to Bitcoin instead of trusting a date:

- **Not before.** A verifier MAY add `["block", "<height>", "<block hash>"]` naming a recent block. The attestation cannot have been made before that block existed.
- **Not after.** A verifier or anyone else MAY timestamp the attestation's id with OpenTimestamps (NIP-03). The attestation existed by the block the proof commits to.

A consumer that relies on either MUST verify it against its own view of the chain.

## Operator-Side Consumption

An operator opts in by setting:

- `ATTESTATION_VERIFIER_PUBKEY` — the verifier xonly to trust. Without this, attestation lookup is disabled and the operator falls back to pubkey-allowlist-only access control (DEP-08).
- `deposit_allowlist.txt` — npubs accepted unconditionally, also used for the `proclaim` path.
- `deposit_domain_allowlist.txt` — domains whose lightning-address attestations are accepted.

On each `deposit_open` request the operator computes the *effective sender* (subject account after DEP-04 subkey resolution) and checks, in order:

1. Effective sender ∈ `deposit_allowlist` ⇒ accept.
2. Otherwise, fetch Kind 55502 events authored by the configured verifier and tagged `#p` with the effective sender. For each:
   - `method = "nip05"` or `"challenge"` and `lightning_address`'s domain ∈ `deposit_domain_allowlist` ⇒ accept.
   - `method = "proclaim"` and `allowlist_npub` ∈ `deposit_allowlist` ⇒ accept.
   - `method = "ringsig"` ⇒ accept (anonymity-set membership is the criterion; the operator trusts the verifier's signature).

   Before accepting, discard every attestation whose id appears in the `#e` tag of a well-formed `method = "revoked"` event (one `#e` tag, equal to `revokes`) from the same verifier in the same result set.
3. No matching attestation ⇒ reject with `code: "not_authorized"`. The reject MAY carry `attestation_required: true` to nudge the wallet to initiate verification.

The operator MUST NOT re-verify the cryptographic content of an attestation beyond the BIP-340 signature on the Kind 55502 event itself. The verifier is the trust anchor by configuration; second-guessing its decisions defeats the abstraction.

## Verifier Configuration

The reference verifier reads its configuration from environment variables (and `_FILE` indirections for secrets):

| Variable | Purpose |
|---|---|
| `VERIFY_NSEC_FILE` | Path to the verifier's secret key (hex or nsec1) |
| `VERIFY_RELAYS` | Comma-separated relay URLs (durable + messaging) |
| `VERIFY_CHALLENGE_SATS` | Default challenge amount (default 1000) |
| `VERIFY_NUM_PAYMENTS` | Number of random payments per challenge (default 3) |
| `VERIFY_TIMEOUT_SECS` | Session timeout (default 600) |
| `VERIFY_FEE_FALLBACK_SATS` | Per-payment fee budget when probing (default 10) |
| `VERIFY_NIP05_CACHE_SECS` | Per-domain `nostr.json` TTL |
| `VERIFY_COVER_REFRESH_SECS` | Ringsig cover republish cadence (DEP-15) |
| `VERIFY_ALLOWLIST_FILE` | Path to the allowlist consulted by `proclaim` |
| `VERIFY_CA_CERT` | Optional custom CA bundle for HTTPS probes |

A verifier MAY support additional methods or configuration; it MUST NOT issue an attestation whose `method` field is not specified in this DEP or a successor. A consumer MUST ignore any `method` it does not recognise, except `revoked`, which every consumer MUST honour.

## Security Considerations

**Verifier trust.** The verifier is fully trusted by every operator who configures it. A compromised verifier can issue attestations for any subject, bypassing access control on every operator that trusts it. Operators SHOULD review the verifier's behavior and SHOULD treat verifier compromise the way they treat root CA compromise.

**Attestation longevity.** Kind 55502 events persist on the durable relay until garbage-collected by the operator's relay policy. An attestation issued today and trusted today might still be on-relay months later. A verifier bounds that exposure by revoking attestations it no longer stands behind, or by rotating its signing key. A lifetime written into the attestation (a `verified_at`-relative TTL) does not bound it: the verifier chooses that date, and so can anyone who obtains the verifier's key.

**Verifier key compromise and revocation.** Whoever holds the verifier's key can issue attestations; they cannot undo a revocation. That is why revocation is terminal and keyed on event ids rather than on timestamps: a later-dated re-issue of a revoked attestation is a different event, and it is that new event, not a resurrection of the old one, that the operator must decide whether to trust. Operators who suspect the key SHOULD stop trusting the verifier, not wait for a revocation.

The same property cuts the other way: whoever holds a stolen verifier key can revoke every attestation that key ever issued, permanently. That is a denial of service, not an escalation, and the only remedy is new attestations under a new key.

**Withheld revocations.** The operator learns of a revocation only from the relays it queries. A relay that drops or withholds the revocation leaves the attestation standing. This is within the trust the operator already places in its verifier and relays, but operators who care SHOULD query more than one relay for the `#p` result set, and verifiers SHOULD publish revocations to every relay they publish attestations to.

**Domain-allowlist scope.** A `nip05` or `challenge` attestation only proves control of a *specific* lightning address. An operator that allowlists `example.com` must trust that *every* `*@example.com` is appropriate to onboard. This is the same trust assumption as TLS certificate authority: scope the allowlist to domains whose user-vetting policy you trust.

**Lightning-challenge soundness.** The challenge flow is sound only if the verifier's lightning payments succeed — a verifier with a flaky lightning node may produce false negatives but cannot produce false positives. The verifier SHOULD use a reliable LN node and SHOULD cache fee estimates so transient fee spikes don't fail otherwise-valid verifications.

**Proclaim authority.** A proclaim request lets a single allowlisted account vouch for an arbitrary npub. Operators SHOULD audit `deposit_allowlist.txt` regularly; an allowlisted key whose private material has leaked can be used to onboard arbitrary other identities. The proclaim flow does NOT support quorum-vouching in this version of the DEP.

## Privacy Considerations

The Kind 25500 verify request is gift-wrapped (NIP-59), so a relay observer cannot link the requester's npub to the lightning address being attested. The Kind 55502 attestation, however, is a public claim by definition — it's the durable record an operator looks up — and so links the subject npub to whichever identifier (`lightning_address`, `allowlist_npub`) the method emits.

Operators wishing to gate access without correlating identities to deposits SHOULD use the ringsig method (DEP-15), which records only an opaque pseudonym (`nullifier`) and the subject's bound pubkey, never the underlying ring-member key.

## Related DEPs

- [DEP-04](DEP-04.md): Peer messaging (gift-wrap envelope, advertisement format)
- [DEP-08](DEP-08.md): Deposits (where `check_attestation` is invoked)
- [DEP-15](DEP-15.md): Anonymous web-of-trust ring signatures (the `ringsig` method)

## References

- NIP-05: Mapping Nostr keys to DNS-based identifiers
- NIP-44: Versioned encryption
- NIP-59: Gift Wrap
- LUD-06 / LUD-16: lnurl-pay over lightning addresses
- BOLT #11: Invoice format
