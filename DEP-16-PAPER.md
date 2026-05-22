# A Monotone Term Calculus for Ledger-based Deposit Authorization

## Abstract

We describe a small term calculus for authorizing operations on accounts in a ledger-based system. A deposit's authorization condition is a closed term in this calculus, evaluated against an operation, a ledger-state snapshot, and a witness, to produce accept or reject. The calculus is strict, total, and statically checked against a single placement rule that guarantees authorization is monotone in the witness. The same calculus authorizes modification of the term itself, so capability attenuation and related policy disciplines are expressible within the language rather than enforced by a separate relation. The design recombines elements from miniscript's implicit positive-position discipline, the capability-attenuation tradition, and the bounded-policy-language tradition of macaroons and Cedar.

Its scope is operations on a single ledger account — not bitcoin script, not UTXOs, not a smart-contract platform.

## 1. Proposal

A *deposit* is an account in a ledger. Each deposit carries an *authorization term* in the calculus described below. *Operations* on the deposit — spending, modifying the authorization term, receiving funds under specified conditions, updating metadata — are presented to the term for authorization. Authorization succeeds iff the term evaluates to `true` against the operation, the current ledger state, and a witness supplied with the operation.

The calculus combines three properties from three distinct precedents:

1. **Decidability and analyzability**, in the Cedar sense (Cutler et al., 2024): evaluation is a strict, total, statically-typed fold, terminating in time polynomial in the sizes of the term, the operation, and the ledger-state snapshot data the term references, with cross-implementation equivalence verifiable by inspection.

2. **Witness-monotonicity**, in the miniscript sense (Wuille, Poelstra, Kanjalkar, Poinsot, Chow): acquiring additional capabilities — signatures, preimages, attestations — cannot revoke authority. Enforced statically.

3. **Reflexive policies**, in the tradition of RDBAC (Olson, Gunter, Madhusudan, 2008) and Becker–Nanz (2010): modification of the authorization term is itself an operation, authorized by the term, evaluated under the same discipline as ordinary operations.

Each property is established. The contribution is combining them in one decidable, deterministic term language.

## 2. The calculus

### 2.1 Sorts

The calculus has three sorts:

- **B**, the sort of authorization decisions. A closed term of sort `B` is an authorization condition.
- **V**, the sort of values. Inhabitants include integers, public keys, hashes, paths into terms, subterms reified as data, and operation arguments drawn from `w`. Witness-dependent data — signatures, preimages, attestation payloads — is not in V; it lives in the witness `m` and is consumed only by proof obligations.
- **O**, the sort of *proof obligations*. A leaf of sort `O` denotes a fact that must be discharged by the witness. Proof obligations are injected into `B` by a coercion `prove : O → B`.

The distinction between leaves of `B` introduced via `prove` and leaves of `B` drawn from closed-world data is load-bearing: in a well-formed term, `prove` is the only construct whose evaluation depends on `m`, and the polarity rule of §2.4 leverages this invariant to guarantee witness-monotonicity.

### 2.2 Syntax

```
B ::=  <bool>                     -- boolean literal
    |  and(B, ..., B)
    |  or(B, ..., B)
    |  thresh(k, B, ..., B)
    |  not(B)
    |  if(B, B, B)
    |  match(V, branch(V, B), ..., branch(else, B))
    |  cmp(@, V, V)               -- @ in {=, <, <=, >, >=}
    |  state(p, V, ..., V)        -- state predicate p applied to values
    |  prove(O)

V ::=  literal | varref | op(V, ..., V)
    -- op is drawn from a fixed signature of total functions

O ::=  pk(V)                       -- signature by a key
    |  hashlock(V)                 -- preimage of a hash
    |  attest(V, V)                -- oracle attestation matching a schema
```

The protocol fixes finite signatures of state predicates `p` (e.g., `blocks_since_open`, `deposit_balance`, `operation_arg(_)`) and value functions `op` (arithmetic, comparison, AST inspection). These signatures are the only avenue by which the calculus accesses the environment.

A *descriptor* is a closed term of sort `B` together with a top-level constant environment, written `with(varref = literal, ..., in T)`. Variable references in `T` resolve against this environment, which is bound once at deposit-open and never re-evaluated. An equivalent characterization: a descriptor is a pair `(Γ, T)` where `Γ` is a finite map from variable names to literals and `T` is closed over the domain of `Γ`.

