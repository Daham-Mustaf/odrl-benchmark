```bash
cd ~/Desktop/tptp-odrl

# All standard categories
uv run Generators/AxisDecomposition/gen_axis_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition --cat all

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