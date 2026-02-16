# TPTP-ODRL Benchmark Suite

**Automated Reasoning for ODRL Policy Conflict Detection**

Mustafa, D. & Sutcliffe, G. (2025)

---

## 1. Motivation

The W3C Open Digital Rights Language (ODRL) defines set-based operators
(`isA`, `isPartOf`, `hasPart`, `isAnyOf`, `isAllOf`, `isNoneOf`) whose
evaluation requires external domain knowledge. The specification leaves
this knowledge unspecified. Without it, every cross-dataspace policy
comparison returns **Unknown**.

This benchmark suite formalises a denotational semantics for ODRL
constraints, parameterised by domain knowledge bases, that enables
automated conflict detection. Each constraint maps to a *denotation*
(the set of KB concepts satisfying it); conflict detection reduces to
intersection testing under a three-valued verdict: **Conflict**,
**Compatible**, or **Unknown**.

48 problems encoded in TPTP FOF. Vampire solves 46/48 (2 timeout, 0 wrong).

---

## 2. Architecture: Two-Layer Stack

```
Layer 0   Domain KBs     GEO000-0.ax, DPV000-0.ax, LANG000-0.ax   Domain facts
Layer 1   ODRL Core      ODRL000-0.ax                               KB properties + denotation rules
Layer 2   Problems       ODRL0xx-1.p                                 Per-problem axioms + conjecture
```

A higher layer never modifies a lower one. Problems include Layer 0
and Layer 1 via TPTP `include()` directives, then add per-problem
axioms (value lists, list closures) and the conjecture.

### Layer 0 — Domain Knowledge Bases

Three production KBs generated from real-world standards:

| File | Domain | \|C\| | Edges | Disjoint | Structure | Source | Generator |
|------|--------|:-----:|:-----:|:--------:|-----------|--------|-----------|
| `GEO000-0.ax` | Spatial (Europe) | 58 | 57 | 315 | Tree | UN M49 | `gen_layer0_geo.py` |
| `DPV000-0.ax` | Purpose | 95 | 100 | 279 | DAG | W3C DPV v2 | `gen_layer0_kb.py` |
| `LANG000-0.ax` | Language | 68 | 43 | 334 | Forest | BCP 47 | `gen_layer0_lang.py` |

All KBs use `--no-una` (no Unique Name Assumption axioms). For tree/forest
KBs, UNA is implicit from sibling disjointness (see §6). For the DAG KB,
DAG-safe sibling disjointness is used (see §5).

**Predicates** (uniform across all KBs):
- `concept/1` — concept membership (Definition 2: C)
- `leq/2` — direct subsumption/containment edges (Definition 2: ≤)
- `disjoint/2` — pairwise disjointness (Definition 2: ⊥⊥)

Layer 1 provides reflexivity, transitivity of `leq` and symmetry,
irreflexivity, downward closure of `disjoint`.

### Layer 1 — ODRL Core (`ODRL000-0.ax`, 33 axioms)

Five parts, all domain-independent:

| Part | Axioms | Content |
|------|:------:|---------|
| A | 9 | Structural predicates (policy, constraint, operand typing) |
| B | 6 | KB properties: `leq` reflexive/transitive/typed, `disjoint` symmetric/irreflexive/downward-closed |
| C | 2 | Derived: disjointness–order consistency (Lemma 1), contrapositive |
| D | 10 | Denotation rules for single-valued operators (eq, neq, isA, isPartOf, hasPart) |
| E | 6 | Denotation rules for set-valued operators (isAnyOf, isAllOf, isNoneOf) |

All denotation rules are **bidirectional** (if + only-if). Without
only-if rules, provers satisfy implications trivially by setting
`in_denotation := true` for all inputs (open-world frame problem).

Key axiom `leq_typed` ensures `leq(X,Y) => concept(X) & concept(Y)`,
faithfully encoding "≤ is a relation on C" (Definition 2).

---

## 3. Operator Encodings

### 3.1 Single-Valued (Layer 1, Part D)

