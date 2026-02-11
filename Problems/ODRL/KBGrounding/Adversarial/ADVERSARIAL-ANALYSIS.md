# Adversarial Robustness Analysis

**TPTP-ODRL Benchmark Suite — Attack Tests (ODRL040–045)**

---

## 1. Attack Design

Each attack targets a specific failure mode of the denotational semantics. We classify attacks into three categories:

- **Soundness attacks (S):** Can we get a definite verdict when the answer should be Unknown?
- **Completeness attacks (C):** Can we get Unknown when there IS a definite answer?
- **Composition attacks (X):** Do rules from different operators interact correctly?

| # | Problem | Attack vector | Category | Target | Expected | Z3 | Vampire |
|---|---------|--------------|:---:|---|:---:|:---:|:---:|
| ATK-1 | ODRL040-1 | Reflexive self-overlap | X | eq ∘ eq | Theorem | ✓ | — |
| ATK-2 | ODRL041-1 | Cross-operator overlap | X | isA ∘ isAnyOf | Theorem | ✓ | — |
| ATK-3 | ODRL042-1 | Forced contradiction | X | isA ∘ isNoneOf | Theorem | ✓ | — |
| ATK-4 | ODRL043-1 | Phantom entity | S | isAllOf open-world | CounterSat | ✓ | — |
| ATK-5 | ODRL044-1 | Type guard bypass | S | mereological/taxonomic | CounterSat | ✓ | — |
| ATK-6a | ODRL045-1 | KB gap (missing negative) | C | isNoneOf + open-world | CounterSat | ✓ | — |
| ATK-6b | ODRL045-2 | KB enrichment resolves | C | isNoneOf + enriched KB | Theorem | ✓ | — |

**Result: 7/7 attacks survived. All verdicts match predictions.**

---

## 2. Attack Details

### ATK-1: Reflexive Self-Overlap (Sanity)

**Setup:** `purpose eq academicResearch` vs `purpose eq academicResearch`

**What could go wrong:** If the eq denotation rule doesn't produce a witness when both constraints have the same value, the encoding is fundamentally broken.

**Why it works:** The eq if-direction fires for both constraints with witness X = academicResearch. The negated conjecture forces `~in_denotation(academicResearch, c1) ∨ ~in_denotation(academicResearch, c2)`, but both are derivable → contradiction → Theorem.

**Verdict: Compatible ✓**

---

### ATK-2: Cross-Operator Composition (isA × isAnyOf)

**Setup:**
- c1: `purpose isA researchAndDevelopment` → denotation = {x | x ⊑ R&D}
- c2: `purpose isAnyOf {commercialPurpose, marketing}` → denotation = {x | x ⊑ commPurpose ∨ x ⊑ marketing}

**What could go wrong:** Denotation rules from different operators might not compose — each operator's rules could live in isolation, unable to produce a shared witness.

**Why it works:** commercialResearch is the shared witness:
- For c1: `subClassOf(commercialResearch, researchAndDevelopment)` (DPV fact) → isA if-direction fires
- For c2: `subClassOf(commercialResearch, commercialPurpose)` (DPV DAG) → isAnyOf if-direction fires

The two operators produce independent `in_denotation` facts that the conjunction picks up.

**Verdict: Compatible ✓ — Operators compose correctly**

---

### ATK-3: Cross-Operator Contradiction (isA vs isNoneOf)

**Setup:**
- c1: `purpose isA researchAndDevelopment` → only-if forces `subClassOf(X, R&D)`
- c2: `purpose isNoneOf {researchAndDevelopment}` → only-if forces `~subClassOf(X, R&D)`

**What could go wrong:** Only-if rules from different operators might not compose. If the prover can't derive the contradiction `subClassOf(X, R&D) ∧ ~subClassOf(X, R&D)`, a spurious CounterSat model would give false Unknown.

**Why it works:** Any witness X would need to satisfy both only-if consequences simultaneously. The isA only-if forces `subClassOf(X, R&D)` and the isNoneOf only-if forces `~subClassOf(X, R&D)`. Direct logical contradiction — no model exists.

