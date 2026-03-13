#!/usr/bin/env bash
# =============================================================================
# build_clean_repo.sh
# Run from: cd ~/Desktop/tptp-odrl && bash build_clean_repo.sh
# Creates:  ~/Desktop/odrl-benchmark-vldb/  (reviewer-ready)
# =============================================================================
set -euo pipefail

SRC="$HOME/Desktop/tptp-odrl"
DST="$HOME/Desktop/odrl-benchmark-vldb"

echo "Source: $SRC"
echo "Target: $DST"

cd "$SRC"

# =============================================================================
# WIPE AND CREATE
# =============================================================================
rm -rf "$DST"
mkdir -p "$DST"/{Problems/ODRL,Axioms/{Layer0-DomainKB,Layer1-ODRLCore,Alignment},\
Isabelle/ODRL_Grounding,results,scripts}

# =============================================================================
# AXIOMS  (the foundation — must come first)
# =============================================================================
echo "Copying axioms..."
cp Problems/ODRL/Axioms/Layer0-DomainKB/*.ax  "$DST/Axioms/Layer0-DomainKB/"
cp Problems/ODRL/Axioms/Layer1-ODRLCore/*.ax   "$DST/Axioms/Layer1-ODRLCore/"
cp Problems/ODRL/Axioms/Alignment/*.ax          "$DST/Axioms/Alignment/"

# =============================================================================
# PROBLEMS — only the paper's benchmark groups
# =============================================================================
echo "Copying problems..."

# E3: Incompleteness Sweep (195 problems across 3 KBs × 5 levels)
# Rename typo: IncompletenessWeep → IncompletenessSwept
mkdir -p "$DST/Problems/ODRL/E3-IncompletenessSwept"
cp -r Problems/ODRL/KBGrounding/IncompletenessWeep/GEO  \
      "$DST/Problems/ODRL/E3-IncompletenessSwept/GEO"
cp -r Problems/ODRL/KBGrounding/IncompletenessWeep/DPV  \
      "$DST/Problems/ODRL/E3-IncompletenessSwept/DPV"
cp -r Problems/ODRL/KBGrounding/IncompletenessWeep/LANG \
      "$DST/Problems/ODRL/E3-IncompletenessSwept/LANG"

# E4: Cross-Dataspace (20 problems)
cp -r Problems/ODRL/CrossDS "$DST/Problems/ODRL/E4-CrossDataspace"

# Supporting: Analysis Modes (7 problems)
cp -r Problems/ODRL/AnalysisModes "$DST/Problems/ODRL/AnalysisModes"

# Supporting: KB Grounding (selected clean subcategories)
mkdir -p "$DST/Problems/ODRL/KBGrounding"
for cat in Spatial MultiHopAlignment DAGMultiParent EdgeCases \
           AdversarialOperators NWayConflict NWayComposed \
           OperatorMonotonicity XONESymmetricDiff; do
  if [ -d "Problems/ODRL/KBGrounding/$cat" ]; then
    cp -r "Problems/ODRL/KBGrounding/$cat" "$DST/Problems/ODRL/KBGrounding/$cat"
  fi
done

# =============================================================================
# CANONICAL RESULTS (latest run only — no timestamps duplicates)
# =============================================================================
echo "Copying results..."
# E3: use the freshest run
E3=$(ls results/hierarchies/e3_all_*.csv | sort | tail -1)
E4=$(ls results/hierarchies/e4_crossds_*.csv | sort | tail -1)
cp "$E3" "$DST/results/e3_incompleteness_sweep.csv"
cp "$E4" "$DST/results/e4_crossds_soundness.csv"

# =============================================================================
# ISABELLE PROOFS
# =============================================================================
echo "Copying Isabelle..."
cp Isabelle/ODRL_Grounding/ODRL_Grounding.thy "$DST/Isabelle/ODRL_Grounding/"
[ -f Isabelle/ODRL_Grounding/ODRL_Analysis_Modes.thy ] && \
  cp Isabelle/ODRL_Grounding/ODRL_Analysis_Modes.thy "$DST/Isabelle/ODRL_Grounding/"
[ -f Isabelle/ROOT ] && cp Isabelle/ROOT "$DST/Isabelle/"

# =============================================================================
# RUNNER SCRIPTS (clean, no internal mess)
# =============================================================================
echo "Copying scripts..."
cp run_e3_sweep.py  "$DST/scripts/run_e3_sweep.py"
cp run_e4_crossds.py "$DST/scripts/run_e4_crossds.py"
cp e3_z3_fix.py      "$DST/scripts/e3_z3_fix.py"

# =============================================================================
# COUNT EVERYTHING
# =============================================================================
echo ""
echo "=== PROBLEM COUNTS ==="
python3 -c "
import os
root = '$DST/Problems/ODRL'
total = 0
for dirpath, dirs, files in os.walk(root):
    p = [f for f in files if f.endswith('.p')]
    if p:
        rel = os.path.relpath(dirpath, root)
        print(f'  {rel:55s} {len(p):4d}')
        total += len(p)
print(f'  {\"TOTAL\":55s} {total:4d}')
"

echo ""
echo "=== RESULT COUNTS ==="
python3 -c "
import csv, collections
for name, path in [
    ('E3', '$DST/results/e3_incompleteness_sweep.csv'),
    ('E4', '$DST/results/e4_crossds_soundness.csv'),
]:
    rows = list(csv.DictReader(open(path)))
    print(f'{name}: {len(rows)} rows')
    for col in ['vampire','z3','pass']:
        if col in rows[0]:
            print(f'  {col}: {dict(collections.Counter(r[col] for r in rows))}')
"

echo ""
echo "=== DONE: $DST ==="
echo "Next step: cd $DST && git init && git add . && git commit -m 'initial'"