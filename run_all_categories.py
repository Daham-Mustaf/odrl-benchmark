#!/usr/bin/env python3
"""
run_all_categories.py — Run ALL KBGrounding benchmark categories with Vampire (+ optional Z3).
Saves per-category CSV to results/categories/<CategoryName>/<timestamp>.csv

Usage (from repo root):
    uv run python run_all_categories.py                  # all categories, Vampire only
    uv run python run_all_categories.py --z3             # + Z3
    uv run python run_all_categories.py --cat DAGMultiParent   # one category
    uv run python run_all_categories.py --timeout 60     # longer timeout
    uv run python run_all_categories.py --generate       # (re-)generate .p files first

Categories covered:
  KBGrounding/
    DAGMultiParent       (Cat 9,  ODRL100–105)
    NestedSetOperators   (Cat 10, ODRL110–114)
    QuantifierStress     (Cat 11, ODRL120–123)
    LargeComposition     (Cat 12, ODRL130–132)
    EdgeCases            (Cat 13, ODRL140–145)
    MultiHopAlignment    (Cat 14, ODRL150–159)
    NWayConflict         (Cat 15, ODRL160–165)
    NWayComposed         (Cat 16, ODRL170–175)
    SetOperatorStress    (Cat 17, ODRL200–205)
    CombinedComplexity   (Cat 18, ODRL210–215)
    AdversarialOperators (Cat 19, ODRL220–225)
    XONESymmetricDiff    (Cat 20, ODRL230–237)
    OperatorMonotonicity (Cat 21, ODRL250–254)
"""

import argparse, csv, re, subprocess, sys, time
from datetime import datetime
from pathlib import Path

# ── colours ──────────────────────────────────────────────────────────────
G="\033[32m"; R="\033[31m"; Y="\033[33m"; B="\033[36m"; X="\033[0m"
ok  = lambda s: f"{G}{s}{X}"
err = lambda s: f"{R}{s}{X}"
dim = lambda s: f"{Y}{s}{X}"

# ── All categories in order ───────────────────────────────────────────────
CATEGORIES = [
    "DAGMultiParent",
    "NestedSetOperators",
    "QuantifierStress",
    "LargeComposition",
    "EdgeCases",
    "MultiHopAlignment",
    "NWayConflict",
    "NWayComposed",
    "SetOperatorStress",
    "CombinedComplexity",
    "AdversarialOperators",
    "XONESymmetricDiff",
    "OperatorMonotonicity",
]

# ── Which generator produces each category ────────────────────────────────
CAT_TO_GENERATOR = {
    "DAGMultiParent":     "gen_advanced_suite.py",
    "NestedSetOperators": "gen_advanced_suite.py",
    "QuantifierStress":   "gen_advanced_suite.py",
    "LargeComposition":   "gen_advanced_suite.py",
    "EdgeCases":          "gen_advanced_suite.py",
    "MultiHopAlignment":  "gen_advanced_suite.py",
    "NWayConflict":       "gen_advanced_suite.py",
    "NWayComposed":       "gen_advanced_suite.py",
    "SetOperatorStress":  "gen_extreme_suite.py",
    "CombinedComplexity": "gen_extreme_suite.py",
    "AdversarialOperators":"gen_extreme_suite.py",
    "XONESymmetricDiff":  "gen_advanced_suite.py",
    "OperatorMonotonicity":"gen_advanced_suite.py",
}

# ── Expected-status normalisation ────────────────────────────────────────
def read_expected(fp: Path) -> str:
    with open(fp) as f:
        for line in f:
            if "% Expected" in line:
                return line.split(":")[-1].strip()
    return "Unknown"

def is_pass(actual: str, expected: str) -> bool:
    ok_map = {
        "Theorem":            {"Theorem", "ContradictoryAxioms", "Unsatisfiable"},
        "Unsatisfiable":      {"Unsatisfiable", "CounterSatisfiable"},
        "CounterSatisfiable": {"CounterSatisfiable", "Unsatisfiable", "Unknown", "Timeout"},
        "ContradictoryAxioms":{"Unsatisfiable", "ContradictoryAxioms", "Theorem"},
        "Unknown":            {"Unknown", "GaveUp", "Timeout"},
    }
    return actual in ok_map.get(expected, {expected})

