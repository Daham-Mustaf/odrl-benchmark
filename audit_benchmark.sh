#!/bin/bash

echo "════════════════════════════════════════════"
echo "1. MISSING ORD000 INCLUDE"
echo "════════════════════════════════════════════"
for f in Problems/ODRL/AxisDecomposition/**/*.p; do
  if ! grep -q "ORD000-0.ax" "$f" && ! grep -q "SUBS000-0.ax" "$f"; then
    echo "  MISSING ORD000: $(basename $f)"
  fi
done

echo ""
echo "════════════════════════════════════════════"
echo "2. OPEN INTERVAL + EXISTENTIAL (potential E timeout)"
echo "════════════════════════════════════════════"
for f in Problems/ODRL/AxisDecomposition/**/*.p; do
  conj=$(grep -A5 "conjecture" "$f" | grep -c "in_open")
  exists=$(grep -A5 "conjecture" "$f" | grep -c "?\[")
  if [ "$conj" -gt 0 ] && [ "$exists" -gt 0 ]; then
    echo "  OPEN+EXISTS: $(basename $f)"
  fi
done

echo ""
echo "════════════════════════════════════════════"
echo "3. SUBS000 BEFORE AXIS000 (wrong include order)"
echo "════════════════════════════════════════════"
for f in Problems/ODRL/AxisDecomposition/**/*.p; do
  if grep -q "SUBS000" "$f"; then
    subs_line=$(grep -n "SUBS000" "$f" | cut -d: -f1)
    axis_line=$(grep -n "AXIS000" "$f" | cut -d: -f1)
    if [ ! -z "$axis_line" ] && [ "$subs_line" -lt "$axis_line" ]; then
      echo "  BAD ORDER: $(basename $f)"
    fi
  fi
done

echo ""
echo "════════════════════════════════════════════"
echo "4. E RESOURCEOUT (9s timeout)"
echo "════════════════════════════════════════════"
for f in Problems/ODRL/AxisDecomposition/**/*.p; do
  result=$(eprover --auto --cpu-limit=9 --silent "$f" 2>/dev/null | grep "SZS status")
  if echo "$result" | grep -q "ResourceOut"; then
    echo "  E FAIL: $(basename $f)"
  fi
done

echo ""
echo "════════════════════════════════════════════"
echo "5. VAMPIRE FAILURES (9s timeout)"
echo "════════════════════════════════════════════"
for f in Problems/ODRL/AxisDecomposition/**/*.p; do
  result=$(vampire --mode casc --time_limit 9 "$f" 2>/dev/null | grep "SZS status")
  if ! echo "$result" | grep -qE "Theorem|CounterSatisfiable|Satisfiable|Unsatisfiable"; then
    echo "  VAMPIRE FAIL: $(basename $f)"
  fi
done

echo ""
echo "════════════════════════════════════════════"
echo "6. Z3 FAILURES"
echo "════════════════════════════════════════════"
for f in Problems/ODRL/AxisDecomposition/**/*.smt2; do
  result=$(z3 "$f" 2>/dev/null | head -1)
  if [ "$result" != "sat" ] && [ "$result" != "unsat" ]; then
    echo "  Z3 FAIL: $(basename $f) → $result"
  fi
done

echo ""
echo "Done."
