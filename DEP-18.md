# dep-18: consensus updates and protocol versioning

## abstract

a consensus rule change — anything that alters what a cosigner must agree is a valid ledger update: state-machine semantics, conformance checks, or the fraud-proof evaluation that replays them — cannot simply be deployed to a live fleet. if one node enforces a new rule and another does not, they diverge; worse, a node enforcing a not-yet-active rule can deem an honest peer's cosignature non-conforming and emit the confiscation-triggering fraud proof of [dep-06](DEP-06.md), seizing reserves the moment the binary rolls out. this dep specifies how new consensus rules are introduced and activated safely, building on the per-ledger version already carried by `QuorumBegin.protocol_version`. the governing invariant: **a rule is evaluated only against the version a ledger's active quorum committed to, never the validating node's newest code.** rules change only when the quorum acts — but "the quorum acts" is broadened beyond the on-chain rotation so that an emergency op-rule fix does not require every ledger to move its reserves on-chain.

## motivation

the protocol already versions one class of consensus rule: the on-chain reserves tapscript cascade. each ledger records an `active_ruleset_name` set from its most recent `QuorumBegin.protocol_version` (required: a `QuorumBegin` without one, or naming an unregistered ruleset, is non-conforming), quorum members advertise the rulesets they can validate (`supported_rulesets`), and `quorum begin` refuses to rotate into a ruleset some member cannot validate (`ruleset::member_supports`). reserves reconstruction reads the ledger's own version, so a node running new code still reconstructs an old ledger under the rules that ledger was created with.

two gaps remain:

1. **ledger-operation conformance rules** (e.g. the `FeeExceedsAssessment` cap in [dep-07](DEP-07.md)) had no version gate — they were enforced unconditionally by whatever binary was running. that is unsafe, for the confiscation reason above.
2. **activation was welded to `QuorumBegin`.** a `QuorumBegin` establishes a reserves UTXO whose tapscript encodes the membership *and* the reserves cascade, so issuing one is an on-chain event. if every consensus change had to ride a `QuorumBegin`, pushing an emergency rule to the fleet would force every ledger to rotate its reserves on-chain at once — a transaction stampede and fee spike, and slow (rotation has its own ceremony). but most consensus changes (the fee cap, and ledger-semantics tweaks generally) touch **no on-chain state**; coupling them to the UTXO move is incidental, not necessary.

this dep closes both: it extends the per-ledger version to cover all version-gated rules, and it adds a lightweight, off-chain, cosigned activation path — `QuorumUpgrade` — for the rules that don't touch the chain.

## the per-ledger consensus version

every ledger has a single active consensus version:

- it is the `active_ruleset_name` on `LedgerState`;
- a `QuorumBegin` MUST name a registered ruleset; there is no default. (the pre-versioning `legacy` cascade and `cltv-offset-literal`, whose recovery tiers used absolute heights rather than `quorum_expiry + offset`, were removed from the registry on 2026-10-02.)
- it names a **ruleset** that defines *both* the on-chain reserves cascade (the tapscript tier factory) *and* the set of ledger-op conformance rules in force.

versions are **named, not ordered**. there is no epoch counter and no `>=` comparison. whether a given rule is active is a *property of the named ruleset*, looked up directly — "does this ledger's ruleset enforce the fee cap?" — exactly as the reserves cascade is looked up by name today. a node knows a finite, append-only registry of rulesets (`ruleset::all_supported_names`); it never invents one. rules that predate versioning (reserve-backing, the `FeeWindowNotElapsed` timing check) are intrinsic to every ruleset.

