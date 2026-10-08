# DEP-06: Fraud Proofs and Recovery

## Abstract

This document specifies fraud proof construction, embedding, broadcast, and verification, as well as the dispute and recovery protocol.

## Fraud Proof Types

1. **Uncredited on-chain payment**: operator saw sufficient confirmations (proved by block_height in signed updates) but did not credit the deposit. Wallet constructs this autonomously.

2. **Uncredited lightning payment**: operator created a cosigned invoice, received payment (proved by preimage), but did not credit the deposit. Requires the payer to provide the preimage to the wallet.

3. **Stale co-signature**: a co-signer's `member_ledger_hash` in a signed update precedes their own later hash — proving they backdated their attestation.

4. **Inactive quorum member**: a member was active (their ledger has updates after the fraud) but did not initiate a dispute within the required block window.

5. **Non-conforming update**: the operator signed a ledger update that violates protocol rules (e.g., spending more than balance, invalid fee collection).

   An operator-signed update that extends nothing in the ledger's history (its `previous_hash` links to no update) is not itself fraud, even though v2 signatures make it attributable: it is provable only as `Equivocation` (it conflicts with another update at its sequence) or as a non-conforming update (if it is cosigned).

6. **Winner collateral deviation**: the lottery winner's broadcast claim TX deviates from the replacement collateral they committed to in `DisputeArmed` — missing the second input, pointing at a different UTXO, committing less than declared, or adding change outputs that drain the pledged amount. Verifiable on-chain by inspecting the claim TX against the disputant's stored `DisputeArmed` declaration.

7. **Unauthorised vault spend**: the reserves UTXO was spent by any script path (Tier 0–3) to outputs that are neither a `QuorumBegin` rotation recorded on the ledger (including its exit, migration, and splice outputs under DEP-20) nor a confiscation transaction backed by a valid dispute. Evidence is the spending transaction, the ledger's latest `QuorumBegin`, and absence of a matching rotation or `DisputeEnter`. Every key whose signature appears in the witness is an accused; the proof is punitive and is presented on each accused's own ledgers. Verifiable by anyone from chain data plus the ledger.

## Proof Construction

A fraud proof is a hashable evidence document:

    tag = SHA256("deposits/fraud_proof")
    proof_hash = SHA256(tag || tag || proof_type_byte || accused_pubkey || ledger_id || evidence_bytes)

The `evidence_bytes` are canonical and vary by proof type.

The list above is descriptive; `proof_type_byte` is the wire discriminant:

| byte | proof type | | byte | proof type |
|---|---|---|---|---|
| 1 | `UncreditedOnchainPayment` (list 1) | | 6 | `QuorumExpired` |
| 2 | `UncreditedLightningPayment` (list 2) | | 7 | `WinnerCollateralDeviation` (list 6) |
| 3 | `StaleCosignature` (list 3) | | 8 | `Equivocation` |
| 4 | `DisputeDereliction` (list 4) | | 9 | `NonConformingCosignature` |
| 5 | `NonConformingUpdate` (list 5) | | 10 | `UnauthorizedVaultSpend` (list 7) |

For `DisputeDereliction`, `accused_pubkey` is the derelict member and

    evidence_bytes = ascii_hex(original_fraud_hash) || original_fraud_block_hash || ascii_hex(member_ledger_id) || ascii_hex(member_pubkey)

where `original_fraud_block_hash` is the 32 raw bytes of the block anchoring the original proof's
detection; in JSON it is serialised as lowercase hex, like every other hash. `required_response_blocks`
and the member's active update are carried but not hashed. The proof is self-evident (the member's own
signed update after the window is the evidence) and needs no embedding.

For `UncreditedOnchainPayment` with DEP-20 §8.3 migration evidence (JSON variant
`UncreditedMigration`), `accused_pubkey` is the receiver, `ledger_id` its ledger, and

    evidence_bytes = ascii_hex(source_notice_update) || ascii_hex(source_qb_update) || ascii_hex(proof_update) || confirmed_at_block_hash

