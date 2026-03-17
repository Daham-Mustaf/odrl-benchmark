#!/usr/bin/env bash
cd "$(dirname "$0")"

INCLUDE="Problems/DeonticOntology"
PASS=0
FAIL=0
ERRORS=()

run_vampire() {
  local mode="$1" file="$2" expected="$3"
  local result
  result=$(vampire --mode $mode -t 60 \
    --include "$INCLUDE" "$file" 2>/dev/null | grep "SZS status" | awk '{print $4}')
  if [[ "$result" == "$expected" ]]; then
    echo "  PASS  [expected=$expected] $(basename $file)"
    PASS=$((PASS+1))
  else
    echo "  FAIL  [expected=$expected got=${result:-TIMEOUT}] $(basename $file)"
    FAIL=$((FAIL+1))
    ERRORS+=("$file")
  fi
}

run_z3() {
  local file="$1" expected="$2"
  local result
  result=$(z3 -T:30 "$file" 2>/dev/null | head -1)
  if [[ "$result" == "$expected" ]]; then
    echo "  PASS  [expected=$expected] $(basename $file)"
    PASS=$((PASS+1))
  else
    echo "  FAIL  [expected=$expected got=${result:-TIMEOUT}] $(basename $file)"
    FAIL=$((FAIL+1))
    ERRORS+=("$file")
  fi
}

echo "====== VAMPIRE (FOF) ======"
run_vampire "portfolio --schedule casc_sat" Problems/DeonticOntology/Consistency/GRND001-1.p           "Satisfiable"
run_vampire "portfolio --schedule casc_sat" Problems/DeonticOntology/Discriminating/GRND007-closed-1.p "Satisfiable"
run_vampire casc Problems/DeonticOntology/Entailment/GRND002-1.p                    "Theorem"
run_vampire casc Problems/DeonticOntology/Entailment/GRND003-1.p                    "Theorem"
run_vampire casc Problems/DeonticOntology/Entailment/GRND004-1.p                    "Theorem"
run_vampire casc Problems/DeonticOntology/Entailment/GRND006-1.p                    "Theorem"
run_vampire casc Problems/DeonticOntology/Discriminating/GRND007-open-1.p           "Theorem"
run_vampire casc Problems/DeonticOntology/Discriminating/GRND008-sanctioned-1.p     "Theorem"
run_vampire casc Problems/DeonticOntology/Entailment/GRND005-1.p                    "Unsatisfiable"
run_vampire casc Problems/DeonticOntology/Discriminating/GRND008-regimented-1.p     "Unsatisfiable"
run_vampire casc Problems/DeonticOntology/Discriminating/GRND009-immunity-1.p       "Unsatisfiable"
run_vampire casc Problems/DeonticOntology/Discriminating/GRND009-no-immunity-1.p    "Unsatisfiable"

echo ""
echo "====== Z3 (SMT-LIB) ======"
run_z3 Problems/DeonticOntology/Entailment/GRND002-1.smt2                  "unsat"
run_z3 Problems/DeonticOntology/Entailment/GRND003-1.smt2                  "unsat"
run_z3 Problems/DeonticOntology/Entailment/GRND004-1.smt2                  "unsat"
run_z3 Problems/DeonticOntology/Entailment/GRND005-1.smt2                  "unsat"
run_z3 Problems/DeonticOntology/Entailment/GRND006-1.smt2                  "unsat"
run_z3 Problems/DeonticOntology/Discriminating/GRND007-open-1.smt2         "unsat"
run_z3 Problems/DeonticOntology/Discriminating/GRND008-sanctioned-1.smt2   "unsat"
run_z3 Problems/DeonticOntology/Discriminating/GRND008-regimented-1.smt2   "unsat"
run_z3 Problems/DeonticOntology/Discriminating/GRND009-immunity-1.smt2     "unsat"
run_z3 Problems/DeonticOntology/Discriminating/GRND009-no-immunity-1.smt2  "unsat"

echo ""
echo "====== SUMMARY ======"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
if [[ ${#ERRORS[@]} -gt 0 ]]; then
  echo "  FAILED:"
  for f in "${ERRORS[@]}"; do echo "    $f"; done
else
  echo "  ALL CORRECT"
fi
