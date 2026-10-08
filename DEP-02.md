# DEP-02: Ledger State Model

## Abstract

This document specifies the wire format, hash chain structure, and signing protocol for Bitcoin Deposits ledger updates. A ledger is an append-only chain of signed updates, cooperatively maintained by an operator and a quorum of co-signing members.

## Notation

- All multi-byte integers are big-endian unless stated otherwise
- `||` denotes concatenation
- `SHA256()` is the SHA-256 hash function
- `[N]` denotes a fixed-length byte array of N bytes
- Amounts are in millisatoshis unless stated otherwise

## TLV Encoding

All structures use Type-Length-Value encoding with BigSize varints, compatible with the Lightning Network TLV format (BOLT #1).

### BigSize

| Value Range | Encoding |
|---|---|
| 0x00..0xfc | 1 byte |
| 0xfd..0xffff | 0xfd followed by 2 bytes |
| 0x10000..0xffffffff | 0xfe followed by 4 bytes |
| 0x100000000..0xffffffffffffffff | 0xff followed by 8 bytes |

### TLV Record

    [BigSize: type] [BigSize: length] [length bytes: value]

Records are ordered by type number. All current field types are even. Odd types are reserved for future forward-compatible extensions that unknown implementations may safely ignore.

## Signed Ledger Update

The event content is a base64-encoded TLV stream:

| Type | Name | Size | Description |
|---|---|---|---|
| 0 | operator_id | 33 | Operator's compressed secp256k1 pubkey |
| 2 | ledger_id | 32 | Ledger identifier hash |
| 4 | sequence_number | 8 | Monotonically increasing sequence (u64 BE) |
| 6 | previous_hash | 32 | Chain hash of the previous update |
| 8 | message | variable | Inner operation (TLV-encoded) |
| 10 | block_height | 4 | Block height at creation (omitted when 0) |
| 12 | block_hash | 32 | Block hash at creation (omitted when all zero) |
| 20 | operator_signature | 64 | Schnorr signature from operator |
| 22 | cosignatures | variable | Majority cosignature list (see Cosignatures below) |

`current_hash` is derived by the receiver (see Hash Chain).

Every field except the signatures is signed (see Signing): `ledger_id`, `block_height` and
`block_hash` are part of `cosign_data`, so no one can move an update to another ledger or
another height without invalidating its signatures. An absent `block_height` or `block_hash` is
signed and hashed as zero; encoders MUST omit a zero value and decoders MUST reject an explicit
zero, so that every update has exactly one encoding. Types 14, 16 and 18 (the pre-majority
single-cosignature format) are retired; decoders MUST reject them.

### Cosignatures (Tag 22)

Tag 22 contains one or more cosignature entries concatenated as length-prefixed records. Each entry is:

    [u16 BE: entry_length] [entry_length bytes: cosig_entry]

Each `cosig_entry` is:

| Offset | Size | Field |
|---|---|---|
| 0 | 33 | cosigner_pubkey (compressed secp256k1) |
| 33 | 64 | cosign_signature (Schnorr BIP-340) |
| 97 | 32 | member_ledger_hash (cosigner's ledger tip) |

Total entry size: 129 bytes. Entries MUST be sorted by cosigner_pubkey (lexicographic on serialized bytes). This ensures deterministic hashing. Decoders MUST either reject unsorted input or canonicalize it before verifying `current_hash` and the operator signature — otherwise a malicious sender can reorder entries to produce a distinct but otherwise-valid hash for the same logical cosignature set, enabling signature malleability.

After `QuorumBegin`, updates MUST carry the cosignature threshold specified in DEP-05 §Lifecycle for the operation's class and the lifecycle tier at the update's `block_height`. Within the active period (`block_height < quorum_expiry`) this resolves to `floor(n/2) + 1` cosignatures from distinct quorum members (where n is the quorum size) — strict majority — for every operation. Past `quorum_expiry`, only establishment operations (`QuorumAddMember`, `QuorumRemoveMember`, `QuorumBegin`) remain cosignable and their required threshold cascades through the tiers in DEP-05 §Lifecycle; updates carrying any other op type past `quorum_expiry` are non-conforming regardless of cosignature count.

## Hash Chain

    current_hash = tagged_hash("deposits/update/v2",
        cosign_data
        || n (2 bytes LE)
        || for each cosig entry (sorted by pubkey): member_ledger_hash || cosign_signature)

    chain_hash = SHA256(current_hash (32 bytes) || operator_signature (64 bytes))

with `cosign_data`, `tagged_hash` and `n` (the number of cosignature entries) as in Signing.

The operator signs the content and all co-signatures (see Signing). Their signature is folded into `chain_hash`, which becomes the next update's `previous_hash`. All signatures are committed to the chain without circularity.

After `QuorumBegin`, the cosig entries are mandatory at whatever threshold DEP-05 §Lifecycle prescribes for the operation type and tier — omitting them entirely, or providing fewer than the prescribed count, is non-conforming. Before quorum establishment, cosig entries are omitted on all updates **except the first `QuorumBegin`**, which MUST carry cosignatures from `floor(n/2) + 1` of the members staged via prior `QuorumAddMember` operations (n = `len(next_quorum_members)` at the point the update is applied). Decoders MUST reject a first `QuorumBegin` that lacks this majority. Without the rule, the operator could unilaterally transition to Active with a fabricated member list or a reserves outpoint that doesn't actually exist on-chain. See DEP-05 §QuorumBegin for the full rule and DEP-03 §QuorumBegin for the on-chain verification obligation cosigners must discharge before signing.

The first update (sequence 0) has `previous_hash` = `[0; 32]`.

**Sequence.** Every update's `sequence` MUST be its predecessor's plus one. An operator-signed update
whose `previous_hash` is the chain hash of the update at sequence k but whose `sequence` is not k + 1
(a *skip*, or a *rewind*) is a `NonConformingUpdate` (DEP-06), provable from the update and the
ledger's chain without cosignatures; a replica that receives one MUST treat it as that fault and
dispute, not as a gap to backfill. An update whose `previous_hash` names no update the replica holds
is a *gap*: the replica fetches the missing updates, and the update is not by itself fraud (DEP-06 §5).

**Publication.** The operator MUST publish every update to its relays (DEP-04), including `LedgerOpen`
(sequence 0): members identify the ledger's original operator from it, and a dispute cannot be
confiscated without it.

## Signing

All protocol signatures use Schnorr (BIP-340). On-chain transaction signatures follow bitcoin consensus rules separately.

    tagged_hash(tag, data) = SHA256(SHA256(tag) || SHA256(tag) || data)

    cosign_data = sequence_number (8 LE)
               || ledger_id (32)
               || block_height (4 LE)
               || block_hash (32)
               || previous_hash (32)
               || len(message) (4 LE)
               || message

`block_hash` is in Bitcoin's internal byte order, as it appears in a block header: the reverse
of the hex that `bitcoind` displays.

`cosign_data` covers every field of the update except the signatures. An update's
`ledger_id` is otherwise signed by no one, and one key may operate several ledgers: were it
outside the signature, anyone could republish an operator's update from one of its ledgers as
an update of another, where it would look like equivocation or a chain break. `block_height`
decides the lifecycle tier and so the cosignature threshold (DEP-05 §Lifecycle); were it outside
the signature, anyone could move an honest update past `quorum_expiry`. The length prefix keeps
the end of `message` from being read as the start of what follows it.

### Co-signing

Each quorum member independently signs the update content and their own ledger's tip:

    digest = tagged_hash("deposits/cosign/v2", cosign_data || member_ledger_hash)

`current_hash` is not signed directly — it incorporates the co-signatures themselves, so it cannot be known at signing time.

The operator collects the threshold of co-signatures specified in DEP-05 §Lifecycle (within the active period this is `floor(n/2) + 1`; past `quorum_expiry` it cascades through the tier schedule and only authorizes establishment operations) before finalizing the update. Each cosigner independently validates the operation against their local state replica and verifies chain continuity from their validated tip before signing.

### Operator

    digest = tagged_hash("deposits/operator-update/v2",
        cosign_data
        || n (2 bytes LE)
        || for each cosig entry (sorted by pubkey): cosign_signature)

where `n` is the number of cosignature entries (0 before `QuorumBegin`). The operator signs after collecting the required majority of co-signatures. This seals the multilateral agreement — the operator's signature covers the content and all co-signatures.

### Versions

These are the v2 digests. Earlier digests (`deposits/cosign`, `deposits/cosign/v1`,
`deposits/operator-update/v1` and the untagged operator forms) left `ledger_id`, `block_height`
and `block_hash` unsigned. They are retired, not accepted alongside v2: a verifier that accepted
them would accept a relabelled or re-dated copy of any update they signed.

### Test vector

See `vectors/dep02-signing-v2.json`.

## Operations

The `message` field contains a TLV-encoded operation. Type 0 is always a 1-byte discriminant. Deposit operations authorize via the dep-16 descriptor language — `pk()` is the common case, but the calculus generalizes miniscript with state predicates, proof obligations, and operation-type routing. See DEP-16 for the full grammar and admission rules; DEP-17 for the canonical encodings the fraud-proof system replays against.

### Discriminants

| Disc | Operation | Category |
|---|---|---|
| 1 | LedgerOpen | Lifecycle |
| 60 | LedgerClose | Lifecycle |
| 12 | QuorumBegin | Quorum |
| 43 | QuorumAddMember | Quorum |
| 44 | QuorumRemoveMember | Quorum |
| 46 | QuorumJoin | Quorum |
| 20 | DepositOpen | Deposits |
| 21 | DepositClose | Deposits |
| 23 | DepositKeyRotate | Deposits |
| 22 | FeeChange | Fees |
| 50 | FeeCollect | Fees |
| 30 | InvoiceCredit | Lightning |
| 31 | InvoiceLock | Lightning |
| 32 | InvoiceFail | Lightning |
| 33 | InvoiceFulfill | Lightning |
| 35 | OnchainCredit | On-chain |
| 36 | OnchainLock | On-chain |
| 37 | OnchainFail | On-chain |
| 38 | OnchainFulfill | On-chain |
| 70 | TransferLock | Transfers |
| 71 | TransferComplete | Transfers |
| 72 | TransferFail | Transfers |
| 54 | DisputeEnter | Dispute |
| 55 | DisputeAcquire | Dispute |
| 56 | DisputeYield | Dispute |
| 57 | DisputeArmed | Dispute |
| 80 | DeliveryEmbed | Delivery |
| 90 | Batch | Batch |
| 100 | ExitRequest | Settlement (DEP-20) |
| 101 | ExitCancel | Settlement (DEP-20) |
| 102 | DormancyNotice | Settlement (DEP-20) |
| 103 | DormancyAccept | Settlement (DEP-20) |
| 104 | LedgerWindDown | Settlement (DEP-20) |

### Operation TLV Fields

#### Common

| Type | Name | Size |
|---|---|---|
| 0 | discriminant | 1 |
| 2 | amount | 8 |
| 36 | block_height | 4 |

#### Ledger

| Type | Name | Size | Used by |
|---|---|---|---|
| 56 | operator_id | 33 | LedgerOpen |
| 58 | reserves_id | variable | LedgerOpen, QuorumBegin, QuorumJoin |
| 62 | reserves_amount_msats | 8 | LedgerOpen, QuorumBegin (deposit capacity) |
| 82 | membership_expires | 4 | QuorumJoin |
| 84 | new_outpoint_txid | 32 | QuorumBegin |
| 86 | quorum_expiry | 4 | QuorumBegin (shortest member membership_until) |
| 42 | ledger_hash | 32 | QuorumBegin (tip hash committed at rotation) |
| 88 | collateral_amount_msats | 8 | LedgerOpen, QuorumBegin (security bond) |
| 90 | spending_txid | 32 | QuorumBegin |
| 92 | new_outpoint_vout | 4 | QuorumBegin |
| 96 | genesis_block | 4 | LedgerOpen |
| 6 | quorum_members | N*33 | QuorumBegin (concatenated 33-byte compressed pubkeys) |
| 276 | quorum_member_ledger_ids | variable | QuorumBegin (parallel to type 6, each entry `u8 len ‖ ledger_id_bytes`) |
| 278 | exit_cutoff_height | 4 | QuorumBegin (DEP-20 §3) |
| 280 | exit_outputs | variable | QuorumBegin (DEP-20 §3; repeated `deposit_id(16) ‖ amount_msats(8) ‖ vout(4)`) |
| 282 | splice_in_outpoint | 36 | QuorumBegin (DEP-20 §4; txid ‖ vout) |
| 284 | splice_in_amount_msats | 8 | QuorumBegin (DEP-20 §4) |
| 286 | protocol_version | variable | QuorumBegin (ruleset name, DEP-18), QuorumUpgrade |
| 316 | migration_manifest | variable | QuorumBegin (DEP-20 §8.3; repeated `deposit_id(16) ‖ amount_msats(8) ‖ annualized_msats(8) ‖ annualized_bps(2) ‖ frequency_blocks(4) ‖ u16 len ‖ descriptor`) |
| 288 | migration_receiver | 33 | QuorumBegin (DEP-20 §8.3; receiver operator pubkey) |
| 290 | migration_vout | 4 | QuorumBegin (DEP-20 §8.3) |
| 292 | reference_feerate_sat_vb | 4 | QuorumBegin (DEP-20 §8; sets `dormancy_amount_msats` for the next bucket) |

#### Settlement (DEP-20)

| Type | Name | Size | Used by |
|---|---|---|---|
| 200 | deposit_id | 16 | ExitRequest, ExitCancel |
| 2 | amount | 8 | ExitRequest |
| 300 | exit_address | variable | ExitRequest (scriptPubKey bytes) |
| 302 | expires_at_height | 4 | ExitRequest (optional) |
| 288 | nonce | 8 | ExitRequest, ExitCancel (DEP-17 replay protection) |
| 290 | expiry | 4 | ExitRequest, ExitCancel (DEP-17 signature expiry height) |
| 204 | witness | variable | ExitRequest, ExitCancel (descriptor satisfaction) |
| 304 | exit_request_id | 32 | ExitCancel (SHA256 of the ExitRequest operation's TLV bytes, DEP-20 §3) |
| 306 | rotation_height | 4 | DormancyNotice, LedgerWindDown |
| 308 | manifest_hash | 32 | DormancyNotice, DormancyAccept |
| 288 | migration_receiver | 33 | DormancyNotice |
| 338 | dormancy_accept | variable | DormancyNotice (the receiver's signed `DormancyAccept` update, DEP-20 §8.3) |
| 316 | migration_manifest | variable | DormancyNotice (the offered manifest; its SHA256 is `manifest_hash`) |
| 340 | premium_msats | 8 | DormancyNotice (DEP-20 §8.3; a multiple of 1000) |
| 310 | offer_event_id | 32 | DormancyAccept (Kind 9110 event id) |
| 312 | accepted_total_msats | 8 | DormancyAccept |
| 300 | exit_address | variable | DormancyAccept (the receiver's funding scriptPubKey) |
| 302 | expires_at_height | 4 | DormancyAccept |
| 200 | deposit_id | 16 | DormancyAccept (optional: the receiver's deposit credited the premium) |
| 314 | min_collateral_bps | 2 | QuorumAddMember (DEP-05 §"Collateral floor"; optional, basis points of the vault) |
| 318 | dormancy_blocks | 4 | QuorumAddMember (DEP-20 §8; optional, the largest staged value applies, default 26280) |
| 332 | dormancy_notice_blocks | 4 | QuorumAddMember (DEP-20 §8; optional, the largest staged value applies, default 2016) |
| 336 | dormancy_outputs | variable | QuorumBegin (DEP-20 §8.2; repeated `deposit_id(16) ‖ amount_msats(8) ‖ vout(4)`) |

#### Deposits

| Type | Name | Size | Used by |
|---|---|---|---|
| 16 | invoice | variable | DepositOpen (BOLT11 string, optional) |
| 18 | cosigner_sig | 64 | DepositOpen (co-signer guarantee, optional) |
| 24 | deposit_pubkey | 33 | DepositOpen |
| 200 | deposit_id | 16 | DepositOpen, DepositClose, FeeChange, DepositKeyRotate, FeeCollect |
| 202 | descriptor | variable | DepositOpen (miniscript) |
| 204 | witness | variable | TransferLock, DepositKeyRotate (nested) |
| 208 | new_descriptor | variable | DepositKeyRotate |
| 232 | receive_requires_sig | 1 | DepositOpen |

#### Fees

| Type | Name | Size | Used by |
|---|---|---|---|
| 12 | fees | variable | DepositOpen (nested FeeStructure) |
| 20 | new_fees | variable | FeeChange (nested FeeStructure) |
| 226 | transfer_fees | variable | DepositOpen (nested TransferFeeSchedule) |
| 244 | fee_change_after_blocks | 4 | DepositOpen |
| 246 | fee_change_notice_blocks | 4 | DepositOpen |
| 248 | fee_change_limit_bps | 2 | DepositOpen |
| 250 | effective_block | 4 | FeeChange |

#### Transfers

| Type | Name | Size | Used by |
|---|---|---|---|
| 210 | nonce | 32 | TransferLock |
| 212 | source_deposit_id | 16 | TransferLock |
| 214 | destination_deposit_id | 16 | TransferLock |
| 216 | completion_script | variable | TransferLock (miniscript) |
| 218 | timeout_height | 4 | TransferLock |
| 220 | transfer_id | 32 | TransferLock, TransferComplete, TransferFail |
| 222 | block_hash | 32 | TransferLock |
| 224 | script_witness | variable | TransferComplete (nested) |
| 228 | fail_reason | 1 | TransferFail (1=timeout, 0=reserved) |

#### Lightning

| Type | Name | Size | Used by |
|---|---|---|---|
| 14 | payment_hash | 32 | InvoiceCredit, InvoiceLock, InvoiceFulfill |
| 26 | invoice_id | variable | InvoiceCredit |
| 28 | sequence_number | 8 | InvoiceCredit, InvoiceLock, InvoiceFulfill |
| 30 | payment_id | 32 | InvoiceCredit, InvoiceLock, InvoiceFulfill |
| 34 | preimage | 32 | InvoiceFulfill |
| 221 | fee | 8 | InvoiceLock (optional, odd tag) |

The InvoiceLock `fee` (tag 221, odd → optional) is the operator's fee budget in
msats charged on top of `amount` for paying the invoice — the LN routing reserve
plus the operator's service margin. When present it is bound into the dep-16
operation preimage (an extra `fee` arg on the spend op — see DEP-16/DEP-17) so the
depositor authorizes it and the operator cannot inflate it. Absent (legacy locks)
the preimage is byte-identical to a pre-fee InvoiceLock, so existing signatures
stay valid. See DEP-10 §"Operator-direct pay" for the settlement model.

#### On-chain

| Type | Name | Size | Used by |
|---|---|---|---|
| 66 | txid | 32 | OnchainCredit, OnchainFulfill |
| 68 | vout | 4 | OnchainCredit |
| 70 | destination_address | variable | OnchainLock, OnchainFulfill |
| 72 | withdrawal_id | 32 | OnchainLock, OnchainFail, OnchainFulfill |
| 74 | funding_address | variable | OnchainCredit |

#### Quorum

| Type | Name | Size | Used by |
|---|---|---|---|
| 44 | quorum_member | 33 | QuorumAddMember, QuorumRemoveMember |
| 46 | quorum_member_sig | 64 | QuorumBegin |
| 48 | operator_sig | 64 | QuorumBegin |
| 114 | member_ledger_id | variable | QuorumAddMember, QuorumJoin |
| 234 | min_fee_bps | 2 | QuorumAddMember |
| 236 | min_fee_fixed | 8 | QuorumAddMember |
| 238 | max_fee_period | 4 | QuorumAddMember |
| 242 | membership_until | 4 | QuorumAddMember |
| 252 | dispute_response_blocks | 4 | QuorumAddMember |
| 254 | dispute_arm_blocks | 4 | QuorumAddMember |
| 256 | service_response_blocks | 4 | QuorumAddMember |
| 258 | max_transfer_timeout_blocks | 4 | QuorumAddMember |
| 262 | max_descriptor_bytes | 4 | QuorumAddMember |
| 264 | compensation_bps | 2 | QuorumAddMember |
| 266 | compensation_deposit_id | 16 | QuorumAddMember |
| 268 | compensation_frequency_blocks | 4 | QuorumAddMember |

#### Dispute

| Type | Name | Size | Used by |
|---|---|---|---|
| 100 | reason | variable | DisputeEnter |
| 102 | last_valid_sequence | 8 | DisputeEnter |
| 108 | new_custodian | 33 | DisputeAcquire |
| 110 | claim_txid | 32 | DisputeAcquire |
| 118 | armed_block | 4 | DisputeArmed |
| 120 | new_reserves_address | variable | DisputeAcquire |
| 112 | commitment_hash | 20 | DisputeArmed (HASH160) |
| 122 | target_reserves | variable | DisputeArmed |

Field IDs 106 (entropy_block_hash) and 116 (entropy_block_height) were used by an earlier entropy-block-based DisputeAcquire shape and are now retired. Selection moved to an on-chain Tapscript lottery (see DEP-03 §"Custody Lottery"); `claim_txid` records the on-chain spend that proves the script-determined winner.

#### Delivery

| Type | Name | Size | Used by |
|---|---|---|---|
| 270 | request_hash | 32 | DeliveryEmbed |
| 272 | target_ledger_id | 32 | DeliveryEmbed |
| 274 | target_operator | 33 | DeliveryEmbed |

#### Balance commitments (odd tags → optional)

| Type | Name | Size | Used by |
|---|---|---|---|
| 223 | balance_after | 8 | Every balance-touching op (see §Balance Commitments) — post-op `balance` of the op's primary deposit |
| 225 | locked_after | 8 | Same ops as 223 — post-op `locked_balance` of the op's primary deposit |
| 227 | dest_balance_after | 8 | TransferComplete — post-op `balance` of the destination deposit |
| 229 | dest_locked_after | 8 | TransferComplete — post-op `locked_balance` of the destination deposit |

All four are odd tags: unknown implementations skip them, and their absence
leaves the operation byte-identical to the pre-commitment encoding, so existing
signatures and hashes are unaffected. Semantics, the conformance rule, and the
`balance-commit-v4` activation gate are specified in §Balance Commitments below.

### Nested TLV: FeeStructure

| Type | Name | Size |
|---|---|---|
| 0 | annualized_msats | 8 |
| 2 | annualized_bps | 2 |
| 4 | frequency_blocks | 4 |

### Nested TLV: TransferFeeSchedule

| Type | Name | Size |
|---|---|---|
| 0 | fixed_msats | 8 |
| 2 | rate_bps | 2 |

## Batch (disc 90)

A single signed update can carry up to `MAX_BATCH_OPS = 64` inner operations via the `Batch` op type. The batch is **transactional**: all inner ops apply or none do. If any inner op fails validation or state-application, the entire batch is rejected and the ledger is left unchanged.

Wire format: the `Batch` op's TLV body carries a single `BATCH_OPS` field (tag 298) whose payload is

    u16 BE: inner-op count
    repeated: u32 BE inner-op length-prefix, inner-op TLV bytes

Each inner op is encoded as a standalone TLV-LedgerOperation; the outer Batch's TLV simply concatenates them with framing.

**Admission gates** (enforced both at TLV decode and at `validate_operation`):

- **Non-empty.** A batch with zero inner ops is rejected.
- **Bounded.** A batch with more than `MAX_BATCH_OPS` inner ops is rejected. The cap bounds both per-update validation cost and fraud-proof scanner cost — even though Batch nesting is forbidden, a single deep batch could pathologically inflate scan time.
- **Flat.** A `Batch` inside a `Batch` is rejected. Nesting would require a recursive guard everywhere a fraud scanner walks the history; the flat-only rule keeps the recursion at most one level deep.

**Fraud-proof semantics.** Scanners that look for a credit on a payment_hash or `(txid, vout)` (DEP-06 §"Uncredited") recurse into Batch contents: a `Batch` containing an `InvoiceCredit` for the disputed payment counts the same as a bare `InvoiceCredit`. This preserves the fraud-proof invariant that the operator can't hide a credit inside a batch to defeat detection.

**Cosignature semantics.** Batched updates carry exactly one set of cosignatures over the outer signed update (which encodes the Batch op in `message`). Cosigners validate by replaying the batch transactionally; on success they sign the same single SignedLedgerUpdate. This is the whole point — N operations cost one cosignature round.

**When to batch.** Agent commerce workloads where one wallet performs many micro-operations (e.g. a settlement service running hundreds of transfers per minute) benefit most. Single-operation updates remain valid and are still the right choice for high-value or one-shot operations where atomic-across-N is irrelevant.

## Balance Commitments (balance-commit-v4)

### Motivation

Every balance-moving operation is a *relative* delta (`amount`). The only way
to learn a deposit's balance is to replay the entire chain from genesis into
ledger state. Two consequences:

1. **Catastrophic-recovery opacity.** If the early chain becomes unavailable
   (relay loss, disk loss during a dispute), the surviving suffix of cosigned
   updates cannot answer "what does this deposit hold, and how much of it is
   locked against which in-flight payments?" — precisely the questions a
   recovery custodian must answer.
2. **Expensive reads.** Auditors, explorers, and fraud verifiers all pay a
   full replay for a single balance.

Balance commitments make every balance-touching update carry the operator's
signed, quorum-cosigned declaration of the resulting absolute state, so any
update is self-describing and any chain suffix carries usable balances.

### Semantics

A **balance-touching operation** is any operation that mutates a deposit's
`(balance, locked_balance)` pair:

| Operation | primary deposit (tags 223/225) | destination (tags 227/229) |
|---|---|---|
| DepositOpen | the opened deposit (0, 0 today) | — |
| DepositClose | the closed deposit (0, 0 after drain) | — |
| FeeCollect | `deposit_id` | — |
| InvoiceCredit / OnchainCredit | `deposit_id` | — |
| InvoiceLock / OnchainLock | `deposit_id` | — |
| InvoiceFail / OnchainFail | `deposit_id` | — |
| InvoiceFulfill / OnchainFulfill | `deposit_id` | — |
| TransferLock | `source_deposit_id` | — |
| TransferFail | source of the pending `transfer_id` | — |
| TransferComplete | `source_deposit_id` | `destination_deposit_id` |

`balance_after` / `locked_after` (and the `dest_*` pair where applicable) are
the deposit's `balance` and `locked_balance` in millisatoshis **after** the
operation is applied. The pair MUST always appear together: a single update
then states the deposit's complete fund state, which is the recovery property
this section exists for. **A decoder MUST reject a half-present pair** (one of
223/225 present without the other, or 227/229) as a malformed operation — this
makes an ambiguous commitment unrepresentable on the wire, not merely
discouraged. Operations that do not touch a pair (DepositKeyRotate, FeeChange,
quorum/dispute/delivery ops) carry no commitment fields.

Inside a `Batch`, commitments ride the inner operations and are evaluated
sequentially against the transactional replay: each inner op's declared pair is
the state immediately after that inner op.

**Locking clarity.** For lock-class operations the triple
(`amount`, `balance_after`, `locked_after`) is deliberately redundant: it
states "this deposit holds X, of which Y is now locked, Z of that for this
payment" in one signed artifact. Combined with the fulfill/fail commitment
that later resolves the lock, an observer can track every in-flight
obligation's lifecycle without state reconstruction.

### Not part of the depositor authorization

Commitment fields are the **operator's assertion, verified by cosigners**.
They are NOT bound into the dep-16 operation preimage (DEP-16/DEP-17): the
depositor continues to sign exactly the fields they sign today. Binding a
racing quantity (balance changes under fee assessment and concurrent ops
between wallet-sign time and apply time) into the depositor signature would
couple authorization to state the wallet cannot know; verification belongs to
the parties that replay state — the quorum.

### Conformance

Two rules, split by ruleset (DEP-18):

- **Intrinsic (every ruleset):** if commitment fields are
  present on an operation, they MUST equal the replayed post-state. A cosigner
  applies the operation and compares; any mismatch is
  `ConformanceViolation::BalanceCommitmentMismatch` and the update MUST NOT be
  cosigned. This is safe to enforce unconditionally: pre-commitment updates
  contain no such fields (odd tags), so no historical update can retroactively
  fault.
- **Under `balance-commit-v4`:** every balance-touching operation MUST carry
  its commitment pair(s). A missing pair is
  `ConformanceViolation::MissingBalanceCommitment`. `cltv-offset-v2` and
  `fee-cap-v3` ledgers accept commitment-less operations indefinitely.

A cosigned update whose commitments are wrong is fraud under the existing
DEP-06 machinery — `NonConformingCosignature` (the quorum signed a
non-conforming update) or `NonConformingUpdate` (operator-only signature) —
and grounds confiscation. No new fraud-proof type is required.

**Operator population is unconditional.** A conforming operator emits the
commitment on every balance-touching op it builds, regardless of the ledger's
active ruleset — a *correct* commitment is conforming everywhere, so this is
safe to ship ahead of any `balance-commit-v4` upgrade (DEP-18 §"second example:
dep-02 balance commitments"). Because `content_hash` is computed over the raw
`message` bytes, a cosigner running pre-commitment code re-derives the identical
`content_hash` while skipping the (odd) commitment tags — so mixed old/new
fleets cosign the same update without divergence. Emitting always also means the
require-presence rule is already satisfied the moment a ledger upgrades.

### Ruleset

`balance-commit-v4` is a named ruleset in the `cltv-offset-v2`
reserves-cascade family (no on-chain script change): its rules are
`fee-cap-v3`'s plus the commitment requirement above. Because the family is
unchanged, a fleet activates it with per-ledger `QuorumUpgrade` sweeps or at
the next `QuorumBegin.protocol_version` — no reserves rotation. Members that
do not advertise `balance-commit-v4` in `supported_rulesets` block the upgrade
per DEP-18 admission.

### Recovery guarantee: bounded staleness, not suffix-sufficiency

Losing genesis is still not fully covered. A deposit's balance is only as
fresh as its most recent balance-touching update, and an **idle** deposit has
none. What bounds the gap is fee collection: `FeeCollect` touches every
fee-bearing deposit on its `frequency_blocks` cadence (DEP-07) and carries a
commitment, so:

- a surviving suffix spanning at least one full fee-assessment period contains
  a committed balance for every deposit on a fee schedule;
- deposits with no fee cadence have unbounded staleness. Operators SHOULD give
  every deposit a `frequency_blocks` even at zero fee rates — a zero-amount
  `FeeCollect` after the window is conforming (`0 ≤` any assessment cap) and
  serves as a balance heartbeat.

This changes the catastrophic posture from "obligations unknowable without
genesis" to "obligations readable from the recent cosigned tail, at worst one
fee period stale, plus any in-flight locks visible in the same tail."

## Related DEPs

- [DEP-03](DEP-03.md): On-chain transactions
- [DEP-04](DEP-04.md): Peer messaging
- [DEP-05](DEP-05.md): Quorum and collateral
- [DEP-06](DEP-06.md): Fraud proofs and recovery
- [DEP-07](DEP-07.md): Fee schedules
- [DEP-08](DEP-08.md): Deposits
- [DEP-09](DEP-09.md): Transfers
- [DEP-10](DEP-10.md): Payment channels
- [DEP-16](DEP-16.md): Self-modifying ledger-aware descriptors (the calculus deposit operations authorize against)
- [DEP-17](DEP-17.md): Canonical encodings (operation preimage, descriptor commitment, witness encoding)

## References

- [BOLT #1](https://github.com/lightning/bolts/blob/master/01-messaging.md) -- TLV encoding
- [BIP-340](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) -- Schnorr signatures, tagged hashing
