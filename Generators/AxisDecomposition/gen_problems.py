"""
gen_problems.py
==========
Unified orchestrator: walks every problem_data_*.py module, collects each
problem dict, and writes its .p (FOF) / .smt2 (SMT-LIB) / .ttl (Turtle)
files via writers.py.

Usage:
    cd ~/projects/odrl-benchmark
    uv run Generators/AxisDecomposition/gen_all.py

By default writes to Problems/ODRL/AxisDecomposition/{<subdir>,Policies}.
"""
import argparse
import importlib
import sys
from pathlib import Path

# Ensure Generators/ is on path so writers.py and header.py resolve
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from writers import write_fof_problem, write_smt2_problem, write_ttl_policy
# from problem_data_semcore       import PROBLEMS as P_SEMCORE


# Modules to load + which list variable to read from each.
# Order matters only for readability; output files are independent.
PROBLEM_MODULES = [
    ("problem_data",             "PROBLEMS"),       # SingleAxis (15)
    ("problem_data_box2d",       "PROBLEMS"),       # Box2D (15)
    ("problem_data_box3d",       "PROBLEMS"),       # Box3D (14)
    ("problem_data_composition", "PROBLEMS"),       # Composition (12)
    ("problem_data_comp",        "PROBLEMS"),       # Composition (10, verdict_algebra)
    ("problem_data_compl",       "PROBLEMS"),       # Completion (8)
    ("problem_data_subs",        "PROBLEMS"),       # BoxContainment (8)
    ("problem_data_pq",          "PROBLEMS"),       # PolicyQuality (17)
    ("problem_data_boundary",    "PROBLEMS"),       # Boundary (16)
    ("problem_data_or",          "PROBLEMS"),       # LogicalOr (12)
    ("problem_data_xone",        "PROBLEMS"),       # LogicalXone (11)
    # ("problem_data_prec",        "PROBLEMS"),       # ConflictCriterion (10)
    ("problem_data_wf",          "PROBLEMS"),       # WellFormedness (8)
    ("problem_data_proj",        "PROBLEMS"),       # Projection (10)
    ("problem_data_csa",         "PROBLEMS"),       # CSA-basic (15)
    ("problem_data_csa_ext",     "PROBLEMS_EXT"),   # CSA-extended (25)
    ("problem_data_sat",         "PROBLEMS"),       # SAT (5)
    ("problem_data_sat_ext",     "PROBLEMS_EXT"),   # SAT-extended (10)
    ("problem_data_uns",         "PROBLEMS"),       # UNS (3)
    ("problem_data_uns_ext",     "PROBLEMS_EXT"),   # UNS-extended (2)
    ("problem_data_criterion", "PROBLEMS"),       # ConflictCriterion (10)
    ("problem_data_semcore",     "PROBLEMS"),       # SemCore (10)
    ("problem_data_runtime",     "PROBLEMS"),       # Runtime (10)
]


def collect_problems():
    """Import each module and gather all problems with provenance."""
    all_problems = []
    for module_name, list_name in PROBLEM_MODULES:
        try:
            mod = importlib.import_module(module_name)
        except ImportError as e:
            print(f"  SKIP {module_name}: {e}", file=sys.stderr)
            continue
        problems = getattr(mod, list_name, None)
        if problems is None:
            print(f"  SKIP {module_name}: no '{list_name}' attribute", file=sys.stderr)
            continue
        for p in problems:
            all_problems.append((module_name, p))
    return all_problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[2])
    ap.add_argument(
        "--out-dir", default="Problems/ODRL/AxisDecomposition",
        help="Root output directory. Subdir per category.",
    )
    ap.add_argument(
        "--policies-subdir", default="Policies",
        help="Subdirectory under --out-dir for .ttl policy files.",
    )
    ap.add_argument(
        "--filter-category", default=None,
        help="Only generate problems whose 'subdir' matches this string.",
    )
    args = ap.parse_args()

    out_dir = Path(args.out_dir).resolve()
    policies_dir = out_dir / args.policies_subdir

    print(f"Output root: {out_dir}", file=sys.stderr)
    print(f"Policies dir: {policies_dir}", file=sys.stderr)
    print("", file=sys.stderr)

    all_problems = collect_problems()
    print(f"Collected {len(all_problems)} problems across "
          f"{len(set(m for m, _ in all_problems))} modules.", file=sys.stderr)
    print("", file=sys.stderr)

    # Track ID collisions (two modules defining the same ODRL number)
    ids_seen = {}
    collisions = []
    for module_name, p in all_problems:
        pid = p["id"]
        if pid in ids_seen:
            collisions.append((pid, ids_seen[pid], module_name))
        else:
            ids_seen[pid] = module_name

    if collisions:
        print(f"WARNING: {len(collisions)} duplicate IDs across modules:",
              file=sys.stderr)
        for pid, first, second in collisions[:10]:
            print(f"  {pid}: first in {first}, also in {second}", file=sys.stderr)
        if len(collisions) > 10:
            print(f"  ...and {len(collisions) - 10} more", file=sys.stderr)
        print("", file=sys.stderr)

    # Generate files
    counts = {"fof": 0, "smt2": 0, "ttl": 0, "errors": 0}
    by_category = {}

    for module_name, p in all_problems:
        if args.filter_category and p.get("subdir") != args.filter_category:
            continue
        try:
            write_fof_problem(p, out_dir)
            counts["fof"] += 1
            if p.get("smt2_asserts"):
                write_smt2_problem(p, out_dir)
                counts["smt2"] += 1
            if p.get("ttl"):
                write_ttl_policy(p, policies_dir)
                counts["ttl"] += 1
            by_category.setdefault(p["subdir"], 0)
            by_category[p["subdir"]] += 1
        except Exception as e:
            counts["errors"] += 1
            print(f"  ERROR generating {p['id']} from {module_name}: {e}",
                  file=sys.stderr)

    print("", file=sys.stderr)
    print("=== Per-category counts ===", file=sys.stderr)
    for cat in sorted(by_category):
        print(f"  {cat:<22s} {by_category[cat]:3d}", file=sys.stderr)
    print("", file=sys.stderr)
    print("=== Totals ===", file=sys.stderr)
    print(f"  .p files:   {counts['fof']}", file=sys.stderr)
    print(f"  .smt2 files: {counts['smt2']}", file=sys.stderr)
    print(f"  .ttl files:  {counts['ttl']}", file=sys.stderr)
    if counts["errors"]:
        print(f"  ERRORS:      {counts['errors']}", file=sys.stderr)

    sys.exit(0 if counts["errors"] == 0 else 1)


if __name__ == "__main__":
    main()
