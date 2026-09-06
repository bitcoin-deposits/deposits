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

**Cutoff.** Each `QuorumBegin` carries `exit_cutoff_height`. Every `ExitRequest`
appended at or before that height, and every escalated request causally visible to
the operator at or before it (DEP-19 §8), MUST be settled in that rotation.

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

### 8. Dormancy exit

A deposit with no signed activity for `dormancy_blocks` (per-quorum, recorded in
`QuorumAddMember`; suggested 26280, ~6 months) whose descriptor yields a bitcoin
address (single-key descriptors do; see DEP-16 for which others) MAY be spun out by
the operator: the operator appends a `DormancyNotice` naming the deposit and a
rotation height at least `dormancy_notice_blocks` ahead (suggested 2016), and at
that rotation includes an exit output for the balance less fees, as in §3. Any
signed activity on the deposit before the rotation cancels the notice. Co-signers
verify dormancy and notice from the ledger.

**Dust floor.** Deposits below `dust_multiple × 34 vB × current feerate` are not
spun out; the fixed fee drains them and the operator closes them at zero. The
floor is set by the fee market, not by the spec. Suggested `dust_multiple` 10.

**Who pays.** The initiator of an exit pays its output fee. A depositor's
`ExitRequest` is debited its output's share of the rotation fee; a dormancy exit or
wind-down output is paid in full and its fee is borne by the operator. Timing a
forced exit into high fees therefore costs the operator, not the depositor.

### 9. Wind-down

An operator MAY close a ledger by appending `LedgerWindDown` with a final rotation
height at least `winddown_notice_blocks` ahead (suggested 4032). During the notice
period the operator MUST continue to process requests. At the final rotation every
deposit above the dust floor with an addressable descriptor is spun out under §8
rules regardless of dormancy; remaining obligations are zero; the rotation's "new
vault" output is to the operator alone, and the ledger is tombstoned. Deposits with
no addressable descriptor SHOULD move by swap or transfer during the notice period.
Any that remain are NOT forfeited: the final rotation retains a vault sized to
their obligations at the collateral ratio, and that vault passes to the quorum
under the respectful custody path (DEP-06); one member takes the remainder by
lottery and inherits those deposits. Wind-down removes the operator, never a
balance.

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
the acquisition rotation is a rotation. Dormancy exit and wind-down give an
operator a clean way to shed obligations it cannot carry, and release members
from ledgers that no longer pay them; the dust floor follows the fee market so
nothing is lost to fees that would not have been drained anyway.

## Related DEPs

DEP-03 (rotation transaction), DEP-04 (guarantee matrix), DEP-09/13/16 (swap
locks), DEP-10 (withdrawal, superseded in part), DEP-11 (obligations), DEP-12
(escalation), DEP-19 (causal visibility, inactivity, `NonConforming`).

## Open questions

4. Whether wind-down should require member co-signature beyond the rotation
   itself. With the operator paying forced-exit fees, no forfeiture, and a long
   notice, the operator's only unilateral power is to end its own service on a
   long clock at its own cost, which is judged sufficient; recorded for review.

1. Minimum rotation interval. A very short interval makes exit fast but multiplies
   on-chain cost and co-signing load; a quorum-negotiated `max_rotation_interval`
   may belong in `QuorumAddMember`.
2. Whether `ExitRequest` should carry an expiry so that a depositor who finds a swap
   in the meantime can release the lock.
3. Fee attribution for exit outputs: pro-rata from the exiting deposits, or borne
   by the operator as a cost of the rotation.
