# Reality Check: ODRL210–213 vs. The Killer Scenario

## What You CLAIM (from your paper's intro scenario)

**The Full Killer Benchmark** (Table 1, p.2):

```
BSB Policy (Munich):
  xone(
    Branch A: and(
      purpose isNoneOf {commercial},
      spatial isPartOf westernEurope
    ),
    Branch B: and(
      purpose isA commercial,
      spatial eq germany
    )
  )

French Archive Request:
  and(
    purpose eq scientificResearch,
    spatial eq france
  )

Expected verdicts:
  KB_A (base DPV):      Unknown (sciRes position unclear)
  KB_A (enriched DPV):  Compatible (Branch A holds, B conflicts)
  KB_B (GDPR/ISO3166):  Unknown (unmapped witnesses)
```

**This exercises:**
- ✓ XONE with 2 branches (Def 6)
- ✓ AND within each branch (Def 6)
- ✓ Multi-operand composition (purpose × spatial)
- ✓ All three verdict states (Unknown → Compatible → Unknown)
- ✓ Cross-KB alignment (Def 7, 8, Prop 1)
- ✓ Enrichment revealing conflict (negative axiom addition)

**Total constraints:** 6 (2 per branch × 2 branches + 2 request)
**Total operands:** 2 (purpose, spatial)
**Total KBs:** 4 (DPV base, DPV enriched, GDPR, ISO3166)

---

## What You ACTUALLY TEST (ODRL210–213)

### ODRL210: Isolated Branch A Purpose Check
```
Constraint: purpose isNoneOf {commercial}
Request:    purpose eq scientificResearch
KB:         DPV base (no negative axiom)
Expected:   Unknown

EXERCISES: Def 3 (isNoneOf), Def 5 (Unknown)
DOES NOT EXERCISE: 
  ✗ XONE composition
  ✗ AND composition
  ✗ Multi-operand
  ✗ Cross-KB alignment
```

### ODRL211: Branch A/B Separately (NOT XONE)
```
File 211-1: Branch A in enriched KB
  Constraints: purpose isNoneOf {comm} AND spatial isPartOf wEurope
  Request:     purpose eq sciRes AND spatial eq france
  Expected:    Compatible (and of two compatible)

File 211-2: Branch B spatial conflict
  Constraint:  spatial eq germany
  Request:     spatial eq france
  Expected:    Conflict

EXERCISES: Def 6 (and), Def 3 (multiple operators)
DOES NOT EXERCISE:
  ✗ XONE composition (tests branches INDEPENDENTLY!)
  ✗ Def 6 XONE semantics
  ✗ Exclusive composition requiring both Compatible AND Conflict
```

### ODRL212: Minimal Abstract Killer
```
KB_A: {root, a, b, d}
KB_B: {a', b'}
c1 = isNoneOf{a}  c2 = isNoneOf{b}

EXERCISES: Def 8 (strengthened), Prop 1.2 (graceful degradation)
DOES NOT EXERCISE:
  ✗ Actual dataspace scenario
  ✗ Real KB hierarchies (DPV, GeoNames)
  ✗ XONE composition
  ✗ Multi-operand
```

### ODRL213: Cross-KB Spatial
```
Constraint: spatial isPartOf westernEurope
Request:    spatial eq france
KB_A:       GEO003 (has westernEurope)
KB_B:       ISO3166 (no westernEurope)

EXERCISES: Def 7, 8, Prop 1.1, 1.2
DOES NOT EXERCISE:
  ✗ Multi-operand composition
  ✗ XONE composition
  ✗ Purpose constraints
```

---

## THE CRITICAL GAP

**NONE of your ODRL210–213 files encode the actual XONE composition!**

You test:
- ✓ Individual branches in isolation
- ✓ AND within a branch
- ✓ Cross-KB alignment per operand

You DON'T test:
- ✗ XONE(Branch_A, Branch_B) with verdict composition
- ✗ Multi-dimensional verdict propagation (purpose × spatial through XONE)
- ✗ The three-stage progression (Unknown → Compatible → Unknown)

---

## What a REAL Killer Benchmark Looks Like

### ODRL214-1.p: Full Killer (Base DPV, KB_A)

```tptp
%------------------------------------------------------------------------------
% File     : ODRL214-1.p
% Problem  : Full BSB/French killer scenario in base DPV KB
% Expected : CounterSatisfiable (Unknown due to missing negative axiom)
%------------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').      % Base DPV (no sciRes disjointness)
include('Axioms/Layer0-DomainKB/GEO003-0.ax').      % GeoNames with westernEurope
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').     % Operator semantics
include('Axioms/Layer2-Grounding/GROUND000-1.ax'). % Grounding layer

% --- BRANCH A: and(purpose isNoneOf {comm}, spatial isPartOf wEurope) ---
fof(branch_a_purpose, axiom,
    has_operand(c_a_purp, purpose) &
    has_operator(c_a_purp, isNoneOf) &
    has_value(c_a_purp, commercial)).

fof(branch_a_spatial, axiom,
    has_operand(c_a_spat, spatial) &
    has_operator(c_a_spat, isPartOf) &
    has_value(c_a_spat, westernEurope)).

% --- BRANCH B: and(purpose isA comm, spatial eq germany) ---
fof(branch_b_purpose, axiom,
    has_operand(c_b_purp, purpose) &
    has_operator(c_b_purp, isA) &
    has_value(c_b_purp, commercial)).

fof(branch_b_spatial, axiom,
    has_operand(c_b_spat, spatial) &
    has_operator(c_b_spat, eq) &
    has_value(c_b_spat, germany)).

% --- REQUEST: and(purpose eq sciRes, spatial eq france) ---
fof(request_purpose, axiom,
    has_operand(c_r_purp, purpose) &
    has_operator(c_r_purp, eq) &
    has_value(c_r_purp, scientificResearch)).

fof(request_spatial, axiom,
    has_operand(c_r_spat, spatial) &
    has_operator(c_r_spat, eq) &
    has_value(c_r_spat, france)).

% --- XONE CONJECTURE (per Lemma 2) ---
% Branch A holds exclusively: both operands compatible + Branch B conflicts
fof(xone_branch_a, conjecture,
    % Purpose: sciRes in isNoneOf{comm} denotation
    (?[P]: (in_denotation(P, c_a_purp) & in_denotation(P, c_r_purp)))
    % AND spatial: france in isPartOf wEurope denotation
    & (?[S]: (in_denotation(S, c_a_spat) & in_denotation(S, c_r_spat)))
    % AND Branch B purpose conflicts (sciRes NOT in isA comm)
    & (~?[P2]: (in_denotation(P2, c_b_purp) & in_denotation(P2, c_r_purp)))
    % AND Branch B spatial conflicts (france != germany)
    & (~?[S2]: (in_denotation(S2, c_b_spat) & in_denotation(S2, c_r_spat)))).
```