Every `match` must include an `else` branch. This ensures total evaluation regardless of scrutinee value, and is the only branch admitted by a scrutinee value that does not equal any literal branch tag.

### 2.3 Evaluation

An *environment* is a triple `(w, s, m)` where `w` is the operation being authorized, `s` is a ledger-state snapshot, and `m` is a *witness* — a finite map from {public keys, hashes, oracle keys} to {signatures, preimages, attestations}.

Evaluation `[[ T ]] (w, s, m)` is a strict, total, structural fold:

- `V`-terms reduce to values by total functions of `(w, s)`.
- `state(p, ...)` and `cmp(...)` reduce to booleans by total functions of `(w, s)`.
- Boolean connectives have standard semantics; `match` selects a branch by equality of scrutinee with branch tag, or `else`.
- `prove(o)` evaluates to `true` iff `m` contains a discharging entry for `o` that verifies against `(w, s)`. The witness is queried by *lookup*: `pk(K)` asks `m` for a signature under key `K` over the canonical encoding of `w`; `hashlock(H)` asks `m` for a preimage of `H`. There is no positional consumption of the witness and no branch-selector data.

Arithmetic in the value sublanguage operates on bounded integers (the ledger's native integer width). To preserve totality and avoid implementation-defined behavior: addition, subtraction, and multiplication saturate at the representable range's endpoints, and division by zero yields zero. Both choices preserve total, deterministic functions of `(w, s)`; descriptors must not depend on saturation occurring.

There is no recursion, iteration, or search. The witness is supplied, not synthesized. Evaluation terminates in time polynomial in `|T|`, `|w|`, and the size of the ledger-state snapshot data the term references — structural comparisons via `subtree_at` and `cmp` over reflective values cost time proportional to operand size, so the bound is not linear in `|T|` alone, though it remains polynomial overall.

By the sort discipline of §2.1 and the totality of state predicates and value functions, `prove(o)` is the only construct whose evaluation depends on `m`. This invariant — m-dependence flows only through `prove` — is what the polarity rule (§2.4) leverages to guarantee witness-monotonicity.

### 2.4 The polarity rule

Define the *positive-position* judgment P inductively on contexts. The root of a term is in positive position. A B-subterm directly under `and(...)`, `or(...)`, `thresh(k, ...)`, or in a branch body of `if(_, B, B)` or `match(_, branch(_, B), ...)` is in positive position iff the enclosing context is. A B-subterm under `not(_)` or in the *condition* slot of `if(B, _, _)` is not in positive position.

The polarity rule is:

> **Every occurrence of `prove(o)` in an authorization term must lie in positive position.**

The rule is checked statically, both at deposit-open and after each modification (see §3.4). Terms that violate it are rejected. The rule applies only to `prove`; `state(...)`, `cmp(...)`, and V-expressions may appear freely under negation and as conditions.

Sort discipline already prohibits `prove(o)` from V positions — comparison arguments, state predicate arguments, value-function arguments, match scrutinees, and match branch tags — since `prove(o) : B` and these positions are sort V. The polarity rule constrains only B positions, and the non-vacuous constraints are exactly two: the argument of `not` and the condition of `if`.

The rule is stronger than the textbook parity-flipping definition of positive position: a `prove` under `not(_)` is rejected absolutely, not admitted when wrapped by an outer `not`. Parity-flipping would accept `not(not(prove(o)))` — monotone in net effect, but with a non-positive sub-occurrence that would violate the m-constancy lemma of §3.1. The stronger discipline trades acceptance of double-negated proof obligations — a syntactic possibility with no practical use — for a clean inductive invariant on the structure of non-positive subterms.

## 3. Properties

### 3.1 Witness-monotonicity

Define a partial order on witnesses: `m <= m'` iff `m'` agrees with `m` on `dom(m)` and may define additional keys. Intuitively, `m'` represents at least as much capability as `m`.

Say a term is *m-constant* iff its evaluation under `(w, s, m)` depends only on `(w, s)`, not on `m`. By construction, V-terms, `state(...)`, and `cmp(...)` are m-constant; among B-leaves, `prove` is the only m-dependent one.

**Lemma.** *In a well-formed term, every B-subterm not in positive position is m-constant.*

*Proof.* By the polarity rule, no `prove` leaf appears in a non-positive B-position. The remaining B-leaves (boolean literals, `state`, `cmp`) and all V-terms are m-constant. The B-connectives are total functions of their arguments, and total functions of m-constants are m-constant. By induction on terms, any B-subterm reachable from the root through only non-positive contexts contains only m-constant leaves and is itself m-constant. ∎

**Theorem (witness-monotonicity).** *For every well-formed term T, every operation w, every state s, and witnesses m <= m', if `[[ T ]] (w, s, m) = true` then `[[ T ]] (w, s, m') = true`.*

*Proof.* By induction on T.

- `and`, `or`, `thresh`: monotone in their B-arguments; the inductive hypothesis applies directly.
- `not(B_1)`: by the lemma, `B_1` is m-constant, so `[[ not(B_1) ]]` is unchanged from `m` to `m'`.
- `if(B_c, B_t, B_e)`: by the lemma, `B_c` is m-constant, so the same branch is selected under `m` and `m'`; apply the inductive hypothesis to the selected branch.
- `match(V_s, ...)`: the scrutinee `V_s` is sort V hence m-constant, so the same branch is selected; apply the inductive hypothesis to the selected branch body.
- `prove(o)`: if `m` discharges `o`, the discharging entry is present in `m'` by `m <= m'`, so `m'` also discharges.
- Boolean literals, `state(...)`, `cmp(...)`, V-positions: m-constant by construction. ∎

