# 04 — findings

Status: **holds** / **holds under condition** / **breaks** / **gap** (spec silent).
Each entry names the goal it touches (1 stability, 2 penalty, 3 fee-driven upside).

## F1 — Hold duration under silence is set by expiry, not by inactivity  (goal 1)

**Status:** gap, with a concrete protocol fix available.

**Claim.** When an operator goes silent, depositors are frozen until `quorum_expiry`,
then a further 720 / 4032 blocks for minority and solo-member paths. Where the silence
falls within the rotation cycle decides the hold, so the bound is "remaining quorum
life plus 5 days" at best and "plus 8 weeks" at worst.

**Why it is a choice, not a constraint.** The Tier 0 majority spending path carries no
timelock (DEP-03 §Spending Tiers). A majority of members can spend the vault at any
height. The only reason they wait for `E` is that `QuorumExpired` is the sole
respectful fraud-proof type (DEP-03 §Fraud-proof classification). Nothing in the script
prevents an earlier respectful confiscation.

**Intended mechanism (per the author, 2026-09-05; not yet in the DEPs).** A per-quorum
`inactivity_blocks` parameter. If that many blocks pass with no co-signed update, a
quorum majority signs an attestation to that effect and it stands as a respectful
proof (`QuorumInactive`). The operator can always break the silence, as a wallet
(self-transfer), by `FeeCollect`, or by any other operator action, so silence is
unambiguously their choice. A majority may then run the respectful lottery
immediately via Tier 0. Minority and solo tiers remain keyed to `E` because those
are script timelocks. Absence is attested, not proven, which is why the majority
signature is the proof: it is the same majority that would have had to co-sign any
activity.

**Incentive check.** The operator keeps collateral either way (respectful path). A
majority that wanted to freeze a live operator can already do so by withholding
co-signatures (M9), and already inherits the ledger at `E`; this only shortens the
depositors' wait. The operator's defence against a false inactivity claim is the
co-signed updates themselves, which the same majority would have had to sign.

**Implementation check (deposits-rust, 2026-09-05).** Not implemented. `QuorumExpired`
is the only respectful proof type; there is no inactivity parameter or proof and no
node-side watch for a silent operator short of expiry.

**Residual.** Does not help when fewer than a majority of members are live; those
paths still wait for `E + 720` and `E + 4032`.

**Related.** Diversification across operators (DEP-11 §Fund Distribution) is the
spec's answer to unavailability, but it is advice, defends only against independent
outages, requires live couriers to execute, and costs a fixed fee per extra deposit.

## F2 — Punitive confiscation cannot be vetoed by a minority  (goal 2)

**Status:** holds under the stated assumption. Corrects `02`/`03`, which called this a
minority-plus-one veto.

The confiscation TX spends through Tier 0, which needs `floor(Q/2)+1` member
signatures (DEP-03 §Spending Tiers). Blocking it therefore takes `Q − floor(Q/2)`
refusals: 2 of 3, 3 of 5, 4 of 7. That is a strict majority in every allowed size, i.e.
the accepted majority-collusion case. Whenever an honest majority exists, the punitive
path completes.

**Residual gap.** "Honest" must include "willing to sign for free". Armers have a
slashing share; non-armers do not, yet their signatures may be needed if fewer than a
majority armed. The spec states no duty to sign a confiscation and no dereliction
proof for refusing. Under the fee-exogeneity assumption arming is cheap (ratio × D
spare capital), so an honest member should arm rather than merely sign; the gap
matters only for members who are honest but illiquid on the 144-block arming clock.

**Fix, if wanted.** Fold "arm or sign the confiscation within `dispute_arm_blocks`"
into the `DisputeDereliction` definition in DEP-11.

## F3 — Member freeze is a majority attack that leaves no evidence  (goal 1)

**Status:** holds under condition (majority honest); the condition is the accepted
one, but the cheapest majority attack is not the one the whitepaper describes.

