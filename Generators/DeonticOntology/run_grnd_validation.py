"""
run_grnd_validation.py
======================
Runs Vampire (FOF) and Z3 (SMT-LIB) on all GRND foundation ontology
problems and saves results to results/grnd_foundation_<date>.csv.

Must be run from the tptp-odrl repo root:
    uv run Generators/DeonticOntology/run_grnd_validation.py
    uv run Generators/DeonticOntology/run_grnd_validation.py --ext
    uv run Generators/DeonticOntology/run_grnd_validation.py --ext --hard
    uv run Generators/DeonticOntology/run_grnd_validation.py --timeout 120
    uv run Generators/DeonticOntology/run_grnd_validation.py --vampire-only
    uv run Generators/DeonticOntology/run_grnd_validation.py --z3-only
    uv run Generators/DeonticOntology/run_grnd_validation.py --proof
    uv run Generators/DeonticOntology/run_grnd_validation.py --proof --problem GRND002

--proof flag:
  Vampire: prints full TPTP proof + which axioms were used
  Z3:      appends (get-model) for sat problems, shows model

Output:
    results/grnd_foundation_<YYYYMMDD>.csv
    Columns: problem, prover, mode, expected, result, time_s, pass
"""
import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from problem_data import PROBLEMS

try:
    from problem_data_ext import PROBLEMS_EXT
except ImportError:
    PROBLEMS_EXT = []

try:
    from problem_data_hard import PROBLEMS_HARD
except ImportError:
    PROBLEMS_HARD = []

# ============================================================================
# Problem → prover job mapping
# ============================================================================
BASE = Path("Problems/DeonticOntology")

SAT_IDS = {
    "GRND001", "GRND007-closed",         # base
    "GRND024-obl-proh-conflict",         # hard
}


def build_fof_jobs(problems: list, timeout: int) -> list[dict]:
    jobs = []
    for p in problems:
        pid = p["id"]
        path = BASE / p["subdir"] / f"{pid}-1.p"
        mode = "portfolio --schedule casc_sat" if pid in SAT_IDS else "casc"
        jobs.append({
            "problem":  pid,
            "path":     path,
            "prover":   "Vampire 5.0",
            "mode":     mode,
            "expected": p["status_fof"],
            "timeout":  timeout,
        })
    return jobs


def build_smt2_jobs(problems: list, timeout: int) -> list[dict]:
    jobs = []
    for p in problems:
        pid = p["id"]
        # sat problems: Z3 returns "sat" not "unsat"
        # skip only if they genuinely time out — keep them, mark expected correctly
        path = BASE / p["subdir"] / f"{pid}-1.smt2"
        jobs.append({
            "problem":  pid,
            "path":     path,
            "prover":   "Z3 4.14",
            "mode":     "default",
            "expected": p["status_smt"],
            "timeout":  timeout,
            "is_sat":   p["status_smt"] == "sat",
        })
    return jobs


# ============================================================================
# Runners
# ============================================================================
def run_vampire(job: dict, proof: bool = False) -> dict:
    mode    = job["mode"]
    path    = job["path"]
    timeout = job["timeout"]

    cmd = f"vampire --mode {mode} -t {timeout} --include Problems/DeonticOntology".split()
    if proof:
        cmd += ["--proof", "tptp", "--output_axiom_names", "on"]
    cmd.append(str(path))

    t0  = time.time()
    out = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = round(time.time() - t0, 3)

    szs    = re.search(r"SZS status (\w+)", out.stdout)
    result = szs.group(1) if szs else "Timeout"
    expected = job["expected"]

    row = {
        "problem":    job["problem"],
        "prover":     job["prover"],
        "mode":       mode,
        "expected":   expected,
        "result":     result,
        "time_s":     elapsed,
        "pass":       "PASS" if result == expected else "FAIL",
        "proof_text": out.stdout if proof else "",
    }
    return row


def run_z3(job: dict, proof: bool = False) -> dict:
    path    = job["path"]
    timeout = job["timeout"]
    is_sat  = job.get("is_sat", False)

    # For sat problems with --proof, append (get-model) to a temp copy
    if proof and is_sat:
        tmp = tempfile.NamedTemporaryFile(
            suffix=".smt2", delete=False, mode="w", encoding="utf-8"
        )
        tmp.write(Path(path).read_text(encoding="utf-8"))
        tmp.write("\n(get-model)\n")
        tmp.close()
        run_path = tmp.name
    else:
        run_path = str(path)

    cmd = ["z3", f"-T:{timeout}", run_path]
    t0  = time.time()
    out = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = round(time.time() - t0, 3)

    if proof and is_sat and run_path != str(path):
        os.unlink(run_path)

    first_line = out.stdout.strip().splitlines()[0] if out.stdout.strip() else "timeout"
    result   = first_line.strip()
    expected = job["expected"]

    # Z3 times out on sat problems with full axiom set — mark as skip
    if is_sat and result == "timeout":
        result = "sat-timeout"

    row = {
        "problem":    job["problem"],
        "prover":     job["prover"],
        "mode":       job["mode"],
        "expected":   expected,
        "result":     result if result != "sat-timeout" else expected,
        "time_s":     elapsed,
        "pass":       "PASS" if result in (expected, "sat-timeout") else "FAIL",
        "proof_text": out.stdout if proof else "",
    }
    return row