**Verdict: Conflict ✓ — Only-if rules compose across operators**

**Paper significance:** This validates that the bidirectional encoding (Section 4.3 of README) is essential. Without only-if rules, neither operator would constrain the witness, and the prover would find a spurious model.

---

### ATK-4: Phantom Entity via Impossible isAllOf (Most Critical)

**Setup:**
- c1: `purpose isAllOf {commercialPurpose, nonCommercialPurpose}` — requires membership in BOTH branches
- c2: `purpose eq commercialResearch`

**What could go wrong:** In open-world FOL, nothing prevents a Skolem constant from satisfying `subClassOf(sk, commercialPurpose) ∧ subClassOf(sk, nonCommercialPurpose)`. If the prover invents such a phantom entity, it would produce a false Compatible for policies that should have no overlap.

**Why it doesn't happen:** The compatibility conjecture is `∃X(denot(X,c1) ∧ denot(X,c2))`. To prove this (Theorem), the prover must find a *concrete* witness. The eq constraint pins X = commercialResearch. Then the isAllOf if-direction requires:
```
subClassOf(commercialResearch, commercialPurpose) ∧ subClassOf(commercialResearch, nonCommercialPurpose)
```
The first holds (DPV fact). The second does NOT hold and is NOT derivable. No contradiction arises from the negated conjecture — the prover simply finds a consistent model where `in_denotation(commercialResearch, c1) = false`.

**Key insight:** The eq constraint on c2 acts as a *grounding anchor* — it pins the witness to a named entity, preventing phantom Skolem entities from satisfying the compatibility test. For the general case (both constraints are non-eq), the open-world correctly yields Unknown.

**Verdict: Unknown ✓ — No phantom entities created**

---

### ATK-5: Operand Type Guard Bypass

**Setup:**
- c1: `purpose isPartOf researchAndDevelopment` — WRONG operator (isPartOf is mereological)
- c2: `purpose eq academicResearch`

**What could go wrong:** If the `mereological(L)` type guard in the isPartOf denotation rule doesn't work, the rule would fire for `purpose` (which is `taxonomic`), treating `subClassOf` subsumption as `partOf` containment. This would give a false Compatible because academicResearch IS a subconcept of R&D.

**Why it works:** The isPartOf if-direction requires `mereological(L)` as a precondition:
```
has_operand(c1, purpose) ∧ has_operator(c1, isPartOf) ∧ mereological(purpose) ∧ ...
```
But the axiom base only asserts `taxonomic(purpose)`, NOT `mereological(purpose)`. The precondition fails → the rule never fires → denotation of c1 is empty → no overlap possible.

**Verdict: Unknown ✓ — Type guard holds**

**Paper significance:** The operand typing system (`mereological`/`taxonomic`) is not just documentation — it's load-bearing in the formal semantics. A policy author using the wrong operator gets a conservative Unknown rather than a false positive.

---

### ATK-6: isNoneOf + KB Gap (The Paper's Core Finding)

**ATK-6a — Missing Negative Fact (ODRL045-1)**

**Setup:**
- c1: `purpose isNoneOf {commercialPurpose}` → everything NOT under commercialPurpose
- c2: `purpose eq scientificResearch`

**Real-world truth:** scientificResearch ⊑ R&D, NOT ⊑ commercialPurpose → **Compatible**

**What happens:** The DPV KB lacks `~subClassOf(scientificResearch, commercialPurpose)`. The isNoneOf if-direction requires this negative fact to fire. Without it:

1. Negated conjecture forces `~in_denotation(scientificResearch, c1)`
2. Contrapositive of isNoneOf if-direction: forces `subClassOf(scientificResearch, commercialPurpose)`
3. This is *consistent* with the KB (no negative fact prevents it)
4. Model found → CounterSat → **Unknown**

**Verdict: Unknown (false negative) ✓ — Conservative but incomplete**

**ATK-6b — KB Enrichment Resolves (ODRL045-2)**

**Same setup** but with one added axiom: `~subClassOf(scientificResearch, commercialPurpose)`

**What happens:**

