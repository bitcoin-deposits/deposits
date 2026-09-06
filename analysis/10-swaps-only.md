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
