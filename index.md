# abstract

an ideal peer-to-peer version of electronic cash would allow online payments to be sent directly from one party to another quickly and with minimal preparation. the lightning network provides part of the solution, but the essential benefits are lost if a trusted third party is required to manage state on your behalf. we propose a solution to this problem using verifiable ledgers and a web of collateral. operators broadcast ledger updates to their peers, creating an auditable record of accounts. wallets broadcast evidence of dishonesty to those peers, who ensure that the ledger maintains an honest operator. unilateral exit is replaced by the guarantee that funds remain available so long as the network does. we arrive at a network that delegates liquidity maintenance, avoids setup fees, is capable of receiving payments offline, and scales independently of the base layer

# introduction

bitcoin deposits aims to provide fast and scalable key controlled funds, trustlessly, off-chain. on-chain activity scales with the number of ledgers and frequency of reserves rotation. throughput scales slightly above linearly with the number of ledgers in the network, making millions of transactions per second across trillions of wallets plausible

there are explicit tradeoffs:
- no unilateral exit: when operators fail funds stay in the network
- no privacy: verification requires transparency
- intermittent availability: a deposit is only as available as the operator. wallets should spread out funds to increase availability

we expect the wallet experience to be similar to a fast base layer, having payment economics similar to the lightning network
