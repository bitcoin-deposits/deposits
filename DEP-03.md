# DEP-03: On-Chain Transactions

## Abstract

This document specifies the on-chain transaction formats used by Bitcoin Deposits: the reserves UTXO structure, tapscript multisig construction for quorum spending, reserves rotation transactions, and the lottery mechanism for contested custody transfers.

## Reserves UTXO

A ledger's funds are held in a single UTXO containing both reserves and collateral. The reserves portion (deposit capacity) must be greater than or equal to the ledger's total obligations. The collateral portion is the operator's security bond. The UTXO is spendable by tiered script paths — quorum members first, operator later, with increasing timelocks.

## Tapscript Construction

The reserves UTXO uses a Taproot output with a tapscript tree containing tiered spending paths. The internal key is an unspendable point (no key-path spend). All spending goes through script-path reveals.

### Spending Tiers

Each tier (other than the immediate quorum-majority path) is gated by an
absolute `OP_CLTV` timelock anchored to the ledger's recorded
`quorum_expiry`. The post-expiry cascade only opens once the quorum's
declared lifetime has elapsed; during the active period the only
on-chain spend path is the quorum-majority tier, which is what the
routine rotation TX uses. This means:

- The on-chain script's protection does **not** decay with UTXO age —
  it decays with `quorum_expiry`. Refreshing `quorum_expiry` (via a
  rotation that emits a new `QuorumBegin`) re-pins all post-expiry
  tiers to the new deadline.
- An operator who fails to rotate before `quorum_expiry` loses
  exclusive spending control on a fixed schedule, with the quorum
  members' recovery paths opening earlier than the operator's own.
- The operator's solo path is the absolute last resort, opening only
  after every quorum-driven path has had time to act.

For a quorum of n voters (the operator and its members, as the tapscript
counts them):

