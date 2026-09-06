# 02 — observation and response

For each discretionary action from `01-actors.md`: who can see it, what evidence it
leaves, who can respond, what the response costs, and the block clock it runs on.
The point is to find where an action is (a) invisible, (b) visible but not attributable,
(c) attributable but nobody is paid to respond, or (d) fully closed.

Closure grades used below:

- **closed** — provable, someone with standing has a positive incentive to act, and the
  action is on a bounded clock
- **paid-but-optional** — provable, a reward exists, but acting is a choice and
  non-action is not punished
- **unpaid** — provable, but the responder gains nothing in-protocol
- **open** — not provable, or no responder exists

## 0. The clocks

All from DEP-11 defaults and DEP-03/06 script constants. Everything below refers to these.

| Symbol | Meaning | Default |
|---|---|---|
| `SRB` | service_response_blocks: embed → censorship provable | 72 |
| `DRB` | dispute_response_blocks: evidence embedded → member must dispute | 144 |
| `DAB` | dispute_arm_blocks: DisputeEnter → arm window closes | 144 |
| `MTT` | max_transfer_timeout_blocks | 1008 |
| `E` | quorum_expiry | negotiated (weeks) |
| `E+720 / E+4032 / E+8064` | Tier 1 / 2 / 3 on-chain and off-chain authority | ~5d / ~4w / ~8w after E |
| lottery CSV 72 | partial-reveal leaf (one missing) | ~12h |
| lottery CSV 144 / 1008 / 4032 | recovery cascade T / T-1 / T-2 | 1d / 1w / 4w |
| lottery CSV 8064 | threshold-1 escape hatch | 8w |
| share CSV 144 | forfeited armer slice sweepable | 1d |
| `deadline_block` | on-chain offer credit deadline | per offer |
| LN hold window | bridge reveal window | 18–125 |
| `fee_change_notice_blocks` | notice before a fee change | negotiated |

Two important ordering facts:

1. `DRB` (144) is *longer than* `SRB` (72). A censored wallet waits 72 blocks for the
   proof to become complete, then up to 144 more for a member to be obligated to act,
   then `DAB` 144 for arming, then confiscation confirmation, then reveal. Best case for
   a censored withdrawal is roughly 3–4 days; the wallet is illiquid throughout.
2. Every punitive path ends in an on-chain confiscation transaction that needs a
   *recovery quorum majority* signature. Punitive disputes "do not cascade through the
   lifecycle tiers" (DEP-06). So if fewer than a majority of non-operator members will
   sign, a punitive dispute cannot complete *at all* until `E`, when the respectful path
   opens instead. Fraud with a captured or absent minority-plus-one is unpunishable
   until expiry, and then only respectfully.

---

## 1. Responses to operator actions

### O13 — fails to credit an on-chain payment past `deadline_block`

- **Visible to:** the wallet holding the cosigned offer; anyone who has the offer.
  The offer is *not* on the ledger (WP §deposits), so third parties cannot see it
  unless the wallet publishes.
- **Evidence:** cosigned offer + any later operator-signed update with
  `block_height > deadline_block` + absence of `OnchainCredit`. Autonomous.
- **Response path:** wallet embeds proof hash (self-transfer nonce, DEP-06 §Embedding)
  → any member whose ledger advances past embed+`DRB` must `DisputeEnter` or be
  provably derelict → members arm within `DAB` → recovery majority co-signs
  confiscation → reveal → claim.
- **Cost to responder:** wallet pays a self-transfer fee (on the *accused* operator's
  ledger, who may refuse it — then the wallet must escalate via a member's ledger and pay
  there). Members pay replacement-collateral opportunity cost and on-chain fees.
- **Reward:** members split collateral + excess reserves equally. Wallet gets nothing
  beyond its balance being honoured by the new custodian.
- **Clock:** deadline + `DRB` + `DAB` + confirmations + reveal.
- **Grade:** closed *if* the operator cooperates with embedding or a member accepts
  the escalation; otherwise depends on M13 (paid-but-optional).
