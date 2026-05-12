## intro
i've spent the last year designing a distributed bitcoin layer 2. i can't bring myself to give it some fancy name, so it's called "bitcoin deposits"

there's no mining, just staked funds covering the obligations of a cryptographic ledger validated by peer nodes. simple wallets are 12 words, miniscript is available for multisig. you can be offline as long as you want and still receive payments. if your ledger's operator goes offline or rogue, another operator will honor your claims when you come back

it's currently untested, but appears sound. it should require less trust and scale better than ark / spark / liquid. it requires full transparency, so there's no inherent privacy. wallets are cheap/free and funds are liquid. all communication is over nostr relays, so only the relay knows your ip address

current state: 100% me running everything. hoping to shake out the remaining bugs and fan things out soon

## q: what happens when dishonest parties steal funds?

a: the basic construction is that the operator updates the ledger, but a quorum controls the on-chain collateral/reserves utxo. if the operator makes invalid updates, the quorum confiscates their collateral and sends the reserves to a random quorum member, who will assume responsibility for the ledger

if quorum members themselves are dishonest or do not reassign reserves in a timely manner, the quorums on their own ledgers will find out, and confiscate their collateral and reassign their reserves

the essential question is: for how many layers does this scale? from my analyses and simulations, it's more than you'd think

## q: how does the quorum reassign ledgers?

a: quorums are composed of other operators running their own ledger that is at least half the size as the validated ledger. quorums have odd-numbered membership, realistically 3, 5, or 7 members. a majority of the quorum is required to co-sign updates (operate), and a majority is required to reassign a ledger (confiscate)

the ledger is assigned to one of the quorum members based on a commit-reveal lottery. before committing, each participating quorum member creates their own fork of the ledger, declares replacement collateral, and organizes a quorum. after the commitment transaction, participants reveal their pre-image and a winner is determined. the operators who lost close their fork with "yield", and the winner continues their fork with "acquire". then the quorum members spend the confiscated reserves along with the replacement collateral into a new quorum

## q: that sounds complicated

a: yes. it makes honesty more profitable than dishonesty, sustains control of wallet funds when dishonesty happens anyway, and allows honest operators to leave without rugging anyone. without proof of fraud, the necessary reserves are confiscated but the rest of the utxo is sent back to the operator

## q: what if the winning operator becomes dishonest?

a: they lose all of the ledgers they are operating, and all of the collateral they have staked, just like any provably dishonest action

## q: i have around 300 sats. is that enough for testing?

a: anyone can run a node, but 300 sats is probably too little because each quorum rotation requires an on-chain transaction of 180 vbytes, which at 2.5 sats/vbyte is 500 sats. current rotations are scheduled every two weeks

eventually the market should result in nodes with very low advertised fees. then you could open a deposit with just a few sats. my early testing nodes have very high per-deposit fees (208 sats / month) and low maximum amounts (1,000 sats per deposit) specifically to discourage people from keeping money on them while i test things

but if those sats are in lightning or ecash you can make deposits wallets, move funds into them, between them, back out of them, etc. fees are only taken when the balance is greater than zero, so moving funds through them quickly only costs bips

## q: what about zaps?

a: every deposit can be trustlessly bridged to lnurl, allowing you to receive zaps. every deposit is similarly bridged to lightning, allowing you to pay invoices with your zaps. for either to be trustless, invoice signatures must be checked and pre-image fraud proofs provided when theft occurs

## q: what do i have to trust?

a: that the network of operators contains some honest ones. that your wallet checks the protocol rules before depositing. that the lightning sidecar doesn't get away with stealing individual payments before someone catches it. there's no specific party you have to trust — just the existence of honest participants somewhere in the cosigning graph

## q: who funded this work?

a: foolishly, just me

## q: why are you doing it?

a: the internet needs a currency
