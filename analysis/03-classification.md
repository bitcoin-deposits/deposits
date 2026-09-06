# 03 — classification: holds vs theft, scale-solved vs open

Every risk surfaced in `02-responses.md`, placed on two axes. Read against the goals
in `README.md`: HOLD rows are goal-1 failures and are the primary concern; OPEN rows
that are unprovable matter only where they cause a HOLD.

**Outcome** (what a depositor actually suffers):

- **HOLD** — funds unavailable for a bounded or unbounded period, then recovered in full
  (less negotiated fees). Cost is time value and liquidity.
- **DRAIN** — funds lost gradually through conforming fees or per-attempt griefing
  charges. Bounded per event, unbounded in aggregate unless the depositor leaves.
- **THEFT** — funds lost outright.

**Resolution** (what makes it go away):

- **MECH** — closed by the protocol's own mechanism under its stated assumption
  (honest, live majority on every quorum).
- **SCALE** — not closed by mechanism, but converges to acceptable as the network
  grows: many independent operators, many candidates for custody, many relays, many
  bridges. Mark what "sufficiently large" has to mean.
- **OPEN** — neither. Either unprovable, or provable with nobody paid to act, or an
  unstated rule.

The whitepaper's own scope exclusions (no unilateral exit, no privacy, availability =
operator availability, majority collusion) are included and labelled as accepted.

---

## 1. The matrix

