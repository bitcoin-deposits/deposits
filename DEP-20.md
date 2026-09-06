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

**Cancellation.** A depositor MAY append `ExitCancel` (signed by the descriptor)
for a pending request before the cutoff; the operator MUST process it within
`service_response_blocks` and the locked amount is released. A request MAY carry
`expires_at_height`; if no rotation settles it by then it is released
automatically. Depositors who find a swap are therefore never held by their own
request longer than the cutoff margin.

**Rotation transaction.** The `QuorumBegin` rotation transaction (DEP-03) spends the
old vault into:

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

**Off-cycle settlement.** The operator MAY append a `QuorumBegin` to the same
member set at any time to settle exits early. It resets `quorum_expiry` as any
rotation does.

### 4. Splice-in

At any rotation the operator MAY add an input `splice_in_outpoint` from its own
funds. `reserves_amount_msats` and/or `collateral_amount_msats` rise by the added
value as declared; co-signers verify the outpoint and the new totals as in DEP-03
§QuorumBegin. Splice-in is optional and unprovable if omitted.

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
(suggested 10 × 34 vB × a reference feerate, revisable at rotation),
`dormancy_notice_blocks` (suggested 2016).

**8.1 Selection.** The operator appends `DormancyNotice` naming a rotation height
at least `dormancy_notice_blocks` ahead. At that rotation every deposit with no
signed activity for `dormancy_blocks` as of the notice is in the bucket; any
signed activity before the rotation removes it. Co-signers MUST refuse a rotation
that includes a deposit outside the bucket or omits one inside it.

**8.2 Large, addressable.** Bucket deposits at or above `dormancy_amount_msats`
whose descriptor yields a bitcoin address are spun out as exit outputs (§3), full
balance, output fee borne by the operator.

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

**8.4 Who pays.** The initiator of an exit pays its output. A depositor's
`ExitRequest` is debited its share of the rotation fee; dormancy and wind-down
outputs are paid in full by the operator. Timing a forced move into high fees
costs the operator, not the depositor.

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