**Expected Vampire result:**
```
% SZS status CounterSatisfiable for ODRL214-1
```

**Why Unknown:**
- Branch A purpose: Can't prove sciRes ∈ isNoneOf{comm} (missing negative axiom)
- Even though spatial compatible and Branch B conflicts, XONE requires ALL of Branch A to hold
- First conjunct fails → entire formula unprovable

---

### ODRL214-2.p: Full Killer (Enriched DPV, KB_A)

Same encoding but:
```tptp
include('Axioms/Layer0-DomainKB/DPV004-0.ax').  % Enriched DPV with ¬(sciRes ⊑ comm)
```

**Expected Vampire result:**
```
% SZS status Theorem for ODRL214-2
```

**Why Compatible:**
- Branch A purpose: Now sciRes ∈ isNoneOf{comm} is PROVABLE ✓
- Branch A spatial: france ⊑ westernEurope ✓
- Branch B purpose: sciRes ⊄ commercial (explicit) ✓
- Branch B spatial: france ≠ germany ✓
- All four conjuncts satisfied → Theorem

---

### ODRL214-3.p: Full Killer (GDPR/ISO3166, KB_B)

```tptp
include('Axioms/Layer0-DomainKB/GDPR001-0.ax').     % No sciRes concept
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').     % No westernEurope concept
include('Axioms/Layer3-Alignment/ALIGN001-0.ax').  % DPV→GDPR alignment (partial)
include('Axioms/Layer3-Alignment/ALIGN002-0.ax').  % GEO→ISO alignment (partial)
```

**Key differences:**
- `scientificResearch` unmapped → γ_B(sciRes) = ⊥ → ⟦c_r_purp⟧_B = ⊤
- `westernEurope` unmapped → γ_B(wEurope) = ⊥ → ⟦c_a_spat⟧_B = ⊤

Per strengthened Def 8:
- Branch A spatial: ⟦c_a_spat⟧_A has {wEurope, france, germany, austria, paris}
  - But {wEurope, paris, austria} ∉ dom(α_spatial)
  - → ⟦c_a_spat⟧_A ⊄ dom(α)
  - → α(c_a_spat) = ⊤

**Expected result:**
```
% SZS status CounterSatisfiable for ODRL214-3
```

**Why Unknown:**
- Multiple ⊤ denotations prevent proving the XONE conjecture
- Graceful degradation (Prop 1.2): Compatible in KB_A → Unknown in KB_B ✓

---

## Coverage Comparison

| Definition/Result | ODRL210–213 | ODRL214 |
|-------------------|-------------|---------|
| Def 6 (AND) | ✓ (211-1) | ✓ (all branches) |
| Def 6 (XONE) | ✗ Meta-level only | ✓ Explicit encoding |
| Lemma 2 (XONE witness) | ✗ Not tested | ✓ Validated |
| Multi-operand composition | Partial (1 file) | ✓ Full (2 operands × 2 branches) |
| Three-stage progression | ✗ Separate files | ✓ Single scenario |
| Prop 1.1 (Conflict preservation) | ✓ (213-3) | ✓ (214-2 vs 214-3) |
| Prop 1.2 (Graceful degradation) | ✓ (212-1, 213-1) | ✓ (214-2 vs 214-3) |
| Strengthened Def 8 | ✓ (212 minimal) | ✓ (actual dataspace KBs) |

---

## Bottom Line

**ODRL210–213 is NOT the killer benchmark.**

It's a **minimal validation suite** that tests the Def 8 fix in isolation, but doesn't actually encode the BSB/French Archive scenario you trace through in detail in the paper and the ASCII art I reviewed.

**To claim "killer benchmark" you need ODRL214 (three variants):**
1. Base KB → Unknown
2. Enriched KB → Compatible  
3. Aligned KB → Unknown (graceful degradation)

This is **one scenario, three KB configurations**, validating the full stack.

---

## Recommendation

Either:

**Option A:** Rename ODRL210–213
- Call it "Alignment Test Suite" or "Def 8 Validation Suite"
- Add ODRL214 as the actual "Killer Benchmark"
- Keep both (210–213 for unit tests, 214 for integration test)

**Option B:** Expand ODRL211
- Merge Branch A and Branch B into XONE encoding (not separate files)
- Add the explicit XONE verdict composition
- Keep 210, 212, 213 as supporting unit tests

**Option C:** Accept the limitation
- Acknowledge that ODRL210–213 validates pieces but not the full scenario
- Note that full XONE with multi-operand composition is left for future work
- Focus on Def 8 fix as the main contribution

I recommend **Option A** - add ODRL214 as a true integration test while keeping 210–213 for targeted validation.