| Tier | Signers | Timelock | Purpose |
|---|---|---|---|
| 0 | Majority of quorum (no operator) | None — anytime | Normal operations: rotation, co-signed settlements |
| 1 | Minority of quorum, `ceil(n/2) - 1` signers (the complement of Tier 0's `floor(n/2) + 1`) | `quorum_expiry + 720` blocks (~5 days) | Degraded quorum recovery when members disappear |
| 2 | Single quorum member (no operator) | `quorum_expiry + 4032` blocks (~4 weeks) | Recovery when only one member remains active |
| 3 | Operator only | `quorum_expiry + 8064` blocks (~8 weeks) | Operator solo, last resort after all quorum paths failed |

The operator is deliberately excluded from Tiers 0–2 and only gets
Tier 3 after every quorum-driven path has been available for weeks.
Routine rotation flows through Tier 0 and so has no timelock — the
quorum-majority cosigns each rotation TX while the current quorum is
still active.

This on-chain tier schedule is mirrored off-chain by the cosignature
threshold for *establishment operations* (`QuorumAddMember`,
`QuorumRemoveMember`, `QuorumBegin`) — see DEP-05 §Lifecycle for the
full event table. The two layers share the same anchor and offsets, so
authority at the chain tip is identical whether you read it from the
tapscript leaves or from the off-chain cosign rule. Non-establishment
operations remain strictly Tier-0 cosignable and become uncosignable
past `quorum_expiry` until a fresh `QuorumBegin` resets the schedule.

For the simple 2-party case (n ≤ 2), the minority and single-member
tiers collapse (in a 2-of-2 quorum, one member IS both), so the
cascade is:

| Tier | Signers | Timelock |
|---|---|---|
| 0 | Both quorum members | None — anytime |
| 1 | Single quorum member | `quorum_expiry + 720` blocks (~5 days) |
| 2 | Operator only | `quorum_expiry + 8064` blocks (~8 weeks) |

Block heights are absolute, encoded as `OP_CLTV` (BIP-65) against
`nLockTime`. Spending a non-zero-tier path requires the spending TX
to set `nLockTime ≥ quorum_expiry + offset`.

## QuorumBegin (disc 12)

When a quorum is established or refreshed, the operator constructs a new Taproot output and broadcasts a transaction spending the old reserves to the new address. The `QuorumBegin` operation records:

- **reserves_id**: the new Taproot address
- **reserves_amount**: the reserves portion of the UTXO (deposit capacity, msats)
- **collateral_amount**: the collateral portion of the UTXO (security bond, msats)
- **spending_txid**: the txid spending the old reserves
- **new_outpoint_txid**: the txid of the new reserves output
- **new_outpoint_vout**: the vout index
- **quorum_members**: the pubkeys included in the new multisig. MUST match the set of members staged via prior `QuorumAddMember` operations (and not since removed by `QuorumRemoveMember`) — `QuorumBegin` promotes exactly that staged set to the new active quorum (see DEP-05 §QuorumBegin).
- **quorum_member_ledger_ids**: parallel array to `quorum_members` carrying each member's own ledger_id (the ledger holding their collateral, sourced from the matching `QuorumAddMember.member_ledger_id`). Lets fraud-proof verifiers and explorers identify the ledger backing each cosigner's `member_ledger_hash` without re-deriving the mapping from prior `QuorumAddMember` history. Older `QuorumBegin` events omit this field; consumers fall back to walking `QuorumAddMember` operations on the operator's ledger.
- **quorum_expiry**: block height when the quorum expires (shortest member commitment)
- **exit_cutoff_height**, **exit_outputs**, **splice_in_outpoint** / **splice_in_amount_msats**, **migration_manifest** / **migration_receiver** / **migration_vout**: settlement fields under DEP-20 (wire tags in DEP-02 §Ledger). Cosigners verify each exit and migration output against the recording update and the due-request set, and the splice input against the chain.

The on-chain UTXO value MUST equal `reserves_amount + collateral_amount`. A rotation MAY carry exit outputs and a splice-in input (DEP-20 §3–4); the new vault's value is then `old vault + splice_in − Σ exits − fee`, with `reserves_amount` reduced by `Σ exits` and obligations reduced by the same amount in the recording update. Cosigners MUST verify, against their own chain source, that the referenced outpoint (`new_outpoint_txid`, `new_outpoint_vout`):

1. exists on-chain,
2. is unspent,
3. carries a value (in sats) equal to `(reserves_amount + collateral_amount) / 1000`,
4. has at least a network-dependent minimum number of confirmations.

The per-network default confirmation thresholds used by an honest cosigner with no explicit override are: 6 for mainnet, 3 for testnet/signet, 1 for regtest. These are policy (not consensus) — a stricter cosigner is free to refuse a request a laxer cosigner would accept. A cosigner receiving a first `QuorumBegin` that fails any of the checks above MUST refuse to sign and MAY emit a diagnostic error; the operator's cosign collector then waits for another responder or times out.

After `QuorumBegin`, co-signatures become required for all subsequent updates. The *first* `QuorumBegin` itself must also carry cosignatures — see DEP-05 §QuorumBegin and DEP-02 §Cosignatures. A new `QuorumBegin` MUST be appended before `quorum_expiry` (see DEP-11).

### On-Chain State Anchor

The reserves rotation transaction should include an `OP_RETURN` output containing the `chain_hash` at the `QuorumBegin` sequence. This gives wallets an on-chain anchor to verify that the ledger state on relays matches the operator's committed state at the time of rotation — without trusting any relay. The `OP_RETURN` output is:

    OP_RETURN <chain_hash (32 bytes)>

This is cheap (one additional output on a transaction the operator is already making) and provides a verifiable checkpoint for wallets that suspect relay censorship or data loss.

## Custody Lottery

When a ledger becomes contested (dispute), the eligible armers compete for custody via an on-chain
Tapscript lottery. Selection is enforced by Bitcoin script: only the drawn participant's signature
satisfies a claim leaf. Off-chain agreement on the outcome is not required, except that a draw over
fewer than all participants (some withheld their reveal) needs the recovery voters to attest which
participants revealed. The full construction is DEP-06 §Lottery; this section summarises it.

### Flow

1. Each disputing member publishes `DisputeArmed` with `commitment_hash = HASH160(preimage)`, where
   `preimage` is 17 to 76 bytes; `contribution = LEN(preimage) − 16` lies in `1..=60`.
2. After the eligibility cut (§"Replacement collateral declaration"), the recovery quorum cosigns a
   confiscation transaction spending the disputed reserves UTXO into the **lottery output**, built
   for the k eligible participants.
3. Each participant publishes its preimage (`CustodyLotteryReveal`, Kind 9106) within 72 blocks of
   the confiscation's confirmation.
4. If all revealed, the winner `(Σ contribution) mod k` claims through the full-set leaf. Otherwise,
   after 72 blocks, the winner over the revealers R, `(Σ_{R} contribution) mod |R|`, claims through
   R's subset leaf with the recovery voters' attestation.
5. The winner appends `DisputeAcquire { new_custodian, claim_txid, new_reserves_address }` to their
   fork. Losers append `DisputeYield`.

### Lottery Output Tapscript Tree

- **Full-set leaf**: all k preimages, `sum mod k` dispatch, no timelock.
- **Revealer-subset leaves**: one per nonempty proper subset (`2^k − 2`), CSV 72, a threshold of
  recovery-voter signatures attesting the subset, then that subset's preimages and `sum mod |S|`
  dispatch.
- **Long-tail recovery cascade** at CSV 144 / 1008 / 4032 with thresholds T / T-1 / T-2, and the
  **timeout-recovery escape hatch** at CSV 8064 with threshold 1. Honest voters spend these only into
  a re-arm round's lottery output (DEP-06 Phase 4), never to the accused operator.
- A sole eligible participant (k = 1) gets a plain signature leaf in place of the claim leaves.

Each preimage check enforces `17 ≤ LEN ≤ 76` (`OP_SIZE OP_DUP <17> OP_GREATERTHANOREQUAL OP_VERIFY
OP_DUP <76> OP_LESSTHANOREQUAL OP_VERIFY` after the hash check), so a committer who hashed an
out-of-range preimage can only fail its own reveal, never shift the draw. The leaf order, scripts and
depths are specified in DEP-06 Phase 2. The internal key is the BIP-341 NUMS point.

### Witness Construction

Full-set leaf: `[signature, preimage_{k-1}, …, preimage_0, leaf_script, control_block]`, signature
at the bottom.

Subset leaf for S = (s_0 … s_{m-1}): `[signature, preimage_{s_{m-1}}, …, preimage_{s_0},
voter_sig_{r-1}, …, voter_sig_0, leaf_script, control_block]` with empty pushes for absent voter
signatures, and the spending input's `nSequence ≥ 72`.

Recovery leaves: `K` of `N` signature slots filled (empty pushes for the rest), `nSequence ≥ csv`.

### Pre-release policy cap

At most `MAX_LOTTERY_PARTICIPANTS = 7` participants (`VALID_QUORUM_SIZES = {3, 5, 7}`, `Q` excludes
the operator, who cannot dispute its own ledger). The subset tree has `2^k − 1` claim leaves, so a
larger cap needs a different claim construction.

### Fraud-proof classification: Respectful vs Punitive

Every dispute is initiated by a fraud proof — quorum members don't dispute on
"vibes." The proof's *type* determines whether the dispute is respectful or
punitive, which in turn shapes both the confiscation tx and cross-ledger
propagation:

| Fraud proof type      | Class       | Trigger condition                                                                  |
|-----------------------|-------------|------------------------------------------------------------------------------------|
| `QuorumExpired`       | Respectful  | Operator failed to rotate before `quorum_expiry`                                   |
| `UncreditedOnchainPayment` | Punitive   | Operator received on-chain payment, didn't credit despite signing past confs       |
| `UncreditedLightningPayment` | Punitive | Operator received Lightning payment, didn't credit despite preimage release        |
| `StaleCosignature`    | Punitive    | Cosigner backdated their `member_ledger_hash` (signed against an outdated state)   |
| `DisputeDereliction`  | Punitive    | Cosigner was online but failed to act on a prior fraud proof within the window     |
| `NonConformingUpdate` | Punitive    | Operator signed a ledger update that violates protocol rules                       |
| `WinnerCollateralDeviation` | Punitive | Lottery winner's broadcast claim TX deviates from their `DisputeArmed` collateral declaration (missing input, smaller commit, or extra drain) |

Punitive shape is available at every tier once a valid punitive proof exists (DEP-06 §Respectful vs Punitive); the tiers gate who may spend, not which shape they may build.

### Respectful custody (QuorumExpired only)

When the operator fails to rotate before `quorum_expiry`, respectful
custody transfer becomes available — but it now races against the
operator's own re-establishment path under the same lifecycle tiers
(see DEP-05 §Lifecycle and DEP-06 §"Race: Re-establishment vs
Confiscation"). If the operator self-rescues first with a degraded
`QuorumBegin`, no custody transfer occurs.

- The fraud proof is `QuorumExpired`. Evidence is just an anchor block hash
  whose height in the verifier's chain exceeds the ledger's `quorum_expiry`.
- Cosigners enforce the deadline at the cosign edge: past `quorum_expiry`,
  they refuse to cosign *value-moving* operations. They WILL still cosign
  *establishment* operations (`QuorumAddMember`, `QuorumRemoveMember`,
  `QuorumBegin`) at the threshold required for the current lifecycle
  tier — see DEP-05 §Lifecycle. Missing `quorum_expiry` is therefore
  not fatal; it opens both the confiscation path (this section) and
  the operator's degraded re-establishment path concurrently.
- Confiscation tx is bifurcated:
  - `obligations` worth of reserves → lottery winner
  - `(reserves − obligations) + full collateral` → operator's pubkey (change)
- The fraud proof does **not** propagate cross-ledger. Other ledgers the
  operator runs are unaffected.

### Punitive custody (proven non-conformance)

When proof of provable misbehaviour is presented:

- The full UTXO (reserves + collateral) goes to the confiscation tx.
  - `obligations` worth of reserves → lottery winner (becomes the new
    backing for inherited deposits).
  - The remainder, `(reserves − obligations) + collateral`, is split equally
    among the `Q` cosigners. **The lottery winner does not retain the
    confiscated collateral as a windfall** — they receive their per-cosigner
    share alongside everyone else, evenly aligning incentives across the
    quorum.
- The lottery winner takes over the ledger, inheriting deposit obligations
  and the lottery output.
- **The winner provides replacement collateral** as a fresh input when
  claiming the lottery output. The replacement amount + the inherited
  `obligations` reserves form the new operating UTXO. Operating a ledger
  is a service commitment, not a windfall; the winner pays the cost of
  fresh collateral to take the role.
- The same fraud proof can be presented to the operator's *other* quorums,
  triggering punitive disputes there as well. Cross-ledger contagion is
  the protocol's mechanism for ensuring an operator with multiple ledgers
  can't insulate one from misbehaviour on another.

### Replacement collateral declaration

Operating a ledger requires backing reserves with a collateral ratio `r`
(see DEP-05). The lottery output by itself only covers the inherited
`obligations` — it does not carry the collateral-ratio padding. To take
custody, the winner must commit *fresh collateral* alongside the lottery
output when constructing the claim transaction.

For both respectful and punitive disputes, every disputant MUST declare
in `DisputeArmed` a **replacement collateral UTXO** they would commit if
they win:

- `replacement_collateral_outpoint`: txid + vout of an unspent UTXO they
  control
- `replacement_collateral_amount`: the value (in sats) they pledge to the
  new vault from that UTXO

Which armers take part in the lottery (and, in a punitive dispute, receive a slashing share) is a
deterministic function of the ledger and the confirmed chain, so every cosigner computes the same
set and no single declaration can stall the dispute.

**Eligibility snapshot.** For each armer take its latest `DisputeArmed` (highest sequence on its
fork; a re-arm replaces the declaration). Let `E` be the highest signed-header `block_height` among
those updates. Under v2 signing the header's `block_hash` binds that height to a real block, so an
armer cannot place E in the future; backdating its own arm lowers E only if it is the latest armer,
and an honest armer's pledge, confirmed before it arms, is still created at or below E.
An armer is a **participant** iff all of:

1. `replacement_collateral_amount ≥ obligations × collateral_ratio + claim_fee_floor`, where
   `obligations` is the total deposit value owed at `last_valid_sequence` (the lottery output
   covers exactly this amount, so only the ratio padding and fee come from the replacement);
2. the outpoint was confirmed in a block at height ≤ E;
3. the outpoint was unspent as of the end of block E (spent in a block > E, or not at all); and
4. its value is ≥ `replacement_collateral_amount`.

Only the confirmed chain counts: mempool state is never consulted, so the verdict is stable once
E is buried, including after the winner spends its pledge into the claim. `claim_fee_floor` is
`reference_feerate_sat_vb` from the governing `QuorumBegin` (DEP-20 §8) × 200 vB, the multi-input
claim's size, or 5,000 sats when no feerate is recorded. It is a rule, not a policy, because cosigners must
agree on it.

An armer that is not a participant is excluded: it is not in the lottery script, receives no
slashing share, and counts as a non-arming member for the recovery quorum (it may cosign the
confiscation). Cosigners MUST refuse a confiscation whose participant set differs from the one
this rule yields, and MUST NOT refuse one because an armer was excluded.

**When the set is final.** The rule is deterministic over the arms a member has seen, but arms
travel by relay: an arm whose header height is at or below the current E can reach one member
before another and join the set without moving E. Two members may therefore compute different
sets for a while; each refuses the other's proposal (its sighash differs), and they converge as
the relay delivers the remaining arms. The set is **final once a confiscation confirms**: it is
exactly the set whose lottery output the confiscation pays, and arms seen afterwards do not change
it. Every later step (reveal, claim, attestation, armer shares, sweeps) uses that set, recovered
from the confirmed output (members try their current cut first, then the subsets of all armers).

**One participant** takes custody without a draw: the lottery's primary leaf is
`<participant_xonly> OP_CHECKSIG` (no preimage is revealed; the recovery leaves are unchanged).
A floor of two would hand the veto back to a colluder: one honest armer plus one colluder with a
spent pledge would stall. A sole participant is safe because the recovery quorum still cosigns
the confiscation against the proof.

**No participant**: no confiscation is built. An armer whose pledge fails the cut MAY re-arm with a
fresh one (same commitment); its latest arm counts and moves E, which reopens the window. Only an
armer's first four `DisputeArmed` (the arm and three re-arms) count, so no one can keep moving E.
If every armer has exhausted its arms and none is a participant, the dispute does not confiscate:
custody of the vault falls to its post-expiry tiers (DEP-05 §Lifecycle), as for a quorum that
never disputed.

A participant whose pledge is spent after E, or who otherwise deviates from its declaration when
claiming, is caught at claim time as a `WinnerCollateralDeviation` (below and DEP-06), not here.

### Claim transaction (multi-input)

The winner's claim TX has two inputs and one output:

- **Input 0**: lottery output (script-path spend through the full-set or a
  revealer-subset leaf — see §"Witness Construction")
- **Input 1**: the disputant's declared replacement collateral UTXO,
  signed natively for whatever script controls it (typically wpkh from
  the disputant's wallet)
- **Output 0**: the new reserves vault at the winner's `target_reserves`
  address, valued at `(input_sum − fee)`

If the winner broadcasts a claim TX whose shape deviates from their
declared commitment — single-input (skipping the replacement), pointing
at a different replacement UTXO, committing a smaller amount than
declared, or adding change outputs that drain replacement value — the
deviation is observable on-chain by comparing the broadcast TX against
the stored `DisputeArmed`. This deviation is a `WinnerCollateralDeviation`
fraud proof: punitive, attributed to the winner's new operator pubkey on
whatever ledger they're operating after takeover. Cross-ledger contagion
applies as for any other punitive proof.

Because Bitcoin script can't gate cross-input requirements atomically,
the constraint is enforced at two edges: cosigner-attested arm-time
verification (refuse to sign confiscation if the declaration is
insufficient) and after-the-fact fraud proof (slash the winner if they
broadcast a non-conforming claim).

## Related DEPs

- [DEP-02](DEP-02.md): Wire format (QuorumBegin, DisputeAcquire, DisputeYield, DisputeArmed fields)
- [DEP-05](DEP-05.md): Quorum membership determines multisig participants
- [DEP-06](DEP-06.md): Dispute lifecycle triggers the lottery