Withholding co-signatures blocks every update once `Q − floor(Q/2)` members do it,
the same majority as theft. Unlike theft it is unprovable, costs the members nothing,
returns the operator's collateral, and hands the ledger to the withholders at `E`
through the respectful path. The whitepaper's "cannot protect against a majority that
cooperates to steal" undersells it: a majority need not steal. Freeze-and-inherit is
strictly safer for them and still a full goal-1 failure for depositors until `E`.

**Observability.** The operator can publish valid, operator-signed, un-co-signed
updates. They are not canonical but they are public evidence that proposals were made
and not signed. Wallets could price a ledger whose relay feed shows live proposals and
no co-signatures. This is reputational only.

**Making it provable.** The DEP-12 pattern extends: the operator pays a *different*
member (or any ledger) to `DeliveryEmbed` the update hash; any withholding member who
later co-signs anywhere referencing a state after the embed has provably seen it. A
`cosign_response_blocks` parameter would then make silent withholding by an active
member a `DisputeDereliction`. This does not stop a majority that goes fully silent,
but silent members lose their own ledgers at their own `E` (F8).

**Interaction with F1.** An inactivity trigger *shortens* this hold: the freezers can
take custody at `inactivity_blocks` instead of `E`, and depositors regain access sooner.
The attack is not made worse, since the freezers already get the ledger at `E`.

## F4 — Serial removal lets a majority own the quorum outright  (goal 1, precondition)

**Status:** holds under condition (majority honest); noted as a wallet signal.

`QuorumRemoveMember` is immediate and needs the current majority's co-signature. A
3-of-5 coalition removes one honest member (threshold becomes 3-of-4), then the other
(2-of-3), and now owns every signature. On-chain rotation still needs 3 of the old 5,
which they have. Each removal is a public ledger event. Nothing tells wallets to treat
quorum shrinkage as an exit trigger; it should be one, alongside a degraded rebuild
(F5).

## F5 — Degraded rebuild may seat a captured quorum  (goal 1)

**Status:** gap.

At `E + 720` the operator plus a minority of old members can `QuorumBegin`
(DEP-05 §Lifecycle). The staged set is whatever the operator added via
`QuorumAddMember`, and the first-`QuorumBegin` rule only requires a majority *of the
staged set* to co-sign. So an operator whose honest majority has gone absent can seat
an all-accomplice quorum with one cooperating old member and the accomplices' own
signatures. This only arises when the old majority is dead or absent, so the ledger
was already in trouble, but the outcome converts a hold into a theft-capable state.

**Fix.** Restrict degraded `QuorumBegin` to a subset of the previous member set, or
require the same `Q` with at least a minority of the old set carried over; and have
wallets treat any post-expiry rebuild as a withdrawal trigger.

## F6 — Single-ledger operators have no contagion exposure  (goal 2)

**Status:** holds under condition (operator runs several ledgers with independent
quorums). The condition is a SHOULD.

The punitive deterrent on an operator's *own* ledger is `C`. Cross-ledger contagion
adds `C` per other ledger whose quorum stays honest. An operator with one ledger and a
captured majority loses nothing; the only collateral at risk is the complicit members'
`min_member_collateral` on *their* ledgers, which is a parameter and which their own
quorums (possibly the same coalition) must act on. The 49% simulation result assumes
`L = 5`. Wallets should price `L` and quorum overlap, and the spec could make
`min_member_collateral` a function of the ledgers a member co-signs for.

## F7 — Escalation holds; the "further embed" fallback has no clock  (goal 1)

**Status:** holds under condition (≥1 member sells embedding). Minor gap.

Unanimous refusal to embed (M13) needs all `Q` members, which is beyond majority
collusion, so under the stated assumption a member will accept. The residual is the
DEP-06 "further" fallback: embedding on an unrelated ledger and waiting for causal
propagation. `service_response_blocks` starts at a `DeliveryEmbed`, not at an
arbitrary embed, so that path never produces a deadline breach. It is evidence of
awareness, not of censorship. Harmless but should be stated.

## F8 — Dereliction cannot be dodged by pausing one's own ledger  (goal 2)

