
## **Major gaps:**

### 1. **Cross-Dataspace Alignment (Section 3.3)**
**Missing tests:**
- Definition 8 (KB Alignment) - order-preserving mappings
- Lemma 3 (Denotation Preservation) - `⟦α(c)⟧ = α(⟦c⟧)`
- Proposition 2 (Verdict Preservation) - conflict preservation across KBs
- Corollary 1 (Subsumption Preservation) - `c₁ ⊑ c₂ in KB_A → α(c₁) ⊑ α(c₂) in KB_B`

**Why critical:** Your paper claims "alignment can only weaken verdicts toward Unknown, never fabricate conflicts" (Prop 2.2) - this needs empirical validation with real KB pairs (e.g., GeoNames ↔ ISO 3166).

### 2. **KB Monotonicity (Proposition 3)**
**Missing tests:**
- Extending disjointness `⊥⊥ ⊆ ⊥⊥⁺` preserves verdicts
- Extending grounding `γ ⊆ γ⁺` resolves Unknown to definite verdicts

**Test idea:** Take a problem yielding Unknown (unmapped value), add grounding axiom, verify it resolves to Conflict or Compatible.

### 3. **Runtime Semantics (Section 3.2.1)**
**Missing tests:**
- Definition 9 (Execution Context) - concrete value assignment
- Definition 10 (Constraint Satisfaction) - `ω ⊨ c`
- Theorem 3 (Runtime Soundness) - static Conflict → no runtime ω satisfies both

**Why important:** This bridges your static analysis to actual policy enforcement. Need tests showing "if static detector says Conflict, no runtime request can satisfy both."

### 4. **⊤ (Top/Unknown) Handling**
**Missing tests:**
- Constraints with `γ(v) = ⊥` (unmapped values)
- Conservative intersection `⊤ ⊓ D = ⊤`
- Verdict degradation to Unknown

**Test idea:** 
```
ODRL070: permission spatial isPartOf <unmapped_value>
         prohibition spatial eq germany
Expected: Unknown (not Conflict, not Compatible)
```

### 5. **Disjointness Axioms - Direct Tests**
**Missing tests:**
- **Symmetry:** `disjoint(X,Y) → disjoint(Y,X)` (used implicitly, never tested)
- **Irreflexivity:** `¬disjoint(X,X)` (tested via contradiction in 015, but not directly)
- **Downward closure:** Your test suite relies on this heavily but never tests it in isolation

**Test idea:**
```
ODRL071: Given disjoint(westernEurope, easternEurope)
         Prove disjoint(germany, poland)  [downward closure]
Expected: Theorem
```

### 6. **Nominal Domain Semantics**
**Missing operands:** `deliveryChannel`, `device`, `event`, `product`, `system`, `unitOfCount`

Your paper says (Def 2): "Under identity, isA degenerates to eq and isAllOf requires all values to coincide."

**Test idea:**
```
ODRL072: permission device eq "mobile"
         prohibition device isA "mobile"
Expected: Compatible (both denote {mobile} under nominal semantics)

ODRL073: permission device isAllOf {laptop, mobile}
Expected: Conflict (no single device equals both - nominal ⊥⊥ is total)
```

### 7. **Other Taxonomic Domains**
**Missing operands:** `language`, `industry`, `fileFormat`, `media`, `recipient`

You test `purpose` extensively (via DPV) but never test other taxonomic domains.

### 8. **Mereological Domain Beyond Spatial**
**Missing operand:** `virtualLocation`

Your paper lists this as mereological (part-whole) but you only test `spatial`.

### 9. **Composition Meta-Theorem**
**Partially missing:** Theorem 2 (Composition Soundness) is tested via *examples* (040-047) but the meta-property isn't validated:

**Test idea:** Encode Theorem 2 itself as a TPTP problem:
```
ODRL074: Given verdict_and(spatial, purpose) = Conflict
         Prove: ¬∃ω : (ω ⊨ c1_spatial ∧ ω ⊨ c1_purpose 
                      ∧ ω ⊨ c2_spatial ∧ ω ⊨ c2_purpose)
```

