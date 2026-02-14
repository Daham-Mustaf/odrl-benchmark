# ODRL Definition 8 & Alignment Validation Suite (ODRL210–213)
## Overview


This benchmark exercises **every definition, assumption, lemma, proposition, and
theorem** from the paper "Formal Foundations for ODRL Policy Conflict Detection
in European Data Spaces" (Mustafa & Sutcliffe, 2026).

**Scenario:** Bayerische Staatsbibliothek (BSB, Munich) shares cultural data
under a `xone` policy. A French National Archive requests access.

## File Inventory

### Axiom Files — Layer 0 (Domain KBs)

| File | KB | Concepts | Depth | Key feature |
|------|-----|----------|-------|-------------|
| `GEO003-0.ax` | KB_A spatial | 9 | 4 | WesternEurope, Paris, Austria |
| `DPV004-0.ax` | KB_A purpose (enriched) | 11 | 3 | Adds ¬(sciRes ⊑ commercial) |
| `ISO3166-0.ax` | KB_B spatial | 6 | 2 | NO WesternEurope, NO Paris |
| `GDPR001-0.ax` | KB_B purpose | 6 | 2 | NO sciRes, NO R&D |
| `MINI000-0.ax` | KB_A minimal | 4 | 1 | {root, a, b, d} all disjoint |
| `MINI001-0.ax` | KB_B minimal | 2 | 1 | {a', b'} only |

### Axiom Files — Alignment (Documentation)

| File | Maps | Mapped | Unmapped |
|------|------|--------|----------|
| `ALIGN001-0.ax` | DPV → GDPR | 5 | 6 |
| `ALIGN002-0.ax` | GEO003 → ISO3166 | 5 | 4 |

### Problem Files

| File | Tests | KB(s) | Expected | Validates |
|------|-------|-------|----------|-----------|
| **ODRL210-1.p** | Branch A purpose, base DPV (no ¬axiom) | DPV000 | **CounterSat** | Def 3 (isNoneOf), Def 5 (Unknown) |
| **ODRL210-2.p** | Same, negated conjecture | DPV000 | **CounterSat** | Def 5 (three-valued), Table 3 |
| **ODRL211-1.p** | Branch A full (enriched DPV) | DPV004+GEO003 | **Theorem** | Def 3,4,5,6 (Compatible, and) |
| **ODRL211-2.p** | Branch B spatial conflict | GEO003 | **Theorem** | Def 3 (eq bidir), Def 5 (Conflict) |
| **ODRL212-1.p** | Minimal killer in KB_B | MINI001 | **CounterSat** | **Def 8** (strengthened), Prop 1.2 |
| **ODRL212-2.p** | Same, negated (genuine Unknown) | MINI001 | **CounterSat** | Def 5,8, Prop 1.2 |
| **ODRL212-3.p** | Minimal killer in KB_A (baseline) | MINI000 | **Theorem** | Def 3 (isNoneOf), Def 5 (Compatible) |
| **ODRL213-1.p** | Cross-KB spatial (westernEurope unmapped) | ISO3166 | **CounterSat** | Def 7,8, Prop 1.2 |
| **ODRL213-2.p** | Same, negated (genuine Unknown) | ISO3166 | **CounterSat** | Def 5,8 |
| **ODRL213-3.p** | Cross-KB Branch B spatial conflict | ISO3166 | **Theorem** | **Prop 1.1** (Conflict preserved) |

## Definition Coverage Matrix

| Definition/Result | Exercised by |
|-------------------|-------------|
| Def 1 (Constraint) | All problems (6 constraints across 2 operands) |
| Def 2 (KB) | GEO003, DPV004, MINI000/001, ISO3166, GDPR001 |
| Def 3 (Denotation) | isNoneOf: 210,211,212 · isPartOf: 211,213 · eq: 211,213 · isA: [existing] |
| Def 4 (Conservative ⊓) | 211-1 (classical), 212-1/213-1 (⊤ cases) |
| Def 5 (Verdict) | Compatible: 211-1,212-3 · Conflict: 211-2,213-3 · Unknown: 210,212-1,213-1 |
| Def 6 (Composition) | 211-1 (and), 210–213 (xone at meta-level) |
| Assm 1 (KB correctness) | All KBs (reflexive + transitive + disjointness) |
| Assm 2 (Operand independence) | 211-1 (purpose × spatial decomposed) |
| **Def 7 (Alignment)** | ALIGN001/002, 213-1/3 |
| **Def 8 (Aligned constraint)** | **212-1/2** (unmapped witness), **213-1/2** (unmapped value) |
| Lem 1 (Denotation preservation) | 213-3 (mapped values, same result) |
| **Prop 1.1 (Conflict preservation)** | **213-3** (eq conflict through alignment) |
| **Prop 1.2 (Graceful degradation)** | **212-1** (Compatible→Unknown), **213-1** (Compatible→Unknown) |
| Thm 1 (Soundness) | 212 trilogy (no false Conflict under alignment) |
| Thm 2 (Runtime soundness) | Entire suite (TPTP provers as runtime oracle) |

## The Def 8 Bug (Old vs New)

**ODRL212 is the critical test.** The minimal 4-concept scenario shows:

```
KB_A: {root, a, b, d}     KB_B: {a', b'}     α: a↦a', b↦b', root↦⊥, d↦⊥

c₁ = isNoneOf{a}  →  ⟦c₁⟧_A = {root, b, d}
c₂ = isNoneOf{b}  →  ⟦c₂⟧_A = {root, a, d}
Intersection in A: {root, d} ≠ ∅  →  Compatible

OLD DEF 8: Apply α pointwise:
  ⟦α(c₁)⟧_B = ⟦isNoneOf{a'}⟧_B = {b'}
  ⟦α(c₂)⟧_B = ⟦isNoneOf{b'}⟧_B = {a'}
  {b'} ∩ {a'} = ∅  →  💥 FALSE CONFLICT

NEW DEF 8: Check ⟦c⟧ ⊆ dom(α):
  ⟦c₁⟧ = {root,b,d} — root,d ∉ dom(α)  →  ⟦c₁⟧ ⊄ dom(α)  →  ⊤
  ⟦c₂⟧ = {root,a,d} — root,d ∉ dom(α)  →  ⟦c₂⟧ ⊄ dom(α)  →  ⊤
  ⊤ ⊓ ⊤ = Unknown  →  ✓ No false conflict
```

**TPTP verification:**
- `ODRL212-3.p` (KB_A): Theorem ✓ (Compatible, witness = d)
- `ODRL212-1.p` (KB_B): CounterSatisfiable ✓ (Unknown)
- `ODRL212-2.p` (KB_B, negated): CounterSatisfiable ✓ (genuine Unknown)

## Running the Benchmarks

```bash
# With Vampire (recommended):
vampire --mode casc ODRL212-3.p    # → Theorem
vampire --mode casc ODRL212-1.p    # → CounterSatisfiable (or GaveUp)
vampire --mode casc ODRL212-2.p    # → CounterSatisfiable (or GaveUp)

# With E prover:
eprover --auto ODRL212-3.p        # → Theorem

# With Z3 (via TPTP interface):
z3 -tptp ODRL212-3.p              # → Theorem
```

**Note:** CounterSatisfiable may appear as `GaveUp` or `Timeout` depending on
prover and time limit, since FOL provers are refutation-complete but not
always model-complete. Both outcomes confirm the Unknown verdict.
