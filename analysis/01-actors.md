# 01 — actors and their discretion

An "actor" here is a role, not a machine. One key can play several roles at once
(an operator is normally also a quorum member elsewhere, a courier is a deposit holder,
a bridge is a deposit holder with an LN node). Coalitions are treated in §9.

For each actor: what they hold at stake, what they earn, and the full list of points
where the protocol leaves them a choice. Choices are tagged:

- **P** parameter chosen at setup, binding later
- **A** action taken during operation
- **Ω** omission: something the protocol expects that they can decline or delay
- **[slashable]** failure is provable and punishable (DEP-11)
- **[advisory]** failure is not provable or not punished; only market consequences
- **[unstated]** the spec does not say what happens

---

## 1. Operator

Runs a ledger: appends updates, holds the reserves+collateral UTXO jointly with the
quorum, is the sole party who can propose updates (WP §ledgers; DEP-02).

**Stake.** Collateral portion of the UTXO (DEP-05 §Collateral); reputation across
all ledgers they run; fee stream; collateral on *other* ledgers they operate, via
cross-ledger slashing (DEP-05 §Slashing, DEP-06 §Punitive).

**Earns.** Periodic balance fees and per-transfer fees (DEP-07), minus compensation
paid to quorum members (DEP-05 §Member Terms, default 3% each).

### Setup discretion

| # | Choice | Ref | Tag |
|---|---|---|---|
| O1 | reserves / collateral split of the UTXO | DEP-05 §Structure | P, only bounded by co-signer agreement |
| O2 | number of ledgers L and how the UTXO is divided | DEP-05 §Multi-Ledger | P, "SHOULD 3–5", not enforced |
| O3 | which operators to invite to the quorum; size 3/5/7 | DEP-05 §Joining | P |
| O4 | which invitees to accept given their terms (min fees, timing params, compensation) | DEP-05 §Member Terms | P |
| O5 | `quorum_expiry` (= shortest membership_until accepted) | DEP-05 §QuorumBegin | P, derived from O4 |
| O6 | advertised fee minimums, guarantee matrix, capabilities | DEP-04 §Advertisements, DEP-07 | P, matrix is a promise not a proof |
| O7 | access control: allowlist / denylist / attestation requirement | DEP-08 §Access Control | P |
| O8 | whether to offer legacy deterrence-mode invoice receive (sidecar holds preimage) | DEP-10 §Offline receive | P |
| O9 | whether to run a bridge / courier from their own deposit | DEP-10, DEP-13 | P |
| O10 | quorum member overlap with their own other ledgers, and with members' ledgers | — | P, **[unstated]** no independence rule |

### Operating discretion

