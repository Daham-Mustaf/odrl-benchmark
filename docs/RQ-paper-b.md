# Strengthening Paper B: KB Grounding Semantics

## Current State: What's Strong
- Denotational semantics for 8 operators (eq, neq, isA, isPartOf,
  hasPart, isAnyOf, isAllOf, isNoneOf)
- Three-valued verdicts (Conflict/Compatible/Unknown) with soundness
- Cross-KB alignment: preservation + graceful degradation
- 154 benchmarks across 6 KB families, Vampire + Z3 agree 100%
- Three semantic domains: taxonomic, mereological, nominal
- Good scenario: BSB + French archive, three escalating challenges
- Composition modes: and/or/xone with Kleene semantics

## What to Add: 8 Improvements

---

### 1. BASELINE COMPARISON WITH EXISTING REASONERS

Problem: You claim existing engines fail. Prove it.

What to do:
- Take 3-4 existing ODRL tools:
  * Steyskal & Polleres evaluator (2015)
  * De Vos et al. compliance checker (2019)
  * Any Eclipse Dataspace Connector policy engine
  * An LLM-based approach (Weyns et al. 2024)

- Run your 154 benchmarks (or a representative subset)
  through each tool.

- Build a comparison table:

  | Tool              | Handles set-ops? | Cross-KB? | Composition? | Correct/154 |
  |-------------------|-----------------|-----------|-------------|-------------|
  | Steyskal (2015)   | No              | No        | No          | 15/154      |
  | De Vos (2019)     | Partial         | No        | No          | 27/154      |
  | EDC engine        | Hardcoded       | No        | Partial     | ??/154      |
  | ODRL-SA (ours)    | All 8           | Yes       | Yes         | 154/154     |

  Even if you can't run all tools, a qualitative feature
  comparison table showing WHICH capabilities each tool
  supports vs. yours would be very strong.

Why it matters:
  Reviewers need to see the delta. "Existing tools fail"
  is a claim. A table showing HOW they fail on YOUR
  benchmarks is evidence.


### 2. SCALABILITY ANALYSIS

Problem: KBs have 1-10 concepts. Real KBs have thousands.

What to do:
- Generate synthetic KBs of increasing size:
  |C| = 10, 50, 100, 500, 1000, 5000

- For each size, run representative benchmark patterns
  (isA conflict, isPartOf compatible, cross-KB alignment)

- Measure wall-clock time for both Vampire and Z3

- Report in a table or figure:

  | |C|   | Vampire (s) | Z3 (s)  | Axioms | Status    |
  |-------|-------------|---------|--------|-----------|
  |    10 |       0.01  |   0.01  |     45 | trivial   |
  |   100 |       0.03  |   0.02  |    420 | fast      |
  |  1000 |       0.15  |   0.08  |   4200 | practical |
  |  5000 |       1.20  |   0.45  |  21000 | feasible  |

- Since you're in EPR (decidable), you can also state
  the theoretical complexity:
  EPR satisfiability is NEXPTIME-complete in general,
  but your fragment (finite domain, no function symbols)
  is likely in NP or PSPACE. Characterise this.

Why it matters:
  Removes the "toy example" objection. Even if large KBs
  are slower, showing they WORK is crucial.


### 3. COMPLEXITY ANALYSIS

Problem: "EPR is decidable" is vague. How decidable?

What to do:
- Count axioms as function of |C|, number of operators,
  number of constraints:
  
  Layer 0 (KB):      O(|C|²) for transitive closure
  Layer 1 (ODRL):    O(1) — fixed operator definitions
  Layer 2 (Ground):  O(|constraints|) — denotation rules
  Total:             O(|C|² + k) where k = #constraints

- State the decision problem formally:
  
  INPUT:  Two ODRL constraints c₁, c₂; KB_ℓ
  OUTPUT: verdict ∈ {Conflict, Compatible, Unknown}
  
  Theorem: The conflict detection problem for single-KB
  reasoning is in coNP (or whatever the actual bound is).

- For cross-KB alignment with two KBs:
  Additional O(|C_A| · |C_B|) for alignment axioms.

Why it matters:
  A complexity result elevates this from "engineering" to
  "computer science." Reviewers at KR/ISWC expect this.


### 4. PROMOTE THE XONE FINDING TO A THEOREM

Problem: Your strongest insight is stated informally
in the composition discussion and shown by two examples.

