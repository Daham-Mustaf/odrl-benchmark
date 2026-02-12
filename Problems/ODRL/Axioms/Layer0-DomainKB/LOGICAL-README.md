# Logical Composition Benchmarks (ODRL 030–033, 080–088)

ODRL groups constraints using `and`, `or`, and `xone`. These benchmarks test all three.

## AND (030–033) — Conjunctive Semantics

All operand pairs must overlap simultaneously. Located in `CrossKB/`.

| Problem | Spatial | Purpose | Overall | SZS |
|---------|---------|---------|---------|-----|
| 030 | Compatible | Compatible | **Compatible** | Theorem |
| 031 | Compatible | Unknown | **Unknown** | CounterSat |
| 032 | Conflict | Conflict | **Conflict** | Theorem |
| 033 | Conflict | Compatible | **Unknown** | CounterSat |

Conjecture: `∃X(d(X,s₁)∧d(X,s₂)) ∧ ∃Y(d(Y,p₁)∧d(Y,p₂))`

## OR (080–084) — Disjunctive Semantics

At least one branch must overlap. One conflict dimension does not block if another branch succeeds.

| Problem | Test | SZS | Key |
|---------|------|-----|-----|
| 080 | or(isA de, isA ar) vs eq arz | Theorem | Second branch: arz ⊑ ar |
| 081 | or(isA de, isA en) vs eq fr | Theorem | Neither branch → Conflict |
| 082 | or(isA nonComm, isA mkt) vs eq sciRes | CounterSat | Both indeterminate → Unknown |
| 083 | spatial AND or(purpose) | Theorem | Cross-DS composition |
| 084 | spatial AND or(purpose) blocked | CounterSat | OR purpose unknown blocks |

Conjecture: `∃X(d(X,c₁)∧d(X,c₃)) ∨ ∃Y(d(Y,c₂)∧d(Y,c₃))`

## XONE (085–088) — Exclusive-Or Semantics

Exactly one branch must overlap. Requires **explicit disjointness** in KB.

| Problem | Test | SZS | Key |
|---------|------|-----|-----|
| 085 | xone(comm, nonComm) vs nonCommRes | Theorem | Exactly one branch + explicit ¬⊑ |
| 086 | xone(comm, nonComm) vs commRes | CounterSat | **Missing ¬⊑ in KB** → Unknown |
| 087 | xone(R&D, nonComm) vs nonCommRes | CounterSat | Both branches hold → violates xone |
| 088 | xone(isA de, isA en) vs eq fr | Theorem | Neither branch → Conflict |

Conjecture: `∃X(d(X,c₁)∧¬d(X,c₂)∧d(X,c₃)) ∨ ∃Y(d(Y,c₂)∧¬d(Y,c₁)∧d(Y,c₃))`

### Key Finding: XONE Requires Stronger KB Axioms

Compare 085 vs 086: both test `xone(commercial, nonCommercial)` but with different request values.

- **085** (nonCommRes): KB has explicit `¬subClassOf(nonCommRes, commercial)` → prover confirms exclusivity → **Theorem**
- **086** (commRes): KB lacks `¬subClassOf(commRes, nonCommercial)` → open world allows dual membership → **CounterSat**

AND and OR work with whatever the KB provides. XONE additionally needs **negative axioms** to rule out the other branch — a strictly stronger requirement.

## Validation

All 13 problems: 100% Vampire/Z3 agreement.

```bash
cd Problems/ODRL
for f in KBGrounding/LogicalOr/*.p KBGrounding/LogicalXone/*.p KBGrounding/CrossDataspace/*.p; do
  result=$(vampire --mode casc -t 10 "$f" 2>&1 | grep "SZS status" | awk '{print $4}')
  printf "%-15s %s\n" "$(basename $f .p)" "$result"
done
```