| Operator | Denotation | Predicate |
|----------|-----------|-----------|
| `eq` | `{g}` | `in_denotation(X, G, eq)` |
| `neq` | `C \ {g}` | `in_denotation(X, G, neq)` |
| `isA` | `{x ∈ C \| x ≤ g}` | `in_denotation(X, G, isA)` |
| `isPartOf` | `{x ∈ C \| x ≤ g}` | `in_denotation(X, G, isPartOf)` |
| `hasPart` | `{x ∈ C \| g ≤ x}` | `in_denotation(X, G, hasPart)` |

`isA` and `isPartOf` have identical denotation rules — the semantic
distinction is carried by the KB's ≤ relation (taxonomic ⊑ vs
mereological ⪯), not the operator label.

### 3.2 Set-Valued (Layer 1, Part E)

| Operator | Denotation | Predicate |
|----------|-----------|-----------|
| `isAnyOf` | `∪ᵢ {x ∈ C \| x ≤ gᵢ}` | `in_denotation_set(X, L, isAnyOf)` |
| `isAllOf` | `{x ∈ C \| ∀i: x ≤ gᵢ}` | `in_denotation_set(X, L, isAllOf)` |
| `isNoneOf` | `C \ ∪ᵢ {x ∈ C \| x ≤ gᵢ}` | `in_denotation_set(X, L, isNoneOf)` |

Set-valued operators use auxiliary predicate `in_value_list(G, ListId)`.
Per-problem **list closure axioms** enumerate the list exhaustively:
```
fof(list_closed, axiom, ![G]: (in_value_list(G, myList)
    => (G = val1 | G = val2 | G = val3))).
```
This is necessary because FOL is open-world: without closure, Vampire
can invent phantom list members that defeat isNoneOf proofs.

---

## 4. Verdict Encoding

| Verdict | Conjecture | SZS Status |
|---------|-----------|:----------:|
| Compatible | `∃x(den₁(x) ∧ den₂(x))` | Theorem |
| Conflict | `¬∃x(den₁(x) ∧ den₂(x))` | Theorem |
| Unknown | either | CounterSatisfiable / Timeout |

The **prover encoding** negates all CounterSatisfiable conjectures so
that every expected verdict maps to **Theorem**. This avoids the CSA
ambiguity where "insufficient axioms" and "provably disjoint" both
return CounterSatisfiable.

All problems are in the **EPR fragment** (function-free, finite
constants, universally quantified implications). Decidable; typical
proof times 0.1–1.4s.

---

## 5. DAG-Safe Sibling Disjointness

Real-world ontologies like W3C DPV have DAG structure (concepts with
multiple parents). Naïve sibling disjointness — asserting all children
of the same parent are pairwise disjoint — produces contradictions when
a multi-parent concept `m` descends from two siblings `a` and `b`:

```
disjoint(a, b)  ∧  leq(m, a)  ∧  leq(m, b)
  → disjoint(m, m)              [disj_downward]
  → ⊥                           [disj_irrefl]
```

**DAG-safe generation** (Definition 3b) asserts `disjoint(a, b)` only
when the downward closures are disjoint: `↓a ∩ ↓b = ∅`.

DPV Purpose taxonomy: 285 total sibling pairs, 279 safe, 6 protected.

| Multi-Parent Concept | Parent A | Parent B | Overlap |
|---------------------|----------|----------|:-------:|
| `commercialResearch` | `commercialPurpose` | `researchAndDevelopment` | 1 |
| `nonCommercialResearch` | `nonCommercialPurpose` | `researchAndDevelopment` | 1 |
| `personalisedAdvertising` | `marketing` | `personalisation` | 2 |
| `servicePersonalisation` | `personalisation` | `serviceProvision` | 6 |
| `communicationForCustomerCare` | `communicationManagement` | `customerManagement` | 1 |
| `improveInternalCRMProcesses` | `customerManagement` | `serviceProvision` | 1 |

**Theorem (Soundness).** DAG-safe generation never introduces
contradictions. If `∃m: m ≤ a ∧ m ≤ b`, then `disjoint(a, b)` is
not asserted, so `disj_downward + disj_irrefl` cannot derive ⊥. □

---

## 6. Implicit UNA Lemma

