# DEP-22: Proofs from Signed Evidence (Commitment Chains)

Status: Draft

## Abstract

A fraud proof should be checkable from what the accused signed, and nothing else. Today a
`NonConformingUpdate` carries only the faulty update. Each verifier replays its own copy of the
ledger's history into state and judges the update against that state. So a verifier whose state
is wrong (a bug, a double apply, a gap) produces a proof that looks real and is false. This DEP
makes every state-dependent rule provable from **two signed updates**. Each update that changes
an item of state commits to the item's new state and points back to the update that last
committed it. A fault is then the pair (a, b): b names a as the item's predecessor and declares
a state that does not follow from a's state and b's own operation. A pointer that skips an
update is itself provable, because two updates by one operator then claim the same predecessor.
No replay, replica or relay search enters a verdict.

## Motivation

On the signet soak (2026-10-30 23:33Z), cld1 caught up ledger F from three threads at once and
applied one transfer twice. The operator's next update, at sequence 103515, was a
`TransferComplete` whose balance commitments were correct, but cld1's state disagreed:

    TRANSFER-COMPLETE: deposit 78682e41… declared (174378829, 0), holds (181966874, 0)
    TRANSFER-COMPLETE: deposit 5147f50b… declared (515349, 0), holds (0, 0)

cld1 published a `NonConformingUpdate` against the operator and contagion proofs against three
cosigners, and entered and armed a dispute. Every other verifier rejected the proofs, but the
dispute could not be withdrawn and cld1 refused that ledger's cosigning for good.

"Holds 181,966,874" is a number cld1 computed, not evidence anyone signed. DEP-06's
verify-before-publish rule (a replay from history before publishing) narrows the window, but it
still trusts the verifier's replay. The 2026-10-31 fee-window incident had the same shape: the
reference implementation's replicas held a fee baseline of 0 and judged a `FeeCollect` against
it (DEP-07). Every rule judged against replayed state can convict on a verifier's bug.

The principle, already applied to vault spends (DEP-06 §Spend challenge) and confiscations
(byte-identical rebuild), is extended here to every state-dependent rule: **a dispute rests only
on a proof that cannot be wrong**, and a proof cannot be wrong when every quantity in it is
signed by the accused.

## Specification

### 1. Items

An **item** is a unit of ledger state whose changes are committed:

| Item | Key | State (canonical, §3) |
|---|---|---|
| Deposit | `deposit_id` | balance, locked_balance, last_fee_assessment, opened_at_block, descriptor commitment, fee schedule hash, pending exits, last signed activity, closed flag |
| Lock | lock id (`transfer_id`, or `payment_hash` for invoice/on-chain locks) | deposit, amount, expiry, status (pending, fulfilled, failed, completed) |
| Ledger | the ledger itself | total obligations, governing `QuorumBegin` (seq, content id), active ruleset name |

Every operation that changes an item's state **touches** it. The touch table is DEP-02
§Balance Commitments' table, extended by:

- deposit items: also `DepositKeyRotate` and `FeeChange` (descriptor and schedule), `ExitRequest`,
  `ExitCancel` and `MigrationCredit` (pending exits, balance), and any depositor-signed operation
  (last signed activity, DEP-20 §8);
- lock items: every lock, fulfil, fail and complete operation;
- the ledger item: every operation that changes total obligations, plus `QuorumBegin` and
  `QuorumUpgrade`.

### 2. Encoding

Each touched item carries, in the update that touches it, a **commitment**:

    commitment = item_kind (1) || item_key (32) || prev_ref (40) || state_hash (32)
    prev_ref   = prev_sequence (8 LE) || prev_content_id (32)
    content_id = tagged_hash("deposits/content/v7", cosign_data)
    state_hash = tagged_hash("deposits/item/v7", canonical item state, §3)

`content_id` is over `cosign_data` (DEP-02 §Signing), so it is the same for every variant of an
update with a different set of cosignatures. A pointer over `chain_hash` would break whenever
two members hold differently cosigned copies of one update; that happened on the 2026-10-28
soak with rotation rungs.

