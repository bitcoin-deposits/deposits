# bitcoin deposits

bitcoin deposits is a protocol similar to custodial lightning, but:
- reserves are proven
- obligations are proven
- fraud is proven
- updates are co-signed by the majority of a quorum
- reserves and collateral are held in a quorum multisig
- non-conformance results in confiscation
- confiscated ledgers find new operators
- disappearance results in "polite" confiscation
- timely confiscation or proof of absence is required
- non-conformance as a quorum member results in confiscation

## primary roles

### alice (node)
- can run a stable node at home
- wants to make yield on her bitcoin
- chooses 3 or 5 established nodes to form a quorum
- spends R into a multisig of this quorum
- acts like a bank, with total deposits up to R/2
- collects fees on balances and transactions
- can participate in other quorums

### bob (wallet)
- only has a mobile phone
- is willing to pay a premium for liquid bitcoin
- finds well connected nodes, possibly near a trust anchor
- picks alice based on fees or responsiveness
- opens an empty wallet
- receives nostr zaps
- accepts pre-negotiated, periodic fees
- buys drinks with his zaps

### charlie (quorum member)
- runs large nodes in a datacenter
- gets yield even when there's no activity
- serves on alice's quorum
- receives a pre-negotiated cut of the fees alice collects
- co-signs her ledger updates
- participates in quorum confiscations when there is a fraud proof
- might continue operating a ledger that was confiscated