| ID | Risk | Actor(s) | Outcome | Resolution | Notes |
|---|---|---|---|---|---|
| O13 | Uncredited on-chain payment | operator | THEFT→HOLD | MECH | Autonomous proof. Becomes a HOLD (deposit honoured by new custodian) if a member disputes and the confiscation gets M20 signatures. Otherwise THEFT. |
| O14 | Uncredited legacy LN payment | operator + payer | THEFT | OPEN | Payer link. Bounded per wallet by W16. Operators can select victims. Wallet can avoid by refusing deterrence-only operators (W6); then it's a HOLD of the *feature* (no offline receive), not of funds. |
| O15 | Selective censorship, operator keeps signing | operator | HOLD (~3–4 days min) | MECH via bounty | Closed only if a member sells embedding (M13) and the recovery majority signs (M20). |
| O15' | Censorship by total silence | operator | HOLD to E, then custody by whoever wants it | SCALE | Operator keeps collateral. Depositor recovers when someone takes respectful custody. Needs: some member willing to post replacement collateral for a ledger with possibly self-filled obligations. |
| O16 | Lock left open past timeout | operator + majority | HOLD | MECH | Needs complicit majority to exist at all; then same as O24. |
| O17 | Request reordering / delay | operator | DRAIN (bridges, couriers) | OPEN | Not provable. Harm capped at one HTLC per event. Bridges price it or leave. SCALE helps the *wallet* (choose another bridge) but not the bridge. |
| O19 | Fee ratcheting within limits | operator | DRAIN | OPEN by design | Bounded per step by `fee_change_limit_bps`, unbounded cumulatively. Depositor's exit is a withdrawal, subject to O15. Note: negotiated at open; a wallet can set limit 0. |
| O20 | Serial member removal to compact the quorum | operator + majority | precondition for THEFT | OPEN | Conforming. Each step needs a majority of the *current* set. Visible on-ledger: wallets could treat quorum shrinkage as a withdrawal trigger, but nothing says so. |
| O21/O29 | Non-rotation, disappearance | operator | HOLD to E (+ tiers) | SCALE | Same as O15'. Worst case E+8064 then Tier 3. |
| O22 | Degraded rebuild with new members | operator | precondition for THEFT | OPEN (unstated) | If a Tier-2 `QuorumBegin` may seat new members, an operator converts an honest quorum into a captured one by waiting. Wallets see the new `QuorumBegin`; nothing says to leave. |
| O23 | Tier 3 solo spend | operator | THEFT if nobody took custody in 8 weeks; else moot | SCALE | In a large network somebody takes respectful custody by E+4032. In a small one, the operator waits 8 weeks and keeps everything. **Accepted by design?** Not stated. |
| O24 | Non-conforming update with complicit majority | operator + majority | THEFT | accepted (WP) | Cross-ledger slashing of members is the only lever; see M26. |
| O27 | Self-fill | operator | none | not an issue | Punitive loss is `C` only, which the design already assumes (PROPOSAL.md). Arming floor is bounded by `r × reserves`, known at join. Only action: whitepaper should not describe excess reserves as part of the deterrent; wallets should not read obligation totals as adoption. |
| M9 | Co-sign withholding by ≥½ members | members | HOLD to E, then custody to withholders | OPEN | Leaves no evidence. Operator's counter is O20 removal, which needs the same majority. Depositors frozen ~E. Collateral returned to operator. Reward to freezers: the ledger. |
| M10 | Member co-signs invalid update | member | enables O24 | OPEN via M26 | Provable; punishment depends on the member's own quorum acting on foreign evidence. |
| M11 | Member pauses own ledger to avoid "active" status | member | disables M14 | OPEN | Not backdating; just not advancing. Makes dereliction unprovable. |
| M13 | All members refuse to sell embedding | members | HOLD, unprovable | OPEN | DEP-12 says "signal to leave" but leaving *is* the censored request. |
| M14 | Dereliction | member | delays HOLD→custody | OPEN via M26 | Provable only if member stays active elsewhere (M11). |
| M17+M20 | Arm/sign refusal (confiscation veto) | strict majority of members | converts THEFT-punishment into HOLD-to-E; operator keeps collateral | accepted (majority) | Needs `Q − floor(Q/2)` refusals = majority in every allowed size (F2). Residual gap: no stated duty for non-armers to sign. |
| M19/M21 | Strategic non-reveal | k colluding disputants | who gets custody; slice forfeiture recycled | partially MECH | Does not by itself cause depositor loss; custody goes to a coalition member, who then must post collateral and can be slashed later. Becomes THEFT only combined with O24 on the new ledger. |
| M22 | Winner deviates on claim | winner | HOLD/THEFT of the ledger's backing | OPEN | Slashable "on the ledger they operate after" — a quorum they choose. In a large network wallets can refuse a winner with a fresh, unknown quorum. |
| M25 | Deviating sweep | recovery quorum | THEFT of forfeited slices (members' money, not depositors') | OPEN, acknowledged | Depositor-neutral. |
| M27 | Member walks | member | reduces effective Q; enables lower tiers | SCALE | Operator recruits replacements; needs candidates. |
| W9/W14 | Wallet skips verification / accepts unconfirmed `DisputeAcquire` | wallet | THEFT (self-inflicted) | OPEN (client quality) | Not protocol; noted because the whole design assumes wallets do expensive checks. |
| W13 | Payer never shares preimage | payer | see O14 | OPEN | — |
| B2/C4 | Bridge/courier abandons after wallet locks | bridge/courier | DRAIN (one fixed fee per attempt) | SCALE | Wallet picks another. The *operator* collects the failure fee, so an operator running a griefing bridge is paid to grief. |
| R1/R2 | Relay drops events/requests | relay (+operator) | HOLD until escalated; cost of escalation | SCALE | Multi-relay reads; wallet pays to escalate. |
| R3 | Stale replaceables | relay | THEFT (key revocation rollback) | OPEN (client) | Client must compare created_at. |
| — | Majority collusion on a quorum | coalition | THEFT | accepted (WP) | Bounded by collateral C on that ledger and by contagion to the coalition's other ledgers (M26). |
| — | Coalition ≤49% of network | coalition | THEFT of self-filled? no; of honest deposits placed on coalition ledgers | SCALE, conditional | Simulation assumes wallets never deposit on sybil ledgers. Without that, the bound is meaningless. |
| — | No unilateral exit | all | HOLD if the network dies | accepted (WP) | — |

---

## 2. Reading the matrix

### 2.1 What is actually theft

Under the stated assumption (honest live majority per quorum, and members willing to
sign confiscations), outright theft of depositor funds reduces to:

1. **Legacy-mode lightning receive** (O14). Genuinely open. Avoidable per-wallet by
   never using deterrence rows. Should be classified as *an optional product with known
   counterparty risk*, not as part of the protocol's security claim.
2. **Majority collusion on a single quorum** (O24 with complicit majority). Accepted.
   The protocol's answer is contagion, which routes through M26.
3. **Tier 3 solo spend** (O23) when no one takes custody for eight weeks. This is theft
   by patience. It requires the network to be small or the ledger to be unattractive
   (self-filled, tiny, or with fee floors nobody wants). Nothing in the spec says the
   operator's obligations survive Tier 3.
4. **Client-side failures** (W9, W14, R3). Outside the protocol but the design leans on
   wallets doing more than mobile wallets historically do.

Everything else that looks like theft in `02` is, on inspection, a **HOLD that becomes
custody transfer**, *provided* someone is willing to take the ledger. That "provided"
is the pivot of the whole classification.

### 2.2 What is a hold