Commitments go in new odd TLVs, so implementations that don't know them skip them and
`content_hash` stays stable for mixed fleets (as with DEP-02's balance commitments):

| Type | Name | Size | Content |
|---|---|---|---|
| 231 | item_commitments | 105 × n | the commitments for every item the operation touches, sorted by (item_kind, item_key) |
| 233 | item_states | variable | optional: the canonical states themselves, for readers that want them without a lookup |

Inside a `Batch`, each inner operation carries its own commitments, evaluated sequentially (as for
DEP-02 balance commitments). The existing balance tags 223–229 remain; under this ruleset the
balance pair is also inside the deposit state, and the two MUST agree.

**First commitment.** An item's first commitment, in the update that creates it (`DepositOpen`,
the lock operation, `LedgerOpen`), has `prev_sequence` equal to its own sequence and
`prev_content_id` all zeros: it has no predecessor. Its state must be exactly the creation state
the operation implies (for example, a deposit opened at the update's height with balance 0).

**Rebase.** On a ledger moving to this ruleset (§6), the first commitment of each existing item
after the move is a rebase. It points to the moving `QuorumBegin` or `QuorumUpgrade` (its
sequence and content id). A rebase is checkable only against the snapshot the moving update
commits to (§6), never against replayed history.

### 3. Canonical item state

Each item kind has one canonical byte encoding: fixed field order, little-endian integers, and
lists sorted by key. Pending exits are sorted by release height, then by request id. The exact
layouts are an open question (§Open questions 1). The requirement is that the state transition
`f(state, operation, header)` is a pure function of the item's own previous state, the
operation, and the touching update's signed header (`block_height`), with no other input.
Anything a transition needs, such as the deposit's fee schedule for a fee check or its
descriptor for a witness check, must therefore be inside the item's state.

### 4. Proofs

Two new evidence forms, valid for `NonConformingUpdate` (operator-signed) and
`NonConformingCosignature` (cosigned) under this ruleset:

**4.1 Transition proof**, for a commitment that does not follow from its predecessor:

    evidence = ascii_hex(update_a) || ascii_hex(update_b) || item_kind || item_key
             || state_a || state_b || u16_le(inner_index)

A verifier requires:

1. both updates are on one ledger and signed by its operator (for the cosignature form, b
   carries the cosignatures it judges);
2. b's commitment for the item has `prev_ref` = (a's sequence, a's `content_id`), and a's
   commitment for the item has `state_hash = H(state_a)`;
3. b's commitment has `state_hash = H(state_b)`;
4. `f(state_a, op_b, header_b) ≠ state_b`, or `f` refuses (`op_b` is the operation, or the
   `inner_index`-th inner operation of a `Batch`).

Nothing else is consulted. Rules that are pure functions of one update alone (missing commitments,
an expired operation, a zero amount, the header rules of DEP-02) are judged from b alone, with a
omitted.

**4.2 Item fork proof**, for a pointer that skips an update:

    evidence = ascii_hex(update_b) || ascii_hex(update_c) || item_kind || item_key

where b and c are distinct updates, both signed by the same operator on one ledger, whose
commitments for the item carry the same `prev_ref`. An item state has exactly one successor
on an operator's chain, so two successors mean one of the pointers lies, or the operator signed
two branches. Either is the operator's fault. If c's `prev_ref` names an update on another branch
(same sequence as an update on b's chain, different content id), the two named updates are an
`Equivocation` (DEP-06), and the verifier may require them as additional evidence.

**4.3 Pair proofs with no new fields.** Some rules already convict on two signed updates and need
only to say so. For example, a nonce replay (DEP-17) is two operations on one deposit carrying the
same nonce, with the earlier one unexpired at the later one's height. Under this ruleset, the
proof also carries the deposit item's pointer path from the later update back to the earlier one,
so the verifier knows both are on one chain.

### 5. What is no longer a conviction

Under this ruleset, a violation found by replaying state, with no transition or fork proof, is
grounds to **refuse** a cosignature, never to convict. That covers `NonConformingUpdate` and
`NonConformingCosignature` evidence that carries only the fault update, as today. Proofs built
from replayed state still convict under every earlier ruleset (DEP-18: a ruleset never changes
how earlier history is judged).

### 6. Activation

A new DEP-18 ruleset, `commitment-chain-v7`, in the `cltv-offset-v2` family (no script change).
Its rules are `balance-anchor-v6`'s plus §2–§5. A ledger reaches it by `QuorumBegin` or
`QuorumUpgrade`. The moving update carries:

| Type | Name | Size | Content |
|---|---|---|---|
| 235 | item_snapshot_root | 32 | Merkle root over every item's (item_kind, item_key, state_hash), as of the moving update |

Each item's rebase (§2) must prove membership in that root with its first post-move commitment.
The snapshot is the operator's cosigned assertion. A wrong snapshot is judged under the prior
ruleset, by replay, which is the last place replay convicts. After the move, a ledger never
needs replay to convict again.

Operator policy (DEP-18 §operator policy): name v7 when every member declares it. Otherwise keep
the current ruleset.

### 7. Interactions

- **Forks and disputes.** Item fork proofs (§4.2) compare only updates by the same operator. A
  disputant's fork continues the items from the fork point under its own key. That's not a fork
  of the operator's chain, and a winner's updates after `DisputeAcquire` continue each item from
  its last pre-fork commitment, pointing back across the custody change.
- **Rotations.** A `QuorumBegin` touches only the ledger item (governing quorum, ruleset). Deposit
  and lock chains run through it unchanged.
- **Migration (DEP-20 §8.3).** A migrated deposit's first commitment on the receiver is a creation
  commitment whose state includes the source's committed state. Pointing back across ledgers to
  the source's last commitment would let the receiver's state be checked against the source's
  signed state (open question 4).
- **Confiscation.** The rebuild reads obligations from the fork point's ledger item and the
  deposits' committed states, signed values rather than a replayed total.
- **Recovery.** With every item committed, a surviving suffix that holds each item's latest
  commitment states all obligations. This extends DEP-02's recovery guarantee from balances to
  locks, exits and fee baselines.

### 8. Cost

A commitment is 105 bytes. Typical operations touch:

| Operation | Items | Added bytes |
|---|---|---|
| `TransferLock` | source deposit, lock, ledger | 315 |
| `TransferComplete` | source, destination, lock, ledger | 420 |
| `FeeCollect` | deposit, ledger | 210 |
| `QuorumBegin` | ledger | 105 |

The soak's ledgers reach about 200k updates in a week, so roughly 60 MB of commitments per
ledger per week, before compression. Shortening `prev_content_id` to a 16-byte prefix (still
collision-resistant against the operator, who signs both ends) would cut that by about a
fifth (open question 2).

## Sweep: every proof and refusal rule

Classes: **(a)** judged from signed evidence only; **(b)** judged against derived state;
**(c)** absence-based, which needs the challenge form or a contiguous signed segment. "Convicts
today" is what both implementations do (deposits-rust `proves_non_conformance`, cl
`cf:violation`).

| Rule (source) | Class now | Convicts today | Literal form under v7 |
|---|---|---|---|
| Header: height decreases, no block hash (DEP-02) | a (predecessor and fault) | yes, v5+ | unchanged: two signed updates |
| Sequence skip/rewind (DEP-02) | a | yes | unchanged |
| `ZeroAmount`, `EmptyDestination`, `ExpiryPassed` | a (one update) | yes | unchanged: b alone |
| `MissingBalanceCommitment` (DEP-02, v4/v6) | a, given the ruleset | yes | b plus the ledger item's ruleset |
| `BalanceCommitmentMismatch` (DEP-02) | **b** | yes | transition proof on the deposit item (the F case) |
| Insufficient balance / lock not found / unknown deposit (`StateMachineRejected`) | **b** | yes | transition proof on the deposit or lock item. A lock resolved twice is an item fork proof |
| `InvalidWitness` (DEP-16 authorisation) | **b** (current descriptor) | yes | transition proof: descriptor commitment in the deposit state |
| `FeeWindowNotElapsed`, `FeeExceedsAssessment` (DEP-07) | **b** (baseline, balance, schedule) | yes, every ruleset | transition proof: baseline, balance and schedule are in the deposit state |
| `NonceReplay` (DEP-17) | **b** (nonce index) | yes | pair proof with a pointer path (§4.3) |
| `InsufficientReserves` | **b** (totals) | yes | transition proof on the ledger item (total obligations) |
| `CollateralBelowFloor` (DEP-05) | a, with the members' declarations carried | yes, v5+ | carry the seated members' `QuorumAddMember`s |
| Quorum expiry within commitments; born expired (DEP-05) | a | yes | unchanged |
| Ruleset unknown / family / undeclared (DEP-18) | b (current ruleset), a (declarations) | yes | ledger item gives the current ruleset; declarations carried |
| Descriptor validity (DEP-16) | refusal only | no | unchanged (refusal only) |
| Exit release, exit queue (DEP-20 §3) | **b** | via the state machine | pending exits in the deposit state |
| Dormancy: activity clock (DEP-20 §8) | **b** | via rotation conformance | last signed activity in the deposit state; a rotation that spins out an active deposit is a transition proof |
| Migration credited twice (DEP-20 §8.3) | b | via the state machine | item fork proof on the migration's lock-like item (open question 4) |
| Uncredited on-chain/Lightning payment (proof 1, 2) | c (no credit within the accused's chain) | yes | contiguous signed segment carried in the proof (literal, no replica). A credit index item would shorten it (open question 5) |
| Stale cosignature (3) | a | yes | unchanged |
| Dereliction (4, DEP-19) | c (no rebuttal known) | yes | unchanged: a rebuttal always wins |
| `QuorumExpired` (6) | c (no later `QuorumBegin`) | respectful only | ledger item's governing quorum and the block; a later `QuorumBegin` rebuts |
| Winner collateral deviation (7) | a | yes | unchanged |
| `Equivocation` (8) | a | yes | unchanged |
| Unauthorised vault spend (10) | a (unanchored), c (lapsed challenge) | yes, v5+ | unchanged |
| Unhonoured obligation (11) | c, plus derived residue | yes | segment, with residue from the confiscation transaction and committed deposit states |
| Censorship (DEP-11/12) | c | no caller today | segment form |
| Cosign refusal, late cosignatures, seating guidance (DEP-05/19) | policy | no | unchanged |

## Worked example: the F case

Under v7, the operator's update b at sequence 103515 completes transfer T from source S to
destination D. For each of S, D and T it commits a `prev_ref` to that item's previous commitment:

- for S and T, typically the `TransferLock` that opened T, call it a, which committed S =
  (balance x, locked y) and T = (pending, amount t);
- for D, D's own latest commitment, which committed D = (balance z, locked 0).

`f` gives S = (x, y − t), D = (z + t, 0) and T = completed. b declares exactly those states
(174,378,829 and 515,349 in the log), so no transition proof exists.

cld1's double apply happened in its own memory. To accuse, it would need a signed predecessor
whose committed state makes b's declaration wrong, and none exists. It could only refuse to
cosign, and verify-before-publish already stops it from publishing.

## Open questions

1. Exact canonical layouts for each item state, and whether descriptor and fee schedule should be
   carried as hashes (with preimages in proofs) or in full.
2. Pointer size: a full 32-byte content id, or a 16-byte prefix.
3. Whether `item_states` (233) should be mandatory, so readers never need a lookup, at the cost of
   bytes.
4. Migration: cross-ledger pointers from a receiver's first commitment to the source's last, and
   a migration item to make double credits a fork proof.
5. A credit-index item per ledger, so an uncredited payment is a transition proof (the operator
   committed "credited set without X" after the deadline) instead of a segment.
6. Whether the snapshot at activation should be checked by members against their replicas before
   cosigning the move (refusal only), which keeps the one remaining replay-based conviction narrow.
7. Proof size for long items: an item touched thousands of times needs no path for transition
   proofs, but a pair proof over a long gap (§4.3) carries every intermediate commitment of that
   item.

## Related DEPs

DEP-02 (encoding, balance commitments), DEP-05 (quorum rules), DEP-06 (proofs; verify before
publishing), DEP-07 (fees), DEP-16 (descriptors), DEP-17 (nonces), DEP-18 (rulesets), DEP-20
(exits, dormancy, migration).