For tree-structured KBs with sibling disjointness at every level,
the Unique Name Assumption is derivable from KB axioms alone:

**Lemma (Implicit UNA).** Let K = (C, ≤, ⊥⊥) where (C, ≤) forms a
tree with sibling disjointness at every level. Then for all distinct
constants a, b ∈ C: a ≠ b is derivable via `leq` antisymmetry +
`disj_downward` + `disj_irrefl`.

This eliminates C(n,2) pairwise distinctness axioms per KB:

| KB | \|C\| | UNA axioms saved |
|----|:-----:|:----------------:|
| GEO | 58 | 1,653 |
| LANG | 68 | 2,278 |
| DPV | 95 | 4,465 |
| **Total** | | **8,396** |

---

## 7. Benchmark Problems (48)

### 7.1 Basic Operators (010–019, 10 problems)

| # | Operators | Verdict | KB |
|---|-----------|---------|-----|
| 010 | KB transitivity test | Valid | GEO |
| 011 | `isPartOf` ∩ `isPartOf` (overlap) | Compatible | GEO |
| 012 | `eq` ∩ `eq` (distinct values) | Conflict | GEO |
| 013 | `isPartOf` ∩ `isPartOf` (disjoint branches) | Conflict | GEO |
| 014 | `isA` ∩ `isA` (ancestor–descendant) | Compatible | GEO |
| 015 | `isA` ∩ `eq` (disjoint) | Conflict | GEO |
| 016 | `hasPart` ∩ `isPartOf` (upward ∩ downward) | Compatible | GEO |
| 017 | `hasPart` ∩ `hasPart` (disjoint upward) | Conflict | GEO |
| 018 | `neq` ∩ `isPartOf` | Compatible | GEO |
| 019 | `eq` ∩ `neq` (same value) | Conflict | GEO |

### 7.2 Set-Valued Operators (020–025, 6 problems)

| # | Operators | Verdict | KB |
|---|-----------|---------|-----|
| 020 | `isAnyOf` ∩ `isPartOf` | Compatible | GEO |
| 021 | `isNoneOf` ∩ `isPartOf` | Compatible | GEO |
| 022 | `isAnyOf` ∩ `isNoneOf` | Conflict | GEO |
| 023 | `isAllOf` ∩ `isNoneOf` | Conflict | GEO |
| 024 | `isAnyOf` ∩ `isNoneOf` (partial) | Compatible | GEO |
| 025 | `isAnyOf` ∩ `isNoneOf` (total cover) | Conflict | GEO |

### 7.3 Constraint Subsumption (030–037, 8 problems)

| # | Test | Verdict | KB |
|---|------|---------|-----|
| 030 | `isPartOf(germany) ⊆ isPartOf(wE)` | Confirmed | GEO |
| 031 | `isPartOf(wE) ⊆ isPartOf(germany)` | Refuted | GEO |
| 032–034 | Various `isA` subsumption | Confirmed | GEO |
| 035 | Subsumption between disjoint operators | Conflict | GEO |
| 036 | Cross-operator: `isPartOf ⊆ neq` | Confirmed | GEO |
| 037 | Cross-operator: `neq ⊆ isPartOf` | Refuted | GEO |

### 7.4 Multi-Operand Composition (040–047, 8 problems)

Uses both GEO (spatial) and DPV (purpose) KBs per problem.

| # | Mode | Spatial | Purpose | Verdict |
|---|------|---------|---------|---------|
| 040 | AND | Compatible | Compatible | Compatible |
| 041 | AND | Compatible | Conflict | Conflict |
| 042 | OR | Conflict | Compatible | Compatible |
| 043 | OR | Conflict | Conflict | Conflict |
| 044 | AND | Conflict | Conflict | Conflict |
| 045 | XONE | Conflict | Compatible | Compatible |
| 046 | XONE | Compatible | Compatible | Unknown |
| 047 | XONE | Conflict | Conflict | Conflict |

### 7.5 Edge Cases (050–055, 6 problems)

