# 11 — operator economics

Model: `models/economics.py`. Per ledger, per year, deposits fund the vault
(DEP-20 accounting), swap-only obligations, rotation exit with batched outputs.
Defaults: 1 BTC capacity, 50/50 split, 70% utilisation, Q=5 at 3% each, 26
rotations a year with 20 exits each at 20 sat/vB, external inventory 15% of
deposits. Membership income assumed symmetric (you earn on others' ledgers what you
pay on yours).

## Results

| profile | ROI on own capital | depositor pays (bps/yr) |
|---|---|---|
| parked balances, 1% balance fee | 0.2% | 100 |
| parked balances, 3% | 1.2% | 300 |
| consumer: 1% + 10 bps × 20 turns | 1.7% | 300 |
| agent: 0.5% + 5 bps × 200 turns | 7.4% | 1050 |
| courier-heavy: 0.5% + spread on 100 turns | 15.4% | 150 |
| consumer at 40/60 split | 1.2% | 300 |
| consumer at 95% utilisation | 2.8% | 300 |

Balance fee alone needed for 5% ROI: 14% at 40/60, 11% at 50/50, 8% at 60/40.

Small ledgers: rotation cost is 12% of revenue at 0.5 BTC capacity, 58% at 0.1,
and exceeds revenue below about 0.05 BTC at 20 sat/vB.

## Readings

1. **Balance fees cannot carry the bond.** Every parked-balance profile returns
   under 2% on own capital at fees depositors would tolerate, and a 5% return needs
   a balance fee around 10%. The collateral is dead capital by design and the
   balance fee is the rent on it; that rent is either too small to matter or too
   large to pay.
2. **Velocity pays.** The agent profile reaches 7% from transfer fees at 5 bps, and
   the courier-heavy profile 15% from spread at 30 bps on swap volume while charging
   depositors the least per year of any profile. The operator's business is
   market-making on its own ledger; the bond is the cost of being allowed to run it.
3. **Reserves fraction is a direct tax on ROI.** Moving from 50/50 to 40/60 cuts the
   consumer return by a third for the same fees. Since the deterrent is collateral
   only (03, F6) and teeth come from member size rather than the operator's own
   split (09), the case for a high collateral share is weaker than the whitepaper's
   defaults suggest; 50/50 or 60/40 is where the economics live.
4. **Utilisation is the operator's own lever.** Unfilled capacity is vault funded
   by the operator alone. Self-fill as courier inventory (DEP-20 §5) turns idle
   capacity into working balance at zero capital cost, so a rational operator runs
   near full and the "unfilled" term disappears.
5. **Minimum viable ledger is a few tenths of a BTC** at today's fee rates, set by
   rotation cost. Rotation exit raises this slightly (34 vB per exit output) but
   batching keeps it linear in exits, not in depositors. Small operators should
   rotate less often and advertise the longer exit latency.
6. **Membership income roughly cancels member compensation** in a symmetric
   network, so the 3% figure is a wash for operators who also serve; it is a pure
   cost for operators who do not, and pure income for members who run no ledger of
   their own. Anchors with large vaults serving many quorums are paid for it.

## Depositor side

The consumer profile costs a depositor about 3% a year, comparable to a lightning
wallet's routing plus channel costs for an active user and far above a custodial
exchange. The courier-heavy profile costs 1.5% with most of it paid only when
moving. The product that clears is: cheap to hold, priced to move, with exit
guaranteed on a rotation timer and fast exit at a market spread.

## Guidance

- Set balance fees to cover rotation and member compensation, not to earn.
- Earn on transfer fees and courier spread; advertise both in the matrix.
- Run near full utilisation using self-fill inventory.
- Choose 50/50 or 60/40 unless a member's floor demands more collateral.
- Size ledgers at 0.3 BTC or above, or rotate monthly and say so.
