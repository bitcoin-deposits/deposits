# DEP-19: Operator Inactivity and Proof Consolidation

Status: Draft (analysis/, 2026-09-05)

## Abstract

This document adds a respectful fraud-proof type for operator inactivity, bounding
depositor holds by a negotiated block count rather than by `quorum_expiry`; merges
the two non-conformance proof types into one whose accused may be any signer of a
bad update; states the duty of a quorum to act on proofs against its own operator
wherever they arise; generalises the DEP-12 service clock to causal visibility; makes
co-sign refusal provable; adds checkable quorum-composition rules; and closes three
post-expiry edges. It does not change
the on-chain script.

## Motivation

The protocol's first goal is deposit stability. Its proofs cover misbehaviour but not
absence. When an operator stops publishing, the only respectful trigger is
`QuorumExpired`, so depositors wait for the end of the rotation cycle plus the tier
offsets even when a live majority could spend the vault at once through Tier 0.
Modelled over a 2016-block cycle, that hold averages about eight days and reaches
two weeks at the 95th percentile regardless of member reliability. With an
inactivity trigger of 144 blocks and a live majority, the same hold is about two
days (`analysis/04-findings.md` F1, F15).

Separately, DEP-05 promises that misbehaving as a co-signer is slashable on the
member's own ledger, but no DEP proof type names a co-signer as the accused, and no
DEP states a duty for the member's own quorum to act. The reference implementation
carries `NonConformingCosignature` and `Equivocation` types that the DEPs lack.

## Specification

### 1. Inactivity parameter

`QuorumAddMember` (DEP-02) gains a field:

| Type | Name | Size | Description |
|---|---|---|---|
| TBD | inactivity_blocks | 4 | Blocks without a co-signed update after which the member may attest inactivity |

The strictest (smallest) value across active members applies, as for the other
timing parameters in DEP-05 §Member Terms. Suggested default: 144. `QuorumBegin`
records the effective value alongside `quorum_expiry`.

The operator can always break silence: `FeeCollect`, a self-transfer from any
deposit they control, or any establishment operation. A ledger whose operator holds
no deposit and has nothing to collect MAY append a no-op update (a `Batch` of zero
operations, DEP-02 disc 90) for this purpose. Silence is therefore unambiguously the
operator's choice.

### 2. Inactivity attestation

A quorum member attests inactivity by signing:

    tag = SHA256("deposits/inactivity")
    data = ledger_id || last_sequence (8 LE) || last_update_hash || anchor_block_hash
    digest = SHA256(tag || tag || data || member_ledger_hash)

where `last_update_hash` is the most recent update the member has validated and
co-signed on the target ledger, and `anchor_block_hash` is a block the member
observes at height `≥ last_update.block_height + inactivity_blocks`. The
`member_ledger_hash` binds the attestation into the web of causality exactly as a
co-signature does (WP §time).

Attestations are published as Kind 9107 events (`deposits/inactivity`, durable).

### 3. `QuorumInactive` fraud proof

A new respectful proof type. Evidence:

- `last_sequence`, `last_update_hash`, `last_block_height` of the target ledger
- `anchor_block_hash`
- `inactivity_blocks` as recorded in the effective `QuorumBegin`
- a set of attestations from distinct active members, each over the same
  `(ledger_id, last_sequence, last_update_hash, anchor_block_hash)`

Verification:

1. `anchor_block_hash` is in the verifier's confirmed chain at height `h`.
2. `h ≥ last_block_height + inactivity_blocks`.
3. `last_update_hash` is the tip of the target ledger in the verifier's view, with no
   majority-co-signed update after it. The verifier MUST query at least two relays
   before concluding absence.
4. The attesting set is a strict majority of the active members recorded in the
   effective `QuorumBegin`, and every attestation verifies.
5. `inactivity_blocks` matches the effective `QuorumBegin`.

Absence is not provable from a chain alone; the majority attestation is the proof.
It is the same majority that would have had to co-sign any activity, so a forged
inactivity claim requires the same collusion that could already freeze the ledger by
withholding co-signatures.

Classification: **respectful**. The confiscation transaction is bifurcated as for
`QuorumExpired` (DEP-03): obligations to the lottery output, change including
collateral to the operator's pubkey. The proof does not propagate cross-ledger.

Threshold and tier: a `QuorumInactive` confiscation spends through Tier 0 and
requires a strict majority at every point in the lifecycle. It does not cascade;
past `quorum_expiry` the existing `QuorumExpired` path provides the minority and
solo-member tiers.

