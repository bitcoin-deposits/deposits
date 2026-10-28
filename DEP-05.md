# DEP-05: Quorum and Collateral

## Abstract

This document specifies the quorum membership protocol and collateral mechanics. An operator's UTXO is split into reserves (deposit capacity) and collateral (security bond), both held in the same Taproot output controlled by the quorum. If the operator misbehaves, the quorum confiscates the collateral directly from the operator's own ledger.

## Quorum Membership

### Joining

An operator requests another operator to join their quorum. The request includes:

- The member's pubkey
- Fee limits the member imposes (minimum fees the operator must charge)

If the member accepts, the operator appends `QuorumAddMember` (disc 43) to their own ledger, and the member appends `QuorumJoin` (disc 46) to their own ledger. This creates a two-sided auditable record.

`QuorumAddMember` **stages** the member: they are appended to a pending list (`next_quorum_members` in the state model) and gain no voting power yet. A subsequent `QuorumBegin` promotes all staged members to active in a single atomic step (see below). This lets an operator add several members across separate ledger updates and activate them together.

To serve as a quorum member, an operator must have at least `min_member_collateral` collateral at stake on their own ledger(s). This ensures quorum members have skin in the game — misbehavior as a quorum member (e.g., co-signing a non-conforming update) can result in slashing on their own ledger.

### Member Terms

When joining, each member specifies:

- **min_fee_bps**: minimum annualized fee rate (basis points) the operator must charge
- **min_fee_fixed**: minimum annualized fixed fee (msats/year)
- **max_fee_period**: maximum fee collection period (blocks)
- **membership_until**: block height until which the member commits to serving

The operator cannot open deposits with fees below the strictest member's minimums. This protects members from inheriting unprofitable obligations after a custody transfer.

- **max_descriptor_bytes**: maximum serialized descriptor size (bytes) the member will accept on deposits they may inherit after custody transfer

Members also specify timing parameters that govern protocol obligations (see DEP-11):

- **dispute_response_blocks**: blocks before a member must respond to embedded fraud evidence
- **dispute_arm_blocks**: blocks after `DisputeEnter` during which members must arm for the lottery
- **service_response_blocks**: blocks before an unprocessed signed request becomes provable censorship (the largest a seated member declared governs; 72 when no member declared one)
- **max_transfer_timeout_blocks**: maximum `timeout_height` distance for `TransferLock`
- **inactivity_blocks**: blocks without a co-signed update before a majority may attest inactivity (DEP-19)
- **cosign_response_blocks**: blocks to co-sign or refuse a visible proposal (DEP-19 §9)
- **exit_cutoff_margin_blocks**: latest a rotation's exit cutoff may sit before its block (DEP-20 §3)
- **dormancy_blocks**, **dormancy_amount_msats**, **dormancy_notice_blocks**: dormancy bucket parameters (DEP-20 §8)

The strictest (smallest) values across all members apply to the quorum. The operator cannot open deposits with descriptors exceeding the quorum's `max_descriptor_bytes` limit.

Members also specify compensation terms — the operator commits to pay each member a share of collected fees (see DEP-07) in exchange for co-signing:

- **compensation_bps**: basis points of collected fees that flow to this member (default 300 = 3%). With Q=7 members at the default, ~21% of fee revenue is distributed to cosigners.
- **compensation_deposit_id**: deposit on the operator's ledger where the member's share lands. The deposit MUST exist when `QuorumAddMember` is appended.
- **compensation_frequency_blocks**: cadence at which accrued compensation is paid out (default 2016 ≈ 2 weeks, mirroring the default fee-collection cycle).

These fields are per-member, not reduced to a quorum-wide minimum — different members can negotiate different rates. Omitting them means the member waived compensation.

### QuorumBegin (disc 12)

`QuorumBegin` does two things atomically:

1. **Promotes the staged membership.** The pending set (`next_quorum_members`, populated by `QuorumAddMember`) **replaces** the active voting set wholesale. Anything not in the staged set at `QuorumBegin` time is dropped. This means refreshing an existing quorum requires re-staging every member the operator wants to keep by issuing a fresh `QuorumAddMember` for each before the new `QuorumBegin`.
2. **Rotates the on-chain multisig.** The operator spends the old reserves UTXO into a new Taproot output whose script reflects the new active member set (see DEP-03).

