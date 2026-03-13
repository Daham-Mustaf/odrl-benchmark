#!/usr/bin/env bash
# =============================================================================
# cleanup_repo.sh  —  Make odrl-benchmark reviewer-ready in one run
# Run from:  cd ~/Desktop/tptp-odrl && bash cleanup_repo.sh
# =============================================================================
set -euo pipefail

echo "=== STEP 0: safety check ==="
if [ ! -f pyproject.toml ]; then
  echo "ERROR: run from repo root (where pyproject.toml lives)"
  exit 1
fi
echo "  OK, in $(pwd)"

# =============================================================================
# STEP 1: Identify canonical (latest) result files
# =============================================================================
echo ""
echo "=== STEP 1: canonical results ==="

E3_CANON=$(ls results/hierarchies/e3_all_*.csv | sort | tail -1)
E4_CANON=$(ls results/hierarchies/e4_crossds_*.csv | sort | tail -1)
CAT_CANON=$(ls results/categories/combined_all_*.csv 2>/dev/null | sort | tail -1 || \
            ls results/categories/combined_all_*.csv 2>/dev/null | head -1 || echo "MISSING")

echo "  E3 canonical: $E3_CANON"
echo "  E4 canonical: $E4_CANON"
echo "  Categories:   $CAT_CANON"

# =============================================================================
# STEP 2: Create clean directory structure
# =============================================================================
echo ""
echo "=== STEP 2: create clean dirs ==="

CLEAN=../odrl-benchmark-clean
rm -rf "$CLEAN"
mkdir -p "$CLEAN"/{Problems/ODRL,Axioms/{Layer0-DomainKB,Layer1-ODRLCore,Alignment},\
Isabelle/ODRL_Grounding,results,scripts,generators}

echo "  Created $CLEAN"

# =============================================================================
# STEP 3: Copy Problems (fix the typo: IncompletenessWeep → IncompletenessSwept)
# =============================================================================
echo ""
echo "=== STEP 3: copy Problems ==="

# KBGrounding — copy all subfolders except the misnamed one
for dir in KBGrounding/DAGMultiParent KBGrounding/EdgeCases KBGrounding/AdversarialOperators \
            KBGrounding/CombinedComplexity KBGrounding/LargeComposition \
            KBGrounding/MultiHopAlignment KBGrounding/NestedSetOperators \
            KBGrounding/NWayConflict KBGrounding/NWayComposed \
            KBGrounding/OperatorMonotonicity KBGrounding/QuantifierStress \
            KBGrounding/XONESymmetricDiff KBGrounding/Spatial; do
  src="Problems/ODRL/$dir"
  if [ -d "$src" ]; then
    cp -r "$src" "$CLEAN/Problems/ODRL/$dir" 2>/dev/null || true
    mkdir -p "$CLEAN/Problems/ODRL/$dir"
    cp -r "$src"/. "$CLEAN/Problems/ODRL/$dir/" 2>/dev/null || true
  fi
done

# IncompletenessWeep → IncompletenessSwept  (fix typo)
if [ -d "Problems/ODRL/KBGrounding/IncompletenessWeep" ]; then
  cp -r Problems/ODRL/KBGrounding/IncompletenessWeep \
        "$CLEAN/Problems/ODRL/KBGrounding/IncompletenessSwept"
  echo "  Renamed IncompletenessWeep → IncompletenessSwept"
fi

# CrossDS, AnalysisModes, AxisDecomposition
for dir in CrossDS AnalysisModes AxisDecomposition; do
  if [ -d "Problems/ODRL/$dir" ]; then
    cp -r "Problems/ODRL/$dir" "$CLEAN/Problems/ODRL/$dir"
    echo "  Copied $dir"
  fi
done

# SelfContained
if [ -d "Problems/ODRL/SelfContained" ]; then
  cp -r Problems/ODRL/SelfContained "$CLEAN/Problems/ODRL/SelfContained"
  echo "  Copied SelfContained"
fi

# =============================================================================
# STEP 4: Copy Axioms (flat clean structure)
# =============================================================================
echo ""
echo "=== STEP 4: copy Axioms ==="