The two source updates are the source's signed `DormancyNotice` (carrying the receiver's signed
`DormancyAccept` and the offered manifest) and its signed `QuorumBegin` that paid the migration;
`proof_update` is the receiver's own signed update whose signed header dates the failure. The
deadline is **never carried**: it is the receiver's governing `service_response_blocks` at the
accept — the largest value declared (`QuorumAddMember`) by a member of the `QuorumBegin` governing
the accept's sequence, 72 if none — read from the receiver's history; a verifier ignores any
deadline a proof carries. A verifier requires: both source updates the same operator's on one
ledger, the notice first; the accept the accused's on `ledger_id`, over the notice's
`manifest_hash`, and unexpired at the `QuorumBegin`'s block height; the `QuorumBegin`'s
`migration_receiver` the accused and its migrated entries all in the manifest;
`confirmed_at_block_hash` on its chain; `proof_update` signed by the accused on `ledger_id`,
present in its history, its block on the verifier's chain at its signed height, at least the
deadline after the confirming block; and some migrated entry without an `OnchainCredit` of its
deposit and exact amount naming (`new_outpoint_txid`, `migration_vout`) at or before
`proof_update`'s sequence. It is self-evident and needs no embedding: every element is a signed
update or a block on the verifier's chain. Any node holding the source ledger may produce it; a
receiver whose next rotating `QuorumBegin` omits the splice is instead caught by
`NonConformingUpdate`.

For `UnauthorizedVaultSpend`, `accused_pubkey` is one witness signer, `ledger_id` is a ledger that signer operates (the one the proof is presented on), and

    evidence_bytes = ascii_hex(spent_ledger_id) || u64_le(governing_quorumbegin_seq) || ascii_hex(spend_tx) || spend_block_hash

where `spend_block_hash` is the 32 raw bytes of the confirming block. The proof also carries each spent input's prevout (`sats:script_pubkey_hex`, needed for the BIP-341 sighash); these are not hashed, since the transaction commits to them. A verifier rebuilds the reserves from the spent ledger's operator and the `QuorumBegin` at `governing_quorumbegin_seq`, finds the input spending its vault outpoint, matches the witness leaf and control block to a tier, verifies the witness signatures to that tier's threshold, and requires the accused among the signers and the block on its chain. A spend whose txid is a recorded `QuorumBegin`'s `new_outpoint_txid` is authorised at once (rotations are recorded before they are broadcast, DEP-03 §Rotation ordering); any other spend is judged only once it is 3 blocks deep, a backstop for a watcher that has not yet received the `QuorumBegin`. A confiscation is excused only when the verifier knows it: one it built, cosigned, or saw confirmed as a dispute's confiscation (its own dispute record); a verifier that missed the dispute may wrongly accuse its signers. The proof is self-evident and needs no embedding.

## Embedding

The 32-byte `proof_hash` is embedded into a ledger chain as wallet-controlled data — typically as the `nonce` field (type 210) in a self-transfer (see DEP-09). Once the operator signs an update containing this hash, the evidence is causally ordered.

Embedding is for evidence that is not itself cryptographic proof of non-conformity: fraud that happens off the ledger, or whose proof depends on when something was known — an uncredited on-chain or lightning payment (types 1–2), an inactive quorum member (type 4), and censorship (DEP-11, DEP-12). A proof whose evidence already is cryptographic proof of non-conformity needs no embedding and no causal chain, and verifiers MUST NOT require one: a non-conforming update (type 5), an equivocation (two signed updates at one sequence), a stale or non-conforming co-signature (type 3), a winner collateral deviation (type 6), an unauthorised vault spend (list item 7, wire type 10), and an expired quorum (block-anchored). Its evidence verifies on its own, and a quorum member reporting its own operator after the fraud could not embed it anyway: the accused chain now contains the fraud, honest members never co-sign past it, so no causal link to the accused ledger can form.

Embedding targets (in order of preference):
- **Direct**: on the accused operator's ledger
- **One hop**: on a quorum member's ledger, entangled at next co-signature
- **Further**: any ledger in the web, waiting for causal propagation

## Broadcast

A fraud broadcast (Kind 9101 Nostr event) contains:

- **proof**: the hashable evidence (proof type, accused, ledger_id, evidence)
- **embedding**: where the hash was placed (ledger_id, sequence, update_hash, field name) — omitted for a proof that is itself cryptographic evidence (see Embedding)
- **causal_chain**: ordered list of co-signed updates linking the embedding to the accused ledger — omitted with the embedding

Each `CausalLink` is a co-signed update on ledger X whose `member_ledger_hash` comes from ledger Y, proving X happened after Y.

