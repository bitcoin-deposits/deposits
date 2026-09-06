# 09 — guidance for nodes and wallets, with the numbers behind it

Derived from `models/teeth.py` (member-selection rules, feasibility, and a rational
coalition that reuses keys across thefts) and `models/coalition.py` (adversarial
structures). Network: 200 operators, Pareto-distributed vaults (a few large, many
small), each running `L` ledgers, quorums formed honestly under each rule. Reach is
assumed (every member's own quorum contains an honest anchor); the numbers measure
bite.

## Results

**Net coalition profit as a share of network capacity.** Coalition is a random
fraction `f` of operators; it robs the ledgers where it holds a majority, choosing
the set that maximises stolen vaults minus exposed keys, sharing keys across thefts.

| Q | rule | f=0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|
| 5 | none | 0.001 | 0.007 | 0.016 | 0.065 |
| 5 | member vault ≥ ½ ledger vault | 0 | 0 | 0.004 | 0.017 |
| 5 | member vault ≥ 1× ledger vault | 0 | 0 | 0 | 0.005 |
| 7 | ≥ ½ | 0 | 0 | 0 | 0.010 |
| 3 | ≥ ½ | 0 | 0 | 0.002 | 0.012 |

**Feasibility** (share of capacity whose quorums cannot be filled under the rule):
½ rule ~10%, 1× rule ~17%, at Q=5, L=3. Any hard cap on quorums served per key is
infeasible by counting: a network needs `Q·L` memberships per operator, so caps
below that leave most ledgers unfilled (70–90%).

**Ledgers per operator.** Smaller ledgers are easier to staff (unfilled 21% at
L=1, 6% at L=5) but slightly more profitable to rob in bulk at f=0.5 (1.1% → 3.0%),
because each theft is small relative to the keys it exposes only once.

**Dilution.** A key serving `m` quorums brings each roughly `1/m` of its vault as
bite in a mass theft. With unlimited memberships the worst-case diluted bite
defends almost no capacity; the actual coalition result above sits between the
single-theft and fully-diluted bounds because a coalition can only reuse a key on
quorums where it also holds the other majority seats.

**Adversarial structures** (`coalition.py`): with declared anchors on every
non-anchor member's quorum and the ½ rule, a front's three signing memberships
stake at least 1.5× what the front can take; with two honest anchors of five a
coalition must fill all three other seats.

## Guidance for nodes

1. **Members at least half your ledger's vault; prefer equal.** The ½ rule makes a
   random coalition of 30% unprofitable at every quorum size and costs about 10% of
   ledgers a full quorum. The 1× rule extends that to 40–50% at ~17% unfilled. Sized
   against the *ledger*, not your total vault, so splitting into more ledgers makes
   the rule easier to satisfy.
2. **Treat heavy membership as a signal, not a divisor.** Dividing a member's
   vault by the quorums it serves is the worst-case bite and it fails almost every
   real ledger: with unlimited memberships a key serves about `Q·L` quorums, and a
   test that divides by that passes 1% of capacity. The coalition result in the
   table is achieved with the plain ½ rule because a coalition can only reuse a key
   where it also holds the other majority seats. Apply rule 1 unweighted; prefer
   members serving fewer quorums when you have the choice.
3. **Two anchors of five, three of seven; anchors on your other members' quorums.**
   Reach is what turns bite into loss. Without it the tables above do not apply.
4. **Five or seven members, not three.** Q=3 has the highest profit at every f and
   collapses to a single member at Tier 1 and Tier 2.
5. **Three ledgers, disjoint quorums.** Balances staffing against bulk-theft
   exposure and gives contagion something to bite.
6. **Liveness as a selection criterion.** Independent hosting and observed uptime
   from members' own ledgers; the hold model (F15) says the tail is set by whether a
   majority is live, not by the rule above.

## Guidance for wallets

1. **Compute the cheapest signing majority.** For a ledger with vault `V` and
   members `j`, take the `⌊Q/2⌋+1` members with the smallest `vault_j`; require
   their sum ≥ `V`. Refuse ledgers that fail. This passes ~90% of capacity in the
   simulated network and is the test the coalition results reward. Do not divide by
   quorums served: that passes 1%. Use memberships only to break ties.
2. **Require declared anchors and check them.** At least two of five members flagged
   as anchors, each with a long co-signing history, and each non-anchor's own quorum
   containing one of them.
3. **Spread across ledgers whose quorums do not share members**, three or more.
   The protocol bounds a hold per ledger only; availability across ledgers is the
   wallet's job.
4. **Exit triggers.** Quorum shrinkage, post-expiry rebuild, inactivity or expiry
   dispute, custody change to an unevaluated quorum, or a member's
   `vault / quorums_served` dropping below the threshold in 1.
5. **Prefer operators with three ledgers over one.** A single-ledger operator has
   no contagion exposure and a larger vault per quorum to staff.

## Capital efficiency

The rules add no capital. Own capital per unit of deposit capacity is set by the
reserves fraction alone: 2.5× at 40/60, 2.0× at 50/50, 1.67× at 60/40, and the
operator additionally custodies the deposits themselves. What the rules change is
*who may serve where*: the ½ rule leaves ~10% of ledgers unstaffable and the 1×
rule ~17%, which those operators resolve by running smaller ledgers or recruiting
larger members. The only rule that would squeeze capital is membership weighting,
which is why it is not recommended:

| wallet test | capacity passing |
|---|---|
| cheapest majority Σ vault ≥ V | 90% |
| same, vault ÷ (served/8) | 70% |
| same, vault ÷ (served/3) | 36% |
| same, vault ÷ served | 1% |

A network that wanted full-dilution teeth would need members holding `Q·L/2`
ledger-vaults each, which is the membership-bond capital problem (06) and is not
fundable from fees.

## What these numbers do not cover

Passive coalitions only in the profit table; the adversarial-structure model shows
anchors are what close the active case. Vault inequality matters: flatter networks
defend better (diluted defended share rises from 12% to 30% as inequality falls).
Reach is assumed throughout; every rule here is conditional on an honest anchor
being present where the rule says one must be.