**Status:** holds. Corrects `02` (M11 note).

The `DisputeDereliction` proof is "member's ledger has updates after
`evidence_block + DRB` and no dispute was initiated". A member who pauses during the
window and later resumes without disputing produces the proof on resumption. The only
escape is permanent silence, which forfeits the member's own ledger at its own `E`.
So pausing delays but does not evade. What remains open is *who acts*: the proof goes
to the member's own quorum, whose duty to act on it is the M26 gap (F9).

## F9 — Contagion has no stated trigger duty  (goal 2)

**Status:** gap; the whole "web of collateral" hangs on it.

Every punishment of a member, and of an operator's other ledgers, is delivered by a
quorum other than the one that observed the misbehaviour. DEP-05 says proof "can be
presented" there; DEP-11's dereliction clause covers only evidence "embedded in the
causal chain" against *their own* operator. So the receiving quorum has a reward
(slashing share) but no duty. Under fee-exogeneity the reward is probably enough for
an honest member, but "probably enough" is exactly what goal 2 should not rest on.

**Implementation check.** deposits-rust defines `NonConformingCosignature`: the
accused's key on a non-conforming update on *any* ledger, as operator or co-signer,
with the disputed ledger being one of the accused's own. That is the attribution half
of contagion and is absent from DEP-06's list; it should be back-ported. The duty half
is absent in both spec and code. (`Equivocation` is likewise code-only.)

**Fix.** State that a punitive proof against any pubkey is actionable by every quorum
that pubkey operates for, that embedding it on any such ledger starts `DRB`, and that
members there are derelict on the same terms as for local evidence.

## F10 — Lottery steering is real but only for a colluding pair or more  (goal 3)

**Status:** holds under condition (no two disputants collude). Depositor-neutral.

Exhaustive model (`models/lottery_steer.py`): a single colluder cannot improve on the
fair odds, because withholding removes them from the revealer set. Two colluders out
of five lift P(one of them wins) from 0.40 to 0.66; three of seven from 0.43 to 0.82.
Cost: one forfeited slice, of which they recover their pro-rata share as revealers.
Two or more withholds fall to the recovery cascade, which an honest majority controls.

This decides who gets the ledger, not whether depositors are paid; under goal 3 the
ledger is a fee asset, so this is a fairness issue among members, not a safety one.
Cheap fix if wanted: make the winner index depend on a hash of all preimages rather
than a sum, and require all-or-nothing reveal; or have the partial-reveal leaf select
using only the *non-withholding* set's commitments in their original positions.

## F11 — Punitive disputes freeze every depositor, not just the victim  (goal 1)

**Status:** holds; by design, but worth stating.

