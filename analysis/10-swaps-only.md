# 10 — swaps-only obligations

Proposal (author, 2026-09-06): the operator guarantees only atomic swaps and
ledger-internal operations. On-chain withdrawal ceases to be an operator duty; exit
is a hash-locked swap against any deposit holder with external liquidity, the
operator's own courier first among them.

## Consequences

- **Obligations are ledger-internal.** Locks, completions, credits, fee terms.
  Withdrawal censorship as a proof class collapses into transfer censorship
  (DEP-12 unchanged). DEP-10 §Withdrawal and the `OnchainLock/Fulfill/Fail` duty
  in DEP-11 become a service, advertised in the guarantee matrix, not owed.
- **Self-fill is courier inventory.** The on-ledger leg costs capacity only; the
  external leg (lightning channels, on-chain coins) is own capital and earns spread.
- **Obligations do not shrink on exit.** A depositor's balance moves to the
  operator's deposit. The vault's usage is unchanged; no rotation is needed to
  release reserves. Reserves are sized once, to capacity.
- **Capital.** `own = vault − customer deposits + external inventory + arming
  reserve + fees`. Inventory replaces the withdrawal buffer and is productive.
  Deposits fund the vault at inflow; inventory pays at outflow; inbound swaps
  replenish.

## What the protocol then guarantees

A funded swap completes or refunds atomically, and a refusal to process the lock is
provable censorship. It does not guarantee that a counterparty exists. Exit is a
market. For a network with many couriers this matches lightning today; for a
single-operator ledger whose courier stalls it is a hold with no proof, resolved by
another liquidity provider or by the inactivity path if the operator is silent.

The depositor's floor is a transfer to another deposit on the same ledger, which
any holder with external liquidity can turn into an exit. The spec should say that
on-chain exit is a service, not a right, and the guarantee matrix should carry the
operator's advertised swap capacity so wallets can price it.

## Spec changes implied

- DEP-10: move withdrawal to a swap regime (`onchain_swap`), remove the operator
  duty; keep `onchain_credit` for funding.
- DEP-11: drop "Withdrawal" from the processing obligation; keep transfers.
- DEP-04 guarantee matrix: `onchain_swap` and `invoice_pay` rows advertise capacity
  and honesty `bridge_only`; wallets treat absence as no exit path.
- WHITEPAPER §deposits: "an operator must allow transfers between deposits on the
  same ledger as well as on-chain exits" becomes "…and must process swap locks; exit
  liquidity is provided by couriers, including the operator's own".

## Cold start improves

A new operator self-fills, then swaps a slice of its own balance for market-priced
balance on an established ledger through a courier. It now holds inventory on both,
which is a channel between the ledgers with no on-chain step. The courier graph
grows by trade rather than by capital.

## Exit floor: rotation exit

Fast exit is a swap. Slow exit is paid from the vault, which already holds
reserves at least equal to obligations and is spendable by the quorum.

- A depositor signs an **exit request** (amount, on-chain address). It is delivered
  to the operator or, on refusal, embedded via DEP-12 so it becomes causally visible.
- The operator MUST include every exit request visible before a published cutoff in
  the next `QuorumBegin` rotation transaction: one output per request (batched, dust
  aggregated), the new vault reduced by the total, and the ledger update recording
  the rotation debiting the deposits by the same amounts. Reserves and obligations
  fall together, so the reserves-fraction invariant holds.
- Co-signers verify the rotation's outputs against the visible requests and MUST
  refuse a rotation that omits one. An operator who rotates without them, or lets
  the cycle pass, is censoring under the `service_response_blocks` clock; custody
  transfer puts the requests before a new operator, who includes them in the
  acquisition rotation.
- The operator MAY run an off-cycle exit batch (a co-signed rotation to the same
  member set) when requests warrant.

Shape: cooperative close now, force close on a timer, as in lightning. The timer is
the rotation cycle plus, if resisted, the escalation and dispute windows. Liquidity
is never the operator's problem; deposit-funded vault capital leaves with the
deposits that funded it. A run appears as a large rotation, not a liquidity crisis.
Depositors who need coins in hours use the swap market.

## Spec changes implied (additional)

- DEP-03 `QuorumBegin`: optional `exit_outputs` list; UTXO value check becomes
  `old vault − exits − fee`.
- DEP-02: `ExitRequest` operation (or a `DeliveryEmbed` target) and the debit
  recorded in the rotation update.
- DEP-11: "Exit inclusion" obligation, provable as censorship.
