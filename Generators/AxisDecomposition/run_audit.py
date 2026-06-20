"""
run_audit.py
============
Comprehensive audit runner for the ODRL Axis Decomposition (OAX)
benchmark.  Runs every configured prover on every problem file matched
by --problems, writes a CSV log, and prints a per-prover reliability
summary.

The benchmark uses three relation types:
  conflict-test    -- asks: does sem(c1) cap sem(c2) overlap?
  subsumption      -- asks: does sem(c1) subseteq sem(c2)?
  verdict_algebra  -- asks: does the UF-encoded verdict reduction
                      give the claimed verdict (Theorem) or refute
                      a wrong claim (CSA)?

Saturation provers (Vampire saturation modes, E) are skipped on
problems with Status: Satisfiable or CounterSatisfiable, since
saturation cannot terminate on these by design. The model finder
(vampire-fmb) handles those cases.

Usage:
    cd ~/projects/odrl-benchmark
    uv run Generators/AxisDecomposition/run_audit.py \\
        --cwd Problems/ODRL/AxisDecomposition \\
        --problems '**/ODRL*.p' '**/HARD*.p' '**/NFV*.p' \\
        --timeout 60
"""
import argparse
import csv
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULT_PROBLEM_GLOBS = ["**/ODRL*.p", "**/HARD*.p", "**/NFV*.p"]
DEFAULT_TIMEOUT       = 60

PAPER_PROVERS = {"vampire-casc", "eprover", "z3"}

EXPECTED_CATEGORIES = [
    "SingleAxis", "Box2D", "Box3D", "Composition", "PolicyQuality",
    "Boundary", "LogicalOr", "LogicalXone", "SemanticCore",
    "ConflictCriterion", "WellFormedness", "Projection",
    "BoxContainment", "Completion", "CSA", "SAT", "UNS", "Hard",
]

# ---------------------------------------------------------------------------
# Prover command builders
# ---------------------------------------------------------------------------
def vampire_casc_cmd(prob, timeout):
    return ["vampire", "--mode", "casc",
            "--time_limit", str(timeout),
            "--include", ".", str(prob)]

def vampire_strategy_cmd(strategy, prob, timeout):
    return ["vampire", "--saturation_algorithm", strategy,
            "--time_limit", str(timeout),
            "--include", ".", str(prob)]

def eprover_cmd(prob, timeout):
    return ["eprover", "--auto", "--tstp-format",
            f"--cpu-limit={timeout}", "-s", str(prob)]

def z3_cmd(smt, timeout):
    return ["z3", f"-T:{timeout}", str(smt)]

def cvc5_cmd(smt, timeout):
    return ["cvc5", f"--tlimit={timeout * 1000}", str(smt)]

def vampire_fmb_cmd(prob, timeout):
    return ["vampire", "--saturation_algorithm", "fmb",
            "--fmb_start_size", "5",
            "--time_limit", str(timeout),
            "--include", ".", str(prob)]

# ---------------------------------------------------------------------------
# Output parsing
# ---------------------------------------------------------------------------
SZS_RE = re.compile(r"SZS status (\w+)")

def parse_szs(stdout, stderr):
    for line in stdout.splitlines():
        m = SZS_RE.search(line)
        if m:
            return m.group(1)
    return "NoStatus"

def parse_smt(stdout, stderr):
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if line in ("sat", "unsat", "unknown"):
            return line
    if "timeout" in stderr.lower() or "timeout" in stdout.lower():
        return "timeout"
    return "NoResult"

def normalize_szs(status):
    norm = {
        "Theorem":             "Theorem",
        "Unsatisfiable":       "Unsatisfiable",
        "ContradictoryAxioms": "Unsatisfiable",
        "CounterSatisfiable":  "CounterSatisfiable",
        "Satisfiable":         "Satisfiable",
        "Timeout":              "Timeout",
        "ResourceOut":          "Timeout",
        "GaveUp":               "GaveUp",
        "NoStatus":             "Error",
    }
    return norm.get(status, status)

