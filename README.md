```markdown
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

**146 problems** encoded in TPTP FOF across 20 categories. Designed for ATP evaluation and TPTP library submission.

---

## 2. Architecture: Two-Layer Stack

```
Layer 0   Domain KBs     GEO000-0.ax, DPV000-0.ax, LANG000-0.ax, ISO3166-0.ax
Layer 1   ODRL Core      ODRL000-0.ax, RUNTIME000-0.ax, ALIGN000-0.ax
Layer 2   Problems       ODRL0xx-1.p (per-problem axioms + conjecture)
```

A higher layer never modifies a lower one. Problems include Layer 0
and Layer 1 via TPTP `include()` directives, then add per-problem
axioms (value lists, list closures, inline KB fragments) and the conjecture.

### Layer 0 — Domain Knowledge Bases

Four production KBs generated from real-world standards:

| File | Domain | \|C\| | Edges | Disjoint | Structure | Source |
|------|--------|:-----:|:-----:|:--------:|-----------|--------|
| `GEO000-0.ax` | Spatial (Europe) | 58 | 57 | 315 | Tree | UN M49 |
| `DPV000-0.ax` | Purpose | 95 | 100 | 279 | DAG | W3C DPV v2 |
| `LANG000-0.ax` | Language | 68 | 43 | 334 | Forest | BCP 47 |
| `ISO3166-0.ax` | Country Codes | 6 | 5 | 15 | Tree | ISO 3166-1 |

All KBs use `--no-una` (no Unique Name Assumption axioms). For tree/forest
KBs, UNA is implicit from sibling disjointness (§6). For the DAG KB,
DAG-safe sibling disjointness is used (§5).

**Predicates** (uniform across all KBs):
- `concept/1` — concept membership
- `leq/2` — subsumption/containment edges
- `disjoint/2` — pairwise disjointness

### Layer 1 — ODRL Core (3 files, 51 axioms total)

| File | Axioms | Content |
|------|:------:|---------|
| `ODRL000-0.ax` | 33 | KB properties + denotation rules (Parts A–E) |
| `RUNTIME000-0.ax` | 8 | Runtime context (`assigns/2`, `satisfies/3`) |
| `ALIGN000-0.ax` | 10 | Cross-dataspace alignment (`align/2`) |

**ODRL000-0.ax** (33 axioms):
- Part A (9): Structural predicates
- Part B (6): KB properties (reflexivity, transitivity, symmetry, irreflexivity, downward closure)
- Part C (2): Derived consistency lemmas
- Part D (10): Single-valued operators (eq, neq, isA, isPartOf, hasPart)
- Part E (6): Set-valued operators (isAnyOf, isAllOf, isNoneOf)

All denotation rules are **bidirectional** (if + only-if). Key axiom `leq_typed`
ensures `leq(X,Y) => concept(X) & concept(Y)`.

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

### 3.2 Set-Valued (Layer 1, Part E)

| Operator | Denotation | Predicate |
|----------|-----------|-----------|
| `isAnyOf` | `∪ᵢ {x ∈ C \| x ≤ gᵢ}` | `in_denotation_set(X, L, isAnyOf)` |
| `isAllOf` | `{x ∈ C \| ∀i: x ≤ gᵢ}` | `in_denotation_set(X, L, isAllOf)` |
| `isNoneOf` | `C \ ∪ᵢ {x ∈ C \| x ≤ gᵢ}` | `in_denotation_set(X, L, isNoneOf)` |

Set-valued operators require per-problem **list closure axioms**:
```fof
fof(list_closed, axiom, ![G]: (in_value_list(G, myList)
    => (G = val1 | G = val2 | G = val3))).
