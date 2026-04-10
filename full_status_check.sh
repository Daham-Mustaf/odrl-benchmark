#!/bin/bash
# full_status_check.sh — complete benchmark statistics + status verification

echo "════════════════════════════════════════════════════"
echo "1. PROBLEM COUNT BY CATEGORY"
echo "════════════════════════════════════════════════════"
total=0
for d in Problems/ODRL/AxisDecomposition/*/; do
  n=$(find "$d" -name "*.p" | wc -l)
  [ "$n" -gt 0 ] && echo "  $(basename $d): $n" && total=$((total+n))
done
echo "  ─────────────────"
echo "  TOTAL: $total"

echo ""
echo "════════════════════════════════════════════════════"
echo "2. DECLARED STATUS DISTRIBUTION"
echo "════════════════════════════════════════════════════"
thm=0; csa=0; sat=0; uns=0; other=0
for f in Problems/ODRL/AxisDecomposition/**/*.p; do
  s=$(grep "^% Status" "$f" | head -1 | awk '{print $3}')
  case "$s" in
    Theorem)              ((thm++)) ;;
    CounterSatisfiable)   ((csa++)) ;;
    Satisfiable)          ((sat++)) ;;
    Unsatisfiable)        ((uns++)) ;;
    *)                    ((other++)); echo "  UNKNOWN STATUS: $(basename $f): '$s'" ;;
  esac
done
echo "  Theorem:            $thm"
echo "  CounterSatisfiable: $csa"
echo "  Satisfiable:        $sat"
echo "  Unsatisfiable:      $uns"
echo "  Unknown/Missing:    $other"
echo "  Total:              $((thm+csa+sat+uns+other))"

echo ""
echo "════════════════════════════════════════════════════"
echo "3. VAMPIRE STATUS VS DECLARED STATUS"
echo "════════════════════════════════════════════════════"
pass=0; fail=0; skip=0
for f in Problems/ODRL/AxisDecomposition/**/*.p; do
  declared=$(grep "^% Status" "$f" | head -1 | awk '{print $3}')
  [[ "$declared" == "Satisfiable" ]] && ((skip++)) && continue
  result=$(vampire --include Problems/ODRL/AxisDecomposition \
    --mode casc --time_limit 9 "$f" 2>/dev/null | grep "SZS status")
  case "$declared" in
    Theorem)
      echo "$result" | grep -q "Theorem" && ((pass++)) || \
        { ((fail++)); echo "  FAIL THM: $(basename $f): $result"; } ;;
    CounterSatisfiable)
      echo "$result" | grep -q "CounterSatisfiable" && ((pass++)) || \
        { ((fail++)); echo "  FAIL CSA: $(basename $f): $result"; } ;;
    Unsatisfiable)
      echo "$result" | grep -q "Unsatisfiable" && ((pass++)) || \
        { ((fail++)); echo "  FAIL UNS: $(basename $f): $result"; } ;;
  esac
done
echo "  PASS=$pass  FAIL=$fail  SKIP(SAT)=$skip"

echo ""
echo "════════════════════════════════════════════════════"
echo "4. Z3 STATUS VS DECLARED STATUS"
echo "════════════════════════════════════════════════════"
pass=0; fail=0
for f in Problems/ODRL/AxisDecomposition/**/*.smt2; do
  declared=$(grep "^; Status" "$f" | head -1 | awk '{print $3}')
  result=$(z3 "$f" 2>/dev/null | head -1)
  if [[ "$declared" == "$result" ]]; then
    ((pass++))
  else
    ((fail++))
    echo "  MISMATCH: $(basename $f): declared=$declared got=$result"
  fi
done
echo "  PASS=$pass  FAIL=$fail"

echo ""
echo "════════════════════════════════════════════════════"
echo "5. E STATUS (THM and UNS only)"
echo "════════════════════════════════════════════════════"
pass=0; fail=0; skip=0
for f in Problems/ODRL/AxisDecomposition/**/*.p; do
  declared=$(grep "^% Status" "$f" | head -1 | awk '{print $3}')
  [[ "$declared" != "Theorem" && "$declared" != "Unsatisfiable" ]] && \
    ((skip++)) && continue
  result=$(eprover --auto --cpu-limit=9 \
    --include-dir=Problems/ODRL/AxisDecomposition \
    --silent "$f" 2>/dev/null | grep "SZS status")
  case "$declared" in
    Theorem)
      echo "$result" | grep -q "Theorem" && ((pass++)) || \
        { ((fail++)); echo "  FAIL E: $(basename $f): $result"; } ;;
    Unsatisfiable)
      echo "$result" | grep -q "Unsatisfiable" && ((pass++)) || \
        { ((fail++)); echo "  FAIL E UNS: $(basename $f): $result"; } ;;
  esac
done
echo "  PASS=$pass  FAIL=$fail  SKIP=$skip"

echo ""
echo "════════════════════════════════════════════════════"
echo "6. METADATA COMPLETENESS"
echo "════════════════════════════════════════════════════"
meta_fail=0
for f in Problems/ODRL/AxisDecomposition/**/*.p; do
  missing=""
  grep -q "^% File"    "$f" || missing="$missing File"
  grep -q "^% Domain"  "$f" || missing="$missing Domain"
  grep -q "^% Status"  "$f" || missing="$missing Status"
  grep -q "^% SPC"     "$f" || missing="$missing SPC"
  grep -q "^% Refs"    "$f" || missing="$missing Refs"
  [ -n "$missing" ] && ((meta_fail++)) && \
    echo "  MISSING[$missing]: $(basename $f)"
done
[ "$meta_fail" -eq 0 ] && echo "  All metadata complete ✓" || \
  echo "  $meta_fail problems with missing metadata"

echo ""
echo "════════════════════════════════════════════════════"
echo "7. DIFFICULTY DISTRIBUTION"
echo "════════════════════════════════════════════════════"
easy=0; med=0; hard=0
for f in Problems/ODRL/AxisDecomposition/**/*.p; do
  d=$(grep "Difficulty" "$f" | head -1)
  echo "$d" | grep -q "Easy"   && ((easy++))
  echo "$d" | grep -q "Medium" && ((med++))
  echo "$d" | grep -q "Hard"   && ((hard++))
done
echo "  Easy:   $easy"
echo "  Medium: $med"
echo "  Hard:   $hard"

echo ""
echo "Done."
