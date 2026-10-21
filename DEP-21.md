# DEP-21: Attested Signers and Depositor Trust Policies

Status: Idea (draft for discussion)

## Abstract

A quorum seat's signing key MAY be generated and held by an enclave running a reproducible
signer image whose policy refuses to sign theft. This document makes that useful to a depositor
without making the enclave a single point of failure: signer images change only at rotation,
each new seat's image and endorsements are recorded in `QuorumBegin`, and every deposit carries
a trust policy naming whose endorsements it accepts and what seating it requires. A rotation
whose new quorum does not satisfy a deposit's policy MUST splice that deposit out. Breaking the
rule is an ordinary `NonConforming` update, provable without reference to any enclave. When an
attestation class is broken, its seats stop counting for every policy, and the protocol falls
back to the collateral economics it already has (DEP-05, DEP-19). A quorum MAY also record an
image policy that its attested signers enforce on every later seat, so an attested quorum stays
attested across rotations without trusting its operator.

## Motivation

Collateral alone tolerates a coalition of roughly a third of operators at R = 0.5 with random
quorums, and about 0.45 with seating guidance (docs/TRUST-MODEL.md §2d-2e in cl-deposits). Capital
efficiency (R/(1-R)) costs tolerance quickly above R = 0.7 (§2h).

An attested key on an intact platform cannot sign a theft, whoever operates it. If every seat of
a quorum is attested, with at most one seat per platform class and at most three per vendor, a
coalition of any size cannot reach the four of seven signatures a theft needs unless three
platforms, or one whole vendor, are broken (§2i). Beyond that bound, the system is no worse than
today: contagion and collateral still apply. Earlier TEE designs failed totally on one break; this
one degrades to a line it already holds.

Two problems stop this from being usable as stated:

1. **Upgrades spend the attestation.** A depositor chose a ledger because of image M. When M is
   replaced by M', the old attestation says nothing about M'.
2. **No registry.** A central allowlist of acceptable images would be a new federation.

Both are solved by making consent per-deposit, evaluated at the one moment it matters (rotation),
and enforced as a ledger rule.

## Specification

### 1. Signer and node

A **signer** holds the epoch vault key and enforces a minimal policy; the **node** does everything
else (ledger validation, relays, fees, UI) and is untrusted by this DEP. The signer policy:

1. Never sign two different updates at the same `(ledger_id, seq)` (monotonic counter or ledger-
   anchored state; rollback of sealed state MUST NOT allow a second signature).
2. Never sign a spend of a vault outpoint unless it is (a) a rotation to a `QuorumBegin` the signer
   has cosigned and that satisfies §4 for every carried deposit, or (b) a confiscation backed by a
   valid DEP-06 proof.
3. Verify header proof-of-work for every chain fact the above relies on.
4. Never cosign a `QuorumBegin` whose seats do not satisfy the quorum image policy in force (§7):
   the signer checks every other seat's quote itself, so an operator cannot swap an unapproved key
   into a quorum by editing the node.

Node upgrades never change the signer's measurement. The signer is small enough to be specified
here and implemented identically, or shared, across implementations.

### 2. Identity and epoch keys

An operator or member has a long-lived **identity key** (ads, ledger identity) and a per-epoch
**vault key** held by its signer. The identity key signs, in the DEP-04 ad, a binding
`(epoch vault pubkey, attestation quote, image measurement)`. A signer upgrade replaces only the
epoch key, at rotation.

The quote carries both keys in its report data, so it cannot be moved to another key:

    seat report_data(64) = identity pubkey(32) ‖ epoch vault pubkey(32)

The report data goes in SEV-SNP's `REPORT_DATA`, TDX's `REPORTDATA`, or a Nitro attestation's
`user_data`. A quote is valid for a seat when its signature chain verifies to the vendor root, it is
not a debug guest, and its report data is the seat's identity key followed by its epoch vault key.

The vault key MUST be in the quote itself. Attesting only the identity key, and letting it sign the
vault key, would let anyone holding the identity's secret attach an unattested vault key to an
attested identity.

Certificate validity windows and TCB status are not judged at verification time; doing so would
make conformance depend on the judge's clock. They are handled by revocation (§6). The measurement
is taken from the quote itself: SNP `MEASUREMENT`, TDX `MRTD`, Nitro `PCR0`, all 48 bytes.

### 3. Images change only at rotation

Each `QuorumBegin` records, per seat (parallel to `quorum_members`):

