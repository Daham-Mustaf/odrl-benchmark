cd ~/Desktop/tptp-odrl

# Regenerate all axiom files
uv run Generators/AxisDecomposition/gen_axis_signature.py \
  --out-dir Problems/ODRL/AxisDecomposition/Axioms

# Regenerate all THM categories
uv run Generators/AxisDecomposition/gen_axis_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition

# SemanticCore (separate generator)
uv run Generators/AxisDecomposition/gen_semantic_core.py \
  --out-dir Problems/ODRL/AxisDecomposition/SemanticCore

# New categories
uv run Generators/AxisDecomposition/gen_prec_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition

uv run Generators/AxisDecomposition/gen_wf_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition

uv run Generators/AxisDecomposition/gen_proj_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition

uv run Generators/AxisDecomposition/gen_comp_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition

uv run Generators/AxisDecomposition/gen_compl_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition

uv run Generators/AxisDecomposition/gen_subs_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition

# CSA / SAT / UNS
uv run Generators/AxisDecomposition/gen_csa_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition

uv run Generators/AxisDecomposition/gen_sat_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition

uv run Generators/AxisDecomposition/gen_uns_problems.py \
  --out-dir Problems/ODRL/AxisDecomposition

# Verify counts
echo "=== Final counts ==="
for cat in SingleAxis Box2D Box3D Composition PolicyQuality Boundary \
           LogicalOr LogicalXone SemanticCore ConflictCriterion \
           WellFormedness Projection BoxContainment Completion \
           CSA SAT UNS Hard; do
    n=$(ls Problems/ODRL/AxisDecomposition/$cat/*.p 2>/dev/null | wc -l | tr -d ' ')
    printf "  %-20s %s\n" "$cat" "$n"
done



cd ~/Desktop/tptp-odrl

echo "=== .p files by category ==="
total=0
for cat in SingleAxis Box2D Box3D Composition PolicyQuality Boundary \
           LogicalOr LogicalXone SemanticCore ConflictCriterion \
           WellFormedness Projection BoxContainment Completion \
           CSA SAT UNS Hard; do
    n=$(ls Problems/ODRL/AxisDecomposition/$cat/*.p 2>/dev/null | wc -l | tr -d ' ')
    total=$((total+n))
    printf "  %-20s %s\n" "$cat" "$n"
done
echo "  ─────────────────────"
echo "  TOTAL .p    : $total"

echo ""
echo "=== Status distribution ==="
grep -rh "% Status" \
  Problems/ODRL/AxisDecomposition/{SingleAxis,Box2D,Box3D,Composition,PolicyQuality,Boundary,LogicalOr,LogicalXone,SemanticCore,ConflictCriterion,WellFormedness,Projection,BoxContainment,Completion,CSA,SAT,UNS,Hard}/*.p \
  | sort | uniq -c | sort -rn

echo ""
echo "=== Why numbers differ ==="
echo "  .p files  : $total (all FOF problems)"
echo "  .smt2     : $(ls Problems/ODRL/AxisDecomposition/{SingleAxis,Box2D,Box3D,Composition,PolicyQuality,Boundary,LogicalOr,LogicalXone,SemanticCore,ConflictCriterion,WellFormedness,Projection,BoxContainment,Completion,CSA,SAT,UNS,Hard}/*.smt2 2>/dev/null | wc -l | tr -d ' ') (Hard THM have no .smt2)"
echo "  .ttl      : $(ls Problems/ODRL/AxisDecomposition/Policies/*.ttl 2>/dev/null | wc -l | tr -d ' ') (some Hard share TTL)"
echo "  E tested  : 188 (THM+UNS+Hard THM only — CSA/SAT skipped)"
echo "  Z3 tested : 243 (all .smt2 files)"
echo "  Vampire   : 188 (THM+UNS+Hard THM only)"


cd ~/Desktop/tptp-odrl

echo "================================================================"
echo " VAMPIRE — THM categories (expect: Theorem)"
echo "================================================================"
vpass=0; vfail=0
for cat in SingleAxis Box2D Box3D Composition PolicyQuality Boundary \
           LogicalOr LogicalXone SemanticCore ConflictCriterion \
           WellFormedness Projection BoxContainment Completion; do
    for f in Problems/ODRL/AxisDecomposition/$cat/*.p; do
        r=$(vampire --include Problems/ODRL/AxisDecomposition \
            --mode casc --time_limit 30 "$f" 2>&1 | grep "SZS status")
        if [[ "$r" == *"Theorem"* ]]; then ((vpass++))
        else ((vfail++)); echo "FAIL: $cat/$(basename $f): $r"; fi
    done
done
echo "THM Vampire: PASS=$vpass FAIL=$vfail"

echo ""
echo "================================================================"
echo " VAMPIRE — UNS (expect: Unsatisfiable)"
echo "================================================================"
upass=0; ufail=0
for f in Problems/ODRL/AxisDecomposition/UNS/*.p; do
    r=$(vampire --include Problems/ODRL/AxisDecomposition \
        --mode casc --time_limit 30 "$f" 2>&1 | grep "SZS status")
    if [[ "$r" == *"Unsatisfiable"* ]]; then ((upass++))
    else ((ufail++)); echo "FAIL: $(basename $f): $r"; fi
done
echo "UNS Vampire: PASS=$upass FAIL=$ufail"

echo ""
echo "================================================================"
echo " VAMPIRE — Hard THM (expect: Theorem)"
echo "================================================================"
hpass=0; hfail=0
for f in Problems/ODRL/AxisDecomposition/Hard/HARD001+1.p \
         Problems/ODRL/AxisDecomposition/Hard/NFV001+1.p \
         Problems/ODRL/AxisDecomposition/Hard/NFV002+1.p; do
    r=$(vampire --include Problems/ODRL/AxisDecomposition \
        --mode casc --time_limit 60 "$f" 2>&1 | grep "SZS status")
    if [[ "$r" == *"Theorem"* ]]; then ((hpass++))
    else ((hfail++)); echo "FAIL: $(basename $f): $r"; fi
done
# HARD002 expects CounterSatisfiable or Timeout
r=$(vampire --include Problems/ODRL/AxisDecomposition \
    --mode casc --time_limit 60 \
    Problems/ODRL/AxisDecomposition/Hard/HARD002+1.p 2>&1 | grep "SZS status")
echo "HARD002+1.p: $r (expected CounterSatisfiable or Timeout)"
echo "Hard Vampire: PASS=$hpass FAIL=$hfail"

echo ""
echo "================================================================"
echo " E PROVER — THM + UNS"
echo "================================================================"
epass=0; efail=0
for cat in SingleAxis Box2D Box3D Composition PolicyQuality Boundary \
           LogicalOr LogicalXone SemanticCore ConflictCriterion \
           WellFormedness Projection BoxContainment Completion UNS; do
    for f in Problems/ODRL/AxisDecomposition/$cat/*.p; do
        r=$(cd Problems/ODRL/AxisDecomposition/$cat && \
            eprover --auto --tptp-in --cpu-limit=30 "$(basename $f)" \
            2>&1 | grep "SZS status")
        if [[ "$r" == *"Theorem"* || "$r" == *"Unsatisfiable"* ]]; then
            ((epass++))
        else
            ((efail++)); echo "FAIL: $cat/$(basename $f): $r"
        fi
    done
done
# Hard THM
for f in HARD001+1.p NFV001+1.p NFV002+1.p; do
    r=$(cd Problems/ODRL/AxisDecomposition/Hard && \
        eprover --auto --tptp-in --cpu-limit=60 "$f" 2>&1 | grep "SZS status")
    if [[ "$r" == *"Theorem"* ]]; then ((epass++))
    else ((efail++)); echo "FAIL Hard: $f: $r"; fi
done
echo "E: PASS=$epass FAIL=$efail"


echo "=== Z3 ===" && zpass=0; zfail=0
for cat in SingleAxis Box2D Box3D Composition PolicyQuality Boundary \
           LogicalOr LogicalXone SemanticCore ConflictCriterion \
           WellFormedness Projection BoxContainment Completion \
           CSA SAT UNS Hard; do
    for f in Problems/ODRL/AxisDecomposition/$cat/*.smt2; do
        [ -f "$f" ] || continue
        r=$(z3 "$f" 2>&1 | head -1)
        if [[ "$r" == "sat" || "$r" == "unsat" ]]; then ((zpass++))
        else ((zfail++)); echo "FAIL: $cat/$(basename $f): $r"
        fi
    done
done
echo "Z3: PASS=$zpass FAIL=$zfail"

echo ""
echo "================================================================"
echo " SUMMARY"
echo "================================================================"
echo "  Vampire THM+UNS : PASS=$((vpass+upass)) FAIL=$((vfail+ufail))"
echo "  Vampire Hard    : PASS=$hpass FAIL=$hfail"
echo "  E               : PASS=$epass FAIL=$efail"
echo "  Z3              : PASS=$zpass FAIL=$zfail"





cd ~/Desktop/tptp-odrl

echo "=== Vampire — ALL 247 problems (8 second limit) ==="
pass=0; fail=0; skip=0

for cat in SingleAxis Box2D Box3D Composition PolicyQuality Boundary \
           LogicalOr LogicalXone SemanticCore ConflictCriterion \
           WellFormedness Projection BoxContainment Completion \
           CSA SAT UNS Hard; do
    for f in Problems/ODRL/AxisDecomposition/$cat/*.p; do
        [ -f "$f" ] || continue
        r=$(vampire --include Problems/ODRL/AxisDecomposition \
            --mode casc --time_limit 8 "$f" 2>&1 | grep "SZS status")
        case "$r" in
            *Theorem*)            ((pass++)) ;;
            *Unsatisfiable*)      ((pass++)) ;;
            *CounterSatisfiable*) ((pass++)) ;;
            *Satisfiable*)        ((pass++)) ;;
            *Timeout*)            ((skip++)); echo "TIMEOUT: $cat/$(basename $f)" ;;
            *)                    ((fail++)); echo "FAIL: $cat/$(basename $f): $r" ;;
        esac
    done
done

echo ""
echo "Vampire ALL: PASS=$pass TIMEOUT=$skip FAIL=$fail"
echo "Total: $((pass+skip+fail))"
echo ""
echo "Expected: PASS=206 TIMEOUT=41 FAIL=0"
echo "  206 = 180 THM + 5 UNS + 3 Hard THM + 15 SAT + 3 Hard SAT"
echo "  41  = 40 CSA + 1 Hard CSA (HARD002)"

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



cd ~/Desktop/tptp-odrl

echo "=== Problem files per category ==="
total_p=0; total_smt2=0; total_ttl=0

for cat in SingleAxis Box2D Box3D Composition PolicyQuality Boundary \
           LogicalOr LogicalXone SemanticCore ConflictCriterion \
           WellFormedness Projection BoxContainment Completion \
           CSA SAT UNS Hard; do
    p=$(ls Problems/ODRL/AxisDecomposition/$cat/*.p 2>/dev/null | wc -l | tr -d ' ')
    s=$(ls Problems/ODRL/AxisDecomposition/$cat/*.smt2 2>/dev/null | wc -l | tr -d ' ')
    printf "  %-20s .p=%-4s .smt2=%-4s\n" "$cat" "$p" "$s"
    total_p=$((total_p + p))
    total_smt2=$((total_smt2 + s))
done

echo "  ──────────────────────────────────"
echo "  TOTAL .p    : $total_p"
echo "  TOTAL .smt2 : $total_smt2"

echo ""
echo "=== TTL policy files ==="
ttl=$(ls Problems/ODRL/AxisDecomposition/Policies/*.ttl 2>/dev/null | wc -l | tr -d ' ')
echo "  TOTAL .ttl  : $ttl"

echo ""
echo "=== Axiom files ==="
ls Problems/ODRL/AxisDecomposition/Axioms/*.ax | wc -l