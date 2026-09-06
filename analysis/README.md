# analysis

Independent game-theoretic analysis of the bitcoin deposits protocol, worked from the
DEPs and whitepaper only. The implementation (deposits-rust) is deliberately out of scope:
it can be more broken than the spec but not more correct.

Design goals, in priority order (stated by the reviewer, 2026-09-05; the whitepaper
implies but does not rank them):

1. **Deposit stability** — funds remain available and honoured.
2. **Penalize obvious non-conformity** — provable misbehaviour is punished.
3. **Upside comes from fees** — operating, co-signing, and taking custody should pay
   through fee streams, not through slashing windfalls or acquisitions.

Whether the design achieves these is unproven. Every finding should say which goal it
touches. A hold is a goal-1 failure even when nobody misbehaved provably; an
unprovable action is only a problem if it threatens goal 1; custody transfer that is
not worth taking on fees alone is a goal-1 failure dressed as a goal-3 detail.

Working assumption: fee levels, the per-action / per-annum fee mix, and
reserve/collateral ratios are tunable and the market will set them so that operating
or taking over a ledger is attractive. Takeover is cheap by construction: the old
operator's confiscated reserves back 100% of obligations, the winner locks only the
collateral ratio (roughly 20–50% of obligations) as additional capital, and
per-action fees are earned even on a post-takeover exodus. Takeover economics is
therefore not treated as a structural concern. The structural questions are hold
duration under silence or member withholding, and whether the punitive path can be
blocked short of majority collusion (it cannot; see F2).

Method:

1. `01-actors.md` — the actors, what each holds at stake, and every point at which
   the protocol leaves them discretion (an action they may or may not take, or a
   parameter they choose). Discretion is where strategy lives.
2. `02-responses.md` (next) — for each discretionary action, who can observe it,
   what they can do in response, and on what clock.
3. `03-games.md` — mechanism-level games assembled from 1 and 2 (lottery reveal,
   dispute participation, expiry race, escalation bounty, cross-ledger contagion,
   coalition exit).
4. `04-findings.md` — claims with status: holds / holds under condition / breaks.

Conventions: cite the DEP section a claim comes from. Mark anything the spec leaves
unstated as **[unstated]** rather than filling it in silently; those gaps are findings.