each ruleset declares a **reserves-cascade family** — the on-chain script shape it produces. two rulesets in the same family produce byte-identical reserves UTXOs and differ only in off-chain op rules. (`fee-cap-v3` is in the same family as `cltv-offset-v2`: same reserves script, plus the fee cap. `balance-commit-v4` is likewise in the `cltv-offset-v2` family: `fee-cap-v3`'s rules plus required balance commitments on balance-touching ops — see [dep-02](DEP-02.md) §Balance Commitments.)

## the registry

the registry is append-only. each entry names a reserves-cascade family and the rules it adds to the rules intrinsic to every ruleset.

| ruleset | family | rules beyond the intrinsic ones |
|---|---|---|
| `cltv-offset-v2` | `cltv-offset-v2` | none |
| `fee-cap-v3` | `cltv-offset-v2` | none since 2026-10 (its fee cap is now intrinsic, [dep-07](DEP-07.md)) |
| `balance-commit-v4` | `cltv-offset-v2` | `MissingBalanceCommitment` ([dep-02](DEP-02.md) §Balance Commitments) |
| `anchor-ladder-v5` | `cltv-offset-v2` | the rules listed under §anchor-ladder-v5 |
| `balance-anchor-v6` | `cltv-offset-v2` | `anchor-ladder-v5`'s rules plus `MissingBalanceCommitment` (§balance-anchor-v6) |

before this section existed, the pre-release registry was amended in place: the tier-1 minority (2026-10-02), and the rules of october 2026, which went in as rules of every ruleset. from 2026-10-29 the entries above are frozen. a change to what a named ruleset enforces is a new name.

### anchor-ladder-v5

`anchor-ladder-v5` keeps the `cltv-offset-v2` reserves script, so a ledger reaches it by `QuorumUpgrade` or `QuorumBegin`. it adds:

1. **signed header** ([dep-02](DEP-02.md) §Block height and hash): heights never decrease along the chain, and every update names a block (`HeightDecreases`, `MissingBlockHash`).
2. **born expired** ([dep-05](DEP-05.md) §Membership Duration): a `QuorumBegin` whose `quorum_expiry` is at or below its `block_height` is non-conforming.
3. **collateral floor** ([dep-05](DEP-05.md) §Collateral floor, `CollateralBelowFloor`).
4. **vault-spend proofs** ([dep-06](DEP-06.md) proof 10, its unanchored and lapsed forms, and §Spend challenge).

it does not include `balance-commit-v4`'s `MissingBalanceCommitment`. a ledger that moves from `balance-commit-v4` to `anchor-ladder-v5` stops requiring balance commitments; `balance-anchor-v6` combines the two.

### balance-anchor-v6

`balance-anchor-v6` is `anchor-ladder-v5`'s four rules plus `balance-commit-v4`'s `MissingBalanceCommitment` ([dep-02](DEP-02.md) §Balance Commitments), in the `cltv-offset-v2` family. a ledger on either of those rulesets loses no rule by moving to it, and can move by `QuorumUpgrade` or `QuorumBegin`. every rule it adds is judged as §which ruleset judges what says for the rule's origin.

### which ruleset judges what

- **rules on a `QuorumBegin`'s own quorum** (born expired, collateral floor) are those of the ruleset the `QuorumBegin` names. a `QuorumBegin` that names an earlier ruleset is never judged by them.
- **vault-spend rules** are those of the ruleset named by the `QuorumBegin` that created the vault being spent (its governing `QuorumBegin`). a spend of a vault created under a ruleset without them is not provable as `UnauthorizedVaultSpend` and opens no challenge. that is the dormant behaviour, and it can only excuse, never convict.
- **every other rule** is that of the ledger's active ruleset before the update: the ruleset of the last `QuorumBegin` or `QuorumUpgrade` before it, or the one its `LedgerOpen` names (`protocol_version`, [dep-02](DEP-02.md) type 286). a ledger whose `LedgerOpen` names none has no active ruleset before its first `QuorumBegin`, and gated rules are dormant there.

a `LedgerOpen`, `QuorumBegin` or `QuorumUpgrade` names its ruleset; nothing is inferred from an order, since there is none. the choice of name is the operator's policy (§operator policy); that every member of the quorum being seated declared the named ruleset is consensus (§version negotiation). vector: `ruleset_gating.txt`; the vault-spend twins are in `vault_spend_anchor.txt`.

### intrinsic changes of october 2026

these went in as rules of every ruleset and stay there. none can make history recorded before it non-conforming or provable:

- **they narrow what convicts:**
  - a dereliction proof binds to a disclosed, seen fraud (FINDINGS D1);
  - a confiscation is excused if it matches any rebuild, including any rung of its ladder;
  - an unlinked update is not itself fraud;
  - a `quorum_expired` dispute does not freeze cosigning, and ends on re-establishment;
  - a dispute's ground is read from its record;
  - a nonce need only be unique within its window ([dep-17](DEP-17.md)).
- **they apply only to operations or fields that did not exist before:**
  - [dep-20](DEP-20.md) exits, dormancy and migration;
  - `ObligationRecord` and proof 11 `UnhonouredObligation`;
  - `QuorumChallenge`;
  - `rotation_rungs`;
  - the offer cosign digest.
- **they were ruled intrinsic as security fixes:**
  - the fee cap ([dep-07](DEP-07.md), FINDINGS L6);
  - exit address types and dust floors (FINDINGS L5/L6/D3).
- **they predate october in both implementations:** `quorum_expiry` within the members' commitments ([dep-05](DEP-05.md) §Quorum expiry).
- **they are constructions and member policy, not judgments:**
  - the rotation and confiscation anchors and fee ladders, and their fees ([dep-03](DEP-03.md)), are built the same under every ruleset; only `anchor-ladder-v5`'s vault-spend rules judge them;
  - the lottery's shape and eligibility cut;
  - late cosignatures;
  - cosign refusal;
  - duplicate delivery;
  - descriptor validity ([dep-16](DEP-16.md) §descriptor validity), which grounds a refusal to cosign and never a conviction.

## two activation paths

a ledger's version changes only by a quorum-authorized, cosigned operation. there are two, distinguished by whether the change touches on-chain state:

### QuorumBegin (on-chain) — reserves-affecting changes

`QuorumBegin` establishes or rotates the quorum and its reserves UTXO. it carries `protocol_version` and is the **only** path that may move a ledger to a ruleset in a *different reserves-cascade family*, because the on-chain UTXO's tapscript must match the active cascade. routine membership rotations and any reserves-script change ride this path; it is inherently on-chain.

### QuorumUpgrade (off-chain) — op-rules-only changes

`QuorumUpgrade` is a new cosigned ledger operation that sets `active_ruleset_name` to a target ruleset **in the same reserves-cascade family** as the current one — i.e. a change to off-chain op-conformance rules only, with no reserves move and no membership change. it requires:

- the same quorum cosignature threshold as any consensus-affecting update (it *is* a quorum action — your invariant "rules don't change until the quorum says so" holds);
- every current member to support the target ruleset (`member_supports`), the same gate `QuorumBegin` applies;
- the target ruleset's reserves-cascade family to equal the current ruleset's. **a `QuorumUpgrade` whose target changes the reserves family MUST be rejected** — that requires `QuorumBegin`.

because it is an ordinary cosigned ledger update with no transaction, an emergency op-rule fix propagates across every ledger as fast as the cosigners can sign — zero mempool pressure, no on-chain stampede.

## lifecycle of a consensus change

1. **specify.** the rule lands in a dep and is assigned to a named ruleset.
2. **implement, dormant.** the code enforces the rule only when the ledger's active ruleset declares it. under any other ruleset the code path is byte-for-byte identical to pre-change behaviour. *shipping the binary changes nothing observable on existing ledgers.*
3. **advertise.** members that can validate the rule publish the new ruleset name in their signed `supported_rulesets` (surfaced in the operator's kind 39100).
4. **activate, per-ledger.** the operator issues a `QuorumUpgrade` (op-rules-only change) or, if the reserves cascade also changes, folds the version bump into the next `QuorumBegin`. either way the cosig threshold + `member_supports` gate applies. from that operation's sequence forward, the rule is active for that ledger.
5. **no flag-day.** ledgers that have not been upgraded keep their prior ruleset and prior rules until their own `QuorumUpgrade`/`QuorumBegin`. the fleet upgrades ledger by ledger.

## confiscation-safety invariant (normative)

this is the property that makes deploying ahead of activation safe.

- conformance evaluation and **all** fraud-proof replay MUST be performed against the ruleset the ledger's active quorum committed to at the relevant sequence — read from `active_ruleset_name` in the replayed state — and MUST NOT use the validating node's newest ruleset.
- a node MUST NOT emit, accept, relay, or act upon a `NonConformingCosignature` (or any other confiscation-triggering fraud proof, per [dep-06](DEP-06.md)) whose only basis is a rule not active under the governing ruleset of the cosigned operation.
- a cosignature is fraudulent only if it blesses an operation non-conforming **under the rules in force for that ledger at that sequence**. a rule introduced in ruleset R can never make an operation cosigned under a ruleset that lacks it retroactively fraudulent.

corollary: deploying a binary that knows a new ruleset is always safe regardless of which ledgers have upgraded. it cannot retroactively fault pre-upgrade history, and it cannot fault peers still running the older binary on not-yet-upgraded ledgers.

## version negotiation and refusal

- **per-ledger (consensus).** the operator selects, at `QuorumUpgrade` or `QuorumBegin`, a ruleset that every member's `supported_rulesets` covers. which covered ruleset to choose is the operator's policy (§operator policy); the choice is not consensus, coverage is. a `QuorumBegin` or `QuorumUpgrade` that seats or keeps a member whose `supported_rulesets` does not contain the named ruleset is non-conforming, and every cosigner refuses it. vector: `ruleset_naming.txt`. a `QuorumBegin`'s ruleset MUST be the one its new reserves output was constructed under, and cosigners verify the reserves script against it (DEP-03); a rotation does not inherit the previous ruleset. a member that cannot validate the target blocks the change — `member_supports` returning false is a hard stop, not a warning, because a quorum that cannot uniformly validate its own rules cannot safely cosign.
- **advertising is a promise.** a node MUST NOT list in `supported_rulesets` a ruleset whose cascade it cannot build and whose op rules it does not enforce. advertising a ruleset it does not enforce lets a quorum activate rules that member will cosign blindly.
- **per-peer (transport).** the wire handshake's `protocol_version` / `min_protocol_version` (`messages::constants`) governs whether two nodes will talk at all. this is independent of the per-ledger consensus version: a node may speak the latest wire protocol while operating ledgers pinned to an older ruleset.

## operator policy

which ruleset an operator names is not consensus. the reference policy, which both implementations follow:

1. **name `balance-anchor-v6`** when every member of the quorum being seated declares it. it carries every rule of `balance-commit-v4` and of `anchor-ladder-v5`, so no ledger loses one by moving. a new ledger's `LedgerOpen` names it.
2. **otherwise keep what protects more.** an operator whose ledger is on `balance-commit-v4` names `balance-commit-v4` again, and never proposes a `QuorumUpgrade` away from it except to `balance-anchor-v6`: `anchor-ladder-v5` lacks `MissingBalanceCommitment`, so moving there would silently drop a rule the depositors had.
3. **otherwise move to `anchor-ladder-v5`** when every member declares it, and keep the current ruleset when one does not.
4. all four registered rulesets past `cltv-offset-v2` share its family, so every move above is available to a `QuorumUpgrade` as well as a `QuorumBegin`; the policy, not the family, decides which. vector: the `plan` cases of `ruleset_naming.txt`.

## downgrade, stall, and emergency paths

- there is no forced upgrade. an operator whose members cannot all support a new ruleset simply keeps its current one and forgoes the new rule; the ledger remains fully operable.
- **emergency op-rule fix:** the operator issues a `QuorumUpgrade` to the patched ruleset on every affected ledger. no transactions, no rotation ceremony, no mempool contention — the bound is cosigner round-trips.
- **emergency reserves-cascade fix** (rare): genuinely requires `QuorumBegin` per ledger, because the on-chain UTXO must change. this is the only case that touches the chain, and it is unavoidable when the fix *is* about on-chain script.
- self-rescue and dispute resolution ([dep-06](DEP-06.md)) evaluate each disputed operation against the ruleset active at that operation's sequence. an upgrade in flight never changes the rules applied to operations already committed under the prior ruleset.

## worked example: the dep-07 fee-assessment cap

- the **operator-side** cap in `calculate_fees_due` (`assessed_blocks = min(blocks_elapsed, frequency_blocks)`) is safe to deploy immediately and unconditionally. it only ever makes the operator collect *less*, which is conforming under every ruleset, including `legacy`.
- *(superseded: `FeeExceedsAssessment` is now a rule of every ruleset, dep-07; the history below is kept as the example of the mechanism.)*
- the **consensus rule** `FeeExceedsAssessment` — cosigners rejecting a `FeeCollect` whose `amount` exceeds the one-period assessment — is part of ruleset **`fee-cap-v3`**, which shares the `cltv-offset-v2` reserves-cascade family (no on-chain change). it activates per-ledger via **`QuorumUpgrade`**. until a ledger is upgraded to `fee-cap-v3`:
  - cosigners do **not** enforce the amount cap (they still enforce the pre-versioning `FeeWindowNotElapsed` timing check), and
  - an over-cap `FeeCollect` is **not** a confiscation basis.
- after the `QuorumUpgrade`, the cap is a hard conformance rule and an over-cap `FeeCollect`, if cosigned, is a valid `NonConformingCosignature` for that ledger.
- the genesis-baseline stamping for `last_fee_assessment` (dep-07) is likewise part of `fee-cap-v3` where it changes a conformance input; it ships dormant and activates with the same `QuorumUpgrade`.

because `fee-cap-v3` shares `cltv-offset-v2`'s reserves family, the fleet can adopt it with a sweep of cheap `QuorumUpgrade` operations — no reserves rotation, even though it is a consensus change.

## second example: dep-02 balance commitments

`balance-commit-v4` follows the same split ([dep-02](DEP-02.md) §Balance Commitments):

- the **verify-when-present** rule (`BalanceCommitmentMismatch` — declared post-op balances must equal the replayed state) is intrinsic to every ruleset. this is safe unconditionally: the commitment fields are odd TLV tags that no pre-commitment update carries, so no historical update can retroactively fault, and an operator only ever opts in by emitting the fields.
- the **require-presence** rule (`MissingBalanceCommitment` — every balance-touching op must carry its commitment pair) is part of ruleset **`balance-commit-v4`** and activates per-ledger via `QuorumUpgrade` or `QuorumBegin.protocol_version`. until then, commitment-less operations remain conforming.
- operator-side population of the fields is safe to deploy immediately (like the operator-side fee cap): emitting a *correct* commitment is conforming under every ruleset, and cosigners running older code skip the odd tags entirely.

## related deps

- [dep-05](DEP-05.md): quorum formation and rotation; member `supported_rulesets` and join-time minimums.
- [dep-06](DEP-06.md): disputes, fraud proofs, and confiscation — the cascade this dep keeps from misfiring during an upgrade.
- [dep-07](DEP-07.md): the fee-assessment cap, the first ledger-op conformance rule to use this process.
- [dep-16](DEP-16.md) / [dep-17](DEP-17.md): descriptor evaluation and the canonical encodings whose bit-for-bit determinism the per-ruleset fraud-proof replay depends on.
