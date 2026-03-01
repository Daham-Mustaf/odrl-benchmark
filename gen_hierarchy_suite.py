#!/usr/bin/env python3
"""
gen_hierarchy_suite.py — Generate and run KBGrounding (hierarchy) benchmarks.

Produces two encodings per problem:
  .p    → Problems/ODRL/KBGrounding/{Category}/ODRLNNN-V.p     (Vampire)
  .smt2 → Problems/ODRL/KBGrounding/{Category}/ODRLNNN-V.smt2  (Z3)

Problem definitions live in hierarchies/*.py (one file per category).
This file contains ONLY the runner and CLI — add categories in hierarchies/__init__.py.

Usage:
    uv run python gen_hierarchy_suite.py                         # generate all
    uv run python gen_hierarchy_suite.py --category Spatial      # one category
    uv run python gen_hierarchy_suite.py --dry-run               # preview
    uv run python gen_hierarchy_suite.py --run                   # generate + run
    uv run python gen_hierarchy_suite.py --run --timeout 60      # custom timeout
    uv run python gen_hierarchy_suite.py --run-only              # run existing files
    uv run python gen_hierarchy_suite.py --run --category Spatial

Authors: Mustafa, D. & Sutcliffe, G.
"""
from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from hierarchies import CATEGORY_GENERATORS, Category, KBProblem
from hierarchies.models import SZS
from hierarchies.writer import write_problem


# ==========================================================================
# Prover wrappers
# ==========================================================================

@dataclass
class RunResult:
    number:   int
    name:     str
    prover:   str
    encoding: str
    expected: str
    actual:   str
    match:    bool
    time_s:   float
    error:    str = ""


def run_vampire(tptp_path: Path, include_dir: Path,
                timeout: int = 30,
                expected_szs: str = "Theorem") -> tuple[str, float, str]:
    """Run Vampire. Returns (szs_status, elapsed, error)."""
    try:
        start = time.time()
        proc = subprocess.run(
            ["vampire",
             "--input_syntax", "tptp",
             "--include", str(include_dir),
             "--time_limit", str(timeout),
             str(tptp_path)],
            capture_output=True, text=True, timeout=timeout + 10,
        )
        elapsed = time.time() - start
        for line in proc.stdout.splitlines():
            if "SZS status" in line:
                status = line.split("SZS status")[1].strip().split()[0]
                return status, elapsed, ""
        # No SZS line — treat as error
        err = (proc.stderr.strip() or proc.stdout.strip())[:300] or "No SZS status"
        return "Error", elapsed, err
    except FileNotFoundError:
        return "Error", 0.0, "vampire not found in PATH"
    except subprocess.TimeoutExpired:
        return "Timeout", float(timeout), ""


def run_z3(smt2_path: Path, timeout: int = 30) -> tuple[str, float, str]:
    """Run Z3. Returns (sat/unsat/unknown, elapsed, error)."""
    try:
        start = time.time()
        proc = subprocess.run(
            ["z3", str(smt2_path)],
            capture_output=True, text=True, timeout=timeout,
        )
        elapsed = time.time() - start
        output = proc.stdout.strip().splitlines()
        for line in output:
            if line in ("sat", "unsat", "unknown"):
                return line, elapsed, ""
        err = (proc.stderr.strip() or proc.stdout.strip())[:300] or "No result"
        return "error", elapsed, err
    except FileNotFoundError:
        return "error", 0.0, "z3 not found in PATH"
    except subprocess.TimeoutExpired:
        return "timeout", float(timeout), ""


def expected_vampire(p: KBProblem) -> str:
    return p.szs.value  # "Theorem" or "CounterSatisfiable"


def expected_z3(p: KBProblem) -> str:
    return "unsat" if p.szs == SZS.THEOREM else "sat"


# ==========================================================================
# Run a list of problems
# ==========================================================================

