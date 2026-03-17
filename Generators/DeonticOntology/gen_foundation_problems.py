"""
gen_foundation_problems.py
==========================
Generates FOF/TPTP (.p), SMT-LIB (.smt2), and Turtle (.ttl) files for the
FOIS 2026 deontic grounding validation (Paper §6).

Module structure:
  axiom_data.py    — FOF_AXIOM_DICT, SMT2_AXIOMS, shared constants
  problem_data.py  — PROBLEMS list, write_ttl_policy()
  writers.py       — write_fof_problem(), write_smt2_problem()
  gen_foundation_problems.py  — this file: main() only (~50 lines)

CHANGELOG v1.4:
  - Split into modules: axiom_data, problem_data, writers
  - Real .ttl policy files written to Problems/DeonticOntology/Policies/
  - Policy link added to every .p and .smt2 header
  - SMT2_PREAMBLE imported from gen_signature.generate_smt2() — no more copy
  - TTL uses real Turtle syntax (no comment prefixes)
CHANGELOG v1.3:
  - Per-problem axiom inlining (fof_axioms key) — eliminates Vampire timeout
  - FOF_AXIOM_DICT for selective inclusion
CHANGELOG v1.2:
  - FOF files use include() for Layer0 + inline Layer1 subset
  - founds/3 throughout

Output layout:
  Problems/DeonticOntology/
    Axioms/
      Layer0-Signature/
        GRND000-0.ax        -- signature    (gen_layer0_signature.py)
        GRND000-0.smt2
      Layer1-Deontic/
        GRND-AX-1.ax        -- theory axioms (gen_layer1_deontic.py)
        GRND-AX-1.smt2      -- SMT-LIB reference copy
    Policies/
        GRND001-policy.ttl  -- real Turtle policy per problem
        ...
        GRND009-no-immunity-policy.ttl
    Consistency/
        GRND001-1.p / .smt2
    Entailment/
        GRND002-1.p / .smt2  ...  GRND006-1.p / .smt2
    Discriminating/
        GRND007-open-1.p / .smt2  ...  GRND009-no-immunity-1.p / .smt2

Usage:
    uv run Generators/DeonticOntology/gen_foundation_problems.py \
      --out-dir Problems/DeonticOntology
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from problem_data import PROBLEMS, write_ttl_policy
from writers import write_fof_problem, write_smt2_problem


def main():
    parser = argparse.ArgumentParser(
        description="Generate FOF/SMT-LIB/TTL files for GRND DeonticOntology v1.4."
    )
    parser.add_argument(
        "--out-dir",
        default="Problems/DeonticOntology",
        help="Root output directory (default: Problems/DeonticOntology)",
    )
    # kept for backward compat with run_all.sh — values ignored
    parser.add_argument("--sig-ax",  default=None, help=argparse.SUPPRESS)
    parser.add_argument("--sig-smt", default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    written = []

    for p in PROBLEMS:
        ttl_path  = write_ttl_policy(p, out_dir)
        fof_path  = write_fof_problem(p, out_dir)
        smt2_path = write_smt2_problem(p, out_dir)
        written.append((fof_path, smt2_path, ttl_path))

        ax_list = ", ".join(p.get("fof_axioms", [])) or "(none)"
        print(f"  {p['id']:25s}  FOF:{p['status_fof']:16s}  {fof_path.name}  [axioms: {ax_list}]")
        print(f"  {'':25s}  SMT:{p['status_smt']:16s}  {smt2_path.name}")
        if ttl_path:
            print(f"  {'':25s}  TTL:             {ttl_path.name}")

    n = len(written)
    print(f"\nTotal: {n} problem triples ({n * 3} files)")

    print("\nRun Vampire (FOF — refutation):")
    print("  for f in Problems/DeonticOntology/{Entailment,Discriminating}/*.p; do")
    print("    echo \"$f:\"; vampire --mode casc -t 60 \\")
    print("      --include Problems/DeonticOntology \"$f\" | grep 'SZS status'; done")

    print("\nRun Vampire (FOF — satisfiable):")
    print("  for f in Problems/DeonticOntology/Consistency/*.p \\")
    print("           Problems/DeonticOntology/Discriminating/GRND007-closed-1.p; do")
    print("    echo \"$f:\"; vampire --mode portfolio --schedule casc_sat -t 60 \\")
    print("      --include Problems/DeonticOntology \"$f\" | grep 'SZS status'; done")

    print("\nRun Z3 (SMT-LIB):")
    print("  for f in Problems/DeonticOntology/**/*.smt2; do")
    print("    [[ \"$f\" == *GRND000* || \"$f\" == *GRND-AX* ]] && continue")
    print("    echo \"$f:\"; z3 -T:30 \"$f\"; done")

    print("\nVerify all:")
    print("  bash verify_all.sh")


if __name__ == "__main__":
    main()