Direct embedding: empty chain. One hop: one link. Longer paths: multiple links.

## Verification

A verifier always checks the proof's own evidence. For a proof that needs embedding (see Embedding), it also:

1. Hashes the proof, confirms it matches the nonce at `embedding.sequence`
2. Walks the causal chain: each link's `source_ledger_id` matches the previous link's `ledger_id`
3. Confirms the last link reaches the accused ledger
4. Fetches and verifies signatures on each referenced update

## On-chain vs Lightning Evidence

**On-chain** (autonomous): the wallet has all evidence — cosigned offer, block height proving confirmations, absence of credit on the ledger. The fraud proof is constructed and embedded without interaction.

**Lightning** (interactive): the wallet has the cosigned invoice but NOT the preimage. The payer must provide the preimage (their receipt of payment). Only then can the wallet verify `SHA256(preimage) == payment_hash` and construct the proof. Without the preimage, the wallet can only flag the invoice as outstanding.

## Dispute Lifecycle

### Enter (disc 54)

When a quorum member detects fraud (via Kind 9101 broadcast or direct observation), they:

1. Create a fork of the disputed ledger from the last valid sequence
2. Append `DisputeEnter` with the reason and last valid sequence
3. Append `DisputeArmed` with a commitment hash (HASH160 of a secret preimage) and target reserves address

### Lottery

The lottery determines which quorum member takes custody of the disputed ledger. Selection happens *on chain*, enforced by a Tapscript that only lets the script-determined winner spend the lottery output. Off-chain agreement on the outcome is not required. DEP-03 §"Custody Lottery" summarises the flow; the construction is specified here.

#### Phase 1: Commitment (DisputeArmed)

Each participating quorum member appends `DisputeArmed` to their fork with:

- **commitment_hash**: `HASH160(preimage)` where `preimage` is a 17-to-76-byte random value chosen by the member, independent of how many others arm. The preimage's *length* contributes the entropy: `contribution = LEN(preimage) - 16` lies in `1..=60` (`LOTTERY_CONTRIBUTION_RANGE = 60`; 76 bytes stays within the 80-byte standard tapscript stack item).
- **target_reserves**: the bitcoin address where the member wants their winnings sent if they win
- **armed_block**: the block height at time of arming
- **replacement_collateral_outpoint**: txid + vout of an unspent UTXO the disputant controls and pledges to commit to the new vault if they win (see DEP-03 §"Replacement collateral declaration")
- **replacement_collateral_amount**: the value (in sats) they pledge to commit from that UTXO; must satisfy `≥ obligations × collateral_ratio + claim_fee_estimate` where `obligations` is the total deposits owed at `last_valid_sequence`

Members must arm within `dispute_arm_blocks` after `DisputeEnter`. Late entries are excluded. Of the armers within the window, only those whose replacement collateral passes the eligibility snapshot in DEP-03 §"Replacement collateral declaration" are lottery participants; a failing declaration excludes that armer and never stalls the dispute. A single participant takes custody without a draw. `dispute_arm_blocks` is recorded in `QuorumAddMember` so all parties agree on the obligation at join time.

The participant ordering (canonical, derived from sorted `quorum_pubkey`) and the committed hashes go into the lottery script that the confiscation transaction will lock funds into.

#### Phase 2: Confiscation

After the arm window closes, the recovery quorum (quorum members minus the disputants — the disputed operator + non-arming members) cosigns a confiscation transaction that spends the disputed reserves UTXO to a new Taproot output: the **lottery output**. The required recovery-quorum threshold for the confiscation cosignature follows the lifecycle schedule in DEP-05 §Lifecycle: a strict majority of the recovery quorum at Tier 0 (immediately past `quorum_expiry`), a minority at Tier 1 (`quorum_expiry + 720`), a single recovery-quorum member at Tier 2 (`quorum_expiry + 4032`). The confiscation transaction's on-chain spend witness uses the matching on-chain tier from DEP-03 §Spending Tiers, so on-chain and off-chain authority always agree at the chain tip when the confiscation TX is signed.

Its tapscript tree (internal key: the NUMS point) contains, for the k eligible participants in
canonical order (sorted x-only pubkey), `2 ≤ k ≤ MAX_LOTTERY_PARTICIPANTS = 7`:

- **Full-set leaf** (no timelock): verifies every participant's preimage and lets only the
  `(Σ contribution) mod k`-th participant spend.