After `QuorumBegin`, every subsequent update MUST carry the cosignature threshold specified in §Lifecycle for the operation's class at the update's `block_height`. Within the active period (before `quorum_expiry`) the threshold is strict majority (`floor(n/2) + 1`) for every operation; past `quorum_expiry` it cascades through the lifecycle tiers and applies only to establishment operations (`QuorumAddMember`, `QuorumRemoveMember`, `QuorumBegin`). The strict-majority rule prevents the operator from maintaining parallel chains within the active period — a majority of cosigners will have seen and validated the canonical chain before signing any new update. `QuorumBegin` also records the `quorum_expiry` (shortest membership duration), `collateral_amount_msats`, and (since 2026-05) a parallel `quorum_member_ledger_ids` array pairing each member's pubkey with their own ledger_id (sourced from the corresponding `QuorumAddMember.member_ledger_id`). The pairing lets fraud-proof verifiers and other consumers tie a cosigner's `member_ledger_hash` (carried in the cosignatures field) back to a specific on-chain ledger without re-walking the operator's `QuorumAddMember` history. Older `QuorumBegin` events omit the array; decoders that need the mapping for those fall back to deriving it from the operator's prior `QuorumAddMember` operations.

**The first `QuorumBegin` (applied from `PreQuorum`) itself MUST carry cosignatures from `floor(n/2) + 1` of the staged set** (n = `len(next_quorum_members)` at apply time). Without this rule the operator could unilaterally transition the ledger to Active with a fabricated member list or a reserves outpoint that doesn't exist on-chain — there is no active quorum yet to refuse a bad update, and post-transition the operator is trusted only because the active quorum attested the rotation. Validators MUST reject a first `QuorumBegin` that lacks this majority, and cosigners MUST verify the reserves UTXO exists, is unspent, carries the declared value, and has a network-dependent minimum number of confirmations before signing (see DEP-03 §QuorumBegin for thresholds). The operator cannot issue a `QuorumBegin` against an empty staged set — it must have first issued one or more `QuorumAddMember` operations.