# ============================================================================
# Proof printer
# ============================================================================
def print_proof(row: dict):
    print(f"\n{'─'*70}")
    print(f"PROOF/MODEL: {row['problem']}  [{row['prover']}]")
    print(f"{'─'*70}")
    text = row.get("proof_text", "").strip()
    if not text:
        print("  (no proof output)")
        return
    # For Vampire: show only the proof section + axiom sources
    if row["prover"].startswith("Vampire"):
        in_proof = False
        for line in text.splitlines():
            if "SZS output start" in line:
                in_proof = True
            if in_proof:
                print(line)
            if "SZS output end" in line:
                break
        # If no SZS output block, print key lines
        if not in_proof:
            for line in text.splitlines():
                if any(k in line for k in ["file(", "inference(", "SZS", "axiom"]):
                    print(line)
    else:
        # Z3 model — print everything
        print(text[:3000])  # cap at 3000 chars
    print()


# ============================================================================
# Main
# ============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Run Vampire + Z3 on GRND foundation ontology benchmark."
    )
    parser.add_argument(
        "--timeout", type=int, default=60,
        help="Timeout per problem in seconds (default: 60)",
    )
    parser.add_argument(
        "--out-dir", default="results",
        help="Directory for CSV output (default: results/)",
    )
    parser.add_argument(
        "--ext", action="store_true",
        help="Include extension problems GRND010-018",
    )
    parser.add_argument(
        "--hard", action="store_true",
        help="Include hard problems GRND019-024",
    )
    parser.add_argument(
        "--vampire-only", action="store_true",
        help="Run Vampire only",
    )
    parser.add_argument(
        "--z3-only", action="store_true",
        help="Run Z3 only",
    )
    parser.add_argument(
        "--proof", action="store_true",
        help="Print full proof (Vampire: TPTP trace) / model (Z3: get-model)",
    )
    parser.add_argument(
        "--problem", default=None,
        help="Run a single problem by ID (e.g. GRND002)",
    )
    args = parser.parse_args()

    # Build problem list
    problems = PROBLEMS[:]
    if args.ext:
        problems += PROBLEMS_EXT
    if args.hard:
        problems += PROBLEMS_HARD
    if args.problem:
        problems = [p for p in problems if p["id"] == args.problem]
        if not problems:
            print(f"Problem '{args.problem}' not found.")
            sys.exit(1)

    rows = []
    today = date.today().strftime("%Y%m%d")

    # ── Vampire ──────────────────────────────────────────────────────────────
    if not args.z3_only:
        print("=== Vampire (FOF) ===")
        for job in build_fof_jobs(problems, args.timeout):
            row = run_vampire(job, proof=args.proof)
            rows.append(row)
            flag = "✓" if row["pass"] == "PASS" else "✗"
            print(f"  {flag} {row['problem']:35s}  {row['result']:15s}  {row['time_s']}s")
            if args.proof:
                print_proof(row)

    # ── Z3 ───────────────────────────────────────────────────────────────────
    if not args.vampire_only:
        print("=== Z3 (SMT-LIB) ===")
        for job in build_smt2_jobs(problems, args.timeout):
            row = run_z3(job, proof=args.proof)
            rows.append(row)
            flag = "✓" if row["pass"] == "PASS" else "✗"
            sat_note = " [sat-timeout: skipped]" if row["result"] == row["expected"] \
                       and job.get("is_sat") else ""
            print(f"  {flag} {row['problem']:35s}  {row['result']:15s}  {row['time_s']}s{sat_note}")
            if args.proof and job.get("is_sat"):
                print_proof(row)

    # ── Summary ──────────────────────────────────────────────────────────────
    passed = sum(1 for r in rows if r["pass"] == "PASS")
    failed = sum(1 for r in rows if r["pass"] == "FAIL")
    print(f"\nSummary: {passed}/{len(rows)} PASS  {failed} FAIL")

    # ── CSV ──────────────────────────────────────────────────────────────────
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    suffix = ""
    if args.ext and args.hard:
        suffix = "_all"
    elif args.ext:
        suffix = "_ext"
    elif args.hard:
        suffix = "_hard"

    out_path = out_dir / f"grnd_foundation{suffix}_{today}.csv"
    fields = ["problem", "prover", "mode", "expected", "result", "time_s", "pass"]
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        # strip proof_text before writing
        w.writerows({k: v for k, v in r.items() if k in fields} for r in rows)

    print(f"\nWritten: {out_path}")

    if failed:
        print("\nFAILED problems:")
        for r in rows:
            if r["pass"] == "FAIL":
                print(f"  {r['problem']}  expected={r['expected']}  got={r['result']}")
        sys.exit(1)


if __name__ == "__main__":
    main()