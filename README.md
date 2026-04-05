This is the **old README** — it describes the deleted architecture. It needs to be completely rewritten to match the current repo. Here is what is wrong:

---

## What the old README describes vs current state

| Old README | Current repo |
|---|---|
| 146 KBGrounding problems | Deleted |
| 165 SelfContained SMT2 problems | Deleted |
| `Problems/ODRL/KBGrounding/` | Deleted |
| `Problems/ODRL/SelfContained/` | Deleted |
| Layer0-DomainKB, Layer1-ODRLCore | Deleted |
| gen_spatial_suite.py etc. | Deleted |
| Two-layer stack | Replaced by AxisDecomposition |

---

## New README to write

```bash
cat > README.md << 'EOF'
# TPTP-ODRL Benchmark Suite
**Automated Reasoning for ODRL Policy Conflict Detection**
Mustafa, D. & Sutcliffe, G. (2026)

---

## Overview

165 benchmark problems for automated reasoning over ODRL 2.2 spatial
and deontic policies, encoded in TPTP FOF and SMT-LIB 2.

| Use Case | Problems | Prover | Format |
|---|---|---|---|
| UC1: Axis Decomposition | 126 | Vampire + Z3 | FOF + SMT2 + TTL |
| UC2: Deontic Ontology Grounding | 39 | Vampire + Z3 | FOF + SMT2 + TTL |
| **Total** | **165** | | |

---

## Repository Structure

```
Problems/
├── ODRL/AxisDecomposition/       ← Use Case 1 (126 problems)
│   ├── Axioms/
│   │   ├── AXIS000-0.ax          interval predicates (18 axioms)
│   │   ├── ORD000-0.ax           strict total order (8 axioms)
│   │   └── ORD001-0.ax           density axiom (1 axiom)
│   ├── SingleAxis/               15 problems
│   ├── Box2D/                    15 problems
│   ├── Box3D/                    14 problems
│   ├── Composition/              12 problems
│   ├── PolicyQuality/            17 problems
│   ├── Boundary/                 16 problems
│   ├── LogicalOr/                12 problems
│   ├── LogicalXone/              11 problems
│   ├── SemanticCore/             14 problems
│   └── Policies/                 126 TTL source policies
└── DeonticOntology/              ← Use Case 2 (39 problems)
    ├── Axioms/
    │   ├── GRND000-0.ax          signature (39 axioms)
    │   └── GRND-AX-1.ax          deontic grounding (28 axioms)
    ├── Consistency/              1 problem
    ├── Discriminating/           13 problems
    └── Entailment/               25 problems
```

---

## Quick Start

**Use Case 1:**
```bash
vampire --include Problems/ODRL/AxisDecomposition --mode vampire --time_limit 10 Problems/ODRL/AxisDecomposition/SingleAxis/ODRL300-1.p
```

**Use Case 2:**
```bash
vampire --include Problems/DeonticOntology --mode casc --time_limit 30 Problems/DeonticOntology/Entailment/GRND002-1.p
```

---

## Validation Results

All 165 problems validated locally with Vampire 5.0.0 and Z3 4.15.4.

| Use Case | Vampire | Z3 |
|---|---|---|
| UC1: Axis Decomposition | 126/126 Theorem | 126/126 concordance |
| UC2: Deontic Ontology | 39/39 PASS | 36/39 PASS (3 sat-timeout by design) |

---

## Generators

```
Generators/
├── AxisDecomposition/
│   ├── gen_axis_problems.py      main generator (--cat all)
│   ├── gen_semantic_core.py      SemanticCore category
│   └── problem_data_*.py         per-category problem data
└── DeonticOntology/
    ├── gen_foundation_problems.py
    ├── gen_layer0_signature.py
    └── gen_layer1_deontic.py
```

Regenerate all:
```bash
uv run Generators/AxisDecomposition/gen_axis_problems.py --out-dir Problems/ODRL/AxisDecomposition --cat all
uv run Generators/DeonticOntology/gen_foundation_problems.py --out-dir Problems/DeonticOntology --coverage
```

---

**Authors:** Daham Mustafa (RWTH Aachen / Fraunhofer FIT), Geoff Sutcliffe (University of Miami)
**License:** MIT
EOF

git add README.md
git commit -m "docs: rewrite README for current benchmark structure (UC1+UC2, 165 problems)"
git push
```