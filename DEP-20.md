# DEP-20: Swap-Only Obligations and Rotation Settlement

Status: Draft

## Abstract

This document narrows the operator's obligations to ledger-internal operations and
atomic swaps, removes on-chain withdrawal as an operator duty, and makes the quorum
rotation the ledger's settlement event: exit requests are paid from the vault at
rotation as a right, and reserve additions (splices) are made at rotation as an
operator option. It also describes the operator's own deposit as courier inventory
and the cold-start path that follows.

## Motivation

DEP-10 §Withdrawal obliges the operator to broadcast on-chain withdrawals from its
own liquidity, and DEP-11 makes failure to do so provable censorship. Deposited
coins are held by the operator, not the vault, so an honest operator facing net
outflow can be unable to pay and is then slashed for illiquidity. The protocol's
own rule (WP §lightning) is that atomic services may be performed by anyone and only
services requiring trust are assigned to the party with slashable collateral;
withdrawal was the one atomic service assigned to the trusted party.

The vault already holds reserves at least equal to obligations and is spendable by
the quorum at every rotation. It is therefore the natural source of a guaranteed
exit that does not depend on operator liquidity.

## Specification

### 1. Operator obligations

The operator's slashable obligations are:

- process signed ledger-internal requests within `service_response_blocks`
  (DEP-11, DEP-12): `TransferLock`, `TransferComplete`, `TransferFail`, deposit
  open/close, key rotation, and `ExitRequest` acceptance (§3);
- credit on-chain funding before the offer's `deadline_block` (DEP-11);
- resolve locks at their timeouts (DEP-11);
- include visible exit requests in the next rotation (§3);
- rotate before `quorum_expiry` and remain active (DEP-11, DEP-19).

On-chain withdrawal (`OnchainLock` / `OnchainFulfill` / `OnchainFail`, DEP-10
§Withdrawal) is no longer an obligation. Operators MAY offer it as a swap service
under §2. DEP-11 §Withdrawal and Transfer Processing is amended to cover transfers
and exit requests only.

### 2. Swaps

Exit to lightning or on-chain is a hash- or point-locked swap (DEP-09, DEP-13,
DEP-16) against any deposit holder with external liquidity. The protocol guarantees
that a funded swap completes or refunds atomically and that refusal to process the
lock is provable censorship. It does not guarantee a counterparty.

Operators SHOULD run a courier from their own deposit and MUST advertise its
capacity and fees in the guarantee matrix (DEP-04) under regimes `onchain_swap`,
`invoice_pay`, and `transfer_courier`, honesty `bridge_only`. Wallets MUST treat the
absence of any exit regime as "no fast exit" and price accordingly; the rotation
exit (§3) is always available.

### 3. Exit requests and rotation exit

**ExitRequest (new operation).** A depositor submits a signed request containing
`deposit_id`, `amount_msats`, and an on-chain `address`. The operator appends
`ExitRequest` to the ledger within `service_response_blocks`; the amount is moved to
`locked_balance` and cannot be spent. A request not appended within the window is
escalated under DEP-12 like any other request.

**Cutoff.** Each `QuorumBegin` carries `exit_cutoff_height`, which MUST be no
earlier than the rotation's `block_height − exit_cutoff_margin_blocks` (per-quorum,
recorded in `QuorumAddMember`, strictest applies, suggested 144). Co-signers refuse
a rotation whose cutoff is earlier. Every `ExitRequest` appended at or before the
cutoff, and every escalated request causally visible to the operator at or before
it (DEP-19 §8), MUST be settled in that rotation.

**Cancellation.** A depositor MAY submit `ExitCancel` (signed by the descriptor)
for a pending request. The operator MUST append it within
`service_response_blocks`, and a cancel appended before the rotation's recording
update takes effect: the request is excluded from settlement and the locked amount
released. A request MAY carry `expires_at_height`; if no rotation has settled it
by that height it is released without further action. What is guaranteed is
therefore that a cancel is processed on the service clock and that an expiring
request releases at its height; a request with no expiry that is not cancelled is
held until the next rotation.