### 4. Race with resumed activity

From `DisputeEnter` citing `QuorumInactive`, members MUST refuse to co-sign updates
on the target ledger (DEP-05 §Co-Signer Obligations #5 already requires this). An
operator who resumes before any member enters a dispute simply continues; the
attestations become moot because condition 3 above fails.

If a member both attests inactivity at `last_sequence` and later co-signs an update
at `last_sequence + 1` whose `block_height` precedes the anchor, the two signatures
are mutually inconsistent and constitute a punitive `NonConforming` proof (§5)
against that member.

### 5. Consolidated non-conformance proof

`NonConformingUpdate` and the implementation's `NonConformingCosignature` are
replaced by a single punitive type, `NonConforming`, with evidence:

- `fault_ledger_id` and the offending signed update
- `accused_pubkey`, which MUST appear on the update as `operator_id` or in
  `cosignatures`
- the rule violated, as a discriminant from DEP-05 §Co-Signer Obligations, DEP-11,
  or DEP-16 §fraud proofs

The proof MAY be presented against any ledger the accused operates. `ledger_id` in
the proof names the ledger being disputed, which need not be `fault_ledger_id`.
Presenting the proof on a ledger the accused merely co-signs for has no effect; the
accused's stake is on the ledgers they operate.

`Equivocation` (two operator signatures at one sequence) is NOT a proof type. DEP-02
requires the operator to sign after collecting the threshold, so two canonical
updates at one sequence imply a member who co-signed both, which is a `NonConforming`
fault of that member. Two operator-signed updates without a majority are both
non-canonical and harm no one. Implementations MAY surface such pairs as a
reputational signal.

### 6. Duty to act on proofs (DEP-11 amendment)

DEP-11 §Dispute Participation is amended. A member is derelict if, within
`dispute_response_blocks` of a valid punitive proof becoming causally visible to
them, they have neither appended `DisputeEnter` nor (if a dispute is already open)
appended `DisputeArmed` or signed the confiscation transaction. "Causally visible"
means the proof hash is embedded on a ledger whose state the member has since
referenced in a `member_ledger_hash`, on any ledger.

This applies equally when the accused is the operator of the member's ledger and the
fault occurred elsewhere (`fault_ledger_id ≠ ledger_id`). Cross-ledger contagion is
thereby a duty with the same dereliction proof as local evidence, not a permission.

### 7. Post-expiry edges

- **Degraded rebuild.** A `QuorumBegin` at Tier 1 or Tier 2 MUST stage only pubkeys
  that were active members of the expiring quorum. New members may be added by a
  subsequent Tier 0 rotation once the ledger is re-established.
- **Tier 3.** An operator spend through the Tier 3 path does not extinguish
  obligations. Any later ledger the operator runs MAY be disputed under
  `NonConforming` with the Tier 3 spend and the unpaid obligations as evidence.
- **Wallet exit triggers.** Wallets SHOULD withdraw on any of: quorum size reduced
  below the size at deposit opening; a `QuorumBegin` past `quorum_expiry`; a
  `QuorumInactive` or `QuorumExpired` dispute; a custody change to a winner whose new
  quorum the wallet has not evaluated.

### 8. Causal visibility and the service clock (DEP-12 amendment)

DEP-12 starts `service_response_blocks` at the `DeliveryEmbed` block. The DEP-06
"further" fallback, embedding on an unrelated ledger and waiting for propagation,
therefore never starts a clock. This section replaces the start rule.

A hash is **causally visible** to a pubkey at the first update, on any ledger, that
the pubkey signed (as operator or co-signer) and whose causal chain (DEP-06
§Broadcast) reaches the embed. For a `DeliveryEmbed` on a member's ledger this is
the target operator's next co-signed update carrying that member's advanced
`member_ledger_hash`, as today. For an embed elsewhere it is whenever the chain
arrives.

`service_response_blocks` starts at the `block_height` of the update that made the
request hash causally visible to the target operator, not at the embed. The
censorship proof (DEP-12 §Censorship Proof Construction) cites that update as the
causal link and a later operator-signed update past the deadline as the breach.

Consequences: a wallet may embed on any ledger it can reach; a member's refusal to
embed (DEP-12 §Incentives) is no longer a hard block, only a delay proportional to
the path length; and the same definition serves §6 and §9 below.

### 9. Provable co-sign refusal (DEP-05 / DEP-11 amendment)

Withholding co-signatures is not observable today (DEP-11 §Co-signing: "not
protocol-enforced"). A majority that withholds freezes a healthy ledger without
evidence and inherits it. This section makes *active* withholding provable; fully
silent members are handled by §1–3 on their own ledgers.

**Proposal signature.** Before collecting co-signatures, the operator signs the
update as a proposal:

    tag = SHA256("deposits/propose")
    digest = SHA256(tag || tag || cosign_data)

with `cosign_data` as in DEP-02 §Co-signing. The proposal is published as a Kind
9108 event. It carries no `member_ledger_hash` and is not an update; it commits the
operator to the content at that sequence.

**Embedding.** The operator, or anyone, may embed `SHA256(proposal)` on any ledger
(§9). For a member `M`, visibility is normally achieved by embedding on a ledger
operated by one of `M`'s own quorum members: `M`'s next update as operator carries
that member's hash and `M`'s signature.

**`cosign_response_blocks`.** A new `QuorumAddMember` field, strictest wins,
suggested default 72. Within that many blocks of a proposal becoming causally
visible to `M`, `M` MUST do one of:

- co-sign the proposal (the update then proceeds normally), or
- publish a signed `CosignRefusal` (Kind 9109) over the proposal hash citing a
  rule discriminant from DEP-05 §Co-Signer Obligations, DEP-11, or DEP-16.

**Proofs.** Two new punitive proofs, both under `NonConforming` (§5) with the
member as accused:

- *Silent withholding*: the proposal was causally visible to `M` at block `v`; `M`
  signed some update at `block_height ≥ v + cosign_response_blocks`; no
  co-signature by `M` on that sequence and no `CosignRefusal` exist. Verifier queries
  at least two relays before concluding absence.
- *Unfounded refusal*: `M`'s `CosignRefusal` cites a rule that the proposal does
  not violate when applied to the public ledger state at `previous_hash`.
  Validity is deterministic, so any verifier can check it.

A refusal citing a rule the proposal *does* violate is conforming and is also the
operator's fault, provable as `NonConforming` against the operator if the proposal
was published (the operator proposed a bad update). Operators therefore SHOULD
propose only what they expect to pass.

**Limits.** A member who signs nothing anywhere is not "active" and cannot be
derelict; such a member is losing their own ledgers under §1–3 at
`inactivity_blocks`. A majority that both withholds here and lets their own
ledgers lapse pays with every ledger they operate, which is the collateral web
working as intended. The freeze itself still lasts until the inactivity trigger
(§1) lets the remaining members, or the same majority, move custody.

### 10. Quorum composition rules (DEP-05 amendment)

Trust cannot be specified; the following can be checked by co-signers from public
data and force a coalition either to expose real collateral under honest reach or to
appear as a visible cluster.

**11.1 Member vault size.** A `QuorumAddMember` is valid only if the member's own
active vault (from their latest `QuorumBegin`) is at least `member_vault_ratio`
(default 50%) of this ledger's vault. Co-signers verify both outpoints on-chain.
Three signers of a theft of `V` then hold at least `1.5 V` between them on ledgers
that can slash them; no separate bond is required.

This is bite per theft, not per membership. A key is slashed once however many
quorums it serves, so a member guarding `m` ledgers offers each roughly `1/m` of
the bite it appears to. Full teeth require the sum of half-vaults a key guards to
fit within its own vault; the protocol does not enforce that (it is the
membership-bond capital problem in another form), so operators and wallets SHOULD
weight a member's vault by the number of quorums it serves. The structure this
implies is a pyramid: members larger than what they guard, and network capacity
secured with full teeth bounded by the size of its largest operators.

**11.2 Declared anchors.** `QuorumBegin` gains an `anchor_members` list, a subset of
the active members chosen by the operator. Wallets read it when scoring a ledger.
It is a declaration, not a proof.

**11.3 Anchor intersection.** A non-anchor member's own active quorum MUST include
at least one of this ledger's `anchor_members`. Co-signers verify against the
member's latest `QuorumBegin`. A member who misbehaves here is then slashable by a
party the operator chose. A key that satisfies the rule with one anchor and four
unknowns is compliant but visibly so.

**11.4 Disjoint quorums per operator.** A key SHOULD NOT be an active member on two
ledgers with the same operator. Co-signers MAY check the operator's other ledgers via
their advertisements (DEP-04); the set is self-reported, so this is advisory.

**11.5 Liveness on the record.** Each cosignature carries `signer_block_height`,
the height at which the member signed. With proposals published (§9), per-member
co-sign latency is derivable from the public record. Wallets and operators SHOULD
use it in member selection.

**Enforcement.** A MUST here names its conforming response, per BOLT usage.
11.2 and 11.5: decoders reject an establishment update or cosignature lacking the
field. 11.1 and 11.3: a conforming wallet MUST NOT open on, and SHOULD exit from, a
ledger whose latest establishment update violates them; this is the tangible
consequence and it is aimed at fronts, which need deposits. Slashing of the signers
under `NonConforming` applies additionally where they are slashable. Rules with no
named response are SHOULD.

These rules are applied by the co-signers of the establishment
update, which for `QuorumBegin` is the staged set itself. An honest staged set
refuses a non-conforming add; a colluding one signs it, and the resulting
`NonConforming` proof lands on keys the coalition chose. The rules therefore bind
honest quorums and expose dishonest ones; they do not prevent them. Their value is
that a violation is a binary fact any wallet computes identically, checked at
admission rather than after deposits arrive, and that 11.2 and 11.5 put on the
record the data that correlation and liveness scoring otherwise infer from relay
timing. **Residual.** A set of coalition keys that seat each other plus one anchor apiece
satisfies 11.1–11.4. It appears as a dense cluster with few anchors and correlated
signing, which is the signal wallets are already told to price. These rules make the
cluster detectable, not impossible.

### 11. Parameters summary

| Parameter | Where | Default |
|---|---|---|
| `inactivity_blocks` | QuorumAddMember, QuorumBegin | 144 |
| `cosign_response_blocks` | QuorumAddMember, QuorumBegin | 72 |
| Proposal kind | Nostr | 9108 |
| `member_vault_ratio` | QuorumBegin | 50% |
| `anchor_members` | QuorumBegin | operator-declared |
| `signer_block_height` | cosignature | — |
| CosignRefusal kind | Nostr | 9109 |
| Attestation kind | Nostr | 9107 |
| `QuorumInactive` discriminant | FraudProofType | TBD |
| `NonConforming` discriminant | FraudProofType, replaces two | TBD |

## Rationale

Sections 8 and 9 reuse one idea: a hash becomes binding on a pubkey when that
pubkey signs anything downstream of it. DEP-12 already relies on this for operators;
extending it to members costs one proposal signature per update and one optional
refusal message, and turns the only unobservable majority attack into a provable
one for any member who remains active anywhere.

The inactivity path adds no on-chain surface; it reuses Tier 0 and the existing
respectful confiscation shape. Its cost is one new operation field and one event
kind. Its benefit is that the depositor hold under silence becomes a negotiated
parameter, and the rotation interval can be lengthened to save on-chain fees without
lengthening holds.

Consolidating the non-conformance types makes the accused a free field rather than
a property of which ledger the update sits on, which is what cross-ledger slashing
needs. Dropping equivocation removes a trigger that punishes an act with no victim.

Section 6 turns the "web of collateral" from a description into a rule: every
punishable party is punished by a quorum that has both a reward and a duty.

## Related DEPs

- DEP-02 (QuorumAddMember field), DEP-03 (respectful confiscation shape),
  DEP-05 (member terms, lifecycle), DEP-06 (proof types, dispute lifecycle),
  DEP-11 (obligations), DEP-12 (causal visibility via embeds).

## Open questions

4. §9 makes proposals public before they are canonical. Wallets MUST ignore
   proposals for balance purposes; relays will carry more traffic. Whether proposals
   should be gift-wrapped to members and only the *hash* published is a privacy vs.
   verifiability trade-off left open.
5. §9 lets an operator generate dereliction pressure by proposing at a high rate.
   `cosign_response_blocks` bounds the response time, not the count; a per-block
   proposal cap or a fee to the member per proposal may be needed.

1. Should `inactivity_blocks` be allowed below `service_response_blocks`? A censored
   wallet's proof needs the operator to keep signing; an operator who goes silent to
   dodge a censorship proof should hit the inactivity trigger no later than the
   censorship deadline. Suggest requiring `inactivity_blocks ≤ service_response_blocks`.
2. Tier 1 "minority" is not given a count in DEP-03. `floor(Q/2)` is assumed here and
   in the model.
3. Whether the no-op `Batch` heartbeat should be fee-free for co-signers or count as
   an operator action for compensation purposes.
