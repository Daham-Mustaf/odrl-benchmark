# Definition Coverage: ODRL210–213 vs ODRL214


From the paper's killer scenario (Table 1, p.2):

```
┌────────────────────────────────────────────────────────────────────┐
│  THE FULL STACK (what needs testing)                              │
├────────────────────────────────────────────────────────────────────┤
│  1. XONE composition (2 branches)                                  │
│  2. AND composition (2 operands per branch × 2 branches)           │
│  3. Multi-operand verdict propagation (purpose × spatial)          │
│  4. Three KB configurations:                                       │
│     - Base DPV (missing negative axiom) → Unknown                  │
│     - Enriched DPV (with negative axiom) → Compatible              │
│     - Aligned GDPR/ISO (partial coverage) → Unknown                │
│  5. Cross-operator usage:                                          │
│     - isNoneOf, isPartOf, isA, eq                                  │
│  6. All formal results:                                            │
│     - Def 1–8, Assm 1–2, Lemma 1–2, Prop 1.1–1.2, Thm 1–2         │
└────────────────────────────────────────────────────────────────────┘
```

---

## What ODRL210–213 Actually Tests

```
ODRL210: Branch A purpose ALONE (no XONE, no spatial)
┌─────────────────────────────────────────────────────────┐
│  Purpose:  isNoneOf{commercial} vs eq scientificResearch│
│  KB:       DPV000 (base)                                 │
│  Verdict:  Unknown (missing negative axiom)              │
│                                                          │
│  ✓ Def 3 (isNoneOf)                                      │
│  ✓ Def 5 (Unknown)                                       │
│  ✗ No XONE                                               │
│  ✗ No AND                                                │
│  ✗ No multi-operand                                      │
└─────────────────────────────────────────────────────────┘

ODRL211-1: Branch A COMPLETE but isolated (no XONE comparison)
┌─────────────────────────────────────────────────────────┐
│  Purpose:  isNoneOf{comm} vs eq sciRes                   │
│  Spatial:  isPartOf wEurope vs eq france                 │
│  KB:       DPV004 + GEO003 (enriched)                    │
│  Verdict:  Compatible (both operands compatible)         │
│                                                          │
│  ✓ Def 6 (AND composition)                               │
│  ✓ Def 3 (multiple operators)                            │
│  ✗ No XONE (Branch A tested ALONE, not vs Branch B)      │
│  ✗ No verdict exclusivity check                          │
└─────────────────────────────────────────────────────────┘

ODRL211-2: Branch B spatial ALONE (partial branch)
┌─────────────────────────────────────────────────────────┐
│  Spatial:  eq germany vs eq france                       │
│  KB:       GEO003                                        │
│  Verdict:  Conflict (UNA)                                │
│                                                          │
│  ✓ Def 3 (eq bidirectional)                              │
│  ✓ Def 5 (Conflict)                                      │
│  ✗ No XONE                                               │
│  ✗ Missing Branch B purpose constraint                   │
│  ✗ Not testing full Branch B vs Request                  │
└─────────────────────────────────────────────────────────┘

ODRL212: Minimal abstract killer (not actual scenario)
┌─────────────────────────────────────────────────────────┐
│  c1: isNoneOf{a}  c2: isNoneOf{b}                        │
│  KB_A: {root,a,b,d}   KB_B: {a',b'}                     │
│  Verdict: Compatible in A, Unknown in B                  │
│                                                          │
│  ✓ Def 8 (strengthened, unmapped witness)                │
│  ✓ Prop 1.2 (graceful degradation)                       │
│  ✗ Not the dataspace scenario (abstract concepts)        │
│  ✗ No XONE                                               │
│  ✗ No multi-operand                                      │
└─────────────────────────────────────────────────────────┘

ODRL213: Cross-KB spatial (single operand)
┌─────────────────────────────────────────────────────────┐
│  Spatial:  isPartOf wEurope vs eq france                 │
│  KB_A: GEO003   KB_B: ISO3166                           │
│  Verdict: Compatible in A, Unknown in B                  │
│                                                          │
│  ✓ Def 7,8 (alignment)                                   │
│  ✓ Prop 1.1,1.2 (conflict preservation, degradation)     │
│  ✗ No XONE                                               │
│  ✗ No multi-operand                                      │
│  ✗ Only tests spatial, missing purpose                   │
└─────────────────────────────────────────────────────────┘
```

---

## What ODRL214 Would Test (Full Integration)