| Type | Name | Content |
|---|---|---|
| 320 | `seat_attestations` | repeated `u16 len ‖ attestation quote` (empty = unattested) |
| 322 | `seat_measurements` | repeated `measurement(48)` |
| 324 | `seat_classes` | repeated `vendor(1) ‖ platform(u16 len ‖ id)` |
| 326 | `seat_endorsements` | repeated `u16 count ‖ count × endorsement event id(32)` |

A seat's image may differ from the previous epoch's only through a new `QuorumBegin`.

**Endorsements** are signed statements by a trust root that a measurement is the reproducible build
of a published source revision: Nostr kind 39106 (replaceable per root and measurement), content
`{measurement, source, revision, build_recipe_hash}`, signed by the root's key. A trust root is any
key a depositor chooses to trust: an auditor, a wallet vendor, a reproducible-build group.

### 4. Deposit trust policy

`DepositOpen` MAY carry `trust_policy` (type 328, variable): a policy document, or its hash with
the document published alongside (type 330, `trust_policy_hash`, 32). A policy states:

- **roots:** a set of trust-root keys and a threshold k;
- **seating:** the minimum number of seats that are attested by an intact class *and* whose
  measurement is endorsed by ≥ k roots, with per-platform and per-vendor caps over those seats
  (suggested: 7 of 7, ≤ 1 per platform, ≤ 3 per vendor);
- **exit:** where the deposit goes when the policy is not met: an on-chain address (DEP-20 §3), or
  any ledger whose quorum satisfies the policy (DEP-20 §10), or both in order of preference.

A deposit without a policy is unaffected by this DEP. `DepositKeyRotate` MAY replace the policy,
signed by the deposit's descriptor.

### 5. Rotation conformance

For every deposit carried into the new vault, cosigners MUST evaluate its policy against the new
quorum's seats (§3), counting a seat only if its class is not demoted (§6). A `QuorumBegin` that
carries a deposit whose policy is not met, instead of settling it as a DEP-20 exit output (or a
migration output to a satisfying ledger), is a `NonConforming` update (DEP-19 §5). The evaluation
uses only the ledger, the endorsement events and the demotion record, so anyone can check it; no
enclave appears in the proof.

**Who pays.** Policy exits are paid by the exiting deposits, as ordinary DEP-20 exits are: each
on-chain exit output bears its own fee, and a migration output's fee is shared pro rata by the
deposits it carries. The operator pays nothing extra; its incentive to obtain endorsements before
upgrading is the deposits it would otherwise lose. (Operator-paid policy exits would let anyone
open many small deposits with unsatisfiable policies and force on-chain cost.)

**Small deposits.** A policy's on-chain exit is honoured only for deposits above the bucket's
`dormancy_amount_msats` (DEP-20 §8, pegged to the reference feerate recorded in `QuorumBegin`).
Below it, the policy's exit is migration only: such deposits are batched into one migration output
per receiving ledger that satisfies their policy, or held to the next rotation if no satisfying
ledger accepts them, exactly as dust exits are aggregated rather than dropped (DEP-20 §3).

### 6. Class demotion (repricing)

An `UnauthorizedVaultSpend` (DEP-06) or `Equivocation` proof whose accused key is bound by §2 to an
attested class demotes that class: from the proof's block on, seats of that class count as
unattested for every policy and for seating guidance. Demotion is not a fraud proof about the
enclave: the proof is the ordinary one, and only the repricing reacts. A class MAY also be demoted
by a policy's own roots (a signed revocation event, for TCB advisories).

The consequence is automatic containment: at the next rotation of every ledger relying on a
demoted class, deposits whose policies are no longer met splice out. A depositor's choice never
silently carries over to an image or a class it did not accept.

### 7. Quorum image policy

§4 lets a depositor decide which quorums to trust. This section lets a quorum decide which seats it
will admit, enforced by the attested signers themselves (§1 item 4).

`QuorumBegin` MAY carry `image_policy` (type 332, variable):

| Field | Content |
|---|---|
| `roots` | `u8 n ‖ n × root pubkey(32)` |
| `k` | `u8`: endorsements required per measurement |
| `pinned` | `u8 m ‖ m × measurement(48)`: measurements admitted without endorsement |
| `max_per_platform` | `u8` (suggested 1) |
| `max_per_vendor` | `u8` (suggested 3) |
| `max_per_source` | `u8` (suggested ⌈n/2⌉ − 1, i.e. 3 of 7) |

