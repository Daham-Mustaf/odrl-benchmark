# full_audit.py
import subprocess
import re
from pathlib import Path

REPO = Path(__file__).parent.parent.parent
PROBLEMS_DIR = REPO / "Problems/ODRL/AxisDecomposition"
AXIOMS_DIR   = PROBLEMS_DIR / "Axioms"

# Import problem data
import sys
sys.path.insert(0, str(Path(__file__).parent))
from problem_data import PROBLEMS

CONJECTURE_SHAPES = {
    # (relation, verdict) -> expected shape pattern
    ("conflict",    "Conflict"):   r"~\?",
    ("conflict",    "Compatible"): r"^\?",
    ("subsumption", "Compatible"): r"!\[",
    ("subsumption", "Conflict"):   r"^\?",
}

def check_conjecture_shape(problem):
    """Layer 2a: conjecture shape matches verdict."""
    rel     = problem["relation"]
    verdict = problem["verdict"]
    conj    = problem["fof_conjecture"].strip()
    expected_pattern = CONJECTURE_SHAPES.get((rel, verdict))
    if expected_pattern and not re.match(expected_pattern, conj):
        return False, f"conjecture '{conj[:40]}' wrong shape for {rel}/{verdict}"
    return True, "ok"

def run_vampire(p_file):
    r = subprocess.run(
        ["vampire", "--mode", "casc", "--time_limit", "30", str(p_file)],
        capture_output=True, text=True
    )
    out = r.stdout + r.stderr
    for line in out.splitlines():
        if "SZS status" in line:
            return line.strip()
    return "NO_STATUS"

def run_z3(smt_file):
    r = subprocess.run(
        ["z3", str(smt_file)],
        capture_output=True, text=True
    )
    return r.stdout.strip().splitlines()[0] if r.stdout.strip() else "NO_OUTPUT"

def check_problem(p):
    pid    = p["id"]
    subdir = p["subdir"]
    p_file   = PROBLEMS_DIR / subdir / f"{pid}-1.p"
    smt_file = PROBLEMS_DIR / subdir / f"{pid}-1.smt2"

    results = []

    # Layer 2a: conjecture shape
    ok, msg = check_conjecture_shape(p)
    results.append(("shape",   ok, msg))

    # Layer 3: Vampire
    if p_file.exists():
        szs = run_vampire(p_file)
        ok  = p["status_fof"] in szs
        results.append(("vampire", ok, szs))
    else:
        results.append(("vampire", False, "file missing"))

    # Layer 3: Z3
    if smt_file.exists():
        smt = run_z3(smt_file)
        ok  = p["status_smt"] in smt
        results.append(("z3", ok, smt))
    else:
        results.append(("z3", False, "file missing"))

    return results

# Run
total = passed = 0
for p in PROBLEMS:
    checks = check_problem(p)
    all_ok = all(ok for _, ok, _ in checks)
    total += 1
    if all_ok:
        passed += 1
        print(f"  PASS  {p['id']}  {p['verdict']}")
    else:
        print(f"  FAIL  {p['id']}  {p['verdict']}")
        for name, ok, msg in checks:
            status = "✓" if ok else "✗"
            print(f"         {status} {name}: {msg}")

print(f"\n{passed}/{total} passed")