What to do:
- State it as a formal theorem:

  Theorem (Xone Requires Negative Axioms):
  Let KB be a knowledge base with (C, ≤, γ) containing
  only positive axioms (subsumption assertions x ≤ y).
  For any xone composition with two branches where
  exactly one branch has a positive witness:
  
  verdict_xone = Unknown
  
  regardless of the positive evidence.

  Proof: Under open-world assumption with only positive
  axioms, for witness w with w ≤ g₁ (branch 1), the
  prover cannot derive w ⋢ g₂ (exclude branch 2).
  A model exists where w ≤ g₂, making both branches
  compatible. Hence exclusivity is unprovable. □

  Corollary: verdict_xone = Compatible requires at least
  one explicit negative axiom (disjointness or non-subsumption)
  per excluded branch.

- Add 4-6 more xone benchmarks exploring the boundary:
  * Two branches, both with positive witnesses → Unknown
  * Two branches, one positive + one negative → Compatible
  * Three branches, need TWO negative axioms
  * Nested xone

Why it matters:
  This becomes a publishable insight in its own right.
  It tells KB designers: "if you want xone to work,
  you MUST include disjointness axioms." Practical
  guidance derived from formal analysis.


### 5. FORMAL CONNECTION TO DEONTIC SEMANTICS

Problem: You reason about constraints but ignore that
ODRL constraints live inside permissions/prohibitions.
A constraint conflict inside a permission means something
different from a constraint conflict between a permission
and a prohibition.

What to do:
- At minimum, add a discussion section:

  §X Rule-Level Conflict Detection

  Our framework detects constraint-level conflicts:
  two constraints that cannot be simultaneously satisfied.
  
  In ODRL, constraints appear inside rules (permissions,
  prohibitions, duties). Two levels of conflict arise:
  
  1. Constraint-level: c₁ ∧ c₂ is unsatisfiable
     (this paper)
  
  2. Rule-level: Permission(c₁) conflicts with
     Prohibition(c₂) when their constraints OVERLAP
     (Compatible at constraint level = Conflict at
     rule level for permission/prohibition pairs)
  
  Note the inversion:
  - Constraint Conflict → rules can coexist (they
    never apply to the same situation)
  - Constraint Compatible → rules MAY conflict
    (both apply, but one permits and one prohibits)

  The rule-level analysis is orthogonal to constraint
  grounding and is left to future work, but our
  three-valued verdicts provide the necessary input.

- If you want to go further, add a brief formalization:

  Definition (Rule-Level Verdict):
  For Permission(c₁) and Prohibition(c₂):
  
  rule_verdict =
    Conflict     if verdict(c₁, c₂) = Compatible
    Compatible   if verdict(c₁, c₂) = Conflict
    Unknown      if verdict(c₁, c₂) = Unknown

  This inversion is the key insight connecting
  constraint-level and rule-level analysis.