A cancel appended after the cutoff but before the recording update changes the
due set, so the operator must rebuild the rotation transaction. Operators SHOULD
construct and collect signatures on the rotation as late in the cutoff margin as
practical, and cosigners compute the due set from the ledger at signing time
regardless.

**Rotation transaction.** The `QuorumBegin` rotation transaction (DEP-03 §Rotation transaction,
which fixes its byte layout and fee) spends the old vault into:

- the new vault, valued at `old vault + splice_in − Σ exits − fee`;
- one output per settled exit request, to its `address`, aggregating requests below
  the dust threshold into the next rotation rather than dropping them.

The `QuorumBegin` update records `exit_outputs` (request ids and amounts),
`splice_in_outpoint` if any, and debits each settled deposit by its exit amount in
the same update. `reserves_amount_msats` and obligations fall by the same total, so
the invariant `obligations ≤ reserves` is preserved. `collateral_amount_msats` is
unchanged by exits.

**Co-signer rule.** Before co-signing a `QuorumBegin`, each member MUST compute the
set of requests due under the cutoff from its own replica and the causal record, and
MUST refuse if any is omitted, mis-amounted, or misaddressed, or if the vault and
ledger debits disagree.

**Proof.** A `QuorumBegin` that settles fewer than the due requests is a
`NonConforming` update against its signers (DEP-19 §5). An operator that lets the
cycle pass without rotating while due requests exist is censoring under
`service_response_blocks` measured from the cutoff, and is subject to the DEP-19
inactivity path if silent. On custody transfer, the winner's acquisition rotation
MUST settle all requests due at `last_valid_sequence`; the lottery output covers
them because it covers obligations.

**Wire and state rules.** These make every replica compute the same due set and the same
balances.

- *Authorisation.* `ExitRequest` and `ExitCancel` are depositor-signed like other spends: they
  carry `nonce` and `expiry` and a `witness` over the DEP-17 operation preimage, op type `spend`,
  with arguments `kind` = symbol `exit`, `amount` (int, msats), `destination` (bytes, the
  `exit_address` scriptPubKey) and, only when present, `expires_at_height` (int); for a cancel,
  `kind` = symbol `exit_cancel` and `exit_request_id` (bytes).
