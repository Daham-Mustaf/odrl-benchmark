#!/usr/bin/env bash
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"

echo "=== Layer 0 ===" 
uv run Generators/DeonticOntology/gen_layer0_signature.py \
  --out-dir Problems/DeonticOntology/Axioms/Layer0-Signature

echo "=== Layer 1 ==="
uv run Generators/DeonticOntology/gen_layer1_deontic.py \
  --out-dir Problems/DeonticOntology/Axioms/Layer1-Deontic

echo "=== Problems ==="
uv run Generators/DeonticOntology/gen_foundation_problems.py \
  --out-dir Problems/DeonticOntology

echo "=== Z3 ==="
for f in Problems/DeonticOntology/**/*.smt2; do
  [[ "$f" == *GRND000* ]] && continue
  echo "$f:"; z3 -T:30 "$f"
done

echo "=== Vampire ==="
for f in Problems/DeonticOntology/**/*.p; do
  echo "$f:"
  vampire --mode casc -t 60 \
    --include Problems/DeonticOntology \
    "$f" | grep 'SZS status'
done