```

---

## 4. Verdict Encoding

| Verdict | Conjecture | SZS Status |
|---------|-----------|:----------:|
| Compatible | `∃x(den₁(x) ∧ den₂(x))` | Theorem |
| Conflict | `¬∃x(den₁(x) ∧ den₂(x))` | Theorem |
| Unknown | either | CounterSatisfiable / Timeout |

All problems use **prover encoding** (negated Conflict conjectures → all expected results are Theorem).

---

## 5. DAG-Safe Sibling Disjointness

Real-world ontologies like W3C DPV have DAG structure (concepts with
multiple parents). Naïve sibling disjointness produces contradictions when
a multi-parent concept `m` descends from two siblings `a` and `b`.

**DAG-safe generation** asserts `disjoint(a, b)` only when `↓a ∩ ↓b = ∅`.

DPV Purpose taxonomy: 285 total sibling pairs, **279 safe**, 6 protected.

**Theorem (Soundness).** DAG-safe generation never introduces contradictions. □

---

## 6. Implicit UNA Lemma

For tree-structured KBs with sibling disjointness at every level,
the Unique Name Assumption is derivable from KB axioms alone via
`leq` antisymmetry + `disj_downward` + `disj_irrefl`.

This eliminates C(n,2) pairwise distinctness axioms:

| KB | \|C\| | UNA axioms saved |
|----|:-----:|:----------------:|
| GEO | 58 | 1,653 |
| LANG | 68 | 2,278 |
| DPV | 95 | 4,465 |
| **Total** | | **8,396** |

---

## 7. Benchmark Problems (146 total)

### 7.1 Workshop Suite (Categories 1–8, ODRL010–095, 68 problems)

| Category | Range | Count | Focus |
|----------|-------|:-----:|-------|
| 1 | 010–019 | 10 | Basic operators (eq, isPartOf, isA, hasPart, neq) |
| 2 | 020–025 | 6 | Set-valued operators (isAnyOf, isAllOf, isNoneOf) |
| 3 | 030–037 | 8 | Constraint subsumption |
| 4 | 040–047 | 8 | Multi-operand composition (GEO×DPV) |
| 5 | 050–055 | 6 | Edge cases (leaf/root, self-overlap) |
| 6 | 060–069 | 10 | Advanced analysis (tautology, redundancy, partial overlap) |
| 7 | 070–079 | 10 | Cross-KB composition patterns |
| 8 | 080–095 | 10 | Ablation tests |

Generated via `gen_spatial_suite.py`.

### 7.2 Advanced Suite (Categories 9–16, 20–21, ODRL100–175 + 230–254, 60 problems)

| Category | Range | Count | Focus |
|----------|-------|:-----:|-------|
| 9 | 100–105 | 6 | DAG Multi-Parent (NAIVE vs DAG-safe) |
| 10 | 110–114 | 5 | Nested Set Operators |
| 11 | 120–123 | 4 | Quantifier Stress (∀∃ alternation) |
| 12 | 130–132 | 3 | Large-Scale Composition (3-operand AND, 5-way ∃) |
| 13 | 140–145 | 6 | Edge Cases & Adversarial |
| 14 | 150–159 | 11 | Multi-Hop Alignment (2–3 hop, witness-loss bug) |
| 15 | 160–165 | 6 | N-Way Conflicts (non-transitive compatibility) |
| 16 | 170–175 | 6 | N-Way Composed (multi-dim × N-way) |
| 20 | 230–237 | 8 | XONE / Symmetric Difference (negative reasoning) |
| 21 | 250–254 | 5 | Operator Monotonicity (meta-properties) |

Generated via `gen_advanced_suite.py`.

**Key Problems:**
- **ODRL100**: NAIVE DAG contradiction (exp: ContradictoryAxioms)
- **ODRL158–159**: Witness-loss bug (Prop 2(2) counterexample)
- **ODRL162**: Non-transitive compatibility (THE N-way insight)
- **ODRL233**: XONE failure (DAG-safe epistemic gap)
- **ODRL250–254**: Universal monotonicity theorems

### 7.3 Extreme Suite (Categories 17–19, ODRL200–225, 18 problems)

| Category | Range | Count | Focus |
|----------|-------|:-----:|-------|
| 17 | 200–205 | 6 | Set Operator Stress (deep isNoneOf/isAllOf/isAnyOf) |
| 18 | 210–215 | 6 | Combined Complexity (multi-hop + N-way + DAG + runtime) |
| 19 | 220–225 | 6 | Adversarial Operators (boundary cases, non-partition) |

Generated via `gen_extreme_suite.py`.

**Difficulty:** 11 Very Hard, 7 Extreme. Tests combinatorial depth without new syntax.

**ODRL215** (Ultimate): 4 KBs × 3 policies × 3 operands × set ops × DAG alignment.

### 7.4 Combined Results

| Suite | Problems | Generator | Status |
|-------|:--------:|-----------|--------|
| Workshop | 68 | `gen_spatial_suite.py` | Production |
| Advanced | 60 | `gen_advanced_suite.py` | Production |
| Extreme | 18 | `gen_extreme_suite.py` | Production |
| **Total** | **146** | | |

---

## 8. Running the Benchmarks

### Quick Start

```bash
# Single problem
vampire --include Problems/ODRL --mode casc \
    Problems/ODRL/KBGrounding/DAGMultiParent/ODRL100-1.p