| # | Test | Verdict | KB |
|---|------|---------|-----|
| 050 | `hasPart(leaf)` ∩ `isPartOf(root)` | Compatible | GEO |
| 051 | `hasPart(germany)` ∩ `eq(world)` | Compatible | GEO |
| 052 | Self-overlap: same constraint | Compatible | GEO |
| 053 | Deep chain: `isPartOf(leaf)` ∩ `hasPart(root)` | Compatible | GEO |
| 054 | Subsumption: `isPartOf(child) ⊆ isPartOf(parent)` | Confirmed | GEO |
| 055 | `hasPart` asymmetry test | Refuted | GEO |

### 7.6 Advanced Analysis (060–069, 10 problems)

| # | Test | Verdict | KB |
|---|------|---------|-----|
| 060 | Tautology: `isPartOf(root) = C` | Tautological | GEO |
| 061–062 | Non-subsumption tests | Non-subsuming | GEO |
| 063–064 | Redundancy detection | Redundant | GEO |
| 065 | Non-subsuming cross-operator | Non-subsuming | GEO |
| 066–068 | Partial overlap (various depths) | Partial | GEO |
| 069 | Full overlap | Full | GEO |

### 7.7 Results Summary

| Status | Count | % |
|--------|:-----:|:-:|
| ✓ Theorem (correct) | 46 | 95.8% |
| ⏱ Timeout (60s) | 2 | 4.2% |
| ✗ Wrong answer | 0 | 0% |
| **Total** | **48** | |

Timeouts: ODRL051 (hasPart chain to root, requires long transitive
chain) and ODRL060 (tautology, requires universal proof over 58
concepts). Both are genuinely hard — rated 1.00 in TPTP difficulty.

### 7.8 Verdict Distribution

| Verdict | Count |
|---------|:-----:|
| Compatible | 15 |
| Conflict | 17 |
| Confirmed (subsumption) | 7 |
| Refuted (subsumption) | 4 |
| Unknown | 1 |
| Other (tautological, redundant, partial, full) | 4 |

---

## 8. Running the Benchmarks

### Quick Start

```bash
# Single problem
vampire --include Problems/ODRL --mode casc \
    Problems/ODRL/KBGrounding/Spatial/ODRL012-1.p

# All 48 problems with timing
for f in Problems/ODRL/KBGrounding/Spatial/ODRL*-1.p; do
    echo -n "$(basename $f): "
    vampire --include Problems/ODRL --time_limit 60 --mode casc \
        "$f" 2>&1 | grep "SZS status"
done
```

### Regenerating KBs

```bash
# GEO (tree, Europe subset of UN M49)
uv run python gen_layer0_geo.py \
    -o Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax \
    --scope europe --sibling-disjointness --no-una

# DPV (DAG, W3C Data Privacy Vocabulary)
uv run python gen_layer0_kb.py \
    -i data/dpv/dpv-owl.ttl \
    -o Problems/ODRL/Axioms/Layer0-DomainKB/DPV000-0.ax \
    -n "https://w3id.org/dpv#" -r Purpose -d taxonomic \
    --sibling-disjointness --no-una \
    --name "W3C DPV Purpose" --source "https://w3id.org/dpv"

# LANG (forest, BCP 47 language tags)
uv run python gen_layer0_lang.py \
    -o Problems/ODRL/Axioms/Layer0-DomainKB/LANG000-0.ax \
    --sibling-disjointness --base-disjointness --no-una
```

### Regenerating Problems

```bash
# Generate + run all 48 problems
uv run python gen_spatial_suite.py \
    -o Problems/ODRL/KBGrounding/Spatial \
    --encoding prover --run
```

### SMT-LIB (Z3)

Z3 encoding planned for future release. The current suite is TPTP-only.

---

## 9. File Map