Witness-monotonicity is the security property the calculus is engineered to guarantee. A party that holds a key cannot fabricate authority by pretending not to hold it: no well-formed term has a branch gated on key-absence, so no branch is unlocked by withholding.

### 3.2 State predicates carry no monotonicity burden

State predicates and value expressions are m-constant by construction: their evaluation depends only on `(w, s)`. Closed-world expressivity — negation, disjunction, comparison, dispatch — is therefore admissible at these leaves without endangering Theorem 3.1, since monotonicity is defined over `m` alone and m-constant data have no witness dimension along which to vary. The polarity rule confines `prove` to positions where this safety is preserved; the rest of the boolean structure inherits Cedar's expressivity over closed-world attributes.

State predicates evaluate correctly whether or not `s` is honest — they are total functions of their inputs — but their value as *authorization guards* depends on `s` reflecting actual ledger history. The calculus does not establish this; it consumes `(w, s)` as given, with the integrity of `s` guaranteed by the protocol's state commitments (a concern outside this calculus). The adversary's relationship to the inputs is asymmetric: they craft `w`, which the descriptor decides whether to authorize, but they do not control `s`. This asymmetry is what makes state-based guards enforceable in practice: a check like `blocks_since_activity_at_least(N)` cannot be shortcut by withholding or fabrication, only by waiting.

### 3.3 Determinism

The value functions and state predicates are specified as total functions of `(w, s)`. Witness lookup is deterministic given `(o, w, s, m)`: the predicate either finds a verifying entry or does not. Evaluation contains no search. It follows that for fixed `(T, w, s, m)`, evaluation yields a fixed verdict in every conforming implementation, given protocol-fixed canonical encodings of operations, state snapshots, and terms. (The canonical encoding of operations is what signatures commit to; canonical encodings of state and terms are what cross-implementation `cmp` and `subtree_at` results agree on.) This property is required for the calculus to underpin a fraud-proof mechanism: a verifier replays `[[ T ]] (w, s, m)` and either confirms or contradicts the operator's verdict, with no ambiguity to adjudicate.

### 3.4 Reflexivity

A term `T` is data. The value signature includes total functions that read `T` as structured data:

```
ast_ref(p)       : V    -- subterm at path p
ast_shape_at(p)  : V    -- head constructor at path p
subtree_at(c, p) : V    -- structural equality of c with the subtree at p
```

The protocol's operation set includes ast-modifying operations `insert(p, s)`, `replace(p, s)`, `delete(p)`. When such an operation is authorized by the current term `T`, the protocol computes the candidate term `T'` from `T` and the operation's arguments and re-runs the admission checks `T` faced at deposit-open: polarity and capability. A `T'` that fails either check is rejected; the modification does not take effect, even though `T` authorized the underlying operation. The deposit binds to `T'` only when the candidate is well-formed.

This preserves a system-level invariant: every term against which the protocol evaluates an operation is well-formed. Theorem 3.1 therefore applies to every evaluation the protocol performs, not only to the term first admitted at deposit-open. The invariant holds inductively: deposit-open establishes it, and each modification preserves it by re-check.

Subject to that invariant, the relationship between the authority sets of `T` and `T'` is unconstrained — it may be subset, superset, or neither — and is determined entirely by the modification guards in `T`. Attenuation, in the sense of the capability-security literature, is a property a well-written `T` may have; the calculus does not require it.