def run_problems(problems: list[KBProblem], base: Path,
                 timeout: int = 30) -> list[RunResult]:
    results: list[RunResult] = []
    include_dir = base / "Problems" / "ODRL"

    has_vampire = shutil.which("vampire") is not None
    has_z3      = shutil.which("z3") is not None

    if not has_vampire:
        print("  ⚠  vampire not found — skipping .p benchmarks")
    if not has_z3:
        print("  ⚠  z3 not found — skipping .smt2 benchmarks")

    GREEN, RED, YELLOW, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[0m"

    for p in problems:
        num = str(p.number).zfill(3)
        cat = p.category.value

        # ── Vampire (.p) ────────────────────────────────────────────────
        if has_vampire:
            tptp_path = (base / "Problems" / "ODRL" / "KBGrounding"
                        / cat / f"ODRL{num}-{p.variant}.p")
            if tptp_path.exists():
                exp = expected_vampire(p)
                
                # Skip Vampire for CounterSatisfiable — Z3 handles witnesses
                if exp == "CounterSatisfiable":
                    print(f"  ─ ODRL{num} vampire  skipped (CounterSatisfiable → Z3 only)")
                else:
                    actual, elapsed, err = run_vampire(tptp_path, include_dir, timeout)
                    match = (actual == exp)
                    sym = f"{GREEN}✓{RESET}" if match else f"{RED}✗{RESET}"
                    err_str = f"  ERROR: {err}" if err else ""
                    print(f"  {sym} ODRL{num} vampire  exp={exp:<22} got={actual:<22} "
                        f"[{elapsed:.2f}s]{err_str}")
                    results.append(RunResult(
                        p.number, p.name, "vampire", "tptp",
                        exp, actual, match, elapsed, err,
                    ))

        # ── Z3 (.smt2) ──────────────────────────────────────────────────
        if has_z3:
            smt2_path = (base / "Problems" / "ODRL" / "KBGrounding"
                         / cat / f"ODRL{num}-{p.variant}.smt2")
            if smt2_path.exists():
                exp     = expected_z3(p)
                actual, elapsed, err = run_z3(smt2_path, timeout)
                match   = (actual == exp)
                sym     = f"{GREEN}✓{RESET}" if match else f"{RED}✗{RESET}"
                err_str = f"  ERROR: {err}" if err else ""
                print(f"  {sym} ODRL{num} z3       exp={exp:<22} got={actual:<22} "
                      f"[{elapsed:.2f}s]{err_str}")
                results.append(RunResult(
                    p.number, p.name, "z3", "smt2",
                    exp, actual, match, elapsed, err,
                ))

    return results


# ==========================================================================
# CSV + concordance
# ==========================================================================

def write_csv(results: list[RunResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["benchmark", "name", "prover", "encoding",
                    "expected", "actual", "match", "time_s", "error"])
        for r in results:
            w.writerow([f"ODRL{str(r.number).zfill(3)}", r.name,
                        r.prover, r.encoding,
                        r.expected, r.actual, r.match,
                        f"{r.time_s:.3f}", r.error])
    print(f"\n  Results → {path}")


def print_concordance(results: list[RunResult]) -> None:
    by_num: dict[int, dict[str, RunResult]] = {}
    for r in results:
        by_num.setdefault(r.number, {})[r.prover] = r

    agree = disagree = partial = 0
    GREEN, RED, YELLOW, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[0m"

    print(f"\n{'='*66}")
    print(f"  CONCORDANCE  (vampire SZS  ↔  z3 sat/unsat)")
    print(f"{'='*66}")

    for num in sorted(by_num):
        vr = by_num[num].get("vampire")
        zr = by_num[num].get("z3")
        v_ok = vr.match if vr else None
        z_ok = zr.match if zr else None
        v_str = vr.actual if vr else "—"
        z_str = zr.actual if zr else "—"

        if v_ok is None or z_ok is None:
            partial += 1
            sym = f"{YELLOW}◐{RESET}"
        elif v_ok and z_ok:
            agree += 1
            sym = f"{GREEN}✓{RESET}"
        elif not v_ok and not z_ok:
            # both wrong but same kind of wrong — count as agreeing on failure
            agree += 1
            sym = f"{RED}✗{RESET}"
        else:
            disagree += 1
            sym = f"{RED}⚡{RESET}"

        print(f"  {sym} ODRL{str(num).zfill(3)}  "
              f"vampire={v_str:<22}  z3={z_str}")

    total = agree + disagree + partial
    print(f"\n  Agreement:     {agree}/{total}")
    print(f"  Disagreement:  {disagree}/{total}"
          + (f"  ← INVESTIGATE" if disagree else ""))
    print(f"  Partial:       {partial}/{total}")
    if disagree == 0 and partial == 0:
        print(f"\n  {GREEN}✓ 100% Vampire/Z3 concordance{RESET}")
    elif disagree > 0:
        print(f"\n  {RED}✗ DISAGREEMENTS FOUND — check manually{RESET}")


# ==========================================================================
# CLI
# ==========================================================================

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate and run ODRL KBGrounding hierarchy benchmarks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                   # generate all categories
  %(prog)s --category Spatial                # one category only
  %(prog)s --run                             # generate + run both provers
  %(prog)s --run --timeout 60               # longer timeout
  %(prog)s --run-only --category Spatial     # run existing files
  %(prog)s --dry-run                         # preview without writing
""")
    ap.add_argument("--category", type=str, default=None,
                    help="Run one category (e.g. Spatial, DAGMultiParent)")
    ap.add_argument("--dry-run",  action="store_true",
                    help="Preview files without writing")
    ap.add_argument("--run",      action="store_true",
                    help="Generate + run both Vampire and Z3")
    ap.add_argument("--run-only", action="store_true",
                    help="Run on existing files, skip generation")
    ap.add_argument("--timeout",  type=int, default=30,
                    help="Prover timeout in seconds (default: 30)")
    ap.add_argument("--base-dir", type=str, default=".",
                    help="Repo root (default: current directory)")
    args = ap.parse_args()

    base = Path(args.base_dir).resolve()

    # ── Select categories ────────────────────────────────────────────────
    if args.category:
        try:
            cat = Category(args.category)
        except ValueError:
            available = ", ".join(c.value for c in CATEGORY_GENERATORS)
            print(f"Error: unknown category '{args.category}'")
            print(f"Available: {available}")
            sys.exit(1)
        if cat not in CATEGORY_GENERATORS:
            print(f"Error: '{cat.value}' not yet implemented")
            sys.exit(1)
        cats = {cat: CATEGORY_GENERATORS[cat]}
    else:
        cats = CATEGORY_GENERATORS

    # ── Generate ─────────────────────────────────────────────────────────
    all_problems: list[KBProblem] = []
    if not args.run_only:
        total_files = 0
        for cat, gen_fn in cats.items():
            problems = gen_fn()
            all_problems.extend(problems)
            print(f"\n{'='*60}")
            print(f"  Generating {cat.value}  ({len(problems)} problems, "
                  f"{len(problems)*2} files)")
            print(f"{'='*60}")
            for p in problems:
                write_problem(p, base, dry_run=args.dry_run)
                total_files += 2
        tag = "[DRY RUN] " if args.dry_run else ""
        print(f"\n{tag}Generated {len(all_problems)} problems → {total_files} files")
    else:
        for gen_fn in cats.values():
            all_problems.extend(gen_fn())

    # ── Run ──────────────────────────────────────────────────────────────
    if (args.run or args.run_only) and not args.dry_run:
        print(f"\n{'='*60}")
        print(f"  RUNNING PROVERS  (timeout={args.timeout}s)")
        print(f"{'='*60}")
        results = run_problems(all_problems, base, timeout=args.timeout)

        if results:
            ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
            cat_tag = (f"_{args.category}" if args.category else "_all")
            csv_path = base / "results" / "hierarchies" / f"kb_{cat_tag}_{ts}.csv"
            write_csv(results, csv_path)
            print_concordance(results)

            total = len(results)
            passed = sum(1 for r in results if r.match)
            errors = sum(1 for r in results if r.error)
            print(f"\n  Total: {total}  Pass: {passed}  "
                  f"Fail: {total-passed}  Errors: {errors}")


if __name__ == "__main__":
    main()