# ── Provers ───────────────────────────────────────────────────────────────
def run_vampire(path: Path, inc_dir: Path, timeout: int) -> tuple[str, float]:
    try:
        t0 = time.time()
        r = subprocess.run(
            ["vampire", "--input_syntax", "tptp",
             "--include", str(inc_dir),
             "--time_limit", str(timeout), str(path)],
            capture_output=True, text=True, timeout=timeout + 10)
        elapsed = time.time() - t0
        for line in r.stdout.splitlines():
            if "SZS status" in line:
                return line.split("SZS status")[1].strip().split()[0], elapsed
        return "Unknown", elapsed
    except FileNotFoundError:
        return "NoVampire", 0.0
    except subprocess.TimeoutExpired:
        return "Timeout", float(timeout)

def run_z3(path: Path, timeout: int) -> tuple[str, float]:
    try:
        t0 = time.time()
        r = subprocess.run(["z3", f"-T:{timeout}", str(path)],
            capture_output=True, text=True, timeout=timeout + 10)
        elapsed = time.time() - t0
        out = (r.stdout + r.stderr).lower()
        if "unsat"   in out: return "unsat",   elapsed
        if "sat"     in out: return "sat",     elapsed
        return "unknown", elapsed
    except FileNotFoundError:
        return "NoZ3", 0.0
    except subprocess.TimeoutExpired:
        return "timeout", float(timeout)

# ── Pretty verdict cell ───────────────────────────────────────────────────
def fmt(v: str, passed: bool) -> str:
    if passed:    return ok(f"{v:<18}")
    if v in ("Unknown","GaveUp","Timeout","unknown","timeout"): return dim(f"{v:<18}")
    return err(f"{v:<18}")

# ── Run one category ──────────────────────────────────────────────────────
def run_category(cat: str, base: Path, timeout: int,
                 use_z3: bool) -> list[dict]:
    cat_dir  = base / "Problems" / "ODRL" / "KBGrounding" / cat
    inc_dir  = base / "Problems" / "ODRL"
    rows     = []

    if not cat_dir.exists():
        print(err(f"  ✗ {cat}: directory not found ({cat_dir})"))
        print(f"    Run: uv run python {CAT_TO_GENERATOR[cat]} --outdir Problems/ODRL")
        return rows

    files = sorted(cat_dir.glob("*.p"))
    if not files:
        print(dim(f"  – {cat}: no .p files found"))
        return rows

    print(f"\n{'='*72}")
    print(f"  {B}{cat}{X}  ({len(files)} problems)")
    print(f"{'='*72}")
    print(f"  {'File':<16} {'Expected':<22} {'Vampire':<18} "
          + ("{'Z3':<14} " if use_z3 else "")
          + f"{'Time':>6}  Result")
    print(f"  {'-'*70}")

    cat_pass = 0

    for fp in files:
        expected          = read_expected(fp)
        vstatus, vtime    = run_vampire(fp, inc_dir, timeout)
        passed            = is_pass(vstatus, expected)
        cat_pass         += passed
        sym               = ok("✓") if passed else err("✗")

        z3status, ztime = ("", 0.0)
        if use_z3:
            z3status, ztime = run_z3(fp, timeout)

        z3_col = f" {dim(z3status):<14}" if use_z3 else ""
        print(f"  {sym} {fp.name:<16} {expected:<22} "
              f"{fmt(vstatus, passed)}{z3_col} {vtime:>5.1f}s")

        rows.append({
            "category":  cat,
            "file":      fp.name,
            "expected":  expected,
            "vampire":   vstatus,
            "vampire_t": f"{vtime:.2f}",
            "z3":        z3status,
            "z3_t":      f"{ztime:.2f}" if use_z3 else "",
            "pass":      passed,
        })

    total = len(files)
    sym   = ok("✓") if cat_pass == total else err("✗")
    print(f"\n  {sym}  {cat}: {cat_pass}/{total} passed")
    return rows

# ── Save CSV ──────────────────────────────────────────────────────────────
def save_csv(rows: list[dict], out_path: Path, use_z3: bool) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["category","file","expected","vampire","vampire_t"]
    if use_z3:
        fields += ["z3","z3_t"]
    fields += ["pass"]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  {ok('CSV →')} {out_path}")

