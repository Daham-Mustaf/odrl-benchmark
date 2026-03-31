#!/usr/bin/env bash
# verify_all.sh
# =============
# Runs Vampire + Z3 on the GRND foundation ontology benchmark.
# All results checked against expected SZS/SMT status.
#
# Usage:
#   bash verify_all.sh              # base only  (GRND001-009, 22 checks)
#   bash verify_all.sh --ext        # base + ext  (GRND001-018, 40 checks)
#   bash verify_all.sh --hard       # base + hard (GRND001-024, 34 checks)
#   bash verify_all.sh --ext --hard # all         (GRND001-024, 52 checks)
#
# Requires: vampire (>=5.0), z3 (>=4.14)
# Run from repo root: cd ~/Desktop/tptp-odrl

cd "$(dirname "$0")"

INCLUDE="Problems/DeonticOntology"
PASS=0
FAIL=0
ERRORS=()

# ============================================================================
# Runners
# ============================================================================
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

# ============================================================================
# BASE problems (GRND001-009) — 22 checks
# ============================================================================
echo "====== VAMPIRE (FOF) — Base ======"
run_vampire "portfolio --schedule casc_sat" \
    Problems/DeonticOntology/Consistency/GRND001-1.p              "Satisfiable"
run_vampire "portfolio --schedule casc_sat" \
    Problems/DeonticOntology/Discriminating/GRND007-closed-1.p    "Satisfiable"
run_vampire casc \
    Problems/DeonticOntology/Entailment/GRND002-1.p               "Theorem"
run_vampire casc \
    Problems/DeonticOntology/Entailment/GRND003-1.p               "Theorem"
run_vampire casc \
    Problems/DeonticOntology/Entailment/GRND004-1.p               "Theorem"
run_vampire casc \
    Problems/DeonticOntology/Entailment/GRND006-1.p               "Theorem"
run_vampire casc \
    Problems/DeonticOntology/Discriminating/GRND007-open-1.p      "Theorem"
run_vampire casc \
    Problems/DeonticOntology/Discriminating/GRND008-sanctioned-1.p "Theorem"
run_vampire casc \
    Problems/DeonticOntology/Entailment/GRND005-1.p               "Unsatisfiable"
run_vampire casc \
    Problems/DeonticOntology/Discriminating/GRND008-regimented-1.p "Unsatisfiable"
run_vampire casc \
    Problems/DeonticOntology/Discriminating/GRND009-immunity-1.p   "Unsatisfiable"
run_vampire casc \
    Problems/DeonticOntology/Discriminating/GRND009-no-immunity-1.p "Unsatisfiable"

echo ""
echo "====== Z3 (SMT-LIB) — Base ======"
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

# ============================================================================
# EXTENSION problems (GRND010-018) — 18 additional checks
# ============================================================================
if [[ " $* " == *" --ext "* ]] || [[ " $* " == *"--ext"* ]]; then
    echo ""
    echo "====== VAMPIRE (FOF) — Extension ======"
    run_vampire casc \
        Problems/DeonticOntology/Entailment/GRND010-strong-perm-1.p      "Theorem"
    run_vampire casc \
        Problems/DeonticOntology/Entailment/GRND011-obl-relator-1.p      "Theorem"
    run_vampire casc \
        Problems/DeonticOntology/Entailment/GRND012-corr-duty-1.p        "Theorem"
    run_vampire casc \
        Problems/DeonticOntology/Entailment/GRND013-corr-power-1.p       "Theorem"
    run_vampire casc \
        Problems/DeonticOntology/Entailment/GRND014-corr-immunity-1.p    "Theorem"
    run_vampire casc \
        Problems/DeonticOntology/Entailment/GRND015-unique-founding-1.p  "Theorem"
    run_vampire casc \
        Problems/DeonticOntology/Entailment/GRND016-conflict-relator-1.p "Unsatisfiable"
    run_vampire casc \
        Problems/DeonticOntology/Entailment/GRND017-violation-chain-1.p  "Theorem"
    run_vampire casc \
        Problems/DeonticOntology/Entailment/GRND018-about-event-1.p      "Theorem"

    echo ""
    echo "====== Z3 (SMT-LIB) — Extension ======"
    run_z3 Problems/DeonticOntology/Entailment/GRND010-strong-perm-1.smt2      "unsat"
    run_z3 Problems/DeonticOntology/Entailment/GRND011-obl-relator-1.smt2      "unsat"
    run_z3 Problems/DeonticOntology/Entailment/GRND012-corr-duty-1.smt2        "unsat"
    run_z3 Problems/DeonticOntology/Entailment/GRND013-corr-power-1.smt2       "unsat"
    run_z3 Problems/DeonticOntology/Entailment/GRND014-corr-immunity-1.smt2    "unsat"
    run_z3 Problems/DeonticOntology/Entailment/GRND015-unique-founding-1.smt2  "unsat"
    run_z3 Problems/DeonticOntology/Entailment/GRND016-conflict-relator-1.smt2 "unsat"
    run_z3 Problems/DeonticOntology/Entailment/GRND017-violation-chain-1.smt2  "unsat"
    run_z3 Problems/DeonticOntology/Entailment/GRND018-about-event-1.smt2      "unsat"
fi

# ============================================================================
# HARD problems (GRND019-024) — 12 additional checks
# ============================================================================
if [[ " $* " == *" --hard "* ]] || [[ " $* " == *"--hard"* ]]; then
    echo ""
    echo "====== VAMPIRE (FOF) — Hard ======"
    run_vampire casc \
        Problems/DeonticOntology/Discriminating/GRND019-two-policy-conflict-1.p  "Unsatisfiable"
    run_vampire casc \
        Problems/DeonticOntology/Discriminating/GRND020-strong-perm-full-h2-1.p  "Unsatisfiable"
    run_vampire casc \
        Problems/DeonticOntology/Discriminating/GRND021-remedy-chain-1.p         "Theorem"
    run_vampire casc \
        Problems/DeonticOntology/Discriminating/GRND022-corr-nonunique-1.p       "Unsatisfiable"
    run_vampire casc \
        Problems/DeonticOntology/Discriminating/GRND023-policy-issuance-1.p      "Theorem"
    run_vampire "portfolio --schedule casc_sat" \
        Problems/DeonticOntology/Discriminating/GRND024-obl-proh-conflict-1.p    "Satisfiable"

    echo ""
    echo "====== Z3 (SMT-LIB) — Hard ======"
    run_z3 Problems/DeonticOntology/Discriminating/GRND019-two-policy-conflict-1.smt2  "unsat"
    run_z3 Problems/DeonticOntology/Discriminating/GRND020-strong-perm-full-h2-1.smt2  "unsat"
    run_z3 Problems/DeonticOntology/Discriminating/GRND021-remedy-chain-1.smt2         "unsat"
    run_z3 Problems/DeonticOntology/Discriminating/GRND022-corr-nonunique-1.smt2       "unsat"
    run_z3 Problems/DeonticOntology/Discriminating/GRND023-policy-issuance-1.smt2      "unsat"
fi

# ============================================================================
# SUMMARY
# ============================================================================
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