**Size policy.** Validators reject any `QuorumBegin` whose `Q` (cosigner count, operator not counted) is not in `VALID_QUORUM_SIZES = {3, 5, 7}` — odd-only so thresholds have a clean majority, ≥3 for redundancy, ≤`MAX_QUORUM_SIZE_POLICY = 7`. This is a policy cap, not a protocol cap — the dispute lottery (see DEP-03 §Custody Lottery) supports up to N=15 disputants, but until production reliability data justifies going higher we limit `Q` to 7 (every cosigner can dispute the operator's custody). Lifting the cap or extending the allowed set is a one-line constant change with no script or wire-format implications.

### Removing Members

`QuorumRemoveMember` (disc 44) takes effect **immediately** on the ledger — the named member is dropped from both the active set and the pending set on apply. No subsequent `QuorumBegin` is required for the member to lose voting rights. However, the on-chain Taproot UTXO still encodes the pre-remove member set, so spends continue to require the removed member's signature until the next `QuorumBegin` rotates the multisig. This creates a window in which ledger-level cosig thresholds use the shrunken quorum while on-chain spends cannot proceed without the departing member — operators typically follow a `QuorumRemoveMember` with a `QuorumBegin` in the next ledger update to close the window.

Unlike `QuorumAddMember` (staged) the remove is immediate because the point of removing a member is usually that they have misbehaved or gone silent; making the operator wait until the next rotation to strip voting rights would let a captured member keep vetoing updates in the meantime.

## Collateral

Collateral is a portion of the operator's own UTXO, held in the same Taproot output as reserves. The quorum controls both reserves and collateral. If the operator misbehaves, the quorum confiscates the collateral directly — no cross-ledger coordination required.

### Structure

The operator's UTXO is split into two portions:

    UTXO = reserves + collateral

- **Reserves**: the deposit capacity — wallets can deposit up to this amount
- **Collateral**: the security bond — cannot be used for deposits, at risk of slashing

Both live in the same Taproot output, controlled by the same quorum via tiered spending paths (see DEP-03). Both `reserves_amount_msats` and `collateral_amount_msats` are declared in `LedgerOpen` and `QuorumBegin`. Co-signers MUST verify that `reserves_amount_msats + collateral_amount_msats` equals the on-chain UTXO value (in msats). `QuorumBegin` may update either value (e.g., to adjust the ratio), subject to quorum member agreement via co-signature.

### Collateral floor

Collateral is a floor on the vault's split, not a cap on credits. Each member MAY require a
minimum collateral share in its `QuorumAddMember` (`min_collateral_bps`, DEP-02 type 314); the
quorum's floor is

    c_min_bps = max(2000, min_collateral_bps of every member the QuorumBegin promotes)

and every `QuorumBegin` MUST satisfy `collateral_amount × 10000 ≥ c_min_bps × (reserves_amount +
collateral_amount)`. The spec-wide lower bound of 2000 bps (20%, so the deposits' share R ≤ 0.8)
follows the collateral-ratio analysis (cl-deposits docs/TRUST-MODEL.md §2h), beyond which the
collusion tolerance falls below a quarter of operators in every seating; quorums attested under
DEP-21 might later justify a lower bound. A cosigned `QuorumBegin` below the floor is
`NonConforming` (DEP-19 §5).

### Slashing

When the operator is proven non-conforming (see DEP-06), the quorum confiscates the entire UTXO. The collateral portion is the operator's real loss — deposits are owed back to depositors, and reserves not covering obligations are the operator's own funds (an operator may hold deposits on their own ledger, so excess reserves are not a dependable penalty). The lottery winner (see DEP-03) takes over the ledger and inherits obligations; the slashed value (excess reserves + the operator's full collateral) is split equally among the `Q` cosigners, and the winner provides *replacement* collateral on lottery claim. Operating a ledger is a service commitment, not a windfall — the winner's economics post-takeover are roughly neutral, and the slashing reward is shared evenly so every cosigner is uniformly incentivized to dispute.

If the operator misbehaves as a **quorum member** on another operator's ledger (e.g., co-signs a non-conforming update), proof of this misbehavior can be presented to the misbehaving member's own quorum, triggering slashing on their own ledger.

### Multi-Ledger Operators

Operators SHOULD run multiple ledgers (recommended: 3-5) with **independent quorums** per ledger. This provides:

1. **Contagion**: misbehaviour proven on one ledger is punishable on every other ledger the operator runs whose quorum holds an honest majority (DEP-19 §5–6), so the operator's total collateral is at stake, not one ledger's. How much this bounds a coalition depends on quorum composition, not on the count of ledgers alone (see §Security Model).
2. **Capital efficiency**: the same total UTXO is split across ledgers, each with independent security.

The UTXO is split evenly: each ledger gets UTXO/L in reserves and UTXO/L in collateral (for L ledgers).

## Obligation Limits

A ledger's total obligations — the sum of every deposit's `balance` — must not exceed the reserves amount (from QuorumBegin). This is enforced when creating new funding offers or invoices (see DEP-10).

### Balance Accounting Model

Each deposit has two fields:

- **`balance`**: the total obligation the operator owes for this deposit (msats). This is the authoritative figure counted toward the ledger's obligations.
- **`locked_balance`**: a subset of `balance` that is currently earmarked for in-flight operations (pending transfers, invoice locks). It is not a separate bucket of funds and is not additive with `balance`.

Per-deposit spendable funds are `available_balance = balance - locked_balance`. Locking funds for an in-flight operation does not change the deposit's `balance` or the ledger's total obligation — the funds were already counted. Only settlement (credit/debit/fulfill) changes `balance`.

### Security Model

The Tier 0 spending path (DEP-03) is a quorum majority without the operator. This is what makes confiscation possible, and it means a quorum majority custodies the operator's entire vault. The arithmetic below bounds what a coalition gains from *ledgers it operates*; it does not bound theft of honest operators' vaults by a coalition holding a quorum majority, nor the case where the signing keys hold no slashable collateral. Those are bounded by quorum composition (DEP-19 §10) rather than by collateral. The simulation results assume wallets deposit only on honest operators and that colluding operators expose every key.

Consider an operator with UTXO = U, reserves fraction R, collateral fraction C = 1-R:

- **Per ledger**: reserves = U×R/L, collateral = U×C/L (for L ledgers)
- **Attack gain**: at most U×R/L per compromised ledger (stolen deposits)
- **Attack cost**: U×C/L per ledger where quorum retains honest majority (collateral slashed)

With R=40%, C=60%, L=5: each compromised ledger yields 0.08U in stolen deposits, but each slashed ledger costs the attacker 0.12U. The attacker must compromise more ledgers than they lose — which requires controlling majority of most quorums simultaneously.

Simulation results (N=50 operators, Q=5, 500 trials, sybil-optimal attacker):

| Reserves | Collateral | L | Max safe sybil% |
|:---:|:---:|:---:|:---:|
| 50% | 50% | 1 | 29% |
| 50% | 50% | 3 | 35% |
| 50% | 50% | 5 | 39% |
| 40% | 60% | 5 | 49% |
| 33% | 67% | 3 | 49% |

See PROPOSAL.md for full simulation methodology and parameter sweep.

## Co-Signer Obligations

Quorum members must maintain a full state replica of any ledger they co-sign for. Before co-signing an update, the member MUST verify:

1. **Chain continuity**: the update's `previous_hash` matches the member's last validated `chain_hash`
2. **State validity**: the operation can be applied to the member's local state replica without error (deposit exists, sufficient balance, valid fees, etc.)
3. **Obligation limits**: the running total of obligations does not exceed reserves. This is the only limit on credits: collateral is not a cap on obligations
4. **Collateral preservation**: operations do not reduce the collateral portion below `collateral_amount_msats`; reserves fall only through rotation exits that reduce obligations equally (DEP-20 §3)
5. **Collateral floor** (for a `QuorumBegin`): `collateral_amount × 10000 ≥ c_min_bps × (reserves_amount + collateral_amount)`, below
6. **Operator not deposed**: custody has not moved, and the ledger is not under a freezing dispute
   (below)

**Deposed operator.** A member MUST refuse to co-sign any update of the operator's chain once:

- **custody has moved**: a `DisputeAcquire` on any fork of the ledger names a new custodian, or
- **the member itself** has entered a dispute on the ledger whose `last_valid_sequence` is at or
  after the latest `QuorumBegin`, for any reason other than `quorum_expired`, or
- **a majority of the quorum** (`floor(n/2) + 1` of the current members) has entered such a dispute.

A dispute counts in every state it reaches (open, armed, yielded or acquired). A `quorum_expired`
dispute does **not** freeze co-signing: it is respectful, and the operator's re-establishment
(`QuorumBegin`, DEP-05 §Lifecycle) is exactly the update its members must still be able to sign.
A dispute is a `quorum_expired` dispute whenever its ground is the quorum's expiry, however the
member came to it: from its own expiry watch, or from a `QuorumExpired` proof (DEP-06) it received.
Its `DisputeEnter` carries reason `quorum_expired`, never a generic reason a peer would count as
freezing. (Signet soak, 2026-10-23: reference members disputed two expired cl ledgers on a received
`QuorumExpired` proof with the reason `auto_dispute`, froze, and the ledgers could never rotate.)
Implementations agree on the cases in the shared vector `cosign_refusal.json`.

**The ground of a dispute.** A `DisputeEnter`'s `reason` names its ground: `quorum_expired`, or the
DEP-06 proof type it rests on in snake_case (`non_conforming_update`, `equivocation`,
`unauthorized_vault_spend`, ...). A member writes the ground, never a generic label. A record that
carries a generic reason (`auto_dispute`, `fraud`, written before this rule) is judged by its
ground as the record shows it: it is a `quorum_expired` dispute iff it carries an expiry anchor
(`anchor_block_height`), or it cites no fraud proof (`fraud_proof_hash`) and its update's
`block_height` is past the `quorum_expiry` of the `QuorumBegin` governing at its
`last_valid_sequence`. Every rule here that asks whether a dispute is a `quorum_expired` dispute
(freezing, ending on re-establishment) asks it of the ground, not the label. (Signet soak,
2026-10-28: reference members' expiry disputes written as `auto_dispute` kept freezing ledgers
after the label rule above was fixed, because the records were older than the fix.) Vector:
`dispute_ground.json`.

**When a `quorum_expired` dispute ends.** Its ground is the expiry of the `QuorumBegin` governing at
its `last_valid_sequence`. Re-establishment answers exactly that ground: once the operator's chain
holds a `QuorumBegin` after the dispute's `last_valid_sequence`, the dispute is over unless its
confiscation already confirmed (DEP-06 §Race). Its disputant yields (`DisputeYield`) and releases
its pledge. No member arms on it, and none signs a confiscation for it. This is judged from the
ledger, not from the chain tip: the re-established quorum may itself have expired since, and that
later expiry is a new ground, which takes a new `DisputeEnter` whose anchor is past the new
`quorum_expiry`. A member MUST NOT let a live dispute on an earlier ground stand in for it.
(Signet soak, 2026-10-27: cl members kept expiry disputes opened before their operators
re-established, because they only stood down while the new quorum was live. When the new quorum
expired too they opened no new dispute, and the reference members, rightly, refused to arm on an
anchor older than the current expiry, so neither path could close the ledger.) Vector:
`expiry_dispute_ends.json`.

If any check fails, the member MUST refuse to co-sign. The chain continuity check (1) is the primary defense against parallel chains — if the operator has published a non-conforming update that the member rejected, subsequent updates will have a different `previous_hash` and the member will refuse.

### Cosignature Threshold

The number of distinct quorum-member cosignatures an update requires depends on the operation's *class* and the *lifecycle tier* at the update's `block_height`. See §Lifecycle below for the full schedule.

Within the active period (`block_height < quorum_expiry`) every update requires `floor(n/2) + 1` cosignatures from distinct quorum members. This ensures a majority of the quorum has validated every update. Since each cosigner verifies chain continuity from their own tip, the operator cannot obtain a majority for two different updates at the same sequence number — at least one member of any majority will have already signed the other version and will refuse.

Past `quorum_expiry`, value-moving operations become uncosignable (no threshold authorizes them); only *establishment operations* (`QuorumAddMember`, `QuorumRemoveMember`, `QuorumBegin`) can still be cosigned, and their required threshold cascades through the tiers in §Lifecycle as time passes.

### Cosign Rounds

A cosignature signs `cosign_data || member_ledger_hash` (DEP-02 §Co-signing). It is bound to that
update and to nothing about when it arrived. A cosignature that reaches the operator after it stopped
waiting is still valid for that `cosign_data`.

- **Keep late cosignatures.** An operator MUST NOT discard a cosignature only because it arrived late.
  It keeps every cosignature that verifies over a `cosign_data` it requested, one per member. A retry
  of the same update (identical `cosign_data`) starts from those, and asks the members only for the
  rest. Once the operator signs a different update at that sequence, the kept cosignatures are dead.
  It never attaches them to other bytes, and it may drop them.
- **`cosign_response_seconds`** (advisory, default 30): the time a member has to answer a cosign
  request, and so the least an operator waits before calling a round short. A member SHOULD answer
  within it, and SHOULD answer cosign requests ahead of other relay traffic. Wall-clock time is not on
  chain, so a late answer is not provable and is not a fault. The provable obligations stay
  block-based (`service_response_blocks`, DEP-11).

Without this rule a member that answers in 12 s, behind a burst of relay traffic, is never counted
against a 10 s deadline. Each retry is a new request, which arrives as late as the one before it.

### Conformance

Co-signing without state validation is non-conforming — a member who co-signs an update that violates obligation limits is complicit in the violation and may have their own collateral slashed on their own ledger(s).

### Membership Duration

Quorum membership duration is limited by `quorum_expiry` — the shortest member's `membership_until`. Before this block, the operator should refresh the quorum via a new `QuorumBegin` to reset the lifecycle and keep the full strict-majority cosign protection active. Missing the deadline is **not** fatal — see §Lifecycle for the graceful self-rescue path.

**Quorum expiry.** A `QuorumBegin`'s `quorum_expiry` MUST NOT exceed the shortest `membership_until` among the members it seats, as recorded in their `QuorumAddMember`s. Members that declared no `membership_until` impose no bound. The operator may shorten a member's commitment, never extend it. A `QuorumBegin` past the bound is non-conforming (`quorum_expiry_exceeds_commitment`), and every validator refuses it. An operator proposes `min(current_block + its own window, that bound)`. Its window is local policy; the suggested default is 4320 blocks. Vector: `quorum_expiry.json`. (Signet soak, 2026-10-24: the reference operator proposed `current_block + 4320` regardless of the members' commitments, so every rotation was refused and its ledgers ran into expiry. cl-deposits proposed the bound but did not check it as a validator.)

**Born expired.** A `QuorumBegin` whose `quorum_expiry` is at or below its own `block_height` is non-conforming (`quorum_expiry_not_after_block`), and every validator refuses it: the quorum it seats would be past expiry from its first update, so the rotation buys nothing and spends the vault's fee. An operator whose members' commitments are at or below the current block collects fresh consents (new `QuorumAddMember`s with a later `membership_until`) before it rotates. Vector: `quorum_expiry.json` (cases `born_expired`, `expiry_at_block`). (Signet soak, 2026-10-28: a reference operator rotated at height 9341 to `quorum_expiry` 7181 from members' stale commitments, and immediately tried again.)

### Lifecycle

A quorum's authority cascades through tiers anchored to `quorum_expiry`. At each tier the off-chain cosignature threshold for *establishment operations* (`QuorumAddMember`, `QuorumRemoveMember`, `QuorumBegin`) matches the on-chain spending tier from DEP-03 §Spending Tiers, so the two layers can never disagree about who has authority at a given chain tip. *Non-establishment operations* (every other op type — `InvoiceLock`, `OnchainFulfill`, transfers, etc.) are only cosignable in Tier 0; past `quorum_expiry` they become uncosignable until a fresh `QuorumBegin` resets the schedule.

| # | Event                          | Block                   | On-chain tier | Off-chain cosign threshold                              |
|---|--------------------------------|-------------------------|---------------|---------------------------------------------------------|
| 0 | begin                          | `H0 = QuorumBegin block`| Tier 0        | initial QuorumBegin signers (see §QuorumBegin)          |
| 1 | (rotation expected)            | `< quorum_expiry`       | Tier 0        | majority of cosigners                                   |
| 2 | quorum expiration              | `quorum_expiry`         | Tier 0 ends   | (value-moving ops become uncosignable)                  |
| 3 | majority confiscation          | `quorum_expiry`         | Tier 0        | majority cosigners → DEP-06 `QuorumExpired` confiscation |
| 4 | minority re-establishment      | `quorum_expiry + 720`   | Tier 1        | operator + minority (`ceil(n/2) - 1`) cosigners → degraded `QuorumBegin` |
| 5 | minority confiscation          | `quorum_expiry + 720`   | Tier 1        | minority cosigners → degraded DEP-06 confiscation        |
| 6 | solo-member re-establishment   | `quorum_expiry + 4032`  | Tier 2        | operator + one cosigner → degraded `QuorumBegin`         |
| 7 | solo-member confiscation       | `quorum_expiry + 4032`  | Tier 2        | one cosigner → degraded DEP-06 confiscation              |
| 8 | solo operator re-establishment | `quorum_expiry + 8064`  | Tier 3        | operator alone (no cosignatures required)                |

At every post-expiry tier, both *re-establishment* (operator-initiated `QuorumBegin`) and *respectful confiscation* (cosigner-initiated `QuorumExpired` dispute — see DEP-06) become available simultaneously. The two paths race for the same on-chain reserves UTXO; whichever spending transaction confirms first prevails, and the loser's path becomes invalid. Tier 3 has no confiscation pair — the operator cannot confiscate from themselves.

The cascade encodes "give the accountable party first crack at each authority level": cosigners get majority confiscation immediately at expiry because they were trusted to keep the quorum healthy; the operator gets minority re-establishment next (self-rescue with whoever they can still reach); minority cosigners get a final confiscation window; the operator gets solo re-establishment as the last resort. An honest operator who values their reputation or other ledger commitments will defend the ledger by re-establishing rather than walking away at Tier 3.

A successful `QuorumBegin` at any tier — degraded or not — spends the reserves UTXO into a new vault whose tapscript bakes a fresh `quorum_expiry` and a new lifetime schedule. All tiers reset.

### Confiscation

If the operator is proven non-conforming (see DEP-06), the quorum confiscates the operator's UTXO at the strict-majority tier. The collateral portion is forfeited; deposit obligations are transferred to the new custodian. This is the primary economic deterrent against operator misbehavior.

Past `quorum_expiry`, respectful confiscation under the `QuorumExpired` proof also becomes available at the same degraded thresholds as re-establishment (see §Lifecycle and DEP-06 §Respectful custody). A minority of cosigners can drive an `QuorumExpired` confiscation at Tier 1, a single cosigner at Tier 2.

## Related DEPs

- [DEP-02](DEP-02.md): Wire format (QuorumAddMember, QuorumRemoveMember, QuorumJoin, QuorumBegin fields)
- [DEP-03](DEP-03.md): On-chain transactions (reserves rotation, tapscript multisig, collateral in UTXO)
- [DEP-06](DEP-06.md): Fraud proofs and recovery (quorum members initiate disputes, confiscation)
- [DEP-07](DEP-07.md): Fee schedules (fee limits negotiated by quorum members)
- [DEP-10](DEP-10.md): Payment channels (obligation limits enforced at offer/invoice creation)
- [DEP-11](DEP-11.md): Time obligations (quorum rotation)
- [DEP-12](DEP-12.md): Certified delivery (service_response_blocks enforcement)