- *Request.* Applying an `ExitRequest` requires `amount > 0` and `amount ≤` the deposit's available
  balance, moves `amount` into `locked_balance`, and records a pending request identified by SHA256 of the operation's TLV bytes
  (as signed, witness included; the depositor's nonce makes it unique), with its deposit, amount,
  `exit_address`, `expires_at_height`, and the `block_height` and sequence of the update carrying it.
- *Cancel.* `ExitCancel` names a pending request of the same deposit by `exit_request_id`; applying it
  unlocks the amount and removes the request. Naming no pending request is non-conforming.
- *Expiry.* Before the operation of any update at `block_height` h is applied, every pending request
  with `expires_at_height ≤ h` is released (unlocked and removed); for a rotating `QuorumBegin` the
  release comes after its settlement, so a request due under the cutoff settles.
- *Due set.* For a `QuorumBegin` that rotates a vault, at `block_height` h with `exit_cutoff_height`
  c (h − `exit_cutoff_margin_blocks` ≤ c ≤ h; absent means c = h − margin), the due requests are the
  pending ones whose update's `block_height ≤ c`, with no `expires_at_height` or one > c, and whose
  output clears the dust floor after its own cost (below), in the order their updates were
  appended. The due set is a function of the ledger and c alone, so every member computes it alike
  whatever its own chain tip. A member asked to sign the rotation (`rotation_sign`, which carries
  c) accepts any c within [tip − margin − 6, tip + 6] of its own tip. Other requests stay pending (dust is
  carried to a later rotation, or released by cancel or expiry).
- *Who pays.* Each exit pays only its own output's marginal cost,
  `exit_cost = feerate × (9 + len(exit_address))` sats, with `feerate` the rotation's (DEP-03); the
  vault pays the rest of the rotation. The output is `floor(amount / 1000) − exit_cost` sats and is
  due only if that is at least 330.
- *Settlement.* `exit_outputs` lists the due requests in that order, entry i with the request's
  deposit, amount and `vout` = i + 1, and the rotation transaction (DEP-03) pays output i + 1
  `floor(amount / 1000) − exit_cost` sats to its `exit_address`. Applying the `QuorumBegin` debits each entry's
  deposit `balance` and `locked_balance` by its amount and removes the request. A `QuorumBegin`
  with no current vault (the first, or the first after `DisputeAcquire`) settles no exits.
- *Amounts.* With V the old vault's value, F the rotation fee and E the sum of the settled exits'
  `exit_cost` (all sats), the vault's own share of the fee is F_v = F − E, the new
  `collateral_amount_msats` is `floor(old_collateral × (V − F_v) × 1000 / (old_reserves +
  old_collateral))`, and `amount` (reserves) is the new vault's value × 1000 minus it. Exits
  therefore come out of reserves only and pay their own outputs; collateral bears only its share of
  the base fee. With no exits this is the existing proportional split.

**Off-cycle settlement.** The operator MAY append a `QuorumBegin` to the same
member set at any time to settle exits early. It resets `quorum_expiry` as any
rotation does.

### 4. Splice-in

At any rotation the operator MAY add an input `splice_in_outpoint` from its own
funds. `reserves_amount_msats` and/or `collateral_amount_msats` rise by the added
value as declared; co-signers verify the outpoint and the new totals as in DEP-03
§QuorumBegin. Splice-in is optional and unprovable if omitted.

**Wire and checks.** The `QuorumBegin` records `splice_in_outpoint` (type 282: the txid in
internal byte order ‖ vout, u32 big-endian) and `splice_in_amount_msats` (type 284), equal to the
outpoint's value × 1000. The rotation transaction (DEP-03) spends it as input 1. Because the
BIP-341 sighash commits to every prevout, a member asked to sign the rotation (`rotation_sign`,
which then carries `splice_in_outpoint`) looks the outpoint up itself: it MUST be confirmed to the
policy depth of DEP-03 §QuorumBegin and unspent, and its value and scriptPubKey enter the sighash.
The operator signs input 1; a cosigner of the `QuorumBegin` MUST verify both inputs' witnesses
(a recorded rotation must be broadcastable).

**Amounts.** With c₀ the collateral the rotation would carry without the splice (§3 *Amounts*, with
F the fee of the transaction actually built, splice input included), the new
`collateral_amount_msats` is any value in [c₀, c₀ + `splice_in_amount_msats`], and `amount`
(reserves) is the new vault's value × 1000 minus it: the operator declares how the added value
divides, and neither part may fall below its no-splice value. The DEP-05 collateral floor applies
as to any `QuorumBegin`.

### 5. Self-fill as inventory

An operator MAY hold deposits on its own ledger. Such balances are obligations like
any other, count toward `obligations ≤ reserves`, pay the quorum's minimum fees, and
are inherited on custody transfer. They are the on-ledger leg of the operator's
courier; the external leg is the operator's lightning or on-chain liquidity.

A depositor exiting by swap moves balance to the courier's deposit; total
obligations are unchanged and no rotation is needed. Reserves therefore shrink only
through §3 exits.

### 6. Cold start

A new ledger with a self-filled operator deposit and no depositors is fully
functional. The operator swaps a slice of its own balance, through any courier, for
balance on an established ledger; it then holds inventory on both and can route
between them. No on-chain step beyond the initial vault is required.

### 7. Wallet rules

- Read `exit_cutoff_height` and the rotation interval from ledger history; treat
  the interval as the guaranteed exit latency.
- Prefer ledgers advertising swap capacity for fast exit; never rely on it for
  amounts above what the wallet can wait one rotation to recover.
- Refuse a ledger whose latest `QuorumBegin` omitted a due `ExitRequest`.

### 8. Dormancy rotation

Dormancy handling is a bucket rule, not a per-deposit decision, so the operator
never selects accounts.

**Parameters** (per quorum, recorded in `QuorumAddMember`, strictest applies):
`dormancy_blocks` (suggested 26280, ~6 months), `dormancy_amount_msats`
(suggested 10 × 34 vB × the `reference_feerate_sat_vb` the operator records in
each `QuorumBegin`; the value in the most recent rotation's recording update is
the one in force for the next dormancy bucket, and cosigners refuse a rotation
whose stated feerate is below the median of their own chain-source estimates),
`dormancy_notice_blocks` (suggested 2016).

**8.1 Selection.** The operator appends `DormancyNotice` naming a rotation height
at least `dormancy_notice_blocks` ahead. At that rotation every deposit with no
signed activity for `dormancy_blocks` as of the notice is in the bucket; any
signed activity before the rotation removes it. Co-signers MUST refuse a rotation
that includes a deposit outside the bucket or omits one inside it.

**8.2 Large, addressable.** Bucket deposits at or above `dormancy_amount_msats`
whose descriptor yields a bitcoin address are spun out as exit outputs (§3), full
balance, output fee borne by the operator.

**Precise rules (8.1–8.2).** These make every replica compute the same bucket.

- *Parameters.* `dormancy_blocks` (type 318) and `dormancy_notice_blocks` (type 332) are optional on
  `QuorumAddMember`; the largest value among the promoted members applies, defaulting to 26280 and
  2016. `dormancy_amount_msats` = 10 × 34 × `reference_feerate_sat_vb` × 1000, with the governing
  `QuorumBegin`'s feerate (DEP-03 §Reference feerate; 2 when none).
- *Signed activity* of a deposit is the `block_height` of the latest update carrying a
  depositor-signed operation it spends from or authorises: `InvoiceLock`, `OnchainLock`,
  `TransferLock` (source), `DepositKeyRotate`, `ExitRequest`, `ExitCancel`; initially its
  `DepositOpen`'s. Receives and fee collections are not activity.
- *Notice.* `DormancyNotice` (op 102) carries `rotation_height` (306) ≥ the notice's
  `block_height` + `dormancy_notice_blocks`. One notice is outstanding at a time; it is consumed by
  the first rotating `QuorumBegin` whose `exit_cutoff_height` is ≥ `rotation_height` (so, like the
  exits' due set, the spin-outs depend on the recorded cutoff, not on any member's tip).
- *Bucket.* At that `QuorumBegin`, the bucket is every deposit with a positive balance, no locked
  balance and no pending exit, whose signed activity is ≤ the notice's `block_height` −
  `dormancy_blocks`. Activity after the notice removes a deposit (its signed activity moves past
  the bound).
- *Addressable.* A deposit is addressable when its descriptor is `pk(K)`; its address is the
  key-path P2TR with K's x-only key as internal key (no script tree). Others are not addressable.
- *Spin-out.* Bucket deposits with balance ≥ `dormancy_amount_msats` that are addressable are paid
  `floor(balance / 1000)` sats each, in ascending `deposit_id` order, as rotation outputs after the
  §3 exits. The `QuorumBegin` records them as `dormancy_outputs` (336), entry j with the deposit,
  its full balance and its vout; applying it debits each deposit's balance to zero. Their output
  costs D = Σ `feerate × (9 + 34)` come out of collateral: with the vault's base share of the fee
  F_v = F − E − D (§3 *Amounts*), the new `collateral_amount_msats` is
  `floor(old_collateral × (V − F_v) × 1000 / (old_reserves + old_collateral)) − 1000 × D`. A `QuorumBegin` that consumes a notice and records any other
  set of `dormancy_outputs` is `NonConforming`.

**8.3 Small, or non-addressable: negotiated migration.** All other bucket
deposits are migrated together to a receiver that has agreed in advance:

1. *Offer.* Before any notice, the operator publishes `DormancyOffer` (Kind
   9110): manifest hash, deposit count, total balance, the fee terms the deposits
   carry, and any premium the operator will pay the receiver. Members and other
   operators MAY respond.
2. *Accept.* A receiver appends `DormancyAccept` to its own ledger naming the
   offer. Its co-signers MUST verify that the receiver's obligations plus the
   manifest total fit within its reserves, and refuse otherwise. The receiver MAY
   splice the incoming coins into its vault at its next rotation (§4) to restore
   headroom.
3. *Notice.* The operator then appends `DormancyNotice` naming the receiver and
   manifest and starting `dormancy_notice_blocks`. Deposits that show activity
   before the rotation are removed from the manifest; the accept covers the
   reduced total.
4. *Rotation.* One output to the receiver's funding address for the manifest
   total; the manifest is recorded in the rotation update. The receiver MUST
   credit each deposit under the same descriptor on confirmation (DEP-10), at
   the terms in the offer. Only a receiver whose quorum fee floors (DEP-05
   §Member Terms) are at or below every migrated deposit's schedule MAY accept;
   its co-signers verify this alongside capacity in step 2, so DEP-05's floor
   rule is never overridden and the depositor's terms are unchanged. The
   receiver MAY later use `FeeChange` within each deposit's negotiated limits.
   Failure to credit is `UncreditedOnchainPayment` against the receiver, with
   the manifest as the offer.

If no receiver accepts, small bucket deposits stay and continue to pay fees; the
operator MAY re-offer. No party is obliged to take a bucket.

**Precise rules (8.3).**

- *Offer.* `DormancyOffer` (Kind 9110) is `{ledger_id, manifest, manifest_hash, total_msats,
  premium_msats}`: `manifest` lists, for each deposit offered, its id, balance, fee schedule and
  descriptor; `manifest_hash` is SHA256 of the manifest encoded as `migration_manifest` (type 316).
- *Accept.* The receiver appends `DormancyAccept` (op 103) to its own ledger: `offer_event_id`,
  `manifest_hash`, `accepted_total_msats`, `exit_address` (the scriptPubKey the migration output
  pays, of the same type as the receiver's DEP-10 funding offers), `expires_at_height`, and
  optionally `deposit_id`, its own deposit credited the premium. Its cosigners, given the manifest
  in the cosign request, MUST check its hash; that obligations + the totals of its unexpired
  uncredited accepts + `accepted_total_msats` ≤ reserves; that its quorum's fee floors (DEP-05)
  are ≤ every manifest deposit's schedule; and that it has no other accept outstanding (one
  migration at a time). Until credited or past `expires_at_height`, an accepted total counts
  against the receiver's capacity.
- *Notice.* The source's `DormancyNotice` names `migration_receiver`, `manifest_hash`, and carries
  the offered `migration_manifest` (316, hashing to `manifest_hash`), `dormancy_accept` (338), the
  receiver's signed `DormancyAccept` update, and `premium_msats` (340, whole satoshis, optional). Source cosigners verify it
  without fetching the receiver's ledger: it decodes, its operator signature is by
  `migration_receiver`, it names this `manifest_hash`, and its `expires_at_height` is after the
  notice's `rotation_height`.
- *Migration.* At the consuming `QuorumBegin` the migrated deposits are those in the manifest that
  are in the bucket and not spun out (§8.2), each at its balance there, taken in ascending deposit
  id when the running total plus it plus `premium_msats` stays ≤ `accepted_total_msats` (the
  accept reserves the premium's credit too) and skipped otherwise; the rest stay. The rotation pays one
  output, after the spin-outs, to the accept's `exit_address`: `floor(Σ / 1000) + premium` sats.
  The `QuorumBegin` records `migration_manifest` (the migrated entries), `migration_receiver` and
  `migration_vout`, and debits each migrated deposit to zero. The output's own cost
  (`feerate × (9 + len)`, a fee in `F_v`'s accounting like a spin-out's) and the premium (value
  paid out, not a fee) both come out of collateral: the §3 collateral is further reduced by
  `1000 × (cost + premium)`.
- *Credit.* Once the output confirms, the receiver appends, for each manifest entry, a
  `DepositOpen` with its descriptor and fee schedule if the deposit is new, then an `OnchainCredit`
  of its exact amount naming the rotation txid and `migration_vout` (several credits name one
  outpoint) with `funding_address` = `migration:` ‖ hex(`manifest_hash`), and the premium to the
  accept's `deposit_id` the same way. Migration credits draw on the accept's reservation, not on
  free capacity. The receiver absorbs the sub-satoshi
  remainder of `floor(Σ / 1000)`.
- *Splice.* The receiver MUST splice the migration output into its vault (§4) at its next rotating
  `QuorumBegin`. Its ledger records the outpoint at the first migration credit; a rotating
  `QuorumBegin` that does not splice it is `NonConforming` (DEP-19 §5): the obligation was
  credited, and the coins backing it must join the vault. The splice closes the accept.
- *Proof.* A receiver that has not credited every migrated entry `service_response_blocks` after
  the migration output confirms is proved by `UncreditedOnchainPayment` with migration evidence
  (DEP-06): the source's `DormancyNotice` update (which carries the receiver's signed accept and
  the manifest), the source's `QuorumBegin` update (migrated entries, receiver, vout, rotation
  txid), and the confirming block; the verifier checks the receiver's ledger for the credits.

