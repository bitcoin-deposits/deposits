# bitcoin deposits
## abstract

ok so imagine you could just venmo someone bitcoin instantly, no setup, no bs. lightning kinda does this but it falls short because you still need some trusted third party managing your stuff. nah, we're not doing that. we built something with verifiable ledgers and a whole web of collateral so nobody can rug you. operators post all their ledger updates publicly — full transparency, zero plausible deniability. wallets report bad actors to peers who keep the operator in check. you can't pull your funds out unilaterally, but as long as the network is alive, your money is safe. we ended up with a network that handles liquidity for you, no setup fees, can receive payments while you're offline, and scales independently of the base layer

## introduction

bitcoin deposits is trying to give you fast, scalable, key-controlled funds — trustlessly, off-chain. on-chain stuff only scales with how many ledgers exist and how often reserves rotate. throughput scales slightly better than linearly with ledger count, so we're talking millions of TPS across trillions of wallets. the math checks out

but honestly, there are tradeoffs:
- no unilateral exit: if operators disappear, your funds stay in the network. you can't just solo leave
- no privacy: verification needs transparency
- intermittent availability: your deposit is only up when the operator is. diversify or you're stuck

we expect the wallet experience to feel like a fast L1 with lightning-tier payment economics

## ledgers

a ledger is basically an append-only chain of updates — each one hashes the previous and gets signed by the operator. different update types have different rules for when and how they can be used. ledgers are completely self-describing, all updates are public and non-repudiable, so anyone can audit whether things are valid or not

each ledger has one active operator, but the mesh keeps things running collectively. any operator can spin one up, but if they disappear or start acting dishonestly, a different operator gets swapped in along with the reserves. you know who's running things by checking which pubkey signed the most recent co-signed update

## deposits

a deposit is basically your account — sends and receives funds, controlled by miniscript. when you open one you lock in a fee schedule and decide whether incoming funds need your wallet's signature. the operator has to let you transfer between deposits on the same ledger and do on-chain exits. they should also let deposits pay lightning invoices

it's the operator's call whether to create on-chain funding offers or lightning invoices for a deposit. if they do, quorum members need to co-sign them, and your wallet better be checking that signature. offers and invoices aren't on the ledger itself so it's your job to verify and keep receipts

## fees

transfers between deposits, on-chain, and through lightning all have fees going to the ledger's operator. there are also periodic balance fees on a set schedule. everything gets negotiated when you open a new deposit — think of it like signing a lease. fees can change after a certain number of blocks, given proper notice and within a percentage cap you agreed to at opening. the quorum can refuse to co-sign updates that would put them in unprofitable situations they might inherit

## transfers

the basic transfer is a two-phase operation between deposits on the same ledger: you request to send funds. if you've got enough, a lock with a spending condition gets appended to the ledger. fulfill the spending condition before the timer runs out and funds move from sender to recipient minus the operator's cut. timer expires? lock gets released, minus a smaller fee. with miniscript spending conditions this is enough for any deposit to run bridges and liquidity services for other deposits on the same ledger

## lightning

operators with a lightning channel can let deposits send and receive over lightning. when a deposit wants a lightning invoice, the operator creates one through their node, gets quorum members to co-sign it proving they'll credit the deposit when paid. your wallet should hold onto that co-signed invoice as proof. when a deposit wants to pay a lightning invoice, the operator pays through their node and debits the deposit after grabbing the preimage

when both sender and receiver are deposits on the same operator, the operator can just settle it internally without routing through lightning at all — credit one, debit the other, done. skips routing fees and avoids failure modes while keeping the same accounting guarantees

## couriers

transfers only work between deposits on the same ledger. to move funds across ledgers, wallets use couriers — services that hold deposits on multiple ledgers and shuttle funds between them. a courier advertises their capacity and per-ledger directional fees on the relay. when you want to send from ledger A to ledger B, you lock funds to the courier's deposit and ask them to create a matching lock from their deposit on the destination ledger to whoever you're paying. once both locks are set, you reveal the preimage to the payee who completes their side. the courier then uses that same preimage to complete the transfer from you to them

this is your standard HTLC pattern. the courier's outbound timeout is always earlier than the inbound, so if you never reveal, both locks just expire and nobody loses anything. zero trust needed beyond the timeout guarantees that operators enforce

couriers set per-ledger fees: fee_in and fee_out for each ledger they cover. your wallet estimates route cost as fee_out on source plus fee_in on destination. couriers can adjust fees by ledger based on available liquidity, which naturally rebalances their positions. wallets find couriers through their relay ads and pick based on fees, capacity, or coverage

## communication

all comms between wallets and operators, and between operators themselves, run on nostr relays. ledger updates get published as durable events that relays keep forever — permanent audit trail. requests and responses between wallets and operators are ephemeral events with a short relay TTL. operators post their terms as replaceable events so wallets can browse and compare operators without needing some centralized directory

this architecture means wallets don't need persistent connections — you can go offline for weeks, come back, and catch up by replaying events from any relay. operators can be reached through any relay they're monitoring, and which relay you use is a deployment choice not a protocol constraint

## reserves and collateral

reserves live in a utxo with an amount >= the sum of a ledger's obligations, spendable by a quorum majority, with fallback to the operator after a significant period

collateral is the operator's own capital — deposited and locked on quorum member ledgers. each member holds a collateral deposit that the operator funds and locks for a set duration. a ledger's total obligations are hard capped at 2x the smallest collateral lock held by any member, and the quorum's duration is capped at the shortest lock time. this makes sure the collateral web always has enough backing to cover a custody transfer no matter what. the same collateral can back multiple ledgers for better capital efficiency but wallets should prefer operators whose collateral sources don't overlap

