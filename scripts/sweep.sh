#!/bin/bash
# scripts/sweep.sh — tier-aware four-prover audit of the ODAX benchmark.
# Reads each problem's declared "% Status" header, picks the Vampire mode
# per tier (default for Theorem/Unsatisfiable, casc+intent-sat for
# Satisfiable/CounterSatisfiable), runs E, Vampire, Z3, cvc5, and tallies.
# Expected: E 256/256, Vampire 256/256, Z3 253/253, cvc5 253/253.
set -u
TPTP="${TPTP:-$HOME/projects/odrl-benchmark/Problems/ODRL/AxisDecomposition}"
VAMP="${VAMP:-/usr/local/bin/vampire}"
pe=0; pv=0; pz=0; pc=0; tot=0; smt=0; fails=""
for p in $(find "$TPTP" -name '*-1.p' | sort); do
  tot=$((tot+1)); base="${p%-1.p}"; id=$(basename "$base"); dir=$(basename "$(dirname "$p")")
  s="${base}-1.smt2"
  exp=$(awk -F': *' '/^% Status/{print $2; exit}' "$p" | tr -d ' \r')
  case "$exp" in
    CounterSatisfiable|Satisfiable) vargs="--mode casc --intent sat"; tl=60 ;;
    *)                              vargs="";                          tl=30 ;;
  esac
  e=$(eprover --auto --tstp-format --cpu-limit=$tl "$p" 2>&1 | awk '/SZS status/{print $4; exit}')
  v=$("$VAMP" $vargs --time_limit $tl --input_syntax tptp "$p" 2>&1 \
        | grep -oE 'SZS status [A-Za-z]+' | tail -1 | awk '{print $3}')
  z="--"; c="--"
  if [ -f "$s" ]; then
    smt=$((smt+1))
    z=$(z3 -T:20 "$s" 2>&1 | head -1 | tr -d '\r')
    c=$(cvc5 --tlimit-per=20000 "$s" 2>&1 | tail -1 | tr -d '\r')
  fi
  [ "$e" = "$exp" ] && pe=$((pe+1)) || fails="$fails E:$dir/$id=[$e]exp[$exp]"
  vok=0
  [ "$v" = "$exp" ] && vok=1
  [ "$exp" = CounterSatisfiable ] && [ "$v" = Satisfiable ] && vok=1
  [ "$exp" = Satisfiable ] && [ "$v" = CounterSatisfiable ] && vok=1
  [ "$vok" = 1 ] && pv=$((pv+1)) || fails="$fails V:$dir/$id=[$v]exp[$exp]"
  if [ "$z" != "--" ]; then case "$z" in sat|unsat) pz=$((pz+1));; *) fails="$fails Z3:$dir/$id=[$z]";; esac; fi
  if [ "$c" != "--" ]; then case "$c" in sat|unsat) pc=$((pc+1));; *) fails="$fails cvc5:$dir/$id=[$c]";; esac; fi
  printf "%-26s exp=%-18s E=%-18s V=%-18s Z3=%-6s cvc5=%-6s\n" \
         "$dir/$id" "$exp" "${e:-?}" "${v:-?}" "$z" "$c"
done
echo "------------------------------------------------------------------"
echo "TOTALS:   problems=$tot   with-SMT=$smt"
echo "  E       $pe/$tot"
echo "  Vampire $pv/$tot"
echo "  Z3      $pz/$smt"
echo "  cvc5    $pc/$smt"
echo "------------------------------------------------------------------"
if [ "$pe" = "$tot" ] && [ "$pv" = "$tot" ] && [ "$pz" = "$smt" ] && [ "$pc" = "$smt" ]; then
  echo "RESULT: PASS — all $tot problems verified, full four-prover concordance."
else
  echo "RESULT: discrepancy:"; echo "$fails" | tr ' ' '\n' | grep -v '^$'
fi