A measurement is **approved** when it is pinned, or when ≥ `k` of `roots` endorse it (kind 39106,
§3). Every seat of the next quorum MUST carry a valid quote (§2) for an approved measurement, and
the seats MUST respect the three caps. `max_per_source` counts seats whose endorsements name the
same `source`, so different builds of one codebase count together. A `QuorumBegin` that breaks the
policy recorded in the previous `QuorumBegin` is `NonConforming` (DEP-19 §5). That is checkable
from the ledger, the quotes and the endorsement events, without trusting any enclave.

**Changing the policy.** A `QuorumBegin` may carry a different `image_policy`, but its seats MUST
satisfy both the old policy and the new one. A policy can only be loosened after the seats that
adopt it were admitted under the stricter one, and every change is visible on the ledger a full
epoch before it governs anything. Deposits whose §4 policy the change would break splice out at
that rotation, as usual.

**Same image as me.** The degenerate policy pins one measurement, `pinned = {self}` with no roots:
a node only talks to keys running exactly its own image. It is valid, but it is a monoculture, and
an upgrade becomes a flag day that must re-pin through a policy change. The intended use is roots
endorsing a set that holds at least two independent implementations. The `max_per_source` cap then
keeps a bug in one codebase from supplying the majority a theft needs.

**What this buys and what it does not.** With every seat on an approved image and the caps met, a
theft needs a majority of signers to run modified code, or a class break beyond the counting bound
(§6). Neither can be done by an operator. Attestation proves which code runs, not that the code is
correct: a bug in an approved image runs faithfully on every seat that uses it. What remains to an
attacker is input from outside the quorum (depositors, relays, chain data, migrating ledgers,
non-member proofs) and bugs in approved images. Implementation diversity and `max_per_source` are the
defence against both, so this DEP does not replace audits of the signer.

### 8. Identity continuity

An identity key generated inside an enclave dies with that enclave's image unless it can move. A
handoff moves it to a new enclave, and a chain of handoffs proves where it has been. Only the
identity key moves. Vault keys are per epoch (§2), so the new enclave generates a fresh one at its
next rotation, and no key that controls funds is ever transferred.

**Genesis.** An identity's chain starts at a quote, from image M₀, whose report data begins with the
identity key. Any seat quote (§2) serves.

**Handoff.** To move from image Mᵢ to Mᵢ₊₁:

1. The new enclave publishes a transport quote:
   `report_data = identity pubkey(32) ‖ SHA256("DEP-21/handoff" ‖ transport pubkey(32))`.
   The hash makes the second half unusable as a vault key: nobody knows a secret key for it.
2. The old enclave verifies the quote and checks that Mᵢ₊₁ is approved under the image policy it
   enforces (§7). If so, it encrypts the identity secret to the transport key.
3. The old enclave signs, with the identity key, a handoff event (Nostr kind 9108):
   `{identity, handoff_seq, from_measurement, to_measurement, transport_quote_hash}`.
   `handoff_seq` is one more than the previous handoff's, or 1 after genesis. The old enclave then
   erases the secret and refuses to sign anything further as that identity.
4. The new enclave shows it received the secret by signing its next event with the identity key.

A verifier walks the chain from genesis through each handoff to the current quote. At every step,
the image holding the key released it, and only to an image it approved.

**Recording.** `QuorumBegin` records, per seat, `seat_handoffs` (type 334): `u32 handoff_seq ‖
handoff event id(32)`, both zero at genesis. A seat's `handoff_seq` never decreases from one epoch
to the next. A signer refuses to cosign with an identity at a lower `handoff_seq` than the highest
it has seen for that identity.

**Forks.** Erasure cannot be proven, so after a handoff two enclaves may hold the secret. Two
handoff events signed by one identity with the same `handoff_seq` prove a fork. A forked identity
is treated as exposed from the fork on. Two live copies that both sign ledger updates are already
provable as `Equivocation` (DEP-06).

**Exposure.** A key is only as safe as every image it has lived in. An identity whose chain passes
through an image of a demoted class (§6), or a demoted measurement, is exposed from the demotion
on: anything signed by the identity alone after that (ads, handoffs) proves nothing. Its seats are
unaffected, because each seat's vault key is attested on its own by its own quote. A stolen
identity costs reputation, not deposits.

## Rationale