- **Revealer-subset leaves**: one per nonempty proper subset S of the participants (`2^k − 2`
  leaves), each behind `<LOTTERY_REVEAL_CSV = 72> OP_CSV OP_DROP`. A subset leaf requires a
  threshold of recovery-voter signatures attesting S (below), verifies the preimages of exactly
  the members of S, and lets only the `(Σ_{i∈S} contribution_i) mod |S|`-th member of S spend.
- **Recovery cascade** at CSV 144 / 1008 / 4032 with thresholds T / T-1 / T-2, and the
  timeout-recovery escape hatch at CSV 8064 with threshold 1, as before.

A sole eligible participant (k = 1) gets a plain signature leaf instead of the first two kinds:
it takes custody without a draw.

**Leaf scripts.** For a member list S = (s_0 … s_{m-1}) in canonical order:

    [ <72> OP_CSV OP_DROP                                      ; subset leaves only
      <v_0> OP_CHECKSIG <v_1> OP_CHECKSIGADD … <v_{r-1}> OP_CHECKSIGADD
      <T> OP_GREATERTHANOREQUAL OP_VERIFY ]                     ; subset leaves only
    for each i in 0..m:  OP_DUP OP_HASH160 <h_{s_i}> OP_EQUALVERIFY
                         OP_SIZE OP_DUP <17> OP_GREATERTHANOREQUAL OP_VERIFY
                         OP_DUP <76> OP_LESSTHANOREQUAL OP_VERIFY
                         OP_SWAP OP_DROP <16> OP_SUB  [OP_TOALTSTACK unless i = m-1]
    (m-1) × (OP_FROMALTSTACK OP_ADD)
    m = 1:  OP_DROP <pk_{s_0}> OP_CHECKSIG
    m ≥ 2:  for b in 5,4,3,2,1,0:  OP_DUP <m·2^b> OP_GREATERTHANOREQUAL OP_IF <m·2^b> OP_SUB OP_ENDIF
            for i in 0..m:  OP_DUP <i> OP_EQUAL OP_IF OP_DROP <pk_{s_i}> OP_CHECKSIG OP_ELSE
            OP_DROP OP_0  m × OP_ENDIF

`v_0 … v_{r-1}` are the recovery voters sorted by x-only key and T the recovery threshold. **The recovery voters** are the members, other than the original operator (the author of sequence 0), of the `QuorumBegin` governing the confiscated vault: the latest `QuorumBegin` authored by the original operator at a sequence ≤ the dispute's fork point (the lowest `last_valid_sequence` any `DisputeEnter` names). Later `QuorumBegin`s (past the fork point, or on any fork) do not count. T = ⌊r/2⌋ + 1. Every implementation derives the lottery address from this set (vector `lottery_recovery_voters.txt`); the
sum is below 64·m, so six conditional subtractions reduce it mod m. Witness, bottom to top:
`winner_sig, preimage_{s_{m-1}} … preimage_{s_0}, [voter_sig_{r-1} … voter_sig_0], leaf, control`
(an absent voter signature is the empty push).

**Leaf order** (it fixes the tree, and so the address): the full-set leaf; then the subset
leaves by decreasing |S|, and within a size in lexicographic order of member indices (the order
`combinations(range(k), m)` yields); then the four recovery leaves. Depths follow the existing
balanced layout (DEP-03): for M leaves with `2^(d-1) < M ≤ 2^d`, the first `2(M − 2^(d-1))` at
depth d and the rest at d-1. At k = 7 that is 131 leaves, depth 8, a 289-byte control block.

#### Phase 3: Reveal (CustodyLotteryReveal)

Once the confiscation transaction confirms, each participant publishes a `CustodyLotteryReveal`
event (Nostr Kind 9106) carrying their preimage, within `LOTTERY_REVEAL_CSV = 72` blocks of the
confiscation's confirmation (the reveal deadline). The signature on the reveal binds
`(ledger_id, preimage)` to the participant's identity.

#### Phase 4: Claim and Settlement (DisputeAcquire)

**Everyone revealed:** the winner is `Σ(LEN(preimage_i) − 16) mod k` over all participants in
canonical order; it spends the full-set leaf at once.