- **Gap:** the operator can refuse the self-transfer used to embed. Then the wallet is
  in the O15 case for the embed itself. The fallback "one hop" embed only works if a
  member sells embedding.

### O14 — fails to credit a legacy-mode lightning payment

- **Visible to:** operator (knows), payer (holds preimage), wallet (knows an invoice is
  outstanding but not whether paid).
- **Evidence:** only complete once the payer hands over the preimage (W13).
- **Response path:** as O13 once preimage is obtained.
- **Grade:** **open** at the payer link. The payer has no protocol relationship and no
  reward. Operator can select victims by payer type (SECURITY.md item 1). Bounded only by
  W16 (wallet limits outstanding legacy invoices).

### O15 — ignores a signed request (censorship, withdrawal hostage)

- **Visible to:** wallet (no response), relay (saw request). Not visible to members
  until escalated.
- **Evidence:** none until `DeliveryEmbed`. Then: signed request + embed at height h +
  operator's co-sign referencing member state ≥ embed + operator update at height ≥
  h+`SRB` without the operation.
- **Response path:** wallet pays a member to embed (M13). Member's incentive per DEP-12:
  small fee now, collateral share later. Then M14 obligation applies to *all* members
  once the hash is entangled.
- **Subtlety:** the causal link requires the *operator* to co-sign on the member's
  ledger after the embed (DEP-12 step 2: "at the next co-signature the member provides
  to the operator's ledger ... the operator, by co-signing, proves they have seen"). Read
  carefully: the member's `member_ledger_hash` on the *operator's* ledger advances past
  the embed, and the operator signs that update. So the operator must keep producing
  updates for the proof to close. An operator who **stops signing entirely** after
  seeing an embed never produces the deadline-breach update. That collapses into O29
  (silence) and the respectful path at `E`, with collateral returned.
- **Clock:** `SRB` after embed, then `DRB`, `DAB`, etc.
- **Grade:** closed against an operator who keeps operating; **open** (degrades to
  respectful) against one who goes silent. Selective silence toward one wallet while
  continuing to sign is the closed case; total silence is the safe exit.

### O16 — leaves a lock past `timeout_height`

- **Visible to:** everyone; the lock and heights are on the ledger.
- **Evidence:** update at height > timeout with lock still open. Autonomous, anyone.
- **Response:** any member, per M14 once embedded, or directly (M15 — obligation
  unstated when evidence is on the accused ledger itself, which it is here).
- **Grade:** closed in principle; note the co-signers should have refused the offending
  update (DEP-05 §Co-Signer Obligations #2), so this needs majority complicity to even
  occur. Same for O24 generally.

### O17 — reorders or delays requests within a block

- **Visible to:** counterparties experience it; nothing distinguishes reordering from
  arrival order. Relays have timestamps but nothing binds them.
- **Evidence:** none.
- **Response:** reputational only; bridges/couriers widen margins or leave.
- **Grade:** **open**. Bounded harm: a bridge that gets its `TransferComplete` delayed
  past the LN hold window loses the HTLC and can't recover from the wallet, since the
  wallet's lock will `TransferFail` back to the wallet with the preimage already public.
  The operator can thus make a bridge eat a payment, and can collect the failure fixed
  fee doing it (DEP-07 §Fee on Failure). Repeat exposure is the bridge's choice.

### O19 — raises fees repeatedly within limits

- **Visible to:** the deposit owner, via ledger.
- **Response:** withdraw (subject to O15), or accept. No proof possible; conforming.
- **Grade:** **open** by design. Quorum can refuse to co-sign "unprofitable" terms
  (WP §fees) but nothing lets them refuse *profitable* ones.

### O20 — removes a member

- **Visible to:** all; on ledger. Needs majority cosign of the update, so the *remaining*
  majority consents.
- **Response:** removed member can still block on-chain spends until next `QuorumBegin`
  (DEP-05 §Removing Members), i.e. can hold the rotation hostage for one cycle. Member
  can dispute nothing; removal is conforming.
- **Grade:** closed on the ledger; a temporary hostage window on-chain. Note a majority
  can serially remove dissenters: remove one, threshold shrinks (3-of-5 → 3-of-4 → 2-of-3
  after two removals). A 3-member coalition in Q=5 can reduce to a quorum it fully owns
  in two updates. The whitepaper's "at least one member of any majority" argument holds
  per update, but the *set* of members is majority-mutable.

### O21 / O29 — stops rotating, goes silent

- **Visible to:** all, once `E` passes with no `QuorumBegin`.
- **Evidence:** `QuorumExpired` — any block > E.
- **Response:** at E, majority respectful confiscation (M16); at E+720 minority; at
  E+4032 one member. Reward: the ledger's future fees, *not* collateral. Cost: replacement
  collateral ≥ obligations × ratio, on-chain fees, and taking on a ledger whose operator
  just proved unreliable and whose depositors may all withdraw.
- **Operator counter-response:** re-establish at the same tier (O22) — races on-chain.
- **Grade:** paid-but-optional. If no member wants the ledger, funds sit until E+8064 and
  the operator alone can spend (O23). **[unstated]** whether a Tier 3 spend that ignores
  obligations is a fraud on any ledger; the operator has no quorum by then to prove it
  to, and the collateral is already theirs.

### O22 — degraded re-establishment after expiry

- **Visible to:** all.
- **Response:** competing confiscation; wallets should treat a Tier 1/2 quorum as a
  weaker one (fewer members). **[unstated]** whether a degraded `QuorumBegin` can pick
  *new* members or only "whoever they can still reach". If new, an operator can walk
  their quorum from 5 honest members to 1 captured one by letting expiry pass and
  rebuilding at Tier 2 with one accomplice — as long as no minority confiscates first
  at Tier 1.
- **Grade:** open pending that question.

### O24 — signs a non-conforming update

- **Visible to:** every co-signer, immediately, by validation.
- **Response:** refuse to co-sign (M9); the update then has < majority and is not
  canonical. If the operator *publishes* it anyway with a minority of cosigs, that's
  evidence; any member can dispute (M15).
- **Grade:** closed under honest majority. The interesting case is when the operator
  has a majority: then the update *is* canonical, and only wallets and the honest
  minority can see it's wrong; they can embed evidence, but a punitive confiscation
  needs a recovery majority that doesn't exist. Collateral-slashing of the *complicit
  members* on their own ledgers (M10) is the only remaining lever, and it needs their
  own quorums to act on foreign evidence (M26, unstated obligation).

### O25 — relay choice / relay collusion

- Indistinguishable from R2. See §5.

### O27 — self-fills reserves

- **Visible to:** nobody. Deposits are pseudonymous descriptors.
- **Response:** none. Wallets can only price obligation *totals*.
- **Consequence, first order:** unfilled reserves are the operator's money and are
  confiscated on a punitive dispute (`(R − D) + C` to armers). Filling them with the
  operator's own deposits moves that money into obligations, which the lottery output
  backs one-to-one and which the operator withdraws from the new custodian. The
  operator's punitive loss falls from `C + (R − D)` to `C` plus a period or so of fees
  at the quorum's floors. The whitepaper's "collateral plus excess reserves" deterrent
  is therefore really just collateral.
- **Consequence, second order:** the arming floor is `D × ratio`, so full self-fill sets
  every disputant's required UTXO at the maximum. Members who cannot show that UTXO
  cannot arm and earn nothing, yet are still needed to sign the confiscation (M20).
- **Not a consequence:** the ledger is not a worse acquisition for the winner. The
  puppets are fully backed, pay fees until they leave, and the winner's replacement
  collateral is locked, not lost; it can be reduced at the next rotation once they
  withdraw.
- **Grade:** **open**, but bounded: it removes the excess-reserves component of the
  deterrent and filters the disputant set; it does not create a theft path.

---

## 2. Responses to quorum member actions

### M9 — withholds or delays co-signature

- **Visible to:** operator, and other members if they compare notes; not on-ledger.
- **Evidence:** none; "not protocol-enforced" (DEP-11).
- **Response:** operator removes (O20) at next update, if the rest of the majority
  co-signs the removal. If the withholding members are ≥ half, nothing can be appended
  and the ledger stalls until E.
- **Grade:** **open**. A stalled ledger is indistinguishable from a silent operator.
  The stall lands on the respectful path at E, where the *withholding members* are
  eligible to take custody. So: a coalition of ⌈n/2⌉ members can freeze a healthy
  operator's ledger, wait to E, and confiscate it respectfully — the operator keeps
  collateral but loses the business, and depositors are frozen for the duration. There
  is no proof of member dereliction because nothing was embedded and nothing happened.

### M10 — co-signs an invalid update

- **Visible to:** all, on ledger, by validation.
- **Evidence:** the update itself. Autonomous.
- **Response:** presented to *the member's own* quorum, which may slash them there.
- **Grade:** unpaid → open. The member's own quorum earns a collateral share if they
  dispute — that's a reward — but the trigger obligation (M26/M14) is written for
  evidence "embedded in the causal chain" against *their* operator. Whether a member
  of ledger B must act on B's operator's misbehaviour as a *cosigner on A* is not
  clearly the `DisputeDereliction` condition. Worth pinning down in `04`.

### M11 — declares a stale `member_ledger_hash`

- **Visible to:** anyone who walks the member's chain and compares.
- **Evidence:** `StaleCosignature`; autonomous, expensive to find (SECURITY.md impl 15).
- **Response:** to member's own quorum.
- **Grade:** unpaid. Nobody is paid to look. Note the *useful* attack is not backdating
  but **withholding own-ledger progress**: a member whose ledger has no updates after
  block N is never "active" for `DisputeDereliction` *during the window*; on resumption without a dispute the proof
  completes, so pausing only delays (F8).

### M13 — refuses to sell `DeliveryEmbed`

- **Visible to:** the wallet only.
- **Response:** try another member; if all refuse, "distribute funds elsewhere"
  (DEP-12) — which requires a withdrawal, which is the thing being censored.
  Alternative: embed on *any* ledger and wait for causal propagation (DEP-06
  "Further"), which only closes the proof if the operator eventually co-signs a
  state downstream of it — and there is no `SRB` clock on that path, since
  `SRB` starts at a `DeliveryEmbed`, not at an arbitrary embed.
- **Grade:** paid-but-optional; unanimous refusal is **open** and leaves the wallet
  frozen with no proof.

### M14 — fails to dispute embedded evidence within `DRB`

- **Visible to:** all, on the member's ledger (updates continue, no `DisputeEnter`).
- **Evidence:** `DisputeDereliction`; autonomous.
- **Response:** to member's own quorum.
- **Grade:** unpaid on the trigger side, but the responder (member's own quorum)
  does get a collateral share. Whether *they* are obligated is the M26 question again.
  Escape: stop own ledger (M11 note) — then not "active".

### M17 — declines to arm

- **Visible to:** all (no `DisputeArmed` from that pubkey).
- **Response:** none. Non-armers get no share; excluded from lottery. **[unstated]**
  whether this is dereliction; DEP-11 says "must initiate a dispute", and arming is
  after that. A member can `DisputeEnter` (satisfying M14) and not arm.
- **Consequence:** the recovery quorum is "members minus disputants" for confiscation
  cosigning (DEP-06 Phase 2) — a member who *doesn't* arm is still in the recovery
  quorum and thus still needed for the confiscation signature. Combined with M20 below,
  not arming and then not signing is a veto with no cost.
- **Grade:** open.

### M18 — pledges minimum replacement collateral vs. more

- Verified by co-signers at confiscation (DEP-03). Pledge is a commitment; deviation is
  slashable (M22). A member who pledges from a UTXO they intend to spend elsewhere
  before the claim would stall the claim; **[unstated]** consequence if the pledged UTXO
  is spent between arm and claim (the check is "unspent at the cosigner's tip" at
  confiscation-cosign time, not at claim time). If the winner's pledge is gone, the
  winner can't produce a conforming claim; then partial-reveal/recovery leaves apply?
  Those are keyed on *reveals*, not on claim ability. Potential stall.
- **Grade:** open at the edge.

### M19/M21 — preimage length choice and selective reveal

- **Visible to:** commitment hashes on-chain in the lottery script; reveals on Nostr
  and/or in the claim witness.
- **Response to non-reveal:** N−1 revealers use the partial-reveal leaf after CSV 72
  for exactly one missing; ≥2 missing falls to the recovery cascade at CSV 144+ with
  thresholds T, T−1, T−2 — meaning the *recovery quorum* (which includes the
  non-revealers) decides. Non-revealer's slice is swept to revealers after CSV 144.
- **Strategic structure:** each disputant knows their own contribution and can compute,
  from the *others'* published reveals, whether they win. The last disputant to move sees
  everything. With N=3 and one adversary, the adversary reveals iff they win; else
  withholds, forfeits one slice (1/3 of the pot), and pushes selection to the
  partial-reveal leaf over the other two — a fresh lottery among two honest members, so
  the adversary gains nothing by withholding *unless* the adversary controls ≥2
  disputants. With two adversarial disputants out of 3: they can choose which of their
  two reveals to withhold to produce any outcome over the remaining set. Cost: one
  slice, swept to revealers, which includes their other identity. Net: a 2-of-3 coalition
  steers the lottery at ~1/3 of the slashing pot in cost, and gets the ledger. But 2-of-3
  is a majority anyway, so this only matters in the 5 and 7 cases. Work out in `03`.
- **Grade:** partially closed; the slice forfeiture is a real cost but is *recycled to
  co-conspirators pro-rata* if they are among the revealers.

### M20 — refuses to co-sign the confiscation TX

- **Visible to:** other members (no signature arrives). Not on any ledger.
- **Evidence:** none. **[unstated]** obligation.
- **Response:** punitive path needs a majority of the recovery quorum; if refusers are
  ≥ half, the punitive dispute cannot complete. Respectful path opens at E with lower
  tiers.
- **Grade:** open for non-armers, but blocking needs `Q − floor(Q/2)` refusals, which
  is a strict majority in every allowed size — the accepted collusion case (F2).

### M25 — deviating sweep of forfeited slices

- Visible on-chain; explicitly not slashable yet ("MaliciousSweep may be added").
- **Grade:** open, acknowledged.

### M27 — walks away

- Same as M9 but permanent. Reduces effective Q; enables Tier 1/2 paths at E.
- **Grade:** open; the protocol's answer is "won't be selected next time", which
  only matters to a member who wants future quorums.

---

## 3. Responses to wallet actions

Wallets can misbehave only by (a) spamming requests/escalations, (b) attempting
double-spends across their own concurrent locks, (c) revealing preimages to the wrong
side in HTLC flows, (d) publishing false fraud proofs. All of (a)–(c) are refused by
validation at the operator/co-signer edge. (d): a false proof does not verify and has
no cost beyond the embedding fee; **[unstated]** whether a member who enters a dispute on
a bad proof is penalized (the confiscation TX needs a majority who each verify, so it
should fail at M20 — but the `DisputeEnter` fork and the arming are already public).
Grade: closed for value; open for griefing (a wallet can pay members to embed garbage
forever, which is just revenue for members).

---

## 4. Responses to bridge / courier actions

- **B2/C2/C4 refuse or abandon after wallet locks:** wallet's lock times out; wallet
  pays operator's fixed failure fee (DEP-07). Nothing provable; reputational. Grade:
  open, bounded to the failure fee per attempt. A bridge/courier can grief at the
  wallet's expense; the operator collects.
- **B3/C3 timeout misordering:** self-harming only.
- **B5 collects wallet's lock without paying the invoice:** impossible; completion
  requires the preimage which only comes from paying. Closed.
- **C6 leaks scalar:** self-harming.
- **Bridge vs operator (O17):** see above; bridge's exposure to its own operator.

---

## 5. Responses to relay actions

- **R1 drops durable events:** wallet notices hash-chain gaps only if it walks the
  chain (W9); can query other relays. Operators choose relays (O25), so an operator can
  choose a relay that drops *particular* wallets' view. Grade: open; mitigated by
  multi-relay reads.
- **R2 drops ephemeral requests:** identical symptom to O15; the wallet's only move is
  escalation (W11) which costs money and shifts the request onto a *member's* relay.
  Grade: open at the relay, closed after escalation.
- **R3 stale replaceables:** rollback of subkey revocation / ads. Grade: open.
- **Relay hides Kind 9106 reveals:** revealers can instead reveal on-chain via the
  reveal-claim leaf of their share output (DEP-06 §Arm-and-reveal). Closed, at on-chain
  cost.

---

## 6. Enforcement routing

Who ultimately punishes whom. Every arrow is "X's misbehaviour is punished by Y", and
Y always needs a majority that is honest and live.

```
operator(A)        ──punitive──▶  majority of quorum(A) [needs M20 signatures]
                   ──respectful─▶  any member of quorum(A) at tier ≥ E
member m of A      ──────────────▶  majority of quorum(m's own ledger)   [M26 obligation unstated]
lottery winner w   ──────────────▶  majority of quorum(w's new ledger)   [which w assembles]
wallet             ──────────────▶  nobody (nothing to slash)
bridge/courier     ──────────────▶  nobody (self-enforcing HTLCs; griefing unpriced)
relay              ──────────────▶  nobody
payer              ──────────────▶  nobody
```

Observations:

1. The winner of a punitive lottery is punished by a quorum *they choose* after
   takeover. `WinnerCollateralDeviation` (M22) is slashable "on whatever ledger they're
   operating after takeover" — a ledger whose quorum the winner just formed.
2. Member punishment always crosses a ledger boundary and always lands on a quorum
   that gains a share but has no stated obligation. Whether M26 is a duty decides
   whether the "web of collateral" has any tension in it.
3. Wallet-initiated enforcement is a bounty market (DEP-12's own word) with members as
   the only bidders. Members' willingness to bid depends on the collateral share
   exceeding replacement-collateral cost plus the burden of running a possibly
   self-filled ledger. That ratio is the number to compute in `03`.

---

## 7. Carried forward to 03

Games that the response map singles out:

- **G1 Lottery reveal** (M19/M21 with N=5,7 and k adversarial disputants).
- **G2 Confiscation veto** (M17+M20): value of not signing; whether a minority can
  hold the punitive path until E and convert it to respectful.
- **G3 Member freeze** (M9): ⌈n/2⌉ members stall a healthy ledger to E and take it.
- **G4 Silent exit vs. fraud** (O29 vs O24): expected value of each for an operator
  with obligations D, collateral C, and the O27 self-fill fraction s.
- **G5 Escalation bounty** (M13/M14/O15): member's price for embedding vs. expected
  collateral share; whether unanimous refusal is an equilibrium with a captured quorum.
- **G6 Serial removal** (O20): majority coalition compacting the quorum.
- **G7 Degraded rebuild** (O22): whether a Tier 1/2 `QuorumBegin` can introduce new
  members and thereby replace an honest quorum with a captured one.
- **G8 Cross-ledger contagion** (M10/M14/M26): does any quorum ever act on foreign
  evidence, and what if members of the misbehaving quorum sit on each other's quorums.
- **G9 Takeover economics**: replacement collateral ≥ obligations × ratio, against a
  slashing share of (C + R − D)/Q, as a function of self-fill.