obligations are enforced when creating new funding offers or invoices. the operator cannot create offers or invoices that would push the ledger's total obligations above reserves or above 2x the smallest collateral lock, whichever is lower

## quorum

operators recruit other operators to their quorum by depositing and locking collateral on the member's ledger. the request includes the collateral commitment (amount and lock duration) and the member's terms: minimum fee schedules that deposits on the ledger need to meet. each member runs their own ledger and can confiscate the operator's collateral if they're proven non-conforming. members set floor fees during their quorum membership — the operator can't open deposits with fees below the strictest member's minimums, protecting members from inheriting bad obligations after a custody transfer

once the quorum is locked in, reserves rotate into a new multisig utxo. members co-sign valid updates and jump in for recovery if the operator signs non-conforming ones. bigger quorums = more communication overhead but less operator risk, better uptime, and collusion becomes way harder and more expensive. wallets should prefer larger quorums

## economic deterrence

the protocol trades unilateral exit for economic deterrence. quorum members are directly incentivized to call out dishonest operators. during normal ops they earn modest fees on collateral, but if an operator gets caught doing provably non-conforming stuff, members get to confiscate the operator's entire collateral deposit on their ledger. one mistake and you lose everything

when a wallet suspects censorship, it can escalate to quorum members via certified delivery. the member embeds the request hash in their own ledger for a small fee, creating causally anchored evidence. if the operator ignores the request, the member has both the receipts and the financial motivation to start a dispute

lightning invoice fraud follows the same deterrence pattern. the operator knows whether a preimage was received but the wallet doesn't. however any payer might share the preimage with the wallet. a single confirmed theft triggers dispute, seizure of reserves, and collateral confiscation. the upside of stealing one payment is capped but the downside is financial ruin — making lightning theft economically irrational even though it's technically not provable without third party cooperation

the failure mode for both censorship and lightning deterrence is unanimous quorum collusion. the protocol can't protect against the entire quorum conspiring to steal, but the web of collateral makes sure collusion costs more than what they'd gain. the network's transparency lets wallets and discovery markets spot suspicious quorum structures before depositing funds

## time

absolute time is measured against the base layer. tolerances can't exceed a reasonable number of confirmations to stay stable during chain reorgs

where higher tolerances are needed we use causal ordering. a cryptographic ledger is a merkle chain. each update proves it came after everything before it, but says nothing about info outside the chain. to build a distributed ordering, we require that co-signatures include the latest update hash from the co-signer's ledger. that hash gets baked into the current update's hash, becoming part of this chain and every other chain the ledger operator co-signs for, creating a web of causality. you can't prove time explicitly, but you can prove that certain pieces of info were created in a specific order

## fraud proofs

we can prove various types of fraud by exposing info that was created in the wrong order. where the info isn't included through normal network ops, it can be smuggled in by creating activity that includes a hash of the evidence. once it's in an operator-signed update, the evidence is revealed as existing at a non-conforming place in the ordering:

- an operator offered to credit a deposit with on-chain funds to a specific address, then signs a ledger update that doesn't contain the credit but does contain a chain revealing a block hash past the confirmation deadline

- an operator created a lightning invoice for a deposit, then signs a ledger update that hasn't credited the deposit even though the preimage is already revealed in the chain

- a co-signature that claims the current ledger hash is one that comes before their own later hash in the chain

- a quorum member on a contested ledger who was clearly active but didn't act on proof of fraud within the required blocks

- signing or co-signing non-conforming ledger updates

a fraud proof = the evidence + a causal chain connecting the embedded hash to the accused operator's ledger. it's a sequence of co-signed updates, each including a member_ledger_hash from the previous link's ledger. verifiers walk the chain without searching, confirming each link is a signed update and that the proof hash matches the embedded data

## recovery

once a ledger goes down or starts acting non-conforming, quorum members can fork it from the last good update. they need to set up a new quorum and provide collateral attestations. members then coordinate to spend the previous reserves output to a lottery of potential successor chains. whoever wins appends an acquisition update to their chain, losers append a yield. wallets keep addressing the same ledger, only accepting replies co-signed by the quorum. periodically, and when replies don't have the expected co-signature, the wallet should check the network and replay ledger updates to catch any custody changes

when non-conformance looks accidental (like a ledger going dark for a while) the custody transfer has to be respectful: only the reserves needed to cover obligations go to the lottery, change goes back to the operator's pubkey. collateral stays untouched

when there's actual proof of non-conformance though? the excess reserves beyond what's needed get split equally among quorum members, and collateral on member ledgers is fair game for confiscation

## network health

one obvious attack vector is forming islands of colluding operators. after building up massive obligations across their ledgers, they coordinate an exit, stealing funds that exceed the collateral they lose. the network can defend against this except in regions where the internal value exceeds the collateral connecting it to the honest network. higher collateral ratios and bigger, more diverse quorums make these pockets less likely, but they can be created on purpose and we can't expect every wallet to audit the entire graph. instead discovery markets should publish operator accountability metrics based on graph analyses like prize-collecting algorithms

## conclusion

we propose a collateral network where stealing requires collusion, but collusion increases the collateral at risk faster than it increases what can be stolen. we use this network to secure cryptographic ledgers backed by full reserves. these ledgers service accounts for offline wallets in exchange for pre-negotiated fees. ledger primitives support miniscript spending conditions sufficient for basic smart contracts. the network scales close to linearly, enabling a massive network to provide billions of wallets and transaction volume that exceeds traditional payment networks