From `DisputeEnter`, honest members refuse to co-sign (DEP-05 §Co-Signer Obligations
#5). Every deposit on the ledger is frozen for `dispute_arm_blocks` plus confiscation
confirmation plus reveal plus claim: about two days under defaults. A fraud against one
wallet halts all of them. Combined with the ~3.5-day censorship pipeline (72 + 144
+ 144 blocks), a censored withdrawal costs its victim roughly a week and everyone
else two days.

## F12 — Tier 3 and the fate of obligations  (goal 1)

**Status:** gap; irrelevant under F1 plus any live member.

After `E + 8064` the operator may spend the vault alone. Nothing says obligations
survive that spend, and there is no quorum left to prove anything to. In practice
this means: if no member acts for eight weeks after expiry, depositors' funds belong
to the operator. Wallets should exit by `E + 4032` at the latest; with F1 adopted and
any member live, custody transfers long before.

## F13 — Legacy lightning receive is custodial  (goal 1, opt-in)

**Status:** breaks, acknowledged, avoidable.

The proof needs the payer to hand over the preimage; the payer has no relationship
with the protocol. Operators can select victims by payer type. Wallets that refuse
deterrence-only guarantee rows are unaffected. Recommend the spec label this path as
custodial rather than "deterrence", since deterrence that the victim cannot trigger
is not deterrence.

## F14 — Diversification is the only availability defence and it is advice  (goal 1)

**Status:** open; scale-dependent.

Spreading across operators (DEP-11 §Fund Distribution) defends only against
independent outages, needs a live courier and both ledgers live to execute, and costs
a fixed annual fee per extra deposit. The protocol offers no availability guarantee
beyond the hold bounds in F1/F11. Cold-start networks, where every operator sits on
every other's quorum, have correlation near one and no diversification available.

---

## Summary

| Goal | Holds | Holds under condition | Gap / breaks |
|---|---|---|---|
| 1 stability | F8, F11 | F3, F4, F7 | **F1, F5, F12, F14**, F13 (opt-in) |
| 2 penalty | F2 | F6 | **F9** |
| 3 fees | — | F10 | — |

The punishment layer holds wherever an honest majority exists (F2), and the
reputational escapes I had flagged (F3 observability, F8 pausing) are narrower than
first read. The stability layer is where the gaps are, and they share one shape:
**the spec has proofs for misbehaviour but no clock for absence.** F1 supplies the
clock for the majority path; F5 and F12 close the post-expiry edges; F9 gives the
web of collateral its trigger. F14 is not fixable in-protocol and should be stated as
the residual.

## F15 — Hold duration under silence, modelled  (goal 1)

**Status:** quantifies F1. Model in `models/hold_duration.py`.

Setup: operator goes silent at a uniformly random point in a 2016-block rotation
cycle; each of `Q` members is independently live with probability `p`; a custody
transfer takes ~170 blocks once a path opens. Tier 1 "minority" is assumed to mean
`floor(Q/2)` live members (DEP-03 does not give the count). Days = blocks / 144.

| Q | p | expiry-only mean / p95 | with 144-block inactivity trigger mean / p95 | lost (Tier 3) |
|---|---|---|---|---|
| 5 | 0.95 | 8.2 d / 14.5 d | 2.2 d / 2.2 d | 0 |
| 5 | 0.80 | 8.6 d / 14.8 d | 3.0 d / 8.2 d | 0 |
| 5 | 0.60 | 11.4 d / 33.6 d | 7.3 d / 33.6 d | 1% |
| 7 | 0.80 | 8.5 d / 14.7 d | 2.7 d / 2.2 d | 0 |
| 3 | 0.80 | 8.7 d / 15.0 d | 3.3 d / 13.1 d | 1% |

Readings:

- **Expiry-only is a coin flip on the calendar.** Mean hold is a week and a half and
  p95 two weeks with a two-week cycle, regardless of how reliable the members are,
  because the wait is dominated by time-to-expiry, not by liveness.
- **The inactivity trigger makes the hold a parameter.** With a reliable quorum the
  hold collapses to `N + pipeline`: about two days at `N = 144`. The p95 then depends
  on whether a majority is live; at `p = 0.8` a 5-member quorum still has a p95 of
  eight days because the minority tier at `E + 720` is the fallback when three of five
  are not.
- **Larger quorums buy tail protection.** At `p = 0.8`, Q=7 holds the p95 at two days
  where Q=5 does not, because a majority of seven is more likely to be live than a
  majority of five. This is a quantitative argument for the whitepaper's "wallets
  should prefer larger quorums" that the whitepaper does not make.
- **Loss (Tier 3) is negligible above `p ≈ 0.6`.** The eight-week solo path almost
  never becomes the operator's exit in a network where members are moderately live.
- **Longer cycles make expiry-only strictly worse** and do not touch the trigger path;
  so with the trigger, `E` can be pushed out to save rotation fees without extending
  depositor holds. Without it, rotation frequency is the only hold control and it is
  paid for on-chain every cycle.

**Caveats.** Liveness is modelled as static per member; correlated outages (shared
infrastructure, which the whitepaper flags as the sybil signal) would lower the
effective `p` for all members together and push results toward the `p = 0.6` rows.
The model ignores the operator's re-establishment race, which under true silence does
not occur.