### 10. **DAG-Safe Disjointness (Note 1)**
**Missing validation:** Your Note on DAG Structure describes the multi-parent problem in DPV but doesn't test:
- Whether naive sibling disjointness causes inconsistency
- Whether DAG-safe generation (suppressing 6 of 285 pairs) resolves it

**Test idea:**
```
ODRL075: Load DPV with NAIVE sibling disjointness
         Conjecture: leq(commercialResearch, researchAndDevelopment)
         Expected: Inconsistency (or Theorem via contradiction)

ODRL076: Load DPV with DAG-SAFE disjointness  
         Same conjecture
         Expected: Theorem (consistent)
```

---
## Weakest Problems

**ODRL141** (single-concept KB) — `leq(universe, universe)` is trivially satisfiable in one step. Pure sanity check, zero reasoning depth.

**ODRL104** (naive ablation) — the KB is already inconsistent from ODRL100, so this just re-proves ⊥ → anything. Adds nothing over ODRL100 except pedagogically.

**ODRL140/142** (eq ∩ neq) — tautological by definition. The prover just unfolds `den_eq_if` + `den_neq_onlyif` and gets a contradiction immediately. Loading 24 concepts in 142 doesn't change the proof path.

**ODRL143** (reflexivity) — one-step: `leq_refl` → `den_isPartOf_if`. Done.

**ODRL114** (isAllOf compatible) — wE ≤ europe makes the intersection trivially = ↓wE.

These are all Easy-rated intentionally — they serve as baselines and sanity checks — but they don't stress any prover.

## What's NOT Tested

This is more important:

**Temporal constraints** — ODRL has `dateTime`, `before`, `after`, `during` left operands. We have zero temporal KB. This is a whole dimension of policy conflict (e.g., permission valid 2024–2025 vs prohibition valid 2025–2026 → overlap in 2025).

**Numeric/arithmetic constraints** — `count ≤ 5` vs `count > 3`, `payAmount`, `percentage`. Needs theory reasoning (LIA/LRA), not pure FOL. Big gap.

**Action hierarchy** — every problem uses `odrl:use`. ODRL defines `play`, `display`, `distribute`, `modify` etc. with subsumption (`use` ⊇ `play`). Action conflict (permission to `play` vs prohibition to `use`) isn't tested.

**OR composition** — we test AND (Theorem 2: one Conflict operand → composed Conflict). OR composition has different semantics (one Compatible → composed Compatible). Not covered.

**Duty/obligation semantics** — all problems are permission vs prohibition. ODRL duties attached to permissions (e.g., "permission to use IF you attribute") are a distinct deontic pattern. Untested.

**Party/assignee constraints** — `assignee isA dpv:DataProcessor` vs `assignee eq acme:Corp`. Organizational hierarchies for parties aren't modeled.

**Runtime + alignment** — Cat 8 tests runtime (single-KB), Cat 14 tests alignment (no runtime). The combination — runtime satisfaction checking across aligned dataspaces — isn't tested.

**n-way policy conflicts** — everything is pairwise (policyA vs policyB). Real dataspaces may have 3+ conflicting policies simultaneously.

**Large-scale KB stress** — GEO has 24 concepts, DPV fragment has 6. Real DPV Purpose taxonomy has 100+. No scalability stress test with hundreds of concepts.

**Mixed set operators across alignment** — e.g., `isAnyOf({dE, fR})` in ISO vs `isNoneOf({zoneEast})` in SYNTH through alignment. Set operators + multi-hop together aren't combined.

## Recommendation

The biggest gaps by impact are **temporal** and **numeric** — these are what real ODRL policies use most. But they require fundamentally different axiomatization (temporal intervals, arithmetic theories) that may be out of scope for a pure FOL TPTP benchmark. Worth flagging as future work in the submission though.