## 4. Precedent

The calculus draws on several bodies of prior work, each contributing one of the threads it combines.

**Bitcoin miniscript** (Wuille, Poelstra, Kanjalkar, Poinsot, Chow; BIP-379) implements a monotone authorization calculus by construction. Its own documentation describes it as "a monotone function (tree of ANDs, ORs and thresholds) of signature requirements, hash preimage requirements, and timelocks." Its leaves are proof obligations on a spending witness, and its expression grammar admits no boolean negation, so the positive-position discipline holds implicitly. Miniscript has no closed-world state predicates beyond the timelocks `older` and `after`, and no notion of self-modification. The present calculus generalizes miniscript along both axes while retaining its monotonicity property; the polarity rule of §2.4 is the discipline miniscript enforces grammatically, made explicit so that closed-world predicates can be admitted without losing it.

**The capability-security tradition** (Dennis and Van Horn 1966; the KeyKOS / EROS / Coyotos / seL4 lineage of capability operating systems; Miller 2006; the E language family) studies authority as a delegable, attenuable resource. It is the source of the vocabulary used in this paper — delegation, attenuation, sub-authority — and of the design instinct that authorization terms should be expressive enough to encode delegation patterns. The tradition's central commitment, however, is that derived authorities are strictly weaker than their originals; this is the property capability languages enforce structurally. The present calculus explicitly rejects this commitment. The reason is contextual: capability security's home setting is centralized authority distributed downward to less-trusted recipients, where strict narrowing prevents privilege escalation. In the deposit setting, the term's author and the authority holder are the same party, and recovery use cases — key replacement after loss, guardian addition after compromise, repair of overly restrictive policies — require expansion of authority. A narrowing-only discipline would foreclose them. Modifications in this calculus may expand, narrow, or rearrange authority; the calculus is silent on which. The recent ERC-7579 / Rhinestone–Biconomy Smart Sessions work and the ERC-7710 / ERC-7715 delegation interfaces in the Ethereum account-abstraction stack sit closer to this stance: session and delegation policies are first-class data with structural rules, and the direction of modification is the policy author's responsibility.

**Macaroons** (Birgisson, Politz, Erlingsson, Taly, Vrable, Lentczner; NDSS 2014) demonstrate that a sufficiently restricted caveat language with conjunction-only composition supports usable reasoning about delegation chains. Macaroons restrict caveats to closed-world predicates and avoid the negation problem by avoiding negation entirely. The present calculus admits negation on closed-world predicates while excluding it on proof obligations, which yields strictly more expressive policies than macaroons admit, at the cost of an explicit polarity check.

**Cedar** (Cutler, Disselkoen, Eline, He, Headley, Hicks, Hietala, Ioannidis, Kastner, Mamat, McAdams, McCutchen, Rungta, Torlak, Wells; OOPSLA 2024) and the broader decidable-policy-language tradition (Datalog with stratified negation; XACML; OPA/Rego with bounded recursion) are policy languages designed for static analyzability over structured authorization data. Cedar's design choice to bound expressivity in service of analyzability — supported by a formal verification effort in Lean — is the same choice the present calculus makes. The differences are that Cedar does not have proof obligations in the present sense — it is a policy-evaluation engine over named principals and resources — and that Cedar does not admit policy reflection. The present calculus does, for a reason specific to its setting: authority lives in user-held keys, which appear as literals in the policy, and the protocol's nodes do not control them. Any operation that touches keys — rotation, recovery, delegation revocation — requires the policy itself to evolve. Cedar's centralized principal-attribute model places authority in entities the system can name and re-attribute without changing policy text; in a setting where authority is cryptographic and user-held, policy reflection is a necessity, not an expressive choice.

**Dynamic and reflective authorization.** Several lines of work address the policy-modification axis directly. The Dependency Core Calculus (Abadi, Banerjee, Heintze, Riecke; POPL 1999) and its access-control reading (Abadi; ICFP 2006) provide a typed monadic framework for dependency and authorization. FLAC (Arden, Myers; CSF 2016) extends DCC with dynamic delegation via `assume` terms that admit new trust relationships under information-flow constraints, building on the Flow-Limited Authorization Model (Arden, Liu, Myers; CSF 2015); FLAC targets noninterference and robust declassification rather than witness-monotonicity. Reflective Database Access Control (Olson, Gunter, Madhusudan; CCS 2008) expresses database privileges as queries over the database itself, formalized via Transaction Datalog, making policies reflective over the data they govern. Becker and Nanz (ACM TISSEC 2010) give a logic for state-modifying authorization policies via Transaction Logic, in which access requests can update the authorization state. Each of these addresses dynamics or reflection along a different axis: FLAC on information flow alongside authorization; RDBAC on data-reflexive policies; Becker–Nanz on state-modifying request semantics. None of them is a witness-monotone term calculus in the miniscript sense, and none places the modification under the same evaluation discipline as the operation it authorizes.