The dominant risk class. Sources: silence (O15', O21, O29), member freeze (M9),
confiscation veto (M17+M20), unanimous embed refusal (M13), relay loss (R1/R2).

Duration bounds:

| Path | Earliest release | Latest release |
|---|---|---|
| Selective censorship, cooperative member | embed + SRB + DRB + DAB + confs ≈ 360 blocks + on-chain | same |
| Silence / freeze | E (majority respectful) | E+4032 (single member), then E+8064 operator solo |
| Confiscation veto by ≥½ | E (respectful, if the vetoers now want the ledger) | as above |

So a depositor's worst-case hold is **the remaining life of the quorum plus four to
eight weeks**, in every non-theft scenario. Since `E` is negotiated (FAQ suggests
two-week rotations), the practical worst case is roughly 6–10 weeks. The whitepaper's
"liveness is part of the security model" should be read as: *you may lose access for
two months without anyone having done anything provable.*

What a HOLD costs the operator: nothing, if achieved by silence. What it costs freezing
members: nothing, and they get first claim on custody.

### 2.3 What scale solves

Scale converts HOLDs into shorter HOLDs by ensuring a taker exists, and converts
some OPEN griefing into market choice. Specifically:

- **A custodian will exist** for an abandoned ledger (O15', O21, O23) — requires
  enough operators with spare collateral ≥ obligations × ratio who judge the ledger's
  fee stream worth it. This fails for self-filled or fee-floored ledgers regardless of
  size. So "sufficiently large" means: *many operators with idle collateral and a
  liquid market for ledgers as assets*. That market does not exist in the spec; the
  respectful path is the only acquisition mechanism and it has a minimum 5-day wait
  past E for a minority.
- **Quorum independence** (O10, M7, coalition bound) — a large operator population lets
  wallets pick non-overlapping quorums and lets operators seat strangers. Requires
  wallets to actually compute correlation. "Sufficiently large" = enough distinct
  operators that a coalition cannot be a majority of many quorums *and* wallets can
  observe tenure. Cold-start is the opposite regime: few operators, everyone on
  everyone's quorum, correlation ≈ 1.
- **Bridge/courier/relay griefing** (O17, B2, C4, R1, R2) — market choice. Small per-
  event cost. Scale is sufficient here.
- **Member replacement** (M27) — needs candidates.

Scale does **not** touch anything internal to one quorum once formed: freeze (M9),
veto (M20), serial removal (O20), degraded rebuild (O22). Those are
per-ledger games played by ≤8 parties and their equilibrium is independent of how many
other ledgers exist — except via *reputation*, which the protocol makes observable but
does not price.

### 2.4 What is open

Grouped by what would close them.

**Unstated obligations** (a spec sentence could close them, but the enforcement would
still route through another quorum):

- M20 confiscation-signing duty for non-armers (only matters below a majority of armers, F2)
- M17 arming as part of "acting" on a dispute
- M26 duty of a quorum to act on foreign evidence against its own operator
- O22 whether degraded `QuorumBegin` may seat new members
- O23 whether obligations survive Tier 3
- W15 whether wallets should exit on expiry / shrinkage / degraded rebuild

**Unprovable by construction** (needs a mechanism, not a sentence):

- M9 co-sign withholding
- M11 own-ledger pausing to dodge "active"
- M13 unanimous embed refusal
- O17 ordering

**Economic, not logical** (closable by parameters, if the numbers work):

- M19/M21 non-reveal steering: forfeiture slice vs value of custody
- Takeover economics: replacement collateral (locked, not lost) vs `(C + R − D)/Q`
  share vs a ledger's fee stream; self-fill drives the share toward `C/Q` and the
  arming floor toward its maximum
- Escalation bounty: member's embed price vs P(dispute succeeds) × share

**Accepted by the whitepaper**: majority collusion, no unilateral exit, availability.

---

## 3. Summary counts

| | MECH | SCALE | OPEN | accepted |
|---|---|---|---|---|
| HOLD | 3 | 6 | 5 | 1 |
| DRAIN | 0 | 2 | 2 | 0 |
| THEFT | 0* | 2 | 6 | 2 |

*O13 is MECH only because it converts to HOLD; no theft path is closed *as theft*
without a custody transfer that someone must volunteer for.

The shape of the result: **the protocol reliably converts theft into holds, and relies
on scale to convert holds into short holds.** The mechanism layer is strong on
*proof* and weak on *compulsion*: it can show that something went wrong, but every step
from proof to remedy is a voluntary act by a party whose only obligation is
reputational or lands on yet another quorum. The next document should put numbers on
the voluntary steps (G2, G5, G9) to see whether "voluntary" is fine in practice.
