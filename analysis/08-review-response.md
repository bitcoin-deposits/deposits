# 08 — response to the fresh-context review (2026-09-06)

Reviewer's points, graded against 01–07, with what was changed.

| Point | Status vs our analysis | Action |
|---|---|---|
| Vault is a static bond; deposits never enter it; own capital is collateral plus courier inventory once deposits fund the vault | **New.** We treated reserves as backing without noticing deposits are floated separately | Whitepaper §reserves now states it; viability left as a pricing question |
| Rogue Tier 0 spend has no proof type naming the signers | **New, real hole.** We used the fact (06) but never noticed no proof covered it | DEP-06 type 7 "unauthorised vault spend"; DEP-11 collateral maintenance now names every witness signer; DEP-19 §5 cross-references |
| Punitive never cascades, so waiting converts punitive to respectful | Known (02 §0), not fixed | DEP-06 and DEP-03: punitive shape permitted at any tier once a valid proof exists; a punitive-shaped spend without proof is type 7 |
| Composition rules checked by the constrained | Known; DEP-19 §10 says so | none |
| Wallet is load-bearing and unspecified | Known; DEP-04 checks added, scoring rule not | open; the scoring rule is a client decision the spec should at least name |
| Offline receive headline vs custodial path | Partly known (F13); abstract inconsistency missed | Abstract reworded |
| Data availability: nobody must serve history | **New** | DEP-11 History Service obligation on members |
| "Scales independently of the base layer" overstated | **New** | Abstract reworded to per-ledger footprint |
| Manufactured lateness by selective withholding | Known (F3, DEP-19 §9); operator-side defence missing | DEP-11: operator SHOULD stall rather than sign into a proof |
| FAQ trust claim vs Ark/Spark/Liquid | **New** | FAQ reworded |
| Q=3 tiers collapse to one member at E+720 | **New** | DEP-19 open question 6 |

Where the review is off:

- "Three units of capital per unit of deposit" counts the deposited coins as the
  operator's capital. They are the depositors' and they fund the vault; the operator's own lock is
  about 1.5 units at 40/60 (collateral) plus courier inventory.
  The viability point stands either way.
- "A two-of-three majority of anonymous keys chosen by the operator can spend the
  vault" is correct as mechanism, but under DEP-19 §10 the keys are not anonymous
  to a conforming wallet: vault sizes, anchors, and co-signing history are on the
  record. More trust than Ark, yes; "anonymous" overstates it.

Net: five new points, two of them spec holes now closed on paper (type 7, punitive
at any tier), one structural fact now stated (bond vs deposits). The review's
closing judgement matches 05: composition, wallet scoring, and majority liveness
are the attack surface, and the documents now say so for the first two.