**8.4 Who pays.** The initiator of an exit pays its output's marginal cost (§3
*Who pays*): a depositor's `ExitRequest` bears its own `exit_cost`; dormancy and wind-down
outputs are paid in full by the operator, from collateral. The vault pays the base rotation.
Timing a forced move into high fees costs the operator, not the depositor.

### 9. Wind-down

An operator MAY close a ledger by appending `LedgerWindDown` with a final rotation
height at least `winddown_notice_blocks` ahead (suggested 4032). During the notice
period the operator MUST continue to process requests. At the final rotation every
deposit is treated as in the bucket: addressable deposits at or above
`dormancy_amount_msats` are spun out (§8.2), the rest migrated to a receiver
negotiated under §8.3; remaining obligations are zero; the rotation's "new
vault" output is to the operator alone, and the ledger is tombstoned. If no receiver
is available, the final rotation pays the remaining obligations into a lottery
output exactly as a respectful confiscation would (DEP-03 §Respectful custody);
the operator keeps its collateral as change, and the winner posts replacement
collateral on claim as in any custody transfer. Nothing is forfeited and nothing
is collateralised twice. Wind-down removes the
operator, never a balance.

Members are released at the final rotation. This is the intended end of life for a
ledger whose activity no longer justifies its quorum; the alternative, letting it
expire, ends in the Tier 3 solo path with depositors' funds inside.

