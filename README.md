# ODRL Conflict Detection Benchmark

Benchmark suite for the VLDB 2026 paper:

> **Conflict Detection via Denotational Semantics: Policy Reasoning over Incomplete Hierarchies**  
> Daham M. Mustafa, Diego Collarana, Rafiqul Haque, Yixin Peng, Christoph Quix, Christoph Lange, Stefan Decker  
> RWTH Aachen University & Fraunhofer FIT

---

## What this benchmark does

ODRL hierarchy operators (`isA`, `isPartOf`, `isAnyOf`, `isNoneOf`) require
external knowledge bases — but no computable semantics existed and no benchmark
suite existed for testing them. This repository provides both.

Each problem is a TPTP or SMT-LIB 2 file encoding the question:
**"Can two ODRL constraints be simultaneously satisfied?"**

The three-valued answer — **Conflict**, **Compatible**, **Unknown** — is
returned by an automated theorem prover.

---

## Repository structure

```
odrl-benchmark-vldb/
├── Axioms/
│   ├── Layer0-DomainKB/        # GEO, DPV, LANG, ISO3166 knowledge bases
│   ├── Layer1-ODRLCore/        # ODRL operator axioms (ODRL000-0.ax)
│   └── Alignment/              # Cross-hierarchy alignment axioms
│
├── Problems/ODRL/
│   ├── E3-IncompletenessSwept/ # 195 problems: 3 KBs × 13 problems × 5 levels
│   │   ├── GEO/                # Geographic hierarchy (GeoNames)
│   │   ├── DPV/                # Purpose hierarchy (W3C Data Privacy Vocabulary)
│   │   └── LANG/               # Language hierarchy (BCP 47)
│   ├── E4-CrossDataspace/      # 20 problems: false positive prevention
│   │   ├── Case1_SharedHub/    # Shared KB — full disjointness
│   │   └── Case2_AsymmetricKB/ # Asymmetric KB — root disjointness only
│   ├── AnalysisModes/          # 7 problems: self-contradiction, redundancy
│   └── KBGrounding/            # Supporting problems: spatial, alignment, DAG
│
├── Isabelle/
│   └── ODRL_Grounding/         # Mechanically verified meta-theorems (HOL)
│
├── results/
│   ├── e3_incompleteness_sweep.csv   # E3 results: 195 problems
│   └── e4_crossds_soundness.csv      # E4 results: 20 problems
│
└── scripts/
    ├── run_e3_sweep.py         # Reproduce E3 results
    ├── run_e4_crossds.py       # Reproduce E4 results
    └── e3_z3_fix.py            # Grounded SMT2 encoder for Z3
```

---

## Key results

| Experiment | Problems | Vampire | Z3 | Agreement |
|---|---|---|---|---|
| E3 Incompleteness Sweep | 195 | 195/195 pass | 195/195 pass | 100% |
| E4 Cross-Dataspace | 20 | 20/20 pass | 20/20 pass | 100% |

**Soundness verified:** Compatible policies return `Theorem` at all 5
incompleteness levels — removing disjointness axioms never produces a false
conflict.

**Graceful degradation:** DPV (DAG structure) degrades earlier than GEO/LANG
(trees) because shared multi-parent concepts require more disjointness axioms.

---

## Reproducing results

### Requirements

```bash
# Vampire 5.5
vampire --version

# Z3 4.14
z3 --version

# Python 3.10+
python3 --version
```

### Run E3 (Incompleteness Sweep)

```bash
# From repo root
cd scripts

# Vampire only (fast, ~5 min)
python3 run_e3_sweep.py --timeout 10

# Vampire + Z3 (full validation, ~15 min)
python3 run_e3_sweep.py --timeout 30 --z3

# One KB only
python3 run_e3_sweep.py --timeout 10 --kb GEO
```

Expected output:
```
✓ GEO: 65/65 passed
✓ DPV: 65/65 passed
✓ LANG: 65/65 passed
✓ SOUNDNESS OK — no Compatible ever became Conflict
✓ STABILITY OK — all Compatible → Theorem at ALL 5 levels
Total: 195   Pass: 195   Fail: 0
```

### Run E4 (Cross-Dataspace)

```bash
python3 run_e4_crossds.py --timeout 10
```

Expected output:
```
Case 1 (Shared Hub KB):    10/10 pass
Case 2 (Asymmetric KB):    10/10 pass
✓ ALL false positive risks correctly abstained (5/5 → Unknown)
✓ All cross-region true conflicts still detected (5/5 → Theorem)
Total: 20/20 pass  ALL CORRECT
```

### Run a single problem manually

```bash
# From Problems/ODRL/ directory
cd Problems/ODRL

# Vampire
vampire --input_syntax tptp --include . --time_limit 10 \
  E3-IncompletenessSwept/GEO/full/GEO_C01_full.p

# Z3
z3 KBGrounding/Spatial/ODRL010-1.smt2
```

---

## Three-layer encoding

Each TPTP problem file uses three layers:

```prolog
% Layer 0 — Domain KB (GeoNames, DPV, BCP 47)
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
fof(geo1, axiom, leq(france, westernEurope)).
fof(geo2, axiom, leq(westernEurope, europe)).
fof(disj1, axiom, disj(westernEurope, easternEurope)).

% Layer 1 — ODRL operator axioms
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Conjecture — conflict or compatibility
fof(conj, conjecture,
  ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
```

A `Theorem` verdict means the conjecture holds — the two constraints share
a satisfying concept (Compatible) or have no satisfying concept (Conflict,
encoded as negated conjecture).

---

## Verdict encoding

| Verdict | Condition | SZS status | SMT-LIB |
|---|---|---|---|
| Conflict | D₁ ∩ D₂ = ∅ | Theorem | unsat |
| Compatible | D₁ ∩ D₂ ≠ ∅ | Theorem | unsat |
| Unknown | D₁ or D₂ = ⊤ | CounterSatisfiable | sat |

---

## Isabelle/HOL verification

Core meta-theorems are mechanically verified in `Isabelle/ODRL_Grounding/`.

```bash
# Verify with Isabelle 2025
isabelle build -D Isabelle/
```

---

## License

Problems, axioms, and scripts: MIT License.  
Isabelle theories: BSD 2-Clause.