**Cryptographic monotone access structures.** A parallel tradition in cryptography uses monotone Boolean formulas and monotone span programs (Karchmer and Wigderson 1993) as access structures in secret sharing, threshold cryptosystems, and attribute-based encryption. The monotonicity property in that tradition serves the same security purpose as ours — preventing absence-of-credential from granting access — but is realized through cryptographic constructions rather than as a property of an evaluated term. The two are complementary: the cryptographic constructions enforce monotone access at the level of secret recovery, while the present calculus enforces it at the level of policy evaluation.

**The rejections cluster.** Strict capability narrowing (capability security, macaroons) and the no-reflection design (Cedar) are derivative of central authority. Narrowing-only is safe because a central authority can reissue capabilities when broader authority is needed; the no-reflection design works because a central authority can re-attribute principals without changing policy text. Neither holds in the deposit setting: no authority can reissue keys a user has lost, so narrowing forecloses recovery; no authority can change a key's attributes without rewriting the policy that names it, so reflection becomes necessary rather than optional.

Information flow control (FLAC) is rejected on different grounds. Decentralized IFC exists and works without central authority (Myers and Liskov's Decentralized Label Model, and the broader DIFC tradition). What this setting lacks is not authority but separation of observers: ledger state is global by construction, observable to the operator, the cosigning quorum, and any party verifying a fraud proof. There are no trust levels to compartmentalize, so the question IFC answers does not arise.

The features we adopt — witness-monotonicity, closed-world expressivity, reflexivity — are exactly the ones that survive these constraints.

We are not aware of prior systems that combine these features into a single decidable, deterministic term language. Each ingredient appears in prior work; the combination is what the calculus contributes — or, equivalently, what the design space requires when authority is cryptographic and user-held rather than centrally administered.

## 5. Why it works

Three observations underpin the design.

**Witness-monotonicity is the property; the polarity rule is the mechanism.** Miniscript guarantees witness-monotonicity by admitting no boolean negation in its grammar — the discipline is enforced by the absence of the relevant constructs. The present calculus admits negation on closed-world data while preserving the same property, by separating proof obligations from state predicates at the sort level and enforcing the positive-position rule on the former. Making the discipline explicit, rather than grammatical, is what permits the generalization.

**Closed-world predicates with negation are admissible at the right leaves.** Cedar establishes that boolean expressivity over closed-world attributes is safe and analyzable. The present calculus admits the same expressivity, restricted to the leaves where m-constancy holds; the polarity rule of §2.4 is the constraint that keeps it there. The structural invariant of §3.1 — m-dependence flows only through positive `prove`, everything else is m-constant — is what makes this work in a witness-monotone setting.

**Reflexive policies are an established design; doing them under witness-monotonicity is what we add.** RDBAC (Olson, Gunter, Madhusudan, 2008) and Becker–Nanz (2010) establish that authorization policies can address and modify themselves. The contribution here is placing modification under the same evaluation discipline as the operations it authorizes, with the system-level invariant of §3.4 maintaining well-formedness across the sequence of terms a deposit's history produces. The direction of modification — narrowing, broadening, or restructuring — is unconstrained: the calculus enforces what the modification guards admit and that the result is well-formed, nothing more. This is a deliberate departure from the capability-security position that derived authorities must be strictly weaker. The departure is forced by the use case: recovery — restoring access after key loss, repairing an overly restrictive descriptor, adding guardians after compromise — requires expansion of authority, and a narrowing-only discipline would foreclose it entirely. The deposit context is one where the term's author bears the consequences of their choices; the correct trade is to give them the full range of modifications rather than a safer-looking subset that prevents the operations they need.

These three observations together yield the calculus: a strict total term language with two sorts of leaves and a polarity rule, that authorizes its own modification under the same evaluation as ordinary operations, and admits closed-world predicates without forfeiting the monotonicity that makes it safe.
