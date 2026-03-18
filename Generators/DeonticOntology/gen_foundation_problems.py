"""
gen_foundation_problems.py
==========================
Generates FOF/TPTP (.p), SMT-LIB (.smt2), and Turtle (.ttl) files for the
FOIS 2026 deontic grounding validation (Paper §6).

Module structure:
  axiom_data.py        — FOF_AXIOM_DICT, SMT2_AXIOMS, shared constants
  problem_data.py      — PROBLEMS list (GRND001-009), write_ttl_policy()
  problem_data_ext.py  — PROBLEMS_EXT (GRND010-018, easy/medium)
  problem_data_hard.py — PROBLEMS_HARD (GRND019-024, hard)
  writers.py           — write_fof_problem(), write_smt2_problem()
  gen_foundation_problems.py  — this file: main() only

CHANGELOG v1.5:
  - --ext flag: include extension problems GRND010-018
  - --hard flag: include hard problems GRND019-024
CHANGELOG v1.4:
  - Split into modules: axiom_data, problem_data, writers
  - Real .ttl policy files written to Problems/DeonticOntology/Policies/
  - Policy link added to every .p and .smt2 header
  - SMT2_PREAMBLE imported from gen_signature.generate_smt2()
  - TTL uses real Turtle syntax
CHANGELOG v1.3:
  - Per-problem axiom inlining (fof_axioms key)
CHANGELOG v1.2:
  - FOF files use include() for Layer0 + inline Layer1 subset

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
    Consistency/
        GRND001-1.p / .smt2
    Entailment/
        GRND002-1.p / .smt2  ...
    Discriminating/
        GRND007-open-1.p / .smt2  ...

Usage:
    # base problems only (GRND001-009)
    uv run Generators/DeonticOntology/gen_foundation_problems.py \\
      --out-dir Problems/DeonticOntology

    # base + extension (GRND001-018)
    uv run Generators/DeonticOntology/gen_foundation_problems.py \\
      --out-dir Problems/DeonticOntology --ext

    # all problems (GRND001-024)
    uv run Generators/DeonticOntology/gen_foundation_problems.py \\
      --out-dir Problems/DeonticOntology --ext --hard
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from problem_data import PROBLEMS, write_ttl_policy
from writers import write_fof_problem, write_smt2_problem

try:
    from problem_data_ext import PROBLEMS_EXT
except ImportError:
    PROBLEMS_EXT = []

try:
    from problem_data_hard import PROBLEMS_HARD
except ImportError:
    PROBLEMS_HARD = []


def main():
    parser = argparse.ArgumentParser(
        description="Generate FOF/SMT-LIB/TTL files for GRND DeonticOntology v1.5."
    )
    parser.add_argument(
        "--out-dir",
        default="Problems/DeonticOntology",
        help="Root output directory (default: Problems/DeonticOntology)",
    )
    parser.add_argument(
        "--ext",
        action="store_true",
        help="Also generate extension problems GRND010-018 (easy/medium)",
    )
    parser.add_argument(
        "--hard",
        action="store_true",
        help="Also generate hard problems GRND019-024",
    )
    # kept for backward compat with run_all.sh — values ignored
    parser.add_argument("--sig-ax",  default=None, help=argparse.SUPPRESS)
    parser.add_argument("--sig-smt", default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()

    problems = PROBLEMS[:]
    if args.ext:
        problems += PROBLEMS_EXT
    if args.hard:
        problems += PROBLEMS_HARD

    out_dir = Path(args.out_dir)
    written = []

    for p in problems:
        ttl_path  = write_ttl_policy(p, out_dir)
        fof_path  = write_fof_problem(p, out_dir)
        smt2_path = write_smt2_problem(p, out_dir)
        written.append((fof_path, smt2_path, ttl_path))

        ax_list = ", ".join(p.get("fof_axioms", [])) or "(none)"
        print(f"  {p['id']:30s}  FOF:{p['status_fof']:16s}  {fof_path.name}")
        print(f"  {'':30s}  SMT:{p['status_smt']:16s}  {smt2_path.name}")
        if ttl_path:
            print(f"  {'':30s}  TTL:             {ttl_path.name}")

    n = len(written)
    tier = "base"
    if args.hard:
        tier = "base+ext+hard"
    elif args.ext:
        tier = "base+ext"
    print(f"\nTotal [{tier}]: {n} problem triples ({n * 3} files)")

    print("\nVerify base (22 checks):")
    print("  bash verify_all.sh")
    print("\nVerify ext (40 checks):")
    print("  bash verify_all.sh --ext")


if __name__ == "__main__":
    main()