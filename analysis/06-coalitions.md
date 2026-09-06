# 06 — coalitions

Our own model of coalition economics, built from the DEP mechanics
(`models/coalition.py`). The aim is to test the whitepaper's headline claim, "safe
against a single coalition controlling up to 49% of the network", under our own
assumptions rather than the author's simulation's.

## Facts the model is built on

1. **Tier 0 spends the whole vault.** A majority of quorum members, without the
   operator and without a timelock, can spend reserves plus collateral to any
   address (DEP-03 §Spending Tiers). An honest operator whose quorum has a coalition
   majority loses their entire capital, not just their depositors' funds.
2. **The exposed keys are the signers, not the ledger's operator.** A theft is
   signed by the quorum majority. Each signer is slashed only on ledgers it
   *operates* whose own quorum holds an honest majority (DEP-05 §Slashing). A key
   whose own quorums are all-coalition cannot be slashed at all.
3. **Membership is unbounded and collateral is flat.** A key may serve on any number
   of quorums; `min_member_collateral` is a floor on the member's own ledger, not a
   per-membership bond.

Fact 1 means the coalition's gain includes honest operators' capital, not only
deposits. Facts 2 and 3 mean the coalition chooses which keys to expose, and can
expose very few.

## The leverage structure

Whatever acceptance rule honest parties apply, a coalition builds the cheapest
structure that passes it:

- **Seeds (A).** A small number `t` of keys with genuinely honest-majority quorums.
  These are slashable and cost their full capital `U` each when the attack lands.
- **Certified keys (B).** Keys whose quorum is `{A, c, c, h, h}`: a majority of
  members that honest parties accept (one seed plus two honest), but a coalition
  majority overall. They pass any rule of the form "majority of your quorum is
  accepted", and they cannot be slashed because honest members are two of five.
  One seed certifies unlimited B keys.
- **Fronts.** Coalition-operated ledgers whose quorums are three B keys plus two
  honest fillers. They pass the same rule, attract deposits, and can be emptied by
  their B majority at zero cost.
- **Honest quorums.** B keys also get drawn into honest operators' quorums in
  proportion to their share of the accepted pool. Where they land a majority, the
  honest operator's vault is taken outright.

DEP-19 §6's duty to act closes one hole here: if seed A refuses to slash a B it
sits on, A is derelict and loses `U`. But A is slashed once, whatever the number
of B keys it certified. The cost stays `t · U`.

## Results

Parameters: 100 operators, `Q = 5`, `L = 3`, reserves 40%, deposits fill accepted
reserves to 50%. Capital per operator `U = 1`. Coalition share `f`. "Max safe f" is
the largest share at which the coalition's best structure is unprofitable.

| Honest acceptance rule | Max safe f | Why |
|---|---|---|
| blind (accept anyone) | 0.00 | zero cost; honest vaults fall to random draws |
| fixpoint, `t = 1` seed | 0.04 | cost `1·U` vs deposits on fronts plus vaults |
| fixpoint, `t = 3` seeds | 0.10 | cost `3·U` |
| depth-1 (majority of every quorum must be anchors) | 0.14 | fronts still profit from deposits alone |
| depth-1 plus slashable per-membership collateral `c ≥ R/3` | > 0.99 | each front's three memberships cost more than its reserves |

Breakdown at `f = 0.30`, fixpoint `t = 3`: honest vaults taken 11.4 U, front
deposits 6.0 U, cost 3.0 U, profit 14.4 U. The vault term dominates: with 30% of
accepted keys in the coalition, 16% of honest operators draw a coalition-majority
quorum and lose everything.

## Reading the results

**The 49% figure measures a different threat.** The author's simulation assumes
wallets deposit only on honest operators and that reserves are self-filled, so the
coalition's only gain is honest operators' collateral through blind quorum draws,
and its only structure is all-sybil quorums that expose every key. Under those
assumptions each coalition ledger with an honest-majority quorum costs its
collateral and the arithmetic in DEP-05 §Security Model follows. The model here
lets the coalition (a) attract deposits, (b) choose which keys to expose, and (c)
certify unslashable keys through a few slashable ones. Any one of these collapses
the bound to single digits.

**Decentralised certification chains, and chaining is the problem.** Every rule of
the form "your quorum majority must be accepted" is satisfied by one accepted key
plus honest fillers, and the key so certified is not slashable. The only rules that
do not chain require a majority of *anchors* on every quorum, which makes the
anchors the network. The whitepaper's "wallets cannot prove independence; they can
only price it" is exactly right, and the pricing signal it names, correlation, is
the one thing this model does not give the coalition for free (see below).