# ── Generate .p files if requested ───────────────────────────────────────
def regenerate(base: Path, cats: list[str]) -> None:
    generators = set(CAT_TO_GENERATOR[c] for c in cats)
    for gen in sorted(generators):
        gen_path = base / gen
        if not gen_path.exists():
            print(err(f"Generator not found: {gen_path}"))
            continue
        print(f"\n{dim('Generating:')} {gen}")
        result = subprocess.run(
            ["python3", str(gen_path), "--outdir", "Problems/ODRL"],
            cwd=base, capture_output=True, text=True)
        if result.returncode != 0:
            print(err(f"  Failed: {result.stderr[:200]}"))
        else:
            print(ok("  Done"))

# ── Main ──────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(
        description="Run all KBGrounding benchmark categories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python run_all_categories.py
  uv run python run_all_categories.py --z3
  uv run python run_all_categories.py --cat DAGMultiParent
  uv run python run_all_categories.py --cat MultiHopAlignment --timeout 60
  uv run python run_all_categories.py --generate          # re-generate first
  uv run python run_all_categories.py --list              # list categories

Available categories:
  """ + "\n  ".join(CATEGORIES))
    ap.add_argument("--cat",      default=None,
                    help="Run only one category (name from list above)")
    ap.add_argument("--timeout",  type=int, default=30)
    ap.add_argument("--z3",       action="store_true")
    ap.add_argument("--generate", action="store_true",
                    help="Re-run generator scripts before benchmarking")
    ap.add_argument("--list",     action="store_true",
                    help="List available categories and exit")
    ap.add_argument("--base-dir", default=".")
    args = ap.parse_args()

    if args.list:
        print("Available categories:")
        for c in CATEGORIES:
            print(f"  {c:<28} ({CAT_TO_GENERATOR[c]})")
        return

    base = Path(args.base_dir).resolve()

    # Filter categories
    if args.cat:
        matches = [c for c in CATEGORIES if args.cat.lower() in c.lower()]
        if not matches:
            print(err(f"Unknown category: {args.cat!r}"))
            print("Available: " + ", ".join(CATEGORIES))
            sys.exit(1)
        cats = matches
    else:
        cats = CATEGORIES

    print(f"\n{B}KBGrounding Benchmark Runner{X}")
    print(f"  Base    : {base}")
    print(f"  Cats    : {', '.join(cats)}")
    print(f"  Timeout : {args.timeout}s")
    print(f"  Z3      : {'yes' if args.z3 else 'no'}")

    # Optionally regenerate
    if args.generate:
        regenerate(base, cats)

    ts          = datetime.now().strftime("%Y%m%d_%H%M%S")
    all_rows    = []
    all_pass    = 0
    all_total   = 0
    cat_summary = []

    for cat in cats:
        rows      = run_category(cat, base, args.timeout, args.z3)
        cat_pass  = sum(1 for r in rows if r["pass"])
        cat_total = len(rows)
        all_pass += cat_pass
        all_total+= cat_total
        all_rows.extend(rows)
        cat_summary.append((cat, cat_pass, cat_total))

        # ── per-category CSV ──────────────────────────────────────────
        if rows:
            out = base / "results" / "categories" / cat / f"{cat}_{ts}.csv"
            save_csv(rows, out, args.z3)

    # ── Global summary ────────────────────────────────────────────────
    print(f"\n{'='*72}")
    print(f"  OVERALL RESULTS")
    print(f"{'='*72}")
    for cat, p, t in cat_summary:
        sym = ok("✓") if p == t else err("✗")
        bar = ok("█" * p) + err("░" * (t - p))
        print(f"  {sym} {cat:<28} {p:>3}/{t:<3}  {bar}")

    c = G if all_pass == all_total else R
    print(f"\n  Total : {all_total}   "
          f"Pass : {c}{all_pass}{X}   "
          f"Fail : {all_total - all_pass}")

    # ── Combined CSV ──────────────────────────────────────────────────
    if all_rows:
        tag = f"_{args.cat}" if args.cat else "_all"
        combined = base / "results" / "categories" / f"combined{tag}_{ts}.csv"
        save_csv(all_rows, combined, args.z3)

if __name__ == "__main__":
    main()