cp Problems/ODRL/Axioms/Layer0-DomainKB/*.ax  "$CLEAN/Axioms/Layer0-DomainKB/" 2>/dev/null || true
cp Problems/ODRL/Axioms/Layer1-ODRLCore/*.ax   "$CLEAN/Axioms/Layer1-ODRLCore/" 2>/dev/null || true
cp Problems/ODRL/Axioms/Alignment/*.ax          "$CLEAN/Axioms/Alignment/"       2>/dev/null || true
echo "  Axioms copied"

# =============================================================================
# STEP 5: Copy canonical results only (no timestamp duplicates)
# =============================================================================
echo ""
echo "=== STEP 5: copy canonical results ==="

cp "$E3_CANON" "$CLEAN/results/e3_incompleteness_sweep.csv"
cp "$E4_CANON" "$CLEAN/results/e4_crossds_soundness.csv"

# Latest axis result
AXIS_CANON=$(ls results/axis/axis_benchmark_*.csv | sort | tail -1)
if [ -n "$AXIS_CANON" ]; then
  cp "$AXIS_CANON" "$CLEAN/results/axis_decomposition.csv"
  echo "  axis: $AXIS_CANON"
fi

# KB grounding — pick the latest spatial (longest run)
KB_CANON=$(ls results/hierarchies/kb__Spatial_*.csv | sort | tail -1)
if [ -n "$KB_CANON" ]; then
  cp "$KB_CANON" "$CLEAN/results/kb_grounding_spatial.csv"
fi

KB_ALIGN=$(ls results/hierarchies/kb__MultiHopAlignment_*.csv | sort | tail -1 || echo "")
[ -n "$KB_ALIGN" ] && cp "$KB_ALIGN" "$CLEAN/results/kb_grounding_alignment.csv"

KB_RT=$(ls results/hierarchies/kb__Runtime_*.csv | sort | tail -1 || echo "")
[ -n "$KB_RT" ] && cp "$KB_RT" "$CLEAN/results/kb_grounding_runtime.csv"

echo "  e3:  $CLEAN/results/e3_incompleteness_sweep.csv"
echo "  e4:  $CLEAN/results/e4_crossds_soundness.csv"

# =============================================================================
# STEP 6: Copy Isabelle proofs
# =============================================================================
echo ""
echo "=== STEP 6: copy Isabelle ==="
cp Isabelle/ODRL_Grounding/*.thy "$CLEAN/Isabelle/ODRL_Grounding/" 2>/dev/null || true
cp Isabelle/ROOT "$CLEAN/Isabelle/" 2>/dev/null || true
echo "  Isabelle copied"

# =============================================================================
# STEP 7: Copy runner scripts (clean names only)
# =============================================================================
echo ""
echo "=== STEP 7: copy scripts ==="
for f in run_e3_sweep.py run_e4_crossds.py run_all_categories.py run_all_experiments.sh; do
  [ -f "$f" ] && cp "$f" "$CLEAN/scripts/$f" && echo "  $f"
done

# =============================================================================
# STEP 8: Copy generators (renamed, no MODELS_PATCH, no ttt)
# =============================================================================
echo ""
echo "=== STEP 8: copy generators ==="
for f in generators/models.py generators/writer.py generators/kb_smt2.py; do
  [ -f "$f" ] && cp "$f" "$CLEAN/generators/" && echo "  $f"
done
# Exclude: MODELS_PATCH.py, ttt.py, cat10-cat19 (internal/messy)

# =============================================================================
# STEP 9: Generate stats from canonical CSVs
# =============================================================================
echo ""
echo "=== STEP 9: generate results summary ==="

python3 << PYEOF
import csv, sys, os, collections

def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return list(csv.DictReader(f))

base = "$CLEAN/results"

e3 = read_csv(f"{base}/e3_incompleteness_sweep.csv")
e4 = read_csv(f"{base}/e4_crossds_soundness.csv")

if e3:
    cols = list(e3[0].keys())
    print(f"\nE3 columns: {cols}")
    print(f"E3 rows: {len(e3)}")
    # Try common verdict column names
    for vcol in ['vampire_verdict','verdict','vampire','result','szs_status']:
        if vcol in cols:
            counts = collections.Counter(r[vcol] for r in e3)
            print(f"  E3 verdicts ({vcol}): {dict(counts)}")
            break
    # Try expected column
    for ecol in ['expected','expected_verdict','label','type']:
        if ecol in cols:
            counts = collections.Counter(r[ecol] for r in e3)
            print(f"  E3 expected ({ecol}): {dict(counts)}")
            break

if e4:
    cols = list(e4[0].keys())
    print(f"\nE4 columns: {cols}")
    print(f"E4 rows: {len(e4)}")
    for vcol in ['vampire_verdict','verdict','vampire','result','szs_status']:
        if vcol in cols:
            counts = collections.Counter(r[vcol] for r in e4)
            print(f"  E4 verdicts ({vcol}): {dict(counts)}")
            break

PYEOF

# =============================================================================
# STEP 10: Count problems per category
# =============================================================================
echo ""
echo "=== STEP 10: problem counts ==="
python3 << PYEOF2
import os, collections

root = "$CLEAN/Problems/ODRL"
counts = {}
total = 0
for dirpath, dirs, files in os.walk(root):
    pfiles = [f for f in files if f.endswith('.p')]
    if pfiles:
        rel = os.path.relpath(dirpath, root)
        counts[rel] = len(pfiles)
        total += len(pfiles)

for k in sorted(counts):
    print(f"  {k:55s} {counts[k]:4d}")
print(f"\n  TOTAL .p files: {total}")
PYEOF2

echo ""
echo "=== DONE ==="
echo "Clean repo at: $CLEAN"
echo "Now paste the output above back to Claude."
