# 07 — operator playbook

How to run a node defensively, derived from 01–06. Everything here is judgment the
protocol prices but does not enforce.

## Quorum composition

The Tier 0 path spends the whole vault without the operator's signature. The quorum
majority is therefore the custodian of the operator's capital. Compose for that.

- **Trusted majority.** Three anchors of five, or four of seven. With a trusted
  majority no combination of the other seats can spend the vault. Two anchors of
  five leaves the vault dependent on one honest pick among three, and grey-market
  keys with tenure are exactly what a patient coalition manufactures (06).
- **Bond the rest to the anchors.** Accept a non-anchor only if its own quorum
  includes at least one of your anchors and has a credible majority. A member that
  signs against you is then slashable by people you trust. Hand-rolled depth-1 rule.
- **Liveness is a separate axis.** p95 hold on a five-member quorum at 80% liveness
  is eight days (F15). Require different hosting, jurisdiction, and software, and
  read uptime from members' own ledger histories before inviting.
- **Disjoint quorums across your ledgers.** Three to five ledgers, no shared
  members. Each vault is your maximum loss from one bad quorum; disjointness gives
  contagion something to bite.

## Operating

- **Freeze playbook.** Monitor co-sign latency per member. Keep a staged alternate
  per seat. Remove a slow member while you still hold a majority to sign the
  removal, and rotate in the same update. Keep `quorum_expiry` short until an
  inactivity trigger exists. Publish signed proposals so withholding is visible.
- **Never leave a signature behind.** No non-conforming update. The difference
  between silence and fraud is your collateral.
- **Stay provably alive.** Heartbeat activity every few hundred blocks (fee
  collection, self-transfer, empty batch).
- **Embed early.** Hash anything you may need to prove later into your own or a
  peer's ledger; causal ordering is free at the time and expensive afterward.
- **Serve on your anchors' quorums.** Mutual deterrence, and the path to becoming
  an anchor. Automate dispute duties; membership is a clock, not a courtesy.

## Terms

- Advertise only atomic paths. No legacy lightning receive.
- Honest guarantee matrix; it is reputational, and reputation is the asset.
- Collateral high early, reserves grown with tenure. Set fee-change limits you
  would accept as a depositor.
- Member fee floors sized to the flows you expect; per-action for agent traffic,
  per-annum for parked balances.

## What this does not cover

A trusted majority that is wrong about itself. Anchors are the residual, and the
only defence against a bad anchor is having several from different worlds.