1. Negated conjecture forces `subClassOf(scientificResearch, commercialPurpose)` (same as above)
2. But the enriched KB asserts `~subClassOf(scientificResearch, commercialPurpose)`
3. **Contradiction** → Refutation → Theorem → **Compatible**

**Verdict: Compatible ✓ — KB enrichment resolves the gap**

**Paper significance:** This pair (045-1 → 045-2) demonstrates the entire paper workflow:
1. Run analysis → Unknown (KB gap)
2. Identify which negative fact is missing
3. Enrich KB → rerun → definite verdict
4. The 76% Unknown reduction in the paper's evaluation comes exactly from this pattern

---

## 3. Correctness Argument (Sketch)

The attack results, combined with the architecture, support the following correctness claims:

### Claim 1: Soundness of Compatible verdicts

**Statement:** If the framework returns Compatible, then there exists a domain entity that satisfies both constraints under the given KB.

**Argument:** A Compatible verdict requires SZS Theorem for the conjecture `∃X(denot(X,c1) ∧ denot(X,c2))`. The proof must derive a contradiction from the negation `∀X: ~denot(X,c1) ∨ ~denot(X,c2)`. This requires:
- The if-direction to populate denotations from KB facts
- A named witness that satisfies both if-directions
- ATK-4 confirms: Skolem phantoms cannot produce false Compatibles because the negated conjecture is universal — the prover must derive contradiction for ALL potential witnesses, not just invent one

### Claim 2: Soundness of Conflict verdicts

**Statement:** If the framework returns Conflict, then no domain entity can satisfy both constraints under the given KB.

**Argument:** A Conflict verdict requires SZS Theorem for `~∃X(denot(X,c1) ∧ denot(X,c2))`. The proof derives a contradiction from the Skolemized witness `denot(sk,c1) ∧ denot(sk,c2)`. This requires:
- Only-if rules to extract domain constraints from `in_denotation`
- KB facts (especially negative facts and disjointness) to contradict the extracted constraints
- ATK-3 confirms: only-if rules compose across operators to produce contradictions
- ATK-5 confirms: type guards prevent false conflicts from operator misuse

### Claim 3: Conservatism of Unknown

**Statement:** If the framework returns Unknown, then the KB is genuinely incomplete — there exists both a model where the constraints overlap and a model where they don't.

**Argument:** Unknown means the negated conjecture is CounterSatisfiable — the prover found a consistent model where no overlap exists. But the original conjecture is also not provable. This is precisely the semantic gap:
- ATK-6a confirms: missing negative facts produce Unknown (not false Compatible)
- ATK-6b confirms: adding the missing fact resolves to a definite verdict
- The open-world semantics ensures no closed-world assumptions leak in

### The Bidirectional Invariant

The if-direction and only-if direction serve complementary roles:

| Direction | Proves | Used for | Consequence of omission |
|---|---|---|---|
| if | `KB facts → in_denotation` | Compatible proofs | False Unknown (ATK-6a pattern) |
| only-if | `in_denotation → KB constraints` | Conflict proofs | False Unknown (ODRL013-1 discovery) |

Both directions are necessary. Neither alone is sufficient. The isAnyOf Skolem explosion (v0.3.0 → v0.3.1) shows that even correct only-if rules can be computationally intractable, requiring per-problem grounding for set operators.

---

## 4. Summary

| Property | Evidence | Key attack |
|---|---|---|
| Compatible verdicts are sound | Witnesses are concrete KB entities, not phantoms | ATK-4 |
| Conflict verdicts are sound | Only-if rules compose across operators | ATK-3 |
| Type guards prevent cross-domain errors | mereological/taxonomic distinction is load-bearing | ATK-5 |
| Open-world is conservative | Missing facts → Unknown, not false verdict | ATK-6a |
| KB enrichment resolves gaps | Adding negative facts → definite verdict | ATK-6b |
| Operators compose correctly | Different operators share witnesses | ATK-2 |
| Bidirectional rules are both necessary | Omitting either direction → false Unknown | ATK-3 + ATK-6a |

**No attack succeeded.** The semantics is robust.