# ---------------------------------------------------------------------------
# Prover registry
# ---------------------------------------------------------------------------
PROVER_FOF = [
    ("vampire-casc",
     lambda p, t: vampire_casc_cmd(p, t),
     parse_szs, normalize_szs),
    ("vampire-discount",
     lambda p, t: vampire_strategy_cmd("discount", p, t),
     parse_szs, normalize_szs),
    ("vampire-lrs",
     lambda p, t: vampire_strategy_cmd("lrs", p, t),
     parse_szs, normalize_szs),
    ("vampire-otter",
     lambda p, t: vampire_strategy_cmd("otter", p, t),
     parse_szs, normalize_szs),
    ("eprover",
     lambda p, t: eprover_cmd(p, t),
     parse_szs, normalize_szs),
]

# FMB: model finder for Satisfiable + CounterSatisfiable problems
PROVER_FOF_UNKNOWN = [
    ("vampire-fmb",
     lambda p, t: vampire_fmb_cmd(p, t),
     parse_szs, normalize_szs),
]

PROVER_SMT = [
    ("z3",
     lambda p, t: z3_cmd(p, t),
     parse_smt, lambda x: x),
    ("cvc5",
     lambda p, t: cvc5_cmd(p, t),
     parse_smt, lambda x: x),
]

# ---------------------------------------------------------------------------
# Problem header parsing
# ---------------------------------------------------------------------------
STATUS_RE   = re.compile(r"%\s*Status\s*:?\s*(\w+)")
VERDICT_RE  = re.compile(r"%\s*Verdict\s*:?\s*(\w+)")
RELATION_RE = re.compile(r"%\s*Relation\s*:?\s*(\w+)")

