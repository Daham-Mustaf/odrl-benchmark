#!/usr/bin/env bash
# =============================================================================
# run_benchmark.sh — Run ODRL TPTP benchmark suite with Vampire
# Usage: ./scripts/run_benchmark.sh [timeout_seconds] [prover]
# =============================================================================
set -euo pipefail

TIMEOUT="${1:-60}"
PROVER="${2:-vampire}"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROBLEM_DIR="$PROJECT_ROOT/Problems/ODRL"
INCLUDE_DIR="$PROBLEM_DIR"
RESULTS_DIR="$PROJECT_ROOT/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTFILE="$RESULTS_DIR/benchmark_${TIMESTAMP}.csv"

mkdir -p "$RESULTS_DIR"

# ── Header ──────────────────────────────────────────────────────────────────
echo "problem,expected_szs,actual_szs,verdict,time_s,pass" > "$OUTFILE"

# ── Parse expected SZS from file header ─────────────────────────────────────
get_expected_szs() {
    local file="$1"
    local expected
    expected=$(grep -oP '% Expected : \K[^ ]+' "$file" | head -1)
    echo "$expected"
}

get_verdict() {
    local file="$1"
    local verdict
    verdict=$(grep -oP '% Verdict  : \K[^\n]+' "$file" | head -1)
    echo "$verdict"
}

# ── Run single problem ──────────────────────────────────────────────────────
run_problem() {
    local pfile="$1"
    local pname
    pname=$(basename "$pfile" .p)

    local expected_szs verdict
    expected_szs=$(get_expected_szs "$pfile")
    verdict=$(get_verdict "$pfile")

    # Skip if no expected status
    if [[ -z "$expected_szs" ]]; then
        echo "  SKIP  $pname (no expected SZS)"
        return
    fi

    local start_time actual_szs elapsed pass

    start_time=$(date +%s%N)

    if [[ "$PROVER" == "vampire" ]]; then
        actual_szs=$(timeout "${TIMEOUT}s" \
            vampire --include "$INCLUDE_DIR" \
                    --time_limit "$TIMEOUT" \
                    --output_axiom_names on \
                    "$pfile" 2>&1 \
            | grep -oP '% SZS status \K\w+' \
            || echo "Timeout")
    elif [[ "$PROVER" == "eprover" ]]; then
        actual_szs=$(timeout "${TIMEOUT}s" \
            eprover --auto \
                    --cpu-limit="$TIMEOUT" \
                    --include-path="$INCLUDE_DIR" \
                    "$pfile" 2>&1 \
            | grep -oP '# SZS status \K\w+' \
            || echo "Timeout")
    else
        echo "Unknown prover: $PROVER" >&2
        exit 1
    fi

    elapsed=$(( ($(date +%s%N) - start_time) / 1000000 ))
    elapsed_s=$(echo "scale=3; $elapsed / 1000" | bc)

    # Check pass/fail
    if [[ "$actual_szs" == "$expected_szs" ]]; then
        pass="PASS"
    elif [[ "$actual_szs" == "Timeout" ]]; then
        pass="TIMEOUT"
    else
        pass="FAIL"
    fi

    # Color output
    case "$pass" in
        PASS)    printf "  \033[32m✓ PASS\033[0m  %-16s  %-20s  %s  (%.3fs)\n" "$pname" "$actual_szs" "$verdict" "$elapsed_s" ;;
        FAIL)    printf "  \033[31m✗ FAIL\033[0m  %-16s  %-20s  expected: %s  (%.3fs)\n" "$pname" "$actual_szs" "$expected_szs" "$elapsed_s" ;;
        TIMEOUT) printf "  \033[33m⏱ TIME\033[0m  %-16s  %-20s  (>%ss)\n" "$pname" "Timeout" "$TIMEOUT" ;;
    esac

    echo "$pname,$expected_szs,$actual_szs,$verdict,$elapsed_s,$pass" >> "$OUTFILE"
}

# ── Main ────────────────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════════════════════════"
echo "  ODRL TPTP Benchmark — $(date)"
echo "  Prover:  $PROVER"
echo "  Timeout: ${TIMEOUT}s per problem"
echo "  Include: $INCLUDE_DIR"
echo "═══════════════════════════════════════════════════════════════"

total=0
pass=0
fail=0
timeout=0

for pfile in "$PROBLEM_DIR"/ODRL*.p; do
    [[ -f "$pfile" ]] || continue
    run_problem "$pfile"

    result=$(tail -1 "$OUTFILE" | cut -d, -f6)
    ((total++))
    case "$result" in
        PASS)    ((pass++)) ;;
        FAIL)    ((fail++)) ;;
        TIMEOUT) ((timeout++)) ;;
    esac
done

echo "═══════════════════════════════════════════════════════════════"
echo "  Results: $pass/$total passed, $fail failed, $timeout timeouts"
echo "  Output:  $OUTFILE"
echo "═══════════════════════════════════════════════════════════════"
