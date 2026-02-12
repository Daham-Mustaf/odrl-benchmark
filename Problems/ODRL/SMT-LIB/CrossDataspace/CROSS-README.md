# Cross-Dataspace Benchmarks (ODRL030–033, 055–056)

**Validates:** Paper title claim — "Across Dataspaces"

## Motivation

Single-domain benchmarks test isolated KB reasoning. Cross-dataspace problems validate that policies with MULTIPLE constraints spanning different KBs compose correctly under conjunctive semantics.

**Key insight:** Zero Layer 2 changes needed. Existing denotation rules handle any number of constraints. Cross-dataspace is purely a Layer 3 concern.

## Conjunctive Semantics

Overall compatible iff ALL operand pairs overlap independently:

```
∃X(denot(X,c1) ∧ denot(X,c2))          — spatial pair
∧ ∃Y(denot(Y,c3) ∧ denot(Y,c4))        — purpose pair
∧ ∃Z(denot(Z,c5) ∧ denot(Z,c6))        — language pair (055 only)
```

Each existential has its own witness. Failure in ANY dimension blocks the conjunction.

## Problems

### Two-KB (GEO + DPV)

| Problem | Spatial | Purpose | SZS | Verdict |
|---|---|---|:---:|:---:|
| ODRL030-1 | isPartOf europe ↔ eq france | isA R&D ↔ eq academicResearch | Theorem | Compatible |
| ODRL031-1 | isPartOf europe ↔ eq bavaria | isA nonComm ↔ eq advertising | CounterSat | Unknown |
| ODRL032-1 | — | isA nonComm ↔ eq advertising | Theorem | Conflict |
| ODRL033-1 | isPartOf france ↔ eq bavaria | isA nonComm ↔ eq scientificResearch | CounterSat | Unknown |

### Three-KB (GEO + DPV + LNG)

| Problem | Spatial | Purpose | Language | SZS | Verdict |
|---|---|---|---|:---:|:---:|
| ODRL055-1 | europe ↔ france ✓ | nonComm ↔ sciResearch ? | de ↔ fr ✗ | CounterSat | Unknown |
| ODRL056-1 | — | — | de ↔ fr | Theorem | Conflict |

## Diagnostic Workflow

1. **ODRL031-1:** Test overall → CounterSat (something blocks)
2. **ODRL032-1:** Test purpose pair only → Theorem (purpose IS the blocker)

Same pattern for three-KB:

1. **ODRL055-1:** Test overall → CounterSat
2. **ODRL056-1:** Test language pair only → Theorem (language blocks)

This models the ODRL-SA diagnostic pipeline: identify which operand dimension causes incompatibility.

## Scenarios

| Problem | Policy holder | Requester |
|---|---|---|
| 030–033 | Generic EU dataspace | Generic requester |
| 055–056 | Bayerische Staatsbibliothek | French national archive |

## Paper Mapping

| What | Where |
|---|---|
| Conjunctive semantics | Definition 6 (Conflict Detection) |
| Independent operands | "Constraints over different operands are independent" |
| Three-KB composition | Contribution 3 (three high-priority operands) |
| Diagnostic workflow | Section 5 (Evaluation) |