### 10. Migration

An exit output (§3, §8, §9) MAY pay another operator's funding-offer address. The
receiving operator credits the deposit on confirmation under DEP-10. Batched exits
therefore move balances between ledgers at one output's cost each, which makes
spreading across operators (DEP-11 §Fund Distribution) cheap in practice.

**How a wallet migrates.** It obtains a cosigned offer from the destination for the deposit it
wants credited, with `min_sats` ≤ the exit's output value (`floor(amount / 1000) − exit_cost`) ≤ `max_sats`, then appends an
`ExitRequest` paying the offer's `funding_address` with `expires_at_height` ≤ the offer's
`deadline_block` − 6. Either the exit settles while the offer can still be completed, or it is
released at `expires_at_height` and the balance stays on the source ledger: the migration never
lands where no offer covers it. Once the rotation confirms, the wallet completes the offer with the
rotation's `txid` and the exit's `vout` (its `exit_outputs` entry). Nothing here is new to the source
ledger: a migration is an exit.

## Rationale

Illiquidity ceases to be fraud: the operator can always sign locks and credits, and
the vault pays exits. Exit becomes cooperative-close-now, force-close-on-a-timer,
with the timer being the rotation interval, which is a market-priced parameter
visible on the ledger. Batching every exit into one transaction per cycle keeps
small depositors from being priced out. The resisted case needs no new machinery:
the acquisition rotation is a rotation. The dormancy bucket gives an operator a
clean way to shed obligations it cannot carry without ever choosing an account, and release members
from ledgers that no longer pay them; the dust floor follows the fee market so
nothing is lost to fees that would not have been drained anyway.

## Related DEPs

DEP-03 (rotation transaction), DEP-04 (guarantee matrix), DEP-09/13/16 (swap
locks), DEP-10 (withdrawal, superseded in part), DEP-11 (obligations), DEP-12
(escalation), DEP-19 (causal visibility, inactivity, `NonConforming`).

## Open questions

1. Minimum rotation interval. A very short interval makes exit fast but multiplies
   on-chain cost and co-signing load; a quorum-negotiated `max_rotation_interval`
   may belong in `QuorumAddMember`.
2. Whether wind-down should require member co-signature beyond the rotation
   itself. With the operator paying forced-exit fees, no forfeiture, and a long
   notice, the operator's only unilateral power is to end its own service on a
   long clock at its own cost, which is judged sufficient; recorded for review.
