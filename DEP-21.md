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
back to the collateral economics it already has (DEP-05, DEP-19).

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

Node upgrades never change the signer's measurement. The signer is small enough to be specified
here and implemented identically, or shared, across implementations.

### 2. Identity and epoch keys

An operator or member has a long-lived **identity key** (ads, ledger identity) and a per-epoch
**vault key** held by its signer. The identity key signs, in the DEP-04 ad, a binding
`(epoch vault pubkey, attestation quote, image measurement)`. A signer upgrade replaces only the
epoch key, at rotation.

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

## Rationale

- **Per-deposit consent replaces a notice period.** No waiting time to calibrate, and no reliance
  on depositors noticing an announcement.
- **No registry.** Roots compete; a policy is the depositor's (in practice, their wallet's) choice.
- **The proof stays chain-verifiable.** Policies are evaluated from public data, and demotion is
  triggered by existing proofs.
- **Degradation, not failure.** A broken class is repriced, and the collateral regime remains.
  Size R for the tolerance wanted after the worst planned break (§2i).
- **No griefing.** Exits pay their own way, so a policy cannot be used to impose cost on an operator.
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
- **Root compromise** is a class break of its own; k-of-n roots handle it as platform diversity does.
- **Liveness is unchanged.** Censorship, co-sign refusal and going offline rest on collateral and
  dereliction as before.

## Related DEPs

DEP-02 (TLVs), DEP-03 (rotation transaction), DEP-04 (ads, event kinds), DEP-05 (cosignature rules),
DEP-06 (proofs that trigger demotion), DEP-19 (`NonConforming`, seating §10), DEP-20 (exits, splice,
migration, fees).

## Open questions

1. Policy language: a fixed schema, or a small descriptor-like language (DEP-16) over seats?
2. Whether members, not only the operator, must satisfy a deposit's policy (this draft: every seat).
3. How a wallet discovers satisfying ledgers cheaply (an ad field summarising seat classes and
   endorsements).
4. Attestation formats per vendor (TDX, SEV-SNP, CCA, Nitro) and how `seat_classes` is derived
   from the quote rather than declared.
5. What a deposit below the dust floor is owed if no satisfying ledger will take it: held
   indefinitely, or released from its policy after some number of rotations.
6. A shared signer implementation or two independent ones (independence is a class axis of its own).