- **Per-deposit consent replaces a notice period.** No waiting time to calibrate, and no reliance
  on depositors noticing an announcement.
- **No registry.** Roots compete; a policy is the depositor's (in practice, their wallet's) choice.
- **The proof stays chain-verifiable.** Policies are evaluated from public data, and demotion is
  triggered by existing proofs.
- **Degradation, not failure.** A broken class is repriced, and the collateral regime remains.
  Size R for the tolerance wanted after the worst planned break (§2i).
- **No griefing.** Exits pay their own way, so a policy cannot be used to impose cost on an operator.
- **Identities outlive images; funds keys never move.** Reputation is worth carrying across an
  upgrade, so the identity can be handed off between attested images. Vault keys are rebuilt each
  epoch, so a handoff gone wrong can never move money.
- **The signers police the seating.** A ledger rule alone only lets a bad seating be proven after
  the fact. An attested signer that checks its peers' quotes refuses to create the bad seating at
  all, and the ledger rule (§7) still catches a quorum whose signers were broken.
- **Zero-day response and opt-out are one mechanism.** Demotion makes the next rotation splice out
  every deposit whose guarantee depended on the broken class.

## Limits

- **The first strike.** Without a spend delay, a broken class beyond the counting bound can take
  every capturable vault in one block before any proof exists (§2j: about 21% of vaults for a vendor
  plus one platform under the suggested caps). Demotion protects everything after. A covenant
  (BIP-345, CTV), or a covenant-free delayed majority path with a pre-signed rescue, would bound it.
- **Emergency upgrades** after a zero-day need many rotations at once; on-chain capacity bounds how
  fast demoted quorums re-seat.
- **Supply.** Policies with strict caps need seven distinct attestable platforms across at least three
  vendors per quorum.
- **Source diversity.** `max_per_source = 3` of 7 needs at least three independent sources per
  quorum (3 + 3 + 1). Two implementations exist today (cl-deposits and the Rust reference), so the
  suggested cap is a target. Until a third exists, policies can set `max_per_source = 4` at the cost
  of one codebase being able to supply a majority. The signer of §1 is a separate source from the
  node; if it is shared, its diversity is one.
- **Root compromise** is a class break of its own; k-of-n roots handle it as platform diversity does.
- **Liveness is unchanged.** Censorship, co-sign refusal and going offline rest on collateral and
  dereliction as before.

## Implementation notes (non-normative)

- A modus image boots as an SEV-SNP guest and can request a report binding 64 bytes of report data.
  Its Nitro path produces attestation documents with `user_data`. Either can be the signer of §1.
- cl-sev-snp (github.com/modus-lisp/cl-sev-snp) verifies SNP reports against the AMD chain and Nitro
  documents against the pinned AWS root, in pure Common Lisp. That is enough to check §2 quotes in
  the cl implementation without FFI. The Rust reference needs an equivalent before the shared
  vectors this DEP will need (a quote, its binding, its measurement, accept/reject) can be pinned.

## Related DEPs

DEP-02 (TLVs), DEP-03 (rotation transaction), DEP-04 (ads, event kinds), DEP-05 (cosignature rules),
DEP-06 (proofs that trigger demotion), DEP-19 (`NonConforming`, seating §10), DEP-20 (exits, splice,
migration, fees).

## Open questions

1. Policy language: a fixed schema, or a small descriptor-like language (DEP-16) over seats?
2. Whether members, not only the operator, must satisfy a deposit's policy (this draft: every seat).
3. How a wallet discovers satisfying ledgers cheaply (an ad field summarising seat classes and
   endorsements).
4. How `seat_classes` is derived from the quote rather than declared: vendor from the root the chain
   ends at, platform from the chip certificate (SNP product, TDX FMSPC). For Nitro, what counts as a
   platform is open. CCA quote binding is not yet specified.
5. What a deposit below the dust floor is owed if no satisfying ledger will take it: held
   indefinitely, or released from its policy after some number of rotations.
6. Whether a seat's `source` should come from the endorsement or from a field the quote itself
   attests (for example SNP `HOST_DATA` or a Nitro PCR), so that `max_per_source` cannot be gamed by
   endorsing one codebase under two names.
7. Whether a fork (§8) should be a DEP-06 proof with a slashing consequence, or only exposure.
8. Whether the handoff's encrypted payload must be published (so that receipt is provable) or can
   stay between the two enclaves.
9. A shared signer implementation or two independent ones (independence is a class axis of its own).
