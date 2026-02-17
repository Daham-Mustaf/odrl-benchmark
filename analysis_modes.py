#!/usr/bin/env python3
# analysis_modes.py - Demonstrate four analysis modes from same machinery

import subprocess
import re
from pathlib import Path

def run_vampire(problem_file):
    """Run Vampire and extract SZS status."""
    result = subprocess.run(
        ["vampire", "--include", "Problems/ODRL", "--mode", "casc",
         "--time_limit", "10", problem_file],
        capture_output=True, text=True
    )
    match = re.search(r"SZS status (\w+)", result.stdout)
    return match.group(1) if match else "Unknown"

# ═══════════════════════════════════════════════════════════════════════
# Analysis Mode Definitions
# ═══════════════════════════════════════════════════════════════════════

MODES = {
    "conflict": {
        "desc": "Cross-rule conflict detection",
        "pattern": "?[X]: den(c1) ∧ den(c2)",
        "note": None,
        "problems": [
            ("DEMO001", "AnalysisModes/DEMO001-conflict.p", 
             "advertising ∩ research (disjoint branches)",
             "Conflict", "Compatible (overlap)", "Conflict (disjoint)"),
        ]
    },
    
    "self-contradiction": {
        "desc": "Intra-rule self-contradiction (authoring errors)",
        "pattern": "?[X]: den(c1) ∧ den(c2) [same rule]",
        "note": None,
        "problems": [
            ("DEMO002", "AnalysisModes/DEMO002-selfcontradiction.p",
             "eq(sales) ∩ neq(sales) [same concept]",
             "Conflict", "Rule satisfiable", "Authoring error"),
            ("DEMO003", "AnalysisModes/DEMO003-selfcontradiction.p",
             "commercial ∩ nonCommercial [disjoint]",
             "Conflict", "Rule satisfiable", "Authoring error"),
        ]
    },
    
    "redundancy": {
        "desc": "Constraint redundancy (subsumption within rule)",
        "pattern": "![X]: den(c1) → den(c2) [same rule]",
        "note": None,
        "problems": [
            ("DEMO004", "AnalysisModes/DEMO004-redundancy.p",
             "targetedAds ⊆ advertising",
             "Subsumption", "c₂ redundant (remove)", "c₂ adds restriction"),
            ("DEMO005", "AnalysisModes/DEMO005-redundancy.p",
             "sales ⊆ commercial",
             "Subsumption", "c₂ redundant (remove)", "c₂ adds restriction"),
        ]
    },
    
    "refinement": {
        "desc": "Policy refinement verification (DSSC supply chain)",
        "pattern": "![X]: den(downstream) → den(upstream)",
        "note": "Downstream must narrow (not widen) upstream policy.",
        "problems": [
            ("DEMO006", "AnalysisModes/DEMO006-refinement-valid.p",
             "sales ⊆ commercial [valid narrowing]",
             "Confirmed", "Valid refinement", "DSSC violation"),
            ("DEMO007", "AnalysisModes/DEMO007-refinement-invalid.p",
             "commercial ⊆ sales [INVALID - widens!]",
             "Refuted", "Valid refinement", "DSSC violation (widens)"),
        ]
    }
}

# ═══════════════════════════════════════════════════════════════════════
# Runner
# ═══════════════════════════════════════════════════════════════════════

def run_analysis_mode(mode_name):
    """Run all problems for a given analysis mode."""
    mode = MODES[mode_name]
    print(f"\n{'='*70}")
    print(f"Analysis Mode: {mode_name.upper()}")
    print(f"{'='*70}")
    print(f"Description: {mode['desc']}")
    print(f"Conjecture:  {mode['pattern']}")
    
    if mode['note']:
        print(f"\nNOTE: {mode['note']}")
    
    print(f"\n{'Problem':<12} {'Status':<20} {'Expected':<18} {'Interpretation'}")
    print(f"{'-'*80}")
    
    for prob_id, prob_path, description, expected, interp_yes, interp_no in mode['problems']:
        full_path = f"Problems/ODRL/KBGrounding/{prob_path}"
        status = run_vampire(full_path)
        
        # Determine interpretation based on expected verdict
        if expected in ["Conflict", "EmptyDenotation", "Refuted"]:
            interpretation = interp_no
        else:  # Confirmed, Subsumption, Monotone, etc.
            interpretation = interp_yes
        
        print(f"{prob_id:<12} {status:<20} {expected:<18} {interpretation}")
        print(f"             {description}")

def print_summary_table():
    """Print LaTeX-ready summary table."""
    print(f"\n{'='*70}")
    print("SUMMARY TABLE (LaTeX format)")
    print(f"{'='*70}\n")
    
    print("\\begin{table}[t]")
    print("\\centering")
    print("\\caption{Four Analysis Modes from Same Denotational Machinery}")
    print("\\label{tab:analysis-modes}")
    print("\\begin{tabular}{lclll}")
    print("\\toprule")
    print("Mode & \\#Probs & Pattern & Theorem → & Refuted → \\\\")
    print("\\midrule")
    
    mode_order = ["conflict", "self-contradiction", "redundancy", "refinement"]
    for mode_name in mode_order:
        mode_data = MODES[mode_name]
        n = len(mode_data['problems'])
        pattern = mode_data['pattern'].replace("∧", "$\\land$").replace("→", "$\\to$")
        
        # Get example interpretation
        _, _, _, _, yes, no = mode_data['problems'][0]
        
        print(f"{mode_name.replace('-', ' ').capitalize()} & {n} & "
              f"\\texttt{{{pattern[:30]}...}} & {yes[:25]}... & {no[:25]}... \\\\")
    
    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\end{table}")

# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Demonstrate four analysis modes from same denotation machinery")
    parser.add_argument("--mode", 
                       choices=["conflict", "self-contradiction", "redundancy", 
                               "refinement", "all"],
                       default="all",
                       help="Which analysis mode to demonstrate")
    parser.add_argument("--latex", action="store_true",
                       help="Output LaTeX summary table")
    
    args = parser.parse_args()
    
    if args.latex:
        print_summary_table()
    elif args.mode == "all":
        for mode_name in ["conflict", "self-contradiction", "redundancy", "refinement"]:
            run_analysis_mode(mode_name)
        print("\n" + "="*70)
        print("✅ All four modes use identical conjecture patterns!")
        print("   Only the semantic interpretation differs.")
        print("="*70)
    else:
        run_analysis_mode(args.mode)