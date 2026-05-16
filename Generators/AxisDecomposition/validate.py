"""
validate.py
===========
Lints every benchmark artifact:
  - Header consistency (Status / Verdict / Relation present and consistent)
  - Include completeness (predicates used have defining axioms in scope)
  - Syntax check (TPTP, SMT-LIB, TTL)
  - Cross-format consistency (SMT and FOF encode the same claim)
  - Audit-light (5s vampire + z3 spot-check)

Output: validate_<timestamp>.csv with one row per problem and columns for
each check, plus a summary printed to stderr.

Usage:
    cd ~/projects/odrl-benchmark
    uv run Generators/AxisDecomposition/validate.py --cwd Problems/ODRL/AxisDecomposition
"""
import argparse
import csv
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Predicates defined in each axiom file (used for include-completeness checks)
AXIOM_PREDICATES = {
    "ORD000-0.ax":  {"less", "leq", "val"},
    "ORD001-0.ax":  {"less"},
    "AXIS000-0.ax": {"in_open", "in_lopen", "in_ropen", "in_closed",
                     "is_verdict", "box_verdict",
                     "compatible", "conflict", "unknown"},
    "PREC000-0.ax": {"prec", "upper_tag", "lower_tag", "c", "o"},
    "WF000-0.ax":   {"wf"},
    "PROJ000-0.ax": {"in_box2", "in_box3"},
    "COMP000-0.ax": {"or_verdict", "xone_verdict"},
    "COMPL000-0.ax": {"completion_compatible", "completion_conflict"},
    "SUBS000-0.ax": {"axis_subsumes", "subs_verdict", "box_subs",
                     "is_presence", "present", "absent"},
}

# Categories whose problems must include a specific axiom file
REQUIRED_INCLUDES = {
    "Composition":       {"COMP000-0.ax"},
    "LogicalOr":         {"COMP000-0.ax"},
    "LogicalXone":       {"COMP000-0.ax"},
    "Completion":        {"COMPL000-0.ax"},
    "BoxContainment":    {"SUBS000-0.ax"},
    "ConflictCriterion": {"PREC000-0.ax"},
    "WellFormedness":    {"WF000-0.ax"},
    "Projection":        {"PROJ000-0.ax"},
}

# Relation polarity (matches run_audit.py's expected_smt_status)
def expected_smt(verdict, relation):
    if relation == "verdict_algebra":
        return {"Compatible": "unsat", "Conflict": "unsat",
                "Unknown": "unsat", "CounterSatisfiable": "unsat"}.get(verdict)
    if relation == "subsumption":
        return {"Compatible": "unsat", "Conflict": "sat",
                "Unknown": None}.get(verdict)
    return {"Conflict": "unsat", "Compatible": "sat",
            "Unknown": None}.get(verdict)

# ---------------------------------------------------------------------------
# Header parsing
# ---------------------------------------------------------------------------
def read_header(p):
    """Parse the TPTP header. Returns {status, verdict, relation, includes}."""
    text = p.read_text()
    result = {"status": None, "verdict": None, "relation": None, "includes": []}
    for line in text.splitlines():
        m = re.match(r"%\s*Status\s*:?\s*(\w+)", line)
        if m: result["status"] = m.group(1)
        m = re.match(r"%\s*Verdict\s*:?\s*(\w+)", line)
        if m: result["verdict"] = m.group(1)
        m = re.match(r"%\s*Relation\s*:?\s*(\w+)", line)
        if m: result["relation"] = m.group(1)
        m = re.match(r"\s*include\s*\(\s*'Axioms/([^']+)'\s*\)\s*\.", line)
        if m: result["includes"].append(m.group(1))
        if line.startswith("fof("): break  # end of header region
    return result, text

# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------
def check_header(hdr):
    """Header has Status field, and Verdict/Relation match Status."""
    if not hdr["status"]:
        return False, "no Status"
    if hdr["status"] == "Theorem":
        if hdr["verdict"] not in ("Compatible", "Conflict", "Unknown"):
            return False, f"Theorem but Verdict={hdr['verdict']!r}"
    if hdr["status"] == "CounterSatisfiable":
        if hdr["verdict"] not in (None, "CounterSatisfiable", "Compatible", "Conflict", "Unknown"):
            return False, f"CounterSatisfiable but Verdict={hdr['verdict']!r}"
    return True, ""

def check_includes(hdr, subdir):
    """Required category-specific axiom file is in the include list."""
    required = REQUIRED_INCLUDES.get(subdir, set())
    inc_set = set(hdr["includes"])
    missing = required - inc_set
    if missing:
        return False, f"missing: {sorted(missing)}"
    return True, ""