| # | Choice | Ref | Tag |
|---|---|---|---|
| O11 | accept or refuse any `deposit_open` (and at what fee ≥ minimums) | DEP-07 §Fee Negotiation | A, advisory |
| O12 | create on-chain funding offers, and their `deadline_block` | DEP-10 §Offers | A, "in the operator's discretion" (WP §deposits) |
| O13 | credit an on-chain payment before deadline | DEP-11 §On-chain Offer Credit | Ω, **slashable** (autonomous proof) |
| O14 | credit a legacy-mode lightning payment | DEP-11 §Lightning Invoice Credit | Ω, slashable only if payer surfaces preimage |
| O15 | process a signed wallet request (transfer, withdrawal) promptly | DEP-11 §Withdrawal and Transfer Processing | Ω, slashable only after DEP-12 escalation |
| O16 | append `TransferFail` after timeout | DEP-11 §Transfer Timeout | Ω, slashable |
| O17 | ordering of requests within a block; which of several valid requests to include first | — | A, **[unstated]** (front-running of locks/bridges) |
| O18 | `FeeCollect` timing within the period | DEP-11 §Fee Collection | A, advisory |
| O19 | `FeeChange` within notice/limit params, repeatedly | DEP-07 §Fee Changes | A, no cumulative cap (see SECURITY.md item 5) |
| O20 | `QuorumRemoveMember` — immediate, unilateral on-ledger effect | DEP-05 §Removing Members | A, needs majority cosign of the update itself but removes one veto |
| O21 | rotate before `quorum_expiry` | DEP-11 §Quorum Rotation | Ω; signing value ops after expiry is slashable; simply stopping is not |
| O22 | re-establish at degraded tiers after expiry | DEP-05 §Lifecycle | A, races confiscation |
| O23 | spend the UTXO via Tier 3 solo path at expiry+8064 | DEP-03 §Spending Tiers | A, "last resort"; after expiry this is not non-conforming **[unstated whether obligations survive]** |
| O24 | sign a non-conforming update (equivocation, over-spend, bad fee) | DEP-06 type 5 | A, slashable *if* quorum refuses / detects |
| O25 | choose which relays to publish to and read from | DEP-04 §Relay Architecture | A, advisory; censorship indistinguishable from relay loss (SECURITY.md item 10) |
| O26 | co-sign invoices/offers with which quorum member (they need one member's cosign) | WP §deposits | A |
| O27 | self-fill: open deposits on own ledger with own funds | PROPOSAL.md assumption | A, invisible to wallets |
| O28 | delegate signing to a subkey | DEP-04 §Delegation | A |
| O29 | stop responding entirely (disappear) | — | Ω, triggers respectful path only; collateral returned |

Note on O29 vs O24: the protocol distinguishes *going quiet* (collateral returned to
operator, DEP-06 §Respectful) from *provable fraud* (collateral confiscated). An
operator who wants out with their collateral intact must therefore never sign anything
non-conforming and simply stop. This is by design ("allows honest operators to leave
without rugging anyone", FAQ) but it also means the strongest deterrent only applies to
operators who leave a signature behind.

---

## 2. Quorum member (co-signer)

Another operator who has joined this ledger's quorum. Must keep a full state replica
and validate every update before co-signing (DEP-05 §Co-Signer Obligations).

**Stake.** Nothing on *this* ledger. Their collateral sits on their *own* ledger(s),
where their own quorum can slash them for misbehaviour here (DEP-05 §Slashing,
"min_member_collateral"). So the member's downside depends on a *different* quorum's
willingness to act.

**Earns.** `compensation_bps` share of the operator's collected fees (default 3%), paid
to a deposit on the operator's ledger (DEP-05 §Member Terms). Note the compensation
deposit is itself an obligation of the ledger they are guarding. Contingent: an equal
share of confiscated collateral if they arm and reveal in a punitive dispute
(DEP-06 §Punitive). Contingent: the ledger itself (fee stream) if they win the lottery.

### Setup discretion

| # | Choice | Ref | Tag |
|---|---|---|---|
| M1 | accept or refuse an invitation | DEP-05 §Joining | A |
| M2 | min_fee_bps, min_fee_fixed, max_fee_period (floors the operator must respect) | DEP-05 §Member Terms | P |
| M3 | membership_until | DEP-05 | P, shortest one sets quorum_expiry for everyone |
| M4 | dispute_response_blocks, dispute_arm_blocks, service_response_blocks, max_transfer_timeout_blocks | DEP-05, DEP-11 | P, strictest wins; these bound *their own* obligations |
| M5 | compensation_bps, frequency, deposit | DEP-05 | P, per member |
| M6 | max_descriptor_bytes | DEP-05 | P |
| M7 | how many quorums to serve on; whether to serve alongside the same peers repeatedly | — | P, **[unstated]**; correlation is what wallets are told to price (WP §network health) |
| M8 | `DeliveryEmbed` price | DEP-12 §Pricing | P |

### Operating discretion

| # | Choice | Ref | Tag |
|---|---|---|---|
| M9 | co-sign a valid update, or not, or slowly | DEP-11 §Co-signing | Ω, **advisory** ("not protocol-enforced") |
| M10 | co-sign an invalid update | DEP-05 §Conformance | A, slashable on own ledger |
| M11 | which `member_ledger_hash` to declare when co-signing | WP §time | A; backdating is slashable (DEP-06 type 3); *not advancing* own ledger is not |
| M12 | co-sign offers / invoices for the operator | WP §deposits | A, advisory |
| M13 | accept a wallet's `DeliveryEmbed` request | DEP-12 | A, advisory ("if no member accepts, wallet learns quorum is uncooperative") |
| M14 | initiate dispute on valid embedded evidence within dispute_response_blocks | DEP-11 §Dispute Participation | Ω, slashable **only if their own ledger keeps advancing** |
| M15 | initiate dispute on evidence that is *not* embedded on a chain they co-sign (e.g. Kind 9101 broadcast only) | DEP-06 §Enter | A, **[unstated]** whether obligated |
| M16 | initiate a `QuorumExpired` respectful dispute after expiry | DEP-06 §Respectful | A, optional; reward is the ledger, not slashing |
| M17 | arm (commit secret + pledge replacement collateral) within dispute_arm_blocks | DEP-06 §Phase 1 | A; not arming = no share, and **[unstated]** whether not arming is itself a failure to "act" under M14 |
| M18 | size of replacement collateral pledged (≥ floor) | DEP-03 §Replacement collateral | P at arm time |
| M19 | preimage length (1..N contribution) | DEP-06 §Phase 1 | P, chosen before seeing others |
| M20 | co-sign the confiscation TX as part of the recovery quorum; verify others' collateral declarations | DEP-03, DEP-06 §Phase 2 | A/Ω, **[unstated]** whether refusing to co-sign confiscation is slashable |
| M21 | reveal preimage, when, and whether at all (after seeing others' reveals) | DEP-06 §Phase 3 | A; non-reveal forfeits slice after CSV 144 sweep |
| M22 | as lottery winner: broadcast conforming claim TX, or deviate | DEP-06 type 6 | A, slashable on their new ledger |
| M23 | as lottery winner: actually operate the acquired ledger well | — | A, becomes an operator (§1) |
| M24 | as loser: append `DisputeYield` | DEP-06 §Phase 4 | Ω, **[unstated]** consequence of not yielding |
| M25 | participate in sweeping forfeited slices pro-rata to revealers, or construct a deviating sweep | DEP-06 §Sweep | A, "enforced by honesty and reputation", no fraud type yet |
| M26 | act on a fraud proof from *another* ledger against an operator who is a member of *my* quorum, or whose ledger I co-sign | DEP-05 §Slashing | A, **[unstated]** obligation and reward |
| M27 | walk away (stop signing) without misbehaving | DEP-11 | Ω, advisory; enables Tier 1/2 degraded paths |

Key structural fact: a member's *punishable* obligations (M10, M14) are all conditioned
on the member continuing to publish on their own ledger. A member who goes silent
everywhere is unpunishable; a member with no ledger of their own (allowed? DEP-05 says
"must have collateral at stake on their own ledger(s)") would be unpunishable too.

---

## 3. Wallet / depositor

Holds deposits controlled by a DEP-16 descriptor. Assumed mostly offline, mobile,
possibly never running its own verification (README "bob").

**Stake.** Balance across deposits. Nothing slashable.

**Earns.** Liquidity. Pays fees.

| # | Choice | Ref | Tag |
|---|---|---|---|
| W1 | which operators, based on fees, quorum size, quorum independence signals, guarantee matrix | WP §quorum, §network health; DEP-04 | A, "wallets cannot prove independence, only price it" |
| W2 | how many operators to spread across; non-overlapping quorums | DEP-11 §Fund Distribution | A, advisory |
| W3 | negotiated fee schedule and change params at open | DEP-07 | P, within operator's and quorum's minimums |
| W4 | `receive_requires_sig` | DEP-08 | P |
| W5 | descriptor (single key, multisig, dep-16 conditions) | DEP-08, DEP-16 | P |
| W6 | accept an operator whose matrix offers only deterrence rows | DEP-04 §Guarantee Matrix | A |
| W7 | which bridge / courier to use; which timeouts to accept | DEP-10, DEP-13 | A |
| W8 | retain evidence (offers, invoices, cosigs) | DEP-11 §Evidence Retention | Ω, self-interest only |
| W9 | verify co-signatures, walk chains, check quorum freshness before open | DEP-11 §Dispute Detection, DEP-04 §Pre-Open Check | Ω, self-interest; most wallets will skip the expensive parts |
| W10 | construct and embed a fraud proof (autonomous for on-chain) | DEP-06 §Embedding | A; costs a self-transfer fee; embedding target chosen |
| W11 | escalate via `DeliveryEmbed`, to which member, paying what | DEP-12 | A, costs money each time |
| W12 | broadcast Kind 9101 fraud proof publicly | DEP-06 §Broadcast | A |
| W13 | as *payer* in a legacy-mode lightning payment: hand the preimage to the payee | DEP-06 §On-chain vs Lightning | A, no incentive in-protocol |
| W14 | after a custody change: accept new custodian only after claim TX confirms | DEP-06 §Recovery | Ω, self-interest; UX pressure to skip |
| W15 | leave funds on an expired-quorum ledger vs. withdraw | DEP-04 §Pre-Open Check | A; opening is forbidden, staying is not addressed **[unstated]** |
| W16 | limit outstanding uncredited legacy invoices | DEP-10 §Trust Boundaries | A |

Wallets have no slashable obligations and no in-protocol reward for vigilance beyond
protecting their own balance. Every enforcement path that starts with a wallet
(W10–W12) costs the wallet money and requires it to be online and run verification.

---

## 4. Bridge (lightning)

Any deposit holder with an LN node. Provides atomic HTLC bridging between the ledger
and lightning (DEP-10 §Lightning).

**Stake.** Its own deposit balance and LN channel capital. Not slashable; "residual
misbehaviour is refusing service" (WP §lightning).

| # | Choice | Ref | Tag |
|---|---|---|---|
| B1 | spread / service fee | DEP-10 | P |
| B2 | which hashes to issue invoices for; refuse service | DEP-10 | A, advisory |
| B3 | timeout ordering between ledger lock and HTLC expiry | DEP-10 §Hold windows | A; wrong ordering hurts only the bridge |
| B4 | whether to settle upstream after reading preimage on ledger (must, or lose funds) | DEP-10 | A, self-enforcing |
| B5 | on pay: actually route the payment, or let the lock expire after taking the fixed fee | DEP-07 §Fee on Failure, DEP-10 §Pay | A, **[unstated]** who gets the failure fee — operator, not bridge, but bridge can grief |
| B6 | for legacy-mode: this role collapses into the operator's sidecar (§1, O8/O14) | DEP-10 | — |

A bridge depends on the operator to append its `TransferLock`/`TransferComplete`
promptly (O15, O17). The operator can front-run or delay a bridge's completion inside
the HTLC window; that is the bridge's exposure to the operator.

---

## 5. Courier (cross-ledger)

Deposit holder on ≥2 ledgers, carries HTLC/PTLC transfers between them (DEP-13).

**Stake.** Own balances on each ledger. Not slashable.

| # | Choice | Ref | Tag |
|---|---|---|---|
| C1 | fee_in / fee_out per ledger, capacity advertised | DEP-13 §Fee Model | P, may misadvertise |
| C2 | accept a route request | DEP-13 | A |
| C3 | timeout_margin_blocks | DEP-13 §Timeout Safety | P |
| C4 | forward (lock on B) after the wallet locks on A, or not | DEP-13 step 4 | A; not forwarding costs wallet a lock-and-fail fee on A |
| C5 | complete on A after wallet reveals on B (must, or lose funds) | DEP-13 step 6 | self-enforcing, subject to operator A appending it (O15/O17) |
| C6 | keep blinding scalar secret (PTLC) | DEP-13 §Security | A |

Couriers are exposed to *two* operators' ordering discretion (O17) and to the max
transfer timeout of both quorums.

---

## 6. Payer (external lightning sender)

Not a protocol participant. Matters in exactly one place: in legacy deterrence mode
they alone hold the proof of payment (W13). Their choice: share the preimage with the
payee or not. No cost or benefit either way. This is the "weak, explicitly
acknowledged" link.

---

## 7. Relay

Nostr relay. Stores durable ledger events, forwards ephemeral requests, serves
advertisements (DEP-04).

**Stake.** None in-protocol.

| # | Choice | Ref | Tag |
|---|---|---|---|
| R1 | retain / drop durable events (Kind 9100 updates, 9103 disputes, 9106 reveals) | DEP-04 | A; wallets told to cross-check hash chain for gaps |
| R2 | forward / drop ephemeral requests (20101) | DEP-04 | A; drop is indistinguishable from operator censorship (SECURITY.md item 10) |
| R3 | serve stale replaceable events (ads, subkeys, wallet state) | DEP-04 | A |
| R4 | log IP addresses | FAQ | A, only privacy leak |

A relay colluding with an operator can make honest requests disappear and the wallet
can only respond by escalating (W11), which costs money. A relay colluding with a
disputant can hide reveals (M21) during the window.

---

## 8. Verifier (attestation service, DEP-14/15)

Optional gatekeeper for `deposit_open`. Discretion over who gets attested, cover
composition for ring signatures, revocation. Affects *who can become a depositor* on
gated operators. Not slashable. Out of scope for the core safety game but relevant to
sybil-formation and to DoS of onboarding.

---

## 9. Coalitions and multi-role identities

The whitepaper's own adversary is a coalition (WP §network health). The roles above
combine in ways the spec does not always name:

| Coalition | What the combination unlocks |
|---|---|
| Operator + majority of own quorum | sign anything; the "cannot protect against" case |
| Operator + one quorum member | co-signed offers/invoices with a captured cosigner (O26/M12); a captured member can also front-run `DeliveryEmbed` refusal (M13) |
| Operator + minority of quorum | block nothing during Tier 0; but at Tier 1 (expiry+720) can re-establish, competing with a confiscating minority |
| Operator + relay | censorship without evidence; forces wallets to pay for escalation |
| Two or more quorum members | coordinate non-reveal to steer the lottery (M19/M21); coordinate sweep destinations (M25) |
| Member of ledger A who also operates ledger B where A's operator is a member | mutual hostage: each can slash the other |
| Operator running L ledgers with overlapping quorums | reduces the independent-quorum assumption the 49% claim rests on (O10) |
| Operator + self-filled depositors (O27) | inflates apparent reserves usage and makes reserves confiscation costless to them |
| Bridge/courier + operator | ordering games (O17) against counterparties |

The unit of trust the protocol actually has is: *for every ledger, a strict majority of
its quorum is honest and live within the block windows.* Every actor's punishability
routes through some other quorum's honest majority. Section 02 traces those routes.

---

## 10. Observed gaps to carry forward

Collected from the **[unstated]** tags above; not yet findings, just questions.

1. No independence constraint on quorum composition (O10, M7). Everything about the
   49% result depends on it, and only wallets are asked to price it.
2. Whether declining to arm (M17), declining to co-sign a confiscation (M20), or
   declining to act on foreign fraud proofs (M26) is an "inactive member" failure.
   DEP-11 defines the failure as "did not initiate a dispute", which is narrower.
3. Operator ordering discretion (O17) is unbounded and unobservable.
4. What happens to obligations after a Tier 3 solo spend (O23).
5. Whether wallets should exit an expired-quorum ledger (W15).
6. Fee-change compounding (O19) as a slow exit that never triggers a proof.
7. Payer has no reason to surface the preimage (§6).
8. Member compensation is a deposit on the guarded ledger: a member who confiscates
   is also confiscating their own unpaid fees, and inherits them as an obligation.