**Some withheld:** after the deadline, let R be the set of participants whose valid reveals
(hashing to their commitment) a recovery voter has observed. The winner is the
`(Σ_{i∈R} contribution_i) mod |R|`-th member of R. It builds the claim, and asks the recovery
voters (`lottery_subset_attest`, DEP-04) to sign its sighash for the R leaf. An honest voter
signs only if: the confiscation has `LOTTERY_REVEAL_CSV` confirmations; R is exactly the set of
participants whose valid reveals it has observed; the requester is R's winner; and the claim
pays as in this section (the lottery output to the winner's `target_reserves`, with the winner's
replacement collateral as the second input, DEP-03). Withholding never helps the withholder: it
is not in R and cannot win. Custody always goes to exactly one participant.

The winner then:

1. Broadcasts the claim TX
2. Appends `DisputeAcquire` to their fork carrying `claim_txid` (the claim TX's hash), `new_custodian`, and `new_reserves_address`
3. Establishes a new quorum on the ledger and begins co-signing updates as the new operator

Losers append `DisputeYield` to their forks, transitioning them to Tombstoned state. Only the winner's fork continues as the canonical ledger.

**Nobody revealed** (R empty at the deadline): no claim leaf is satisfiable. The recovery quorum
spends the lottery output through the CSV-144 recovery leaf (or a later tier if fewer sign) into
a **new lottery output for a fresh arm round** over the same ledger: a new `DisputeArmed` round
under the DEP-03 eligibility rule and its re-arm bound, after which the same claim rules apply.
Honest voters MUST NOT sign a recovery spend that pays the accused operator, or that pays any
destination other than the re-arm round's lottery output; such a spend is an unauthorised spend
of disputed funds. *(Implementation status: neither implementation orchestrates the re-arm round
yet; both refuse to sign any other recovery spend, so the output waits.)*

**Influence and bias.**
- *Last revealer:* a participant can still choose between revealing (draw over R) and withholding
  (draw over R without it), one bit of influence per withholder; it can never steer the draw to
  itself by withholding. A withholder that privately shares its preimage with a partner gives the
  partner the same one bit (the full-set leaf, or the attested R), not a choice of subsets: the
  voter attestation pins R.
- *Late reveals:* a reveal published after voters attested R also enables the full-set leaf, so the
  R winner and the full-set winner may race; the R winner should broadcast as soon as it has the
  attestations.
- *Modulo bias:* a uniform contribution over 1..60 is exactly uniform mod m for every m ∈ 1..6
  (60 = lcm(1..6)). For m = 7, residues 1–4 occur with probability 9/60 and 5, 6, 0 with 8/60, so a
  participant's chance is between 13.3% and 15.0% rather than 14.3%. A wider range would need
  preimages beyond the 80-byte standard stack item.

#### Pre-release policy cap

`MAX_LOTTERY_PARTICIPANTS = 7`, matching `VALID_QUORUM_SIZES = {3, 5, 7}` and
`MAX_QUORUM_SIZE_POLICY = 7` (`Q` excludes the operator, who cannot dispute its own ledger, so
participants ≤ Q). The subset tree has `2^k − 1` claim leaves, which bounds k: raising the cap
needs a different claim construction, not a constant change.

#### Respectful vs Punitive

**Respectful** (unavailability without proven fraud, `QuorumExpired`):
- Only the amount covering the ledger's obligations goes to the winner
- Change (including collateral) is returned to the original operator's pubkey
- Past `quorum_expiry`, this path races against the operator's own
  re-establishment under the same lifecycle tiers — see §Race below
  and DEP-05 §Lifecycle. The recovery-quorum cosignature threshold
  for the confiscation TX cascades through the same tiers, so a
  minority of cosigners can drive a respectful confiscation at
  Tier 1, a single cosigner at Tier 2.

**Punitive** (proven non-conformance):
- The amount covering the ledger's obligations goes to the lottery output (the winner inherits those obligations against that backing)
- The remainder (excess reserves + full collateral) is split equally across the **armers** (DisputeArmed participants), one per-armer slashing-share output. Non-armers get no slice — arming is the gate to a share, revealing is the gate to keeping it (see §"Arm-and-reveal forfeiture" below).
- If the operator runs multiple ledgers, proof of non-conformance on one ledger can be presented to the other ledgers' quorums, triggering slashing there as well
- Punitive disputes operate at strict majority in Tier 0. Past
  `quorum_expiry`, a valid punitive proof MAY be executed by whichever
  subset the current tier admits (minority at Tier 1, single member at
  Tier 2) using the punitive transaction shape. The proof is verifiable
  by anyone, so a smaller signer set does not weaken it; what the tiers
  gate is authority to spend, not the classification. A tier-path
  spend with punitive shape and no valid proof is itself an
  unauthorised vault spend (list item 7, wire type 10). Without this, a majority
  that is complicit or absent converts every punitive outcome into a
  respectful one by waiting.

##### Arm-and-reveal forfeiture

Each armer's slashing-share output is a P2TR with two tapscript leaves:

- **Reveal-claim** (`OP_HASH160 <commitment_hash> OP_EQUALVERIFY <armer_xonly> OP_CHECKSIG`): the armer spends by revealing the same preimage they committed to in their `DisputeArmed` plus a Schnorr signature. Spending this leaf publishes the preimage on-chain — if the armer somehow missed the Nostr reveal window, the on-chain spend doubles as a reveal that other observers can use.

- **Sweep** (`<ARMER_SHARE_SWEEP_CSV_BLOCKS> OP_CSV OP_DROP` + recovery-voter threshold CHECKSIGADD pattern): after `ARMER_SHARE_SWEEP_CSV_BLOCKS = 144` blocks (~1 day, matching the lottery's recovery long-tail floor), the recovery quorum (= quorum minus original operator) can sweep the slice as forfeited.

The internal key is the standard NUMS point so the key path is unspendable. The recovery_voters set for the sweep leaf matches the main lottery's recovery_voters — same set, same threshold — so the two outputs' sweep semantics are in lockstep. An armer remains in the recovery set that can sweep their own slice, but the threshold requires cooperation from other cosigners, which a non-revealing armer is unlikely to get.

The "abort option" — armer arms (so the dispute proceeds and the confiscation TX names them in the per-armer outputs), then withholds their reveal — now carries a real cost: their slice falls to the sweep after the CSV expires. See `tapscript_reserves::build_armer_share_output` for the implementation and the `armer_*` tests in `lottery_script_execution.rs` for the witness paths.

##### Sweep recipients: pro-rata to revealers

The sweep leaf permits the recovery quorum to spend the slice; the leaf does NOT constrain where the funds go (tapscript has no general output-commitment opcode). The protocol-defined contract for honest sweepers is:

> **The sweep TX MUST pay the slice (less fee) pro-rata to the set of revealers, split into one P2TR output per revealer keyed by `armer.pubkey`.**

A *revealer* is an armer whose preimage appears in the lottery output's claim TX witness OR in a published `CustodyLotteryReveal` event before the sweep TX is constructed. Equivalently: an armer whose preimage appears in the full-set or a revealer-subset claim, or who signed a Kind 9106 reveal that the sweepers can verify against the on-chain `commitment_hash`. The set of revealers is derivable from public evidence (chain + relay) at sweep time; sweepers are expected to compute it deterministically and agree on the resulting recipient list before cosigning the sweep TX.

##### Sweep orchestration

The reference flow is `deposits-node recovery forfeit-sweep <ledger_id>`: the initiating recovery-quorum member rebuilds the armer set and recovery voters from the ledger's public history, locates the lottery claim TX on-chain, extracts the revealer set from its witness, identifies the share outputs that are both unspent and past `ARMER_SHARE_SWEEP_CSV_BLOCKS`, constructs the deterministic sweep TX per forfeited share, signs, and collects the remaining threshold cosignatures via a `forfeit_sweep_sign` peer request (DEP-04 §"Request Actions").

The cosigner's defense is determinism: before signing, each cosigner independently recomputes the expected sweep TX byte-for-byte from the request's claimed revealer set and fee, rebuilds the share output from its own local view of the armers, and recomputes the sighash. A sweep request that pays anyone other than the revealers — or mis-states the revealer set — cannot reproduce the bytes and is refused. Where the cosigner has independently observed the claim TX, it also cross-checks the claimed revealers against that witness directly.

Math for a single sweep:
```
slice_value = <per-armer share from the confiscation TX>
fee         = <sweep TX fee estimate>
per_revealer = (slice_value - fee) / N_revealers
dust         = (slice_value - fee) - (per_revealer * N_revealers)   // absorbed as additional fee
```
Order recipients by sorted `armer.pubkey` so the constructed TX is deterministic and reproducible by every honest signer.

Edge case — `N_revealers == 0`: no one revealed at all, so the lottery output itself goes to the
re-arm round (Phase 4). The share slices follow it: sweepers MUST pay them into the re-arm round's
lottery output, never to the accused operator. Until that round exists the slices stay unswept.

Honest-sweeper enforcement: a sweep TX whose outputs deviate from this pro-rata-to-revealers contract is publicly observable. Sweepers who construct a deviating TX are themselves cosigners of the same ledger, and the deviation is a form of provable misbehavior. A `MaliciousSweep` fraud-proof type may be added later; for now the contract is enforced by recovery-quorum honesty and the social/reputational cost of public deviation. This is no stronger an honesty assumption than the recovery-quorum already requires for the lottery's own recovery long-tail.

### Race: Re-establishment vs Confiscation

Past `quorum_expiry`, two paths compete for the same on-chain
reserves UTXO at every lifecycle tier (see DEP-05 §Lifecycle for the
full schedule):

- **Re-establishment** — the operator initiates a fresh `QuorumBegin`
  with whatever cosigners they can still reach, spending the reserves
  UTXO into a new vault. The off-chain cosignature threshold and the
  on-chain script-path threshold both come from the current tier.
- **Confiscation** — a sufficient quorum-member subset files a
  `QuorumExpired` dispute (respectful only — see §"Respectful vs
  Punitive" above), arms, and cosigns a confiscation TX. Same
  tier-keyed threshold on both layers.

Because both paths consume the same on-chain UTXO, the tiebreaker is
which spending transaction confirms on-chain first. The losing path's
TX, if broadcast at all, becomes a double-spend and is dropped from
mempools. Off-chain ledger state follows: the prevailing TX is either
the `new_outpoint` of a fresh `QuorumBegin` (re-establishment won) or
the input of a confiscation lottery output (confiscation won).
Wallets verifying ledger continuity reconcile against whichever
appears on-chain.

The cascade is not "first to act in a tier wins"; it is "first tier
opens, both options simultaneously become valid." At Tier 1
(`quorum_expiry + 720`), the operator and a minority of cosigners can
re-establish, AND a minority of cosigners can confiscate — the
on-chain UTXO contention resolves the race. The operator's incentive
to win is preserving reputation and other ledger commitments; the
cosigners' incentive to win is the slashing reward (punitive) or the
operator-fee takeover (respectful).

Tier 3 has no confiscation pair — only the operator can sign Tier 3
on-chain, so only re-establishment is available there. By the time
the chain tip reaches `quorum_expiry + 8064`, every cosigner-driven
path has been available for ~8 weeks; the choice is the operator's
reputation against the unconditional Tier-3 spend.

### Recovery

Wallets continue addressing the same ledger by its `ledger_id`, accepting only replies co-signed by the quorum. When co-signatures stop or fail verification, the wallet should:

1. Query the network for dispute events (Kind 9103) on the ledger
2. Replay ledger updates to identify the last valid sequence
3. Look for `DisputeAcquire` events to identify the new operator and the `claim_txid`
4. Wait for the lottery output's claim transaction to confirm on-chain and verify that the `DisputeAcquire`'s `claim_txid` matches a confirmed transaction that spends the expected lottery output (see DEP-03)
5. Verify the new operator's quorum and begin accepting their co-signed updates

Wallets must not accept post-dispute updates until the on-chain claim transaction is confirmed. The claim transaction's witness satisfies the lottery script's `(sum mod N)`-th-disputant rule, so Bitcoin itself proves the new custodian is the script-selected winner. This prevents an attacker from publishing fake `DisputeAcquire` events claiming custody before the lottery resolves.

## Related DEPs

- [DEP-02](DEP-02.md): Wire format (DisputeEnter, DisputeAcquire, DisputeYield, DisputeArmed fields)
- [DEP-03](DEP-03.md): On-chain transactions (lottery construction, respectful custody)
- [DEP-04](DEP-04.md): Peer messaging (Kind 9101 fraud proof, Kind 9103 dispute events)
- [DEP-05](DEP-05.md): Quorum and collateral (quorum members initiate disputes, collateral confiscation)
- [DEP-09](DEP-09.md): Transfers (nonce field used for proof embedding)
- [DEP-10](DEP-10.md): Payment channels (cosigned offers/invoices as evidence)
