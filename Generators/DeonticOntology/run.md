Run everything from the repo root (`~/Desktop/tptp-odrl`). Three stages:

---

**Stage 1 — Generate signatures and axiom files**

```bash
cd ~/Desktop/tptp-odrl

# Layer 0 signature (GRND000-0.ax + GRND000-0.smt2)
python3 Generators/DeonticOntology/gen_layer0_signature.py \
  --out-dir Problems/DeonticOntology/Axioms/Layer0-Signature

# Layer 1 axioms (GRND-AX-1.ax + GRND-AX-1.smt2)
python3 Generators/DeonticOntology/gen_layer1_deontic.py \
  --out-dir Problems/DeonticOntology/Axioms/Layer1-Deontic
```

---

**Stage 2 — Generate all problem files**

```bash
# Base only (GRND001–009)
python3 Generators/DeonticOntology/gen_foundation_problems.py \
  --out-dir Problems/DeonticOntology

# Base + extension (GRND001–018)
python3 Generators/DeonticOntology/gen_foundation_problems.py \
  --out-dir Problems/DeonticOntology --ext

# Everything (GRND001–024)
python3 Generators/DeonticOntology/gen_foundation_problems.py \
  --out-dir Problems/DeonticOntology --ext --hard
```

---

**Stage 3 — Run validation**

```bash
# Base problems only
python3 Generators/DeonticOntology/run_grnd_validation.py

# Base + extension
python3 Generators/DeonticOntology/run_grnd_validation.py --ext

# Single problem (fast iteration)
python3 Generators/DeonticOntology/run_grnd_validation.py --problem GRND004

# Vampire only (skip Z3)
python3 Generators/DeonticOntology/run_grnd_validation.py --ext --vampire-only

# Z3 only (skip Vampire)
python3 Generators/DeonticOntology/run_grnd_validation.py --ext --z3-only

# With proof output for a specific problem
python3 Generators/DeonticOntology/run_grnd_validation.py --problem GRND004 --proof

# Longer timeout if Vampire hits limits
python3 Generators/DeonticOntology/run_grnd_validation.py --ext --timeout 120
```

Results land in `results/grnd_foundation_<date>.csv`. Exit code is 0 if all pass, 1 if any fail.

---

**Quick sanity check before full validation:**

```bash
# Confirm SMT2 preamble is the corrected v1.5 (NormContent, permission, founds-rem)
python3 -c "
import sys; sys.path.insert(0,'Generators/DeonticOntology')
from gen_signature import generate_smt2
p = generate_smt2()
assert 'NormContent' in p, 'FAIL: NormContent missing'
assert 'permission' in p, 'FAIL: permission missing'
assert 'founds-rem' in p, 'FAIL: founds-rem missing'
assert 'liberty' not in p, 'FAIL: liberty still present'
assert 'cnt-f' not in p, 'FAIL: cnt-f still present'
print('OK: preamble is v1.5')
"

# Confirm a generated SMT2 file parses cleanly under Z3
{ cat Problems/DeonticOntology/Entailment/GRND004-1.smt2; } | z3 -in
# expected: unsat
```

Clear dependency chain, bottom to top:

```
gen_layer0_signature.py
│
│  generates: GRND000-0.ax  (FOF preamble, included by all .p files)
│             GRND000-0.smt2 (SMT2 preamble, embedded by writers.py)
│
├──► axiom_data.py
│      │  contains: FOF_AXIOM_DICT, SMT2_AXIOMS, SMT2_APPENDIX_SORTS
│      │  depends on: nothing (standalone data module)
│      │
│      ├──► gen_layer1_deontic.py
│      │      imports: axiom_data.SMT2_AXIOMS
│      │      generates: GRND-AX-1.ax  (FOF axiom file)
│      │                 GRND-AX-1.smt2 (reference copy only)
│      │
│      ├──► problem_data.py
│      │      imports: axiom_data.FOF_AXIOM_DICT (via writers.py key lookup)
│      │      contains: PROBLEMS list (GRND001-009)
│      │
│      ├──► problem_data_ext.py    (GRND010-018)
│      ├──► problem_data_hard.py   (GRND019-024)
│      │
│      └──► writers.py
│             imports: axiom_data.FOF_AXIOM_DICT
│                      axiom_data.SMT2_AXIOMS
│                      axiom_data.SMT2_APPENDIX_SORTS
│             imports preamble from: gen_layer0_signature.generate_smt2()
│             writes: .p files (include Layer0 + inline Layer1 subset)
│                     .smt2 files (preamble + appendix + axioms + problem)
│                     (problem content comes from problem_data.py dicts)
│
└──► gen_foundation_problems.py
       imports: problem_data.PROBLEMS
                problem_data_ext.PROBLEMS_EXT
                problem_data_hard.PROBLEMS_HARD
                writers.write_fof_problem, write_smt2_problem
                problem_data.write_ttl_policy
       role: main() only — orchestrates everything
```

**The single source of truth chain:**

`axiom_data.py` → `writers.py` → `.p` / `.smt2` files

If axiom_data changes, writers.py picks it up automatically. `gen_layer1_deontic.py` and `writers.py` must stay in sync with axiom_data — that's where all the naming bugs cascaded from.