Why it matters:
  - Shows you understand the bigger picture
  - Addresses the obvious reviewer question:
    "but what about permissions vs prohibitions?"
  - Sets up future work cleanly
  - Connects to deontic logic literature (Hohfeld,
    which you're working on with Guizzardi)


### 6. HANDLE COMPARISON OPERATORS OVER KB OPERANDS

Problem: ODRL allows (purpose, lt, v) — a comparison
operator over a KB operand. Your paper only handles
set-based operators. What happens here?

What to do:
- Classify this formally:

  Proposition (Comparison Operators on KB Operands):
  For ℓ ∈ L_K and ⊲⊳ ∈ {lt, lteq, gt, gteq}:
  the constraint (ℓ, ⊲⊳, v) is well-formed in ODRL
  syntax but semantically ill-typed: KB concept spaces
  have a partial order ≤ (subsumption) but no total
  order compatible with numeric comparison.

  Therefore: ⟦(ℓ, ⊲⊳, v)⟧ = ⊤ for ⊲⊳ ∈ O_cmp and ℓ ∈ L_K.

  This is a principled design choice: rather than
  guessing an ordering, the framework honestly reports
  that it cannot evaluate the constraint.

- Alternative: if the KB provides a total order on
  concepts (e.g., version numbers), comparison operators
  COULD be meaningful. Add a remark:

  Remark: If KB_ℓ is augmented with a total order ≤_T
  compatible with the partial order ≤, then comparison
  operators can be interpreted as interval denotations
  over (C, ≤_T). This bridges KB and dimensional
  semantics but requires domain-specific ordering
  commitments.

Why it matters:
  Shows completeness of operator coverage. Reviewers
  checking the ODRL spec will notice the 4 missing
  operators and ask about them.


### 7. IMPLEMENTATION SKETCH

Problem: No tool. Theory-only papers face skepticism
about practical applicability.

What to do:
- You already have ODRL-SA (your Z3-based tool).
  Add a brief section:

  §X Implementation

  We implement the framework in ODRL-SA, a Python-based
  static analyser that:
  1. Parses ODRL policies (JSON-LD/Turtle)
  2. Loads KB axiom files (Layer 0)
  3. Generates SMT-LIB encodings (Layers 1-2)
  4. Invokes Z3 and interprets results
  5. Reports per-operand verdicts with diagnostics

  Architecture:
  ODRL Policy → Parser → KB Loader → SMT Encoder → Z3 → Verdict

  The tool is available at [repository URL].

- Even if ODRL-SA isn't polished enough for release,
  mentioning it with a "tool available upon request"
  signals practical applicability.

Why it matters:
  Bridges theory and practice. Many top papers at ISWC
  include tool availability. Even a brief section helps.


### 8. STRENGTHEN THE EVALUATION NARRATIVE

Problem: 154 benchmarks is impressive but the evaluation
section reads as a checklist. Tell a story.

What to do:
- Restructure evaluation around RESEARCH QUESTIONS:

  RQ1: Does the denotational semantics correctly capture
       all 8 ODRL operators across all 3 domains?
       → 90 single-KB problems, 100% agreement

  RQ2: Do the three composition modes (and/or/xone)
       produce correct verdicts, including under
       incomplete knowledge?
       → 21 composition problems, xone finding

  RQ3: Does cross-KB alignment preserve conflicts and
       degrade gracefully?
       → 23 alignment problems, zero false conflicts

  RQ4: Do design-time verdicts guarantee runtime
       enforcement?
       → 6 runtime problems

  RQ5: Do independent provers agree? (encoding correctness)
       → 154/154 agreement between Vampire and Z3

- For each RQ, state the hypothesis, the test, and the
  result. This is standard empirical methodology and
  reviewers expect it.

---

## Priority Ranking

If you can only add a few things, prioritize:

1. **Baseline comparison** (#1) — biggest reviewer concern
2. **Xone as theorem** (#4) — strongest unique finding
3. **Research questions** (#8) — structures the evaluation
4. **Scalability** (#2) — removes "toy" objection
5. **Rule-level discussion** (#5) — shows bigger picture
6. **Complexity** (#3) — theoretical depth
7. **Comparison operators** (#6) — completeness
8. **Implementation** (#7) — practical credibility

Items 1, 4, and 8 are easy to add. Items 2 and 3
require some experiments. Item 5 connects to your
Guizzardi/FOIS work and could be a bridge.

---

## Revised Paper B Structure

§1  Introduction (keep, strengthen scenario)
§2  Semantic Grounding Framework
    §2.1 Preliminaries + Type Classification (cite Paper A)
    §2.2 Constraint Interpretation (denotation)
    §2.3 Conflict Detection (three-valued)
    §2.4 Composition (and/or/xone)
§3  Cross-Dataspace Alignment
    §3.1 KB Alignment (definition)
    §3.2 Verdict Preservation + Degradation
    §3.3 Runtime Soundness
§4  The Xone Asymmetry (NEW — promoted from observation to theorem)
    §4.1 Theorem: xone requires negative axioms
    §4.2 Implications for KB design
§5  EPR Encoding
    §5.1 Bidirectional denotation rules
    §5.2 Negated-conjecture pattern
    §5.3 Complexity analysis (NEW)
§6  Evaluation
    §6.1 Research questions (NEW framing)
    §6.2 Benchmark design
    §6.3 Operator coverage (RQ1)
    §6.4 Composition (RQ2) — xone benchmarks expanded
    §6.5 Cross-KB alignment (RQ3)
    §6.6 Runtime soundness (RQ4)
    §6.7 Prover agreement (RQ5)
    §6.8 Scalability (NEW — RQ6)
    §6.9 Comparison with existing tools (NEW — RQ7)
    §6.10 Threats to validity
§7  Discussion
    §7.1 Comparison operators over KB operands (NEW)
    §7.2 Rule-level conflict detection (NEW)
    §7.3 Connection to deontic semantics (NEW)
§8  Related Work
§9  Conclusion