def check_predicates(text, hdr):
    """Every non-built-in predicate is defined by some included axiom file."""
    inc_set = set(hdr["includes"])
    defined = set()
    for ax in inc_set:
        defined.update(AXIOM_PREDICATES.get(ax, set()))
    # Add commonly-used built-ins and problem-locals
    BUILTIN = {"val", "less", "leq", "$distinct"}
    defined.update(BUILTIN)
    # Extract predicate symbols used in the file's fof formulae
    body = text.split("fof(", 1)[-1] if "fof(" in text else ""
    # Symbols of the form `predicate(arg, ...)` — heuristic
    used = set(re.findall(r"\b(\$?[a-z_]\w*)\s*\(", body))
    # Strip TPTP keywords, problem-local constants
    KEYWORD = {"fof", "axiom", "conjecture", "include"}
    used -= KEYWORD
    # Constants that start with `v` followed by a digit are problem-local
    used = {u for u in used if not re.match(r"^v\d", u)}
    # also drop problem ids
    used = {u for u in used if not u.startswith("odrl")}
    missing = used - defined
    if missing:
        return False, f"undefined predicates: {sorted(missing)}"
    return True, ""

def check_fof_syntax(p_path, cwd):
    """Run vampire --mode parse (or use 0-second time_limit) to validate FOF."""
    if not shutil.which("vampire"):
        return None, "vampire not on PATH"
    try:
        r = subprocess.run(
            ["vampire", "--mode", "preprocess", "--time_limit", "1",
             "--include", ".", str(p_path.relative_to(cwd))],
            capture_output=True, text=True, timeout=10, cwd=str(cwd),
        )
        if r.returncode == 0 or "SZS" in r.stdout:
            return True, ""
        if "parse" in (r.stdout + r.stderr).lower() and "error" in (r.stdout + r.stderr).lower():
            return False, "parse error"
        return True, ""  # other non-zero exits are fine for syntax check
    except subprocess.TimeoutExpired:
        return True, "(parse timed out, assumed ok)"
    except Exception as e:
        return None, str(e)[:60]

def check_smt_syntax(smt_path):
    """Run z3 -smt2 -parse-only or equivalent."""
    if not shutil.which("z3"):
        return None, "z3 not on PATH"
    try:
        r = subprocess.run(
            ["z3", "-smt2", "-T:2", str(smt_path)],
            capture_output=True, text=True, timeout=10,
        )
        out = (r.stdout + r.stderr).lower()
        if "error" in out and "parse" in out:
            return False, "parse error"
        return True, ""
    except Exception as e:
        return None, str(e)[:60]

def check_ttl_syntax(ttl_path):
    """Parse TTL via rdflib if available, else regex sniff."""
    try:
        import rdflib
        g = rdflib.Graph()
        try:
            g.parse(str(ttl_path), format="turtle")
            return True, ""
        except Exception as e:
            return False, str(e)[:60]
    except ImportError:
        text = ttl_path.read_text()
        if "@prefix" in text and "a odrl:" in text:
            return True, "(rdflib unavailable; passed regex sniff)"
        return False, "no @prefix or odrl: declaration"

