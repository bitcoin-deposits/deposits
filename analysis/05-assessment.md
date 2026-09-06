# 05 — assessment

A verdict per design goal, for the protocol as specified and with `DEP-19-draft`
applied. Conditions are the assumptions each verdict rests on. Anything not modelled
is listed at the end rather than assumed away.

## Standing assumptions

- On every ledger, a strict majority of the quorum is honest and live within the
  block windows. This is the whitepaper's own assumption and nothing below relaxes it.
- Fees, fee mix, and reserve/collateral ratios are set by the market so that
  operating or taking over a ledger is attractive.
- Wallets do what the DEPs say wallets SHOULD do: verify co-signatures, check quorum
  freshness before opening, retain evidence, refuse deterrence-only receive paths,
  and wait for the claim transaction before accepting a new custodian.

The third assumption is the weakest and is addressed under goal 1.

## Goal 1 — deposit stability

**As specified: holds for value, fails for time.**

No honest-majority scenario loses depositor funds. Every theft path reduces to a
hold followed by custody transfer, and custody transfer is cheap for the taker
(reserves are inherited one-to-one; the winner posts only the ratio). Outright loss
requires majority collusion, an opt-in custodial receive path, or eight weeks of
total member absence.

But the hold itself is unbounded by anything the depositor controls. Silence and
freezing leave no evidence and resolve at `quorum_expiry` plus tier offsets. Modelled
over a two-week cycle that is eight days on average and two weeks at p95, regardless
of how reliable members are, because the wait is calendar, not liveness. The
protocol's answer, diversification, is advice, fails under correlated outages, and
costs a fixed fee per extra deposit.

**With DEP-19: holds, with the hold a negotiated parameter.**

The inactivity trigger makes the hold `inactivity_blocks` plus about 170 blocks
whenever a majority is live: two days at the default. Larger quorums protect the tail
(seven members hold p95 at two days where five slip to eight at 80% liveness).
Freezing majorities still freeze, but now for `inactivity_blocks`, and pay with every
ledger they operate. The remaining residual is correlated member outages, which no
per-ledger rule addresses.

**Condition worth stating loudly.** Stability for a *given wallet* depends on that
wallet running verification that mobile wallets historically skip. A wallet that
trusts one relay and accepts an unconfirmed custody claim can be robbed with no
protocol failure at all. The spec should treat the wallet verification set as
normative, or ship it as a library, rather than as a SHOULD.

## Goal 2 — penalize obvious non-conformity

**As specified: holds on the operator's own ledger; hangs in the air elsewhere.**

Every listed operator fault is provable, and the punitive path cannot be blocked
short of a majority. That part is sound. What is missing is compulsion beyond the
local quorum: co-signer misbehaviour is promised to be slashable "on their own
ledger" but no DEP proof names a co-signer as accused, and no DEP obliges the
receiving quorum to act. The implementation has the attribution (`NonConformingCosignature`)
but not the duty. The "web of collateral" is therefore a description of what an
honest network *may* do, not a rule.

**With DEP-19: holds.** One consolidated proof with a free accused field, a duty to
act with the same dereliction proof as local evidence, and provable co-sign refusal
for any member who stays active anywhere. Equivocation is dropped because it
punishes an act with no victim.

## Goal 3 — upside from fees, not from slashing or acquisition

**Holds.** Winner economics are neutral by construction: inherited reserves back
inherited obligations, replacement collateral is locked not spent, and the slashing
pot is split evenly among armers so nobody is paid extra for winning. Lottery
steering by a colluding pair shifts who gets the fee asset (40% to 66% for two of
five) but not whether depositors are paid; it is a fairness issue among members with
a cheap fix if wanted. Fee compounding within negotiated limits is a market matter,
bounded per step and exitable.

## What the protocol is, in one paragraph

A proof system with a voluntary enforcement layer. It is unusually good at making
misbehaviour attributable: causal ordering through co-signatures, autonomous proofs
for on-chain credits, escalation that turns censorship into evidence, and an on-chain
lottery that lets Bitcoin adjudicate custody. It is correspondingly weak wherever the
remedy is an act someone must choose to perform, and it has no clock for absence.
DEP-19 adds the clock and converts the largest voluntary steps into duties with the
same proof shape the protocol already uses. After that, the residual risks are the
ones the whitepaper accepts: majority collusion per quorum, correlated outages, and
the fact that a depositor's availability is only as good as their spread across
operators.

## Not modelled

These would change the verdict if they came out badly. None has been checked here.

1. **Network-level coalition economics.** The 49% claim rests on the author's
   simulation with strong assumptions (single coalition, random honest quorum
   formation, perfect wallet sybil detection, `L = 5`). We have not built our own. A
   model of coalition size versus collateral at risk, with wallets that cannot detect
   sybils, is the next thing to do if the aim is to test the headline number.
2. **Correlated liveness.** The hold model treats members as independent. Shared
   hosting, shared jurisdiction, or a common software bug lowers effective liveness
   for everyone at once and pushes every result toward the pessimistic rows.
3. **Cold start.** With few operators everyone is on everyone's quorum, correlation
   is near one, and diversification does not exist. The protocol has no separate
   security story for this regime.
4. **The courier and bridge layer.** Analysed only for atomicity, which holds. Not
   analysed for liquidity: whether cross-ledger movement stays possible when several
   ledgers are in dispute at once, which is exactly when depositors want to move.
5. **Rotation and dispute costs on-chain.** Every rotation, confiscation, claim, and
   sweep is a transaction. At high fee rates small ledgers may be uneconomic to
   defend, and the replacement-collateral fee floor is policy.
6. **DEP-19 itself.** The attestation-as-proof rule, the proposal-flood question, and
   the interaction of `inactivity_blocks` with `service_response_blocks` have been
   argued, not modelled.

## Verdict (revised after 06-coalitions)

The protocol is a professional custody tier: operators are counterparties who take
quorum risk for fees, depositors are twelve words plus a wallet that verifies for
them. Fraud is provable, custody survives failure, holds are bounded (with DEP-19),
and safety against organised operators comes from quorum composition, which the
protocol prices but cannot enforce. The collateral-arithmetic claim and the 49%
figure are not supported by the mechanism and should be restated as conditional
on anchored quorums (06 §Reframed).


Under the stated assumptions the protocol achieves goals 2 and 3 as specified and
achieves goal 1 for value but not for time. With DEP-19 it achieves all three, with
holds bounded by a negotiated window and enforcement made a duty. The claims that
remain unproven are network-scale ones, and they are the same claims the whitepaper
itself supports only by simulation.

## Deployment note: agents as the user class

If depositors and operators are software agents rather than people, the verdict
shifts further in the protocol's favour on goal 1 and further against the coalition
claim.

Improves: every wallet SHOULD becomes free (multi-relay chain walking, evidence
retention, claim-confirmation waits, freshness checks); diversification and courier
rebalancing become continuous, so a hold is a liquidity event rather than lost
access; tenure and correlation become computable scores; the custodial legacy
receive path has no users; offline-first transport fits ephemeral agents.

Worsens: identity is free, so sybil seeds cost only slashable capital and anchors
plus tenure carry all the weight; failures propagate at machine speed, so the
inactivity, arm, and reveal windows may be an order of magnitude too long; fee floors
sized for human deposits mis-price many-small-transfer flows.

The case for the network is that it is the only rail an agent can use without a
human: credential is a key, terms are machine-readable, fraud is provable, custody
survives the counterparty.
