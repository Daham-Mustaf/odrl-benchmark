```bash
cd ~/Desktop/tptp-odrl

# All standard categories
uv run Generators/AxisDecomposition/gen_axis_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition --cat all

  # Generate
uv run Generators/AxisDecomposition/gen_prec_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition

# SemanticCore separately
uv run Generators/AxisDecomposition/gen_semantic_core.py
```

```bash
echo "=== AxisDecomposition file counts ===" && \
echo "TTL policies : $(find Problems/ODRL/AxisDecomposition/Policies -name "*.ttl" | wc -l)" && \
echo "FOF problems : $(find Problems/ODRL/AxisDecomposition -name "*.p"    | wc -l)" && \
echo "SMT2 problems: $(find Problems/ODRL/AxisDecomposition -name "*.smt2" | wc -l)"
```

And per category:

```bash
echo "=== Per category ===" && \
for d in Problems/ODRL/AxisDecomposition/*/; do
    cat=$(basename "$d")
    [ "$cat" = "Axioms" ] && continue
    [ "$cat" = "Policies" ] && continue
    p=$(find "$d" -name "*.p"    | wc -l | tr -d ' ')
    s=$(find "$d" -name "*.smt2" | wc -l | tr -d ' ')
    printf "  %-15s  .p=%-3s  .smt2=%-3s\n" "$cat" "$p" "$s"
done
```

cd ~/Desktop/tptp-odrl

# Step 1 — regenerate all axiom files
uv run Generators/AxisDecomposition/gen_axis_signature.py \
  --out-dir Problems/ODRL/AxisDecomposition/Axioms

# Step 2 — regenerate all problem files
for cat in SingleAxis Box2D Box3D Composition PolicyQuality \
           Boundary LogicalOr LogicalXone; do
  uv run Generators/AxisDecomposition/gen_axis_problems.py \
    --out-dir Problems/ODRL/AxisDecomposition --cat $cat
done
uv run Generators/AxisDecomposition/gen_semantic_core.py

# Step 3 — validate all with Vampire + Z3
echo "=== Vampire ===" && pass=0; timeout=0; fail=0
for f in Problems/ODRL/AxisDecomposition/**/*.p; do
    r=$(vampire --include Problems/ODRL/AxisDecomposition \
        --mode vampire --time_limit 10 "$f" 2>&1 | grep "SZS status")
    if [[ "$r" == *"Theorem"* ]]; then ((pass++))
    elif [[ -z "$r" ]]; then ((timeout++)); echo "TIMEOUT: $(basename $f)"
    else ((fail++)); echo "FAIL: $(basename $f): $r"
    fi
done
echo "Vampire: PASS=$pass  TIMEOUT=$timeout  FAIL=$fail"

echo "=== Z3 ===" && pass=0; fail=0
for f in Problems/ODRL/AxisDecomposition/**/*.smt2; do
    r=$(z3 "$f" 2>&1)
    if [[ "$r" == "sat" || "$r" == "unsat" ]]; then ((pass++))
    else ((fail++)); echo "FAIL: $(basename $f): $r"
    fi
done
echo "Z3: PASS=$pass  FAIL=$fail"



echo "=== .p files (FOF problems) ==="
find Problems/ODRL/AxisDecomposition -name "*.p" | wc -l

echo ""
echo "=== .smt2 files ==="
find Problems/ODRL/AxisDecomposition -name "*.smt2" | wc -l

echo ""
echo "=== .ttl files (policies) ==="
find Problems/ODRL/AxisDecomposition -name "*.ttl" | wc -l

echo ""
echo "=== Per-category breakdown ==="
for d in Problems/ODRL/AxisDecomposition/*/; do
  p=$(find "$d" -name "*.p" | wc -l)
  s=$(find "$d" -name "*.smt2" | wc -l)
  t=$(find "$d" -name "*.ttl" | wc -l)
  echo "  $(basename $d): $p .p  $s .smt2  $t .ttl"
done