```
ODRL214-1: Base KB (Unknown)
┌──────────────────────────────────────────────────────────────────┐
│  POLICY: xone(                                                   │
│    Branch A: and(purpose isNoneOf{comm}, spatial isPartOf wEu), │
│    Branch B: and(purpose isA comm, spatial eq germany)          │
│  )                                                               │
│  REQUEST: and(purpose eq sciRes, spatial eq france)              │
│                                                                  │
│  KB: DPV000 (no ¬(sciRes ⊑ comm)) + GEO003                      │
│                                                                  │
│  Expected: CounterSat (Unknown)                                  │
│  Reason: Branch A purpose unprovable (missing negative axiom)    │
│                                                                  │
│  ✓ Def 6 (XONE + AND nested)                                     │
│  ✓ Lemma 2 (XONE witness with multi-operand)                     │
│  ✓ All 4 operators (isNoneOf, isPartOf, isA, eq)                 │
│  ✓ Multi-operand verdict propagation                             │
└──────────────────────────────────────────────────────────────────┘

ODRL214-2: Enriched KB (Compatible)
┌──────────────────────────────────────────────────────────────────┐
│  SAME policy and request as 214-1                               │
│                                                                  │
│  KB: DPV004 (WITH ¬(sciRes ⊑ comm)) + GEO003                    │
│                                                                  │
│  Expected: Theorem (Compatible)                                  │
│  Reason: All 4 XONE conditions now provable:                     │
│    - Branch A purpose: sciRes ∈ isNoneOf{comm} ✓                │
│    - Branch A spatial: france ⪯ wEurope ✓                       │
│    - Branch B purpose: sciRes ⊄ comm (conflict) ✓               │
│    - Branch B spatial: france ≠ germany (conflict) ✓            │
│                                                                  │
│  ✓ Shows impact of ONE AXIOM on XONE verdict                     │
│  ✓ Validates Table 3 claim (XONE needs strong axioms)            │
└──────────────────────────────────────────────────────────────────┘

ODRL214-3: Aligned KB (Unknown via degradation)
┌──────────────────────────────────────────────────────────────────┐
│  SAME policy and request as 214-1/2                             │
│                                                                  │
│  KB: GDPR001 (no sciRes!) + ISO3166 (no wEurope!)               │
│  Alignment: DPV→GDPR (partial), GEO→ISO (partial)               │
│                                                                  │
│  Expected: CounterSat (Unknown)                                  │
│  Reason: Multiple constraints → ⊤ via Def 8:                    │
│    - c_branch_a_spatial: westernEurope unmapped → ⊤             │
│    - c_request_purpose: sciRes unmapped → ⊤                     │
│    - c_branch_a_purpose: denotation has unmapped elements → ⊤   │
│                                                                  │
│  ✓ Prop 1.2 (Compatible in 214-2 → Unknown in 214-3)            │
│  ✓ Strengthened Def 8 prevents false Conflict                    │
│  ✓ Full cross-KB scenario with actual taxonomies                 │
└──────────────────────────────────────────────────────────────────┘
```

**Summary:** Tests the COMPLETE stack in ONE scenario across THREE KB configs.

---

## Side-by-Side Coverage Matrix

| What Needs Testing | ODRL210–213 | ODRL214 |
|--------------------|-------------|---------|
| **Structure** |
| XONE composition | ✗ Meta-level only | ✓ Explicit encoding |
| AND composition | ✓ (211-1) | ✓ (4 branches) |
| Multi-operand | Partial (211-1) | ✓ Full (2×2) |
| **Operators** |
| eq | ✓ | ✓ |
| isA | ✗ (only in 085/086) | ✓ |
| isPartOf | ✓ (213) | ✓ |
| isNoneOf | ✓ (210, 212) | ✓ |
| **Knowledge Bases** |
| Base DPV | ✓ (210) | ✓ (214-1) |
| Enriched DPV | ✓ (211) | ✓ (214-2) |
| GDPR taxonomy | ✗ | ✓ (214-3) |
| GeoNames | ✓ (211, 213) | ✓ (214-1/2) |
| ISO 3166 | ✓ (213) | ✓ (214-3) |
| **Verdicts** |
| Unknown (KB gap) | ✓ (210) | ✓ (214-1) |
| Compatible | ✓ (211-1, 212-3) | ✓ (214-2) |
| Conflict | ✓ (211-2, 213-3) | ✓ (implicit in 214-2) |
| Unknown (alignment) | ✓ (212-1, 213-1) | ✓ (214-3) |
| **Formal Results** |
| Def 1–5 | ✓ | ✓ |
| Def 6 (AND) | ✓ | ✓ |
| Def 6 (XONE) | ✗ | ✓ |
| Def 7 (Alignment) | ✓ | ✓ |
| Def 8 (Strengthened) | ✓ | ✓ |
| Lemma 1 (Den. preservation) | ✓ | ✓ |
| **Lemma 2 (XONE witness)** | **✗** | **✓** |
| Prop 1.1 (Conflict preserved) | ✓ | ✓ |
| Prop 1.2 (Graceful degrade) | ✓ | ✓ |
| Thm 1 (Soundness) | ✓ | ✓ |
| Thm 2 (Runtime soundness) | ✓ | ✓ |
| **Scenario** |
| BSB/French Archive | ✗ Pieces only | ✓ Full scenario |
| 3-stage progression | ✗ Separate files | ✓ Same scenario |

---

## The Critical Missing Piece

**ODRL210–213 never tests:**

```
XONE(
  and(operand1_constraint1, operand2_constraint1),
  and(operand1_constraint2, operand2_constraint2)
)
vs
and(operand1_request, operand2_request)
```

This is THE defining structure of the killer scenario!

Without this, you haven't validated:
- ✗ Lemma 2 (XONE witness characterization for multi-operand)
- ✗ Def 6 XONE composition
- ✗ The actual paper scenario