```
tptp-odrl/
├── README.md
├── gen_layer0_kb.py                 L0 generator (OWL → TPTP, DAG-safe)
├── gen_layer0_geo.py                L0 generator (UN M49, hardcoded)
├── gen_layer0_lang.py               L0 generator (BCP 47, hardcoded)
├── gen_spatial_suite.py             Problem generator (48 problems)
├── data/
│   └── dpv/dpv-owl.ttl             Source ontology for DPV
├── Isabelle/                        Mechanical verification (22 theorems, 0 sorry)
├── Problems/ODRL/
│   ├── Axioms/
│   │   ├── Layer0-DomainKB/
│   │   │   ├── GEO000-0.ax         58 concepts, 430 axioms (tree)
│   │   │   ├── DPV000-0.ax         95 concepts, 474 axioms (DAG-safe)
│   │   │   └── LANG000-0.ax        68 concepts, 445 axioms (forest)
│   │   └── Layer1-ODRLCore/
│   │       └── ODRL000-0.ax        33 axioms (KB properties + denotation)
│   └── KBGrounding/
│       └── Spatial/
│           ├── ODRL010-1.p          Basic operators (10)
│           ├── ODRL020-1.p          Set-valued operators (6)
│           ├── ODRL030-1.p          Subsumption (8)
│           ├── ODRL040-1.p          Composition GEO×DPV (8)
│           ├── ODRL050-1.p          Edge cases (6)
│           └── ODRL060-1.p          Advanced analysis (10)
└── results/
    └── benchmark_prover_*.csv       Vampire results
```

---

## 10. Key Design Decisions

**Why two layers instead of three?** The original Layer 2 (GROUND000-1.ax)
separated denotation rules from KB properties. This created an unnecessary
indirection — denotation rules are domain-independent and belong with KB
axioms in Layer 1. The 2-layer architecture is simpler and all problems
use the same axiom file.

**Why bidirectional denotation rules?** Sufficient conditions alone allow
`in_denotation := true` everywhere in open-world FOL. Necessary conditions
constrain witness properties, enabling conflict proofs.

**Why `leq_typed`?** FOL is untyped. Without `leq(X,Y) => concept(X) &
concept(Y)`, Vampire can invent phantom elements with `leq` relationships
but no `concept` membership, defeating `neq` and subsumption proofs.
This faithfully encodes "≤ is a relation on C" from Definition 2.

**Why list closure axioms?** Set-valued operators (`isNoneOf`, `isAllOf`)
require universally quantifying over list members. In open-world FOL,
without `![G]: (in_value_list(G, L) => (G = v1 | G = v2 | ...))`,
Vampire can invent phantom list members that defeat the universal.

**Why no UNA?** Tree + sibling disjointness makes all constants provably
distinct (Implicit UNA Lemma, §6). This saves 8,396 axioms across three
KBs and eliminates SInE pruning issues.

**Why DAG-safe disjointness?** Real ontologies have multi-parent concepts.
Naïve sibling disjointness produces contradictions. DAG-safe generation
(Definition 3b) preserves 98% of disjointness pairs while guaranteeing
consistency (§5).

**Why prover encoding (all Theorem)?** The original encoding produced
mixed SZS statuses (Theorem for Compatible, CounterSatisfiable for
Conflict). CounterSatisfiable is ambiguous — it conflates "provably
disjoint" with "insufficient axioms". The prover encoding negates
Conflict conjectures so all expected results are Theorem.

---

## 11. Prover Details

**Vampire** (CASC mode, `--mode casc`, `--time_limit 60`).
Typical: 0.1s for basic problems, 1.4s for isNoneOf with partial
overlap. Two problems timeout at 60s.

**Z3** encoding planned for future release.

---

## 12. Version History

| Version | Changes | Problems |
|---------|---------|:--------:|
| 0.1 | Initial eq, isPartOf, isA | 6 |
| 0.2 | Bidirectional denotation discovery | 15 |
| 0.3–0.5 | Set operators (isAnyOf, isAllOf, isNoneOf) | 29 |
| 0.6–0.9 | Cross-dataspace, SMT-LIB, extended operators | 154 |
| 1.0–1.2 | Operator pairs, adversarial, alignment | 154/154 |
| **2.0** | **Complete rewrite: 2-layer architecture** | |
| | DAG-safe DPV (95 concepts, 279 disjoint pairs) | |
| | Implicit UNA Lemma (saves 8,396 axioms) | |
| | `leq_typed` + list closure fixes | |
| | Prover encoding (all Theorem) | **48 (46 solved)** |

---

