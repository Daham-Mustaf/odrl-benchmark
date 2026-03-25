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