
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

## **Summary Table:**

| **Axiom/Property** | **Paper Ref** | **Tested?** | **Priority** |
|---|---|---|---|
| KB Alignment | Def 8, Lemma 3, Prop 2, Cor 1 | ❌ | **HIGH** |
| KB Monotonicity | Prop 3 | ❌ | **HIGH** |
| Runtime Soundness | Thm 3 | ❌ | **HIGH** |
| ⊤ handling | Def 3, 4, 5 | ❌ | **MEDIUM** |
| Disjointness downward closure (direct) | Def 2 | ⚠️ implicit | **MEDIUM** |
| Nominal domain (6 operands) | Def 2 | ❌ | **MEDIUM** |
| Taxonomic (5 operands) | Def 2 | ❌ | **LOW** |
| virtualLocation | Def 2 | ❌ | **LOW** |
| DAG-safe disjointness | Note 1 | ❌ | **LOW** |

**Recommendation:** Add 10-15 problems covering alignment (HIGH priority) and nominal domains (MEDIUM priority) to strengthen your empirical validation of the theoretical framework.