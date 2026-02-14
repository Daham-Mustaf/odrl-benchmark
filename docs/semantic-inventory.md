Complete inventory.

---

**DEFINITIONS (10)**

| # | Name | Label | Role |
|---|---|---|---|
| 1 | ODRL Constraint | def:constraint | **Input** — defines what you're reasoning about |
| 2 | Knowledge Base | def:kb | **Core** — the structure everything is parameterized by |
| 3 | Constraint Denotation | def:denotation | **Core** — maps syntax to semantics (the central definition) |
| 4 | Conservative Intersection | def:intersection | **Core** — three-valued meet that handles incomplete knowledge |
| 5 | Conflict Detection | def:conflict | **Core** — the main verdict function |
| 6 | Constraint Composition | def:composition | **Core** — lifts single-operand to multi-operand |
| 7 | Constraint Subsumption | def:subsumption | **Extension** — enables refinement/redundancy analysis |
| 8 | KB Alignment | def:alignment | **Cross-dataspace** — formal bridge between KBs |
| 9 | Aligned Constraint | def:constraint-alignment | **Cross-dataspace** — translates constraints across KBs |
| 10 | Execution Context + Satisfaction | def:context, def:satisfaction | **Runtime** — bridges static analysis to runtime enforcement |

---

**THEOREMS (3)**

| # | Name | Label | What it proves |
|---|---|---|---|
| 1 | Soundness | thm:soundness | If Conflict, no value satisfies both constraints — **the central guarantee** |
| 2 | Composition Soundness | thm:composition-soundness | Soundness lifts through and/or/xone — **closes the multi-operand gap** |
| 3 | Runtime Soundness | thm:refined-soundness | Static Conflict implies no runtime context satisfies both — **bridges design-time to runtime** |

---

**LEMMAS (3)**

| # | Name | Label | What it proves |
|---|---|---|---|
| 1 | Disjointness–Order Consistency | lem:disj-consistency | ⊥⊥ and ≤ cannot contradict — **KB well-formedness** |
| 2 | Denotation Preservation | lem:denotation-equality | Alignment commutes with interpretation — **foundation for all cross-KB results** |
| 3 | Conflict Propagation | lem:conflict-propagation | Conflict inherits through subsumption — **enables refinement chains** |

---

**PROPOSITIONS (3)**

| # | Name | Label | What it proves |
|---|---|---|---|
| 1 | Decidability | prop:decidability | Verdict is computable over finite KB — **complexity baseline** |
| 2 | Verdict Preservation | prop:alignment | Conflict preserved under alignment, degradation toward Unknown only — **cross-dataspace safety** |
| 3 | KB Monotonicity | prop:kb-monotonicity | Enriching ⊥⊥ or γ never invalidates existing verdicts — **KB evolution safety** |

---

**COROLLARIES (1)**

| # | Name | Label | What it proves |
|---|---|---|---|
| 1 | Subsumption Preservation | cor:subsumption-preservation | Refinement ordering preserved under alignment — **cross-dataspace refinement** |

---

**ASSUMPTIONS (2)**

| # | Name | Label | What it assumes |
|---|---|---|---|
| 1 | KB Correctness | assm:kb-correctness | ≤ and ⊥⊥ are correct (may be incomplete) — **soundness precondition** |
| 2 | Operand Independence | assm:operand-independence | No cross-operand axioms — **enables modular decomposition** |

---

**DEPENDENCY CHAIN — what proves what:**

```
Assumption 1 (KB Correctness)
  └→ Theorem 1 (Soundness)
       ├→ Theorem 3 (Runtime Soundness)
       └→ Theorem 2 (Composition Soundness)
            └→ Assumption 2 (Operand Independence)

Def 3 (Denotation)
  ├→ Def 5 (Conflict Detection)
  ├→ Def 7 (Subsumption)
  │    └→ Lemma 3 (Conflict Propagation)
  └→ Def 4 (Conservative Intersection)

Lemma 2 (Denotation Preservation)
  ├→ Proposition 2 (Verdict Preservation)
  ├→ Corollary 1 (Subsumption Preservation)
  └→ depends on Def 8 (Alignment)

Lemma 1 (Disjointness–Order Consistency)
  └→ standalone, depends only on Def 2 (KB)

Proposition 3 (KB Monotonicity)
  └→ standalone, depends on Def 5 + Def 4
```

---

**FOR EVALUATION — which results map to benchmark validation:**

| Result | What your benchmarks test |
|---|---|
| Theorem 1 (Soundness) | Every Conflict verdict confirmed by both Vampire and Z3 |
| Theorem 2 (Composition Soundness) | Multi-operand and/or/xone benchmarks |
| Proposition 1 (Decidability) | 100% termination across 154+ problems |
| Theorem 3 (Runtime Soundness) | Not directly tested (theoretical bridge) |
| Proposition 2 (Verdict Preservation) | Cross-KB alignment test cases (if you have them) |
| Proposition 3 (KB Monotonicity) | Testable by running suite before/after ⊥⊥ enrichment |