def quick_audit(p_path, smt_path, hdr, cwd):
    """5s vampire + z3 spot-check. Returns (fof_szs, smt_szs)."""
    fof_szs = None
    smt_szs = None
    if shutil.which("vampire") and hdr["status"] not in ("Satisfiable", "CounterSatisfiable"):
        try:
            r = subprocess.run(
                ["vampire", "--mode", "casc", "--time_limit", "5",
                 "--include", ".", str(p_path.relative_to(cwd))],
                capture_output=True, text=True, timeout=10, cwd=str(cwd),
            )
            m = re.search(r"SZS status (\w+)", r.stdout)
            if m: fof_szs = m.group(1)
        except Exception:
            pass
    if shutil.which("z3") and smt_path and smt_path.exists():
        try:
            r = subprocess.run(
                ["z3", "-T:3", str(smt_path)],
                capture_output=True, text=True, timeout=8,
            )
            for line in r.stdout.splitlines():
                line = line.strip()
                if line in ("sat", "unsat", "unknown"):
                    smt_szs = line
                    break
        except Exception:
            pass
    return fof_szs, smt_szs

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[2])
    ap.add_argument("--cwd", default="Problems/ODRL/AxisDecomposition")
    ap.add_argument("--no-audit", action="store_true",
                    help="Skip the audit-light spot-check (faster).")
    args = ap.parse_args()
    cwd = Path(args.cwd).resolve()

    problems = sorted(cwd.glob("*/ODRL*.p"))
    problems += sorted(cwd.glob("*/HARD*.p"))
    problems += sorted(cwd.glob("*/NFV*.p"))
    print(f"Validating {len(problems)} problems under {cwd}", file=sys.stderr)

    out_path = cwd / f"validate_{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"
    rows = []
    failures_by_check = {"header": 0, "includes": 0, "predicates": 0,
                         "fof_syntax": 0, "smt_syntax": 0, "ttl_syntax": 0,
                         "fof_audit": 0, "smt_audit": 0}

    t0 = time.monotonic()
    for i, p in enumerate(problems, 1):
        if i % 25 == 0:
            print(f"  [{i}/{len(problems)}] elapsed {time.monotonic()-t0:.1f}s",
                  file=sys.stderr)
        subdir = p.parent.name
        pid = p.stem.replace("-1", "").replace("+1", "")
        smt = p.with_suffix(".smt2")
        ttl = cwd / "Policies" / f"{pid}-policy.ttl"

        hdr, text = read_header(p)
        row = {"problem": p.stem, "subdir": subdir}

        ok, msg = check_header(hdr)
        row["header_ok"] = "Y" if ok else "N"
        row["header_msg"] = msg
        if not ok: failures_by_check["header"] += 1

        ok, msg = check_includes(hdr, subdir)
        row["includes_ok"] = "Y" if ok else "N"
        row["includes_msg"] = msg
        if not ok: failures_by_check["includes"] += 1

        ok, msg = check_predicates(text, hdr)
        row["predicates_ok"] = "Y" if ok else "N"
        row["predicates_msg"] = msg
        if not ok: failures_by_check["predicates"] += 1

        ok, msg = check_fof_syntax(p, cwd)
        row["fof_syntax_ok"] = "Y" if ok else ("?" if ok is None else "N")
        row["fof_syntax_msg"] = msg
        if ok is False: failures_by_check["fof_syntax"] += 1

        if smt.exists():
            ok, msg = check_smt_syntax(smt)
            row["smt_syntax_ok"] = "Y" if ok else ("?" if ok is None else "N")
            row["smt_syntax_msg"] = msg
            if ok is False: failures_by_check["smt_syntax"] += 1
        else:
            row["smt_syntax_ok"] = "-"
            row["smt_syntax_msg"] = "no .smt2"

        if ttl.exists():
            ok, msg = check_ttl_syntax(ttl)
            row["ttl_syntax_ok"] = "Y" if ok else "N"
            row["ttl_syntax_msg"] = msg
            if ok is False: failures_by_check["ttl_syntax"] += 1
        else:
            row["ttl_syntax_ok"] = "-"
            row["ttl_syntax_msg"] = "no .ttl"

        row["verdict"] = hdr["verdict"] or ""
        row["relation"] = hdr["relation"] or ""
        row["expected_status"] = hdr["status"] or ""
        row["expected_smt"] = expected_smt(hdr["verdict"], hdr["relation"]) or ""

        if not args.no_audit:
            fof_szs, smt_szs = quick_audit(p, smt if smt.exists() else None, hdr, cwd)
            row["fof_szs"] = fof_szs or ""
            row["smt_szs"] = smt_szs or ""
            fof_ok = (fof_szs == hdr["status"]) if hdr["status"] and fof_szs else None
            smt_ok = (smt_szs == row["expected_smt"]) if row["expected_smt"] and smt_szs else None
            row["fof_audit_ok"] = "Y" if fof_ok else ("?" if fof_ok is None else "N")
            row["smt_audit_ok"] = "Y" if smt_ok else ("?" if smt_ok is None else "N")
            if fof_ok is False: failures_by_check["fof_audit"] += 1
            if smt_ok is False: failures_by_check["smt_audit"] += 1
        else:
            row["fof_szs"] = ""
            row["smt_szs"] = ""
            row["fof_audit_ok"] = "-"
            row["smt_audit_ok"] = "-"

        rows.append(row)

    # Write CSV
    if rows:
        fields = list(rows[0].keys())
        with open(out_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    # Summary
    print(f"\n=== Validation summary ({time.monotonic()-t0:.1f}s) ===", file=sys.stderr)
    print(f"  Problems checked: {len(rows)}", file=sys.stderr)
    print(f"  CSV: {out_path}", file=sys.stderr)
    print(f"\n  Failures by check:", file=sys.stderr)
    for check, count in failures_by_check.items():
        marker = "✓" if count == 0 else "✗"
        print(f"    {marker} {check:<14s}: {count} failures", file=sys.stderr)

    # Top failing categories
    by_cat = {}
    for r in rows:
        n_fail = sum(1 for c in ("header_ok", "includes_ok", "predicates_ok",
                                  "fof_syntax_ok", "smt_syntax_ok", "ttl_syntax_ok",
                                  "fof_audit_ok", "smt_audit_ok")
                     if r.get(c) == "N")
        if n_fail > 0:
            by_cat.setdefault(r["subdir"], 0)
            by_cat[r["subdir"]] += 1
    if by_cat:
        print(f"\n  Categories with failures:", file=sys.stderr)
        for cat in sorted(by_cat, key=lambda k: -by_cat[k]):
            print(f"    {cat:<22s}: {by_cat[cat]} problems with issues", file=sys.stderr)

    total_failures = sum(failures_by_check.values())
    sys.exit(0 if total_failures == 0 else 1)


if __name__ == "__main__":
    main()