def read_header_field(prob_path, regex):
    try:
        with open(prob_path) as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                m = regex.search(line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return None

def expected_smt_status(verdict, relation):
    """Map (verdict, relation) -> expected Z3/cvc5 result."""
    if relation == "verdict_algebra":
        return {
            "Compatible":         "unsat",
            "Conflict":           "unsat",
            "Unknown":            "unsat",
            "CounterSatisfiable": "unsat",
        }.get(verdict)
    if relation == "subsumption":
        return {
            "Compatible": "unsat",
            "Conflict":   "sat",
            "Unknown":    None,
        }.get(verdict)
    return {
        "Conflict":   "unsat",
        "Compatible": "sat",
        "Unknown":    None,
    }.get(verdict)

# ---------------------------------------------------------------------------
# Pre-flight: Axioms symlink check
# ---------------------------------------------------------------------------
def check_axiom_symlinks(cwd):
    missing = []
    cwd = Path(cwd).resolve()
    if not (cwd / "Axioms").is_dir():
        return False, [".../Axioms (the shared axiom directory itself)"]
    for cat in EXPECTED_CATEGORIES:
        cat_dir = cwd / cat
        if not cat_dir.is_dir():
            continue
        link = cat_dir / "Axioms"
        if not link.exists():
            missing.append(cat)
    return (len(missing) == 0), missing

def print_symlink_fixup_hint(cwd, missing):
    print("", file=sys.stderr)
    print("=== Pre-flight failure: Axioms symlinks missing ===", file=sys.stderr)
    print(f"  CWD: {cwd}", file=sys.stderr)
    print(f"  Missing in: {', '.join(missing)}", file=sys.stderr)
    print("", file=sys.stderr)
    print("  Fix:", file=sys.stderr)
    print(f"    cd {cwd}", file=sys.stderr)
    print(f"    for d in {' '.join(missing)}; do", file=sys.stderr)
    print( "        ln -sfn ../Axioms \"$d/Axioms\"", file=sys.stderr)
    print( "    done", file=sys.stderr)
    print("", file=sys.stderr)

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def run_one(name, cmd_argv, timeout, cwd):
    if not shutil.which(cmd_argv[0]):
        return ("", f"binary not found: {cmd_argv[0]}", 0.0, -1)
    t0 = time.monotonic()
    try:
        res = subprocess.run(
            cmd_argv,
            capture_output=True, text=True,
            timeout=timeout + 5,
            cwd=str(cwd),
        )
        elapsed = time.monotonic() - t0
        return (res.stdout, res.stderr, elapsed, res.returncode)
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - t0
        return ("", "host timeout", elapsed, -2)

def audit_problem(prob_path, smt_path, expected_fof, expected_verdict,
                  expected_relation, timeout, cwd):
    """Run all configured provers on one problem."""
    rows = []
    name = prob_path.stem
    expected_smt = expected_smt_status(expected_verdict, expected_relation)
    prob_rel = prob_path.relative_to(cwd)
    smt_rel  = smt_path.relative_to(cwd) if smt_path else None

    # FOF saturation provers.
    # Saturation provers cannot prove CounterSatisfiable or Satisfiable
    # problems by definition (no refutation exists), so skip them.
    if expected_fof not in ("CounterSatisfiable", "Satisfiable"):
        for prover_name, build_cmd, parser, normalizer in PROVER_FOF:
            cmd = build_cmd(prob_rel, timeout)
            out, err, wall, rc = run_one(prover_name, cmd, timeout, cwd)
            raw = parser(out, err)
            actual = normalizer(raw)
            passed = (expected_fof is not None and actual == expected_fof)
            rows.append({
                "problem": name, "prover": prover_name, "kind": "fof",
                "verdict": expected_verdict or "",
                "relation": expected_relation or "",
                "expected": expected_fof or "",
                "raw": raw, "actual": actual,
                "wall_s": f"{wall:.3f}", "rc": rc,
                "passed": "Y" if passed else ("N" if expected_fof else "?"),
                "diag": (err.strip().splitlines() or [""])[0][:120],
            })

    # FMB: run on both Satisfiable and CounterSatisfiable
    if expected_fof in ("CounterSatisfiable", "Satisfiable"):
        for prover_name, build_cmd, parser, normalizer in PROVER_FOF_UNKNOWN:
            cmd = build_cmd(prob_rel, timeout)
            out, err, wall, rc = run_one(prover_name, cmd, timeout, cwd)
            raw = parser(out, err)
            actual = normalizer(raw)
            passed = (expected_fof is not None and actual == expected_fof)
            rows.append({
                "problem": name, "prover": prover_name, "kind": "fof",
                "verdict": expected_verdict or "",
                "relation": expected_relation or "",
                "expected": expected_fof,
                "raw": raw, "actual": actual,
                "wall_s": f"{wall:.3f}", "rc": rc,
                "passed": "Y" if passed else "N",
                "diag": (err.strip().splitlines() or [""])[0][:120],
            })

    # SMT provers
    if smt_rel and (cwd / smt_rel).exists():
        for prover_name, build_cmd, parser, normalizer in PROVER_SMT:
            cmd = build_cmd(smt_rel, timeout)
            out, err, wall, rc = run_one(prover_name, cmd, timeout, cwd)
            actual = parser(out, err)
            passed = (expected_smt is not None and actual == expected_smt)
            rows.append({
                "problem": name, "prover": prover_name, "kind": "smt",
                "verdict": expected_verdict or "",
                "relation": expected_relation or "",
                "expected": expected_smt or "",
                "raw": actual, "actual": actual,
                "wall_s": f"{wall:.3f}", "rc": rc,
                "passed": "Y" if passed else ("N" if expected_smt else "?"),
                "diag": (err.strip().splitlines() or [""])[0][:120],
            })
    return rows

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[2])
    ap.add_argument("--problems", nargs="+", default=DEFAULT_PROBLEM_GLOBS)
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--out", default=None)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--cwd", default=".")
    ap.add_argument("--skip-symlink-check", action="store_true")
    args = ap.parse_args()
    cwd = Path(args.cwd).resolve()

    if not args.skip_symlink_check:
        ok, missing = check_axiom_symlinks(cwd)
        if not ok:
            print_symlink_fixup_hint(cwd, missing)
            sys.exit(2)

    problems = []
    for glob_pat in args.problems:
        problems.extend(sorted(cwd.glob(glob_pat)))
    seen = set()
    problems = [p for p in problems if not (p in seen or seen.add(p))]
    if not problems:
        print(f"No problems matched {args.problems} under {cwd}", file=sys.stderr)
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = Path(args.out or (cwd / f"audit_{timestamp}.csv"))

    work = []
    n_no_relation = 0
    for prob in problems:
        smt = prob.with_suffix(".smt2")
        expected = read_header_field(prob, STATUS_RE)
        verdict  = read_header_field(prob, VERDICT_RE)
        relation = read_header_field(prob, RELATION_RE)
        if relation is None:
            relation = "conflict"
            n_no_relation += 1
        work.append((prob, smt if smt.exists() else None,
                     expected, verdict, relation))

    print(f"Auditing {len(work)} problems with timeout {args.timeout}s", file=sys.stderr)
    print(f"CWD: {cwd}", file=sys.stderr)
    print(f"Output: {out_path}", file=sys.stderr)
    if n_no_relation > 0:
        print(f"WARNING: {n_no_relation}/{len(work)} problems have no "
              f"`% Relation :` header field — defaulting to 'conflict'.",
              file=sys.stderr)
    print("", file=sys.stderr)

    all_rows = []
    if args.workers <= 1:
        for prob, smt, expected, verdict, relation in work:
            print(f"  {prob.stem} (status: {expected or '?'}, "
                  f"verdict: {verdict or '?'}, relation: {relation})",
                  file=sys.stderr)
            rows = audit_problem(prob, smt, expected, verdict, relation,
                                 args.timeout, cwd)
            all_rows.extend(rows)
            for r in rows:
                mark = {"Y": "✓", "N": "✗", "?": "·"}[r["passed"]]
                print(f"    {mark} {r['prover']:<20s} "
                      f"{r['actual']:<24s} {r['wall_s']}s",
                      file=sys.stderr)
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {
                ex.submit(audit_problem, prob, smt, expected, verdict,
                          relation, args.timeout, cwd):
                    (prob, expected, verdict, relation)
                for prob, smt, expected, verdict, relation in work
            }
            for fut in as_completed(futures):
                prob, expected, verdict, relation = futures[fut]
                rows = fut.result()
                all_rows.extend(rows)
                fail = sum(1 for r in rows if r["passed"] == "N")
                tag = "✓" if fail == 0 else f"✗ ({fail} fail)"
                print(f"  {prob.stem} ({verdict or '?'}, {relation})  {tag}",
                      file=sys.stderr)

    fieldnames = ["problem", "prover", "kind",
                  "verdict", "relation", "expected",
                  "raw", "actual", "wall_s", "rc", "passed", "diag"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(all_rows)

    print("", file=sys.stderr)
    n_problems = len({r["problem"] for r in all_rows})
    n_pass = sum(1 for r in all_rows if r["passed"] == "Y")
    n_fail = sum(1 for r in all_rows if r["passed"] == "N")
    n_skip = sum(1 for r in all_rows if r["passed"] == "?")
    print("=== Summary ===", file=sys.stderr)
    print(f"  Problems: {n_problems}", file=sys.stderr)
    print(f"  Prover runs: {len(all_rows)}", file=sys.stderr)
    print(f"  Passed: {n_pass}  Failed: {n_fail}  No-expectation: {n_skip}",
          file=sys.stderr)
    print(f"  CSV: {out_path}", file=sys.stderr)
    print("", file=sys.stderr)
    print("=== Per-prover reliability ===", file=sys.stderr)
    print("  (★ = paper-essential prover for §10 concordance claim)",
          file=sys.stderr)
    by_prover = {}
    for r in all_rows:
        by_prover.setdefault(r["prover"], []).append(r)
    for prover in sorted(by_prover):
        rs = by_prover[prover]
        passes = sum(1 for r in rs if r["passed"] == "Y")
        total  = sum(1 for r in rs if r["passed"] in ("Y", "N"))
        marker = " ★" if prover in PAPER_PROVERS else "  "
        if total == 0:
            print(f"  {marker}{prover}: no expectation", file=sys.stderr)
        else:
            print(f"  {marker}{prover}: {passes}/{total} "
                  f"({100 * passes // total}%)", file=sys.stderr)

    if n_fail > 0:
        print("", file=sys.stderr)
        print("=== Failures (problem, prover, verdict/relation, expected -> actual) ===",
              file=sys.stderr)
        for r in all_rows:
            if r["passed"] == "N":
                vrel = f"{r['verdict']}/{r['relation']}"
                print(f"  {r['problem']:<14s} {r['prover']:<18s} "
                      f"{vrel:<28s} {r['expected']:<10s} -> {r['actual']}",
                      file=sys.stderr)

    sys.exit(0 if n_fail == 0 else 1)

if __name__ == "__main__":
    main()
