cd ~/Desktop/tptp-odrl

# Step 1 — Generate axiom files
uv run Generators/DeonticOntology/gen_layer0_signature.py \
  --out-dir Problems/DeonticOntology/Axioms

uv run Generators/DeonticOntology/gen_layer1_deontic.py \
  --out-dir Problems/DeonticOntology/Axioms

# Step 2 — Generate all 39 problems
uv run Generators/DeonticOntology/gen_foundation_problems.py \
  --out-dir Problems/DeonticOntology --coverage

# Step 3 — Validate
uv run Generators/DeonticOntology/run_grnd_validation.py \
  --coverage --timeout 10