# Advanced suite summary
python gen_advanced_suite.py --summary

# Extreme suite summary
python gen_extreme_suite.py --summary

# Run all problems
for f in Problems/ODRL/KBGrounding/*/*.p; do
    echo -n "$(basename $f): "
    vampire --include Problems/ODRL --time_limit 60 --mode casc \
        "$f" 2>&1 | grep "SZS status"
done
```

### Regenerating Problems

```bash
# Workshop suite (68 problems)
python gen_spatial_suite.py -o Problems/ODRL/KBGrounding/Spatial --encoding prover

# Advanced suite (60 problems)
python gen_advanced_suite.py --outdir Problems/ODRL

# Extreme suite (18 problems)
python gen_extreme_suite.py --outdir Problems/ODRL
```

### Regenerating KBs

```bash
# GEO (tree, Europe subset of UN M49)
python gen_layer0_geo.py \
    -o Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax \
    --scope europe --sibling-disjointness --no-una

# DPV (DAG, W3C Data Privacy Vocabulary)
python gen_layer0_kb.py \
    -i data/dpv/dpv-owl.ttl \
    -o Problems/ODRL/Axioms/Layer0-DomainKB/DPV000-0.ax \
    -n "https://w3id.org/dpv#" -r Purpose -d taxonomic \
    --sibling-disjointness --no-una \
    --name "W3C DPV Purpose" --source "https://w3id.org/dpv"

# LANG (forest, BCP 47 language tags)
python gen_layer0_lang.py \
    -o Problems/ODRL/Axioms/Layer0-DomainKB/LANG000-0.ax \
    --sibling-disjointness --base-disjointness --no-una
```

---

## 9. File Map

```
tptp-odrl/
├── README.md
├── gen_layer0_kb.py                 L0 generator (OWL → TPTP, DAG-safe)
├── gen_layer0_geo.py                L0 generator (UN M49)
├── gen_layer0_lang.py               L0 generator (BCP 47)
├── gen_spatial_suite.py             Workshop suite (68 problems)
├── gen_advanced_suite.py            Advanced suite (60 problems)
├── gen_extreme_suite.py             Extreme suite (18 problems)
├── data/dpv/dpv-owl.ttl            Source ontology for DPV
├── Isabelle/                        Mechanical verification (22 theorems)
├── Problems/ODRL/
│   ├── Axioms/
│   │   ├── Layer0-DomainKB/
│   │   │   ├── GEO000-0.ax         58 concepts, 430 axioms (tree)
│   │   │   ├── DPV000-0.ax         95 concepts, 474 axioms (DAG-safe)
│   │   │   ├── LANG000-0.ax        68 concepts, 445 axioms (forest)
│   │   │   └── ISO3166-0.ax        6 concepts, 26 axioms (tree)
│   │   ├── Layer1-ODRLCore/
│   │   │   ├── ODRL000-0.ax        33 axioms (KB properties + denotation)
│   │   │   ├── RUNTIME000-0.ax     8 axioms (runtime context)
│   │   │   └── ALIGN000-0.ax       10 axioms (cross-dataspace alignment)
│   │   └── Alignment/
│   │       └── ALIGN-GEO-ISO.ax    6 axioms (GEO→ISO alignment data)
│   └── KBGrounding/
│       ├── Spatial/                 Workshop suite (68)
│       ├── DAGMultiParent/          Category 9 (6)
│       ├── NestedSetOperators/      Category 10 (5)
│       ├── QuantifierStress/        Category 11 (4)
│       ├── LargeComposition/        Category 12 (3)
│       ├── EdgeCases/               Category 13 (6)
│       ├── MultiHopAlignment/       Category 14 (11)
│       ├── NWayConflict/            Category 15 (6)
│       ├── NWayComposed/            Category 16 (6)
│       ├── SetOperatorStress/       Category 17 (6)
│       ├── CombinedComplexity/      Category 18 (6)
│       ├── AdversarialOperators/    Category 19 (6)
│       ├── XONESymmetricDiff/       Category 20 (8)
│       └── OperatorMonotonicity/    Category 21 (5)
└── results/
    └── benchmark_results.csv        Vampire results
```

---

## 10. Key Design Decisions

**Why two layers?** Denotation rules are domain-independent and belong with KB axioms. Simpler than 3-layer architecture.

**Why bidirectional denotation rules?** Prevents open-world frame problem (`in_denotation := true` everywhere).

**Why `leq_typed`?** Faithfully encodes "≤ is a relation on C" — prevents phantom elements.

**Why list closure axioms?** Prevents phantom list members in open-world FOL.

**Why no UNA?** Tree + sibling disjointness makes constants provably distinct (saves 8,396 axioms).

**Why DAG-safe disjointness?** Preserves 98% of disjointness pairs while guaranteeing consistency for multi-parent concepts.

**Why prover encoding?** All expected results map to Theorem (avoids CounterSatisfiable ambiguity).

---

## 11. Prover Details

**Vampire** (CASC mode, `--mode casc`, `--time_limit 60`).  
Typical: 0.1–1.4s. All problems in EPR fragment (decidable).

**Z3** encoding planned for future release.

---

## 12. Version History

| Version | Changes | Problems |
|---------|---------|:--------:|
| 0.1–1.2 | Iterative development | 154 |
| **2.0** | Complete rewrite: 2-layer architecture, DAG-safe DPV, Implicit UNA | 48 |
| **2.1** | Advanced suite (Categories 9–14) | 96 |
| **3.0** | **Extended benchmark: Advanced + Extreme suites** | **146** |
| | Categories 15–16 (N-way analysis) | |
| | Categories 17–19 (Extreme suite) | |
| | Categories 20–21 (XONE + Monotonicity) | |
| | Witness-loss bug demonstration (ODRL158–159) | |
| | Multi-hop alignment (up to 4 dataspaces) | |

---

## 13. Citation



---

**Authors:** Daham Mustafa (RWTH Aachen / Fraunhofer FIT), Geoff Sutcliffe (University of Miami)  
**License:** MIT  
**Status:** Production (v3.0, 146 problems)
```
## Benchmark Organization

### Stage 2: KB-Dependent Reasoning (TPTP)
- **Location:** `Problems/ODRL/KBGrounding/`
- **Format:** TPTP (FOF logic)
- **Solver:** Vampire
- **Problems:** 146
- **Categories:** Spatial, Purpose, Language, Multi-hop alignment

### Stage 1: Self-Contained Reasoning (SMT2)
- **Location:** `Problems/ODRL/SelfContained/`
- **Format:** SMT-LIB2 (QF_LRA logic)
- **Solver:** Z3
- **Problems:** 165
- **Categories:** delayPeriod, elapsedTime, percentage, resolution, dateTime, payAmount