**Per-membership collateral is the lever, if it is slashable.** With a bond `c` per
quorum served, a front's three memberships cost `3c` against at most `R` of
deposits. At `c ≥ R/3` fronts are unprofitable at any coalition size, and honest
vault theft needs three bonded keys per stolen vault. The FAQ's "members run a
ledger at least half the size" is this intuition. But the bond only bites if it can
be taken by honest hands, and under chained certification a B key's bond sits on a
ledger the coalition controls. So the bond and the certification rule have to be
designed together: bond posted somewhere an honest majority controls, or
certification by depth-1 anchors for bonded keys only.

**What the coalition cannot fake is time and independence.** Fronts must operate
honestly long enough to attract deposits; B keys must behave as members long enough
to be drawn into honest quorums. Correlation in the public record, members that
sign, stall, and rotate in lockstep, is the whitepaper's own suggested signal and is
not modelled here. It is the residual defence, and it is a heuristic.

## Conclusions

1. Under blind or chained acceptance the protocol is not safe against small
   coalitions; the bound is roughly `t · U` of seed capital against the deposit and
   vault mass the coalition can reach, which is single-digit percent for the
   parameters above.
2. The "49%" claim holds only under the author's simulation assumptions, which
   exclude the strategies that matter.
3. The strongest structural fix is per-membership slashable collateral combined with
   a certification rule that does not chain. Neither is in the DEPs. Both centralise
   toward whoever the anchors are.
4. The honest-operator exposure (fact 1) is independent of wallets entirely. An
   operator's capital is only as safe as their member choice, and the spec gives
   them no better tool than wallets have.

## Reframed: quorum composition is the security parameter

The results above measure the mechanism without judgment. The intended deployment
is a professional operator tier where quorum composition is a business decision,
and the protocol's job is to make that decision legible (proofs, tenure,
correlation, succession) rather than to make it safe. Under that framing the
useful statement is: a coalition must fill every seat the operator did not anchor.

| Q | trusted anchors | seats coalition must fill | random-fill odds at 30% coalition share |
|---|---|---|---|
| 5 | 2 | all 3 remaining | 2.7% |
| 5 | 1 | 3 of 4 | 8.4% |
| 7 | 3 | all 4 remaining | 0.8% |

With two honest anchors of five, one honest pick among the other three blocks any
theft. This is cheap and strong, and it is advice, exactly as diversification is for
depositors. The whitepaper's collateral-arithmetic claim and the 49% figure should
be replaced by this conditional statement.

## Caveats

Analytic expectations, not Monte Carlo; uniform deposit spreading; every coalition
key operates `L` fronts; honest operators draw members uniformly from the accepted
pool; no tenure, no correlation signal, no fee income foregone by the coalition
while building the structure. Adding tenure and correlation would raise the safe
share; how much depends on heuristics the spec does not define.

## Membership bond: evaluated and rejected as sized

The bond is the right shape and the wrong size.

**Sizing.** Against fronts, three memberships must cover a front's reserves:
`c ≥ R/3`. Against honest-vault theft (fact 1), they must cover reserves plus
collateral: `c ≥ U/(3L)`, about 2.5× larger at a 40/60 split. No script change
removes the vault exposure: without covenants, whichever key set can spend the vault
can spend it anywhere, and gating that set behind the operator's signature would
also gate confiscation.

**Capital.** Memberships are supplied at `Q` per ledger, so an average operator
serves on `Q·L` quorums. With `Q = 5`, `L = 3`:

| Bond | per membership | per operator (15) | total capital vs today's 1 U |
|---|---|---|---|
| front-sized `R/3` | 0.044 U | 0.67 U | 1.7 U |
| vault-sized `U/3L` | 0.111 U | 1.67 U | 2.7 U |

**Yield.** A member earns `compensation_bps` (default 3%) of a ledger's fees per
membership: about `0.004·y·U` on a full ledger at fee rate `y`. That is ~9% of `y`
on the front-sized bond and under 4% of `y` on the vault-sized one, against up to
`0.4·y` for operating the same capital. Making bonds worth posting needs member
compensation of roughly 15–30% of fees per member, which across five members
exceeds the fee stream.

**Conclusion.** Not fundable at any compensation depositors would pay. The
sections sketched below are kept for the record, not proposed for DEP-19. The
coalition defence stays where the whitepaper put it: tenure, observable correlation,
directly trusted anchors, genuinely disjoint quorums across an operator's ledgers,
and acceptance that small, patiently built coalitions are profitable.

## Sketched additions (not proposed)

- **§11 Membership bond.** A member posts `membership_bond ≥ R/⌈Q/2⌉` per quorum
  served, into an output controlled by that ledger's *honest-recoverable* path
  (to be designed; a 2-of-{operator, anchor-set} or the served ledger's next
  quorum). Slashed on any `NonConforming` proof naming the member.
- **§12 Certification.** Wallets and operators SHOULD accept a key as a member only
  if a majority of its quorum are anchors the acceptor trusts directly, or bonded
  keys whose bond is controlled outside the key's own quorum. Chained acceptance
  MUST NOT count toward the majority.
