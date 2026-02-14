#!/usr/bin/env python3
"""
ODRL Benchmark Suite — Multi-Prover Evaluation Runner
=====================================================

Runs the full ODRL TPTP benchmark suite against multiple ATP/SMT provers,
collects timing data, SZS statuses, and generates TPTP-grade analysis.

Usage:
    python evaluate_provers.py                    # Discover problems, dry run
    python evaluate_provers.py --run              # Run all provers
    python evaluate_provers.py --run --timeout 60 # Custom timeout
    python evaluate_provers.py --analyze          # Analyze existing results
    python evaluate_provers.py --headers          # Generate TPTP headers

Provers detected automatically if on PATH:
    vampire, eprover (E), z3, cvc5, iprover, spass

Output:
    results/evaluation.json     — Raw results
    results/summary.csv         — Per-problem summary table
    results/cactus.csv          — Data for cactus plots
    results/difficulty.csv      — TPTP difficulty ratings
    results/category_stats.csv  — Per-category breakdown
    results/prover_matrix.csv   — Agreement matrix
    results/syntax_stats.csv    — EPR fragment characterization
"""

import json
import os
import re
import subprocess
import sys
import time
import csv
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from typing import Optional

# ============================================================
# Configuration
# ============================================================

TPTP_ROOT = "Problems/ODRL/KBGrounding"
SMT_ROOT = "SMT/ODRL/KBGrounding"
RESULTS_DIR = "results"
DEFAULT_TIMEOUT = 60  # seconds

# Prover configurations: (name, command_template_tptp, command_template_smt, szs_extractor)
# Command templates use {file} for the problem file and {timeout} for seconds
PROVER_CONFIGS = {
    "vampire": {
        "binary": "vampire",
        "tptp_cmd": ["vampire", "--mode", "casc", "-t", "{timeout}", "{file}"],
        "smt_cmd": None,  # Vampire can read SMT-LIB but TPTP is native
        "szs_pattern": r"% SZS status (\w+)",
        "time_pattern": r"% Time elapsed: ([\d.]+) s",
        "proof_pattern": r"% SZS output start",
    },
    "eprover": {
        "binary": "eprover",
        "tptp_cmd": ["eprover", "--auto", "--cpu-limit={timeout}",
                     "--proof-object", "--tstp-format", "{file}"],
        "smt_cmd": None,
        "szs_pattern": r"# SZS status (\w+)",
        "time_pattern": r"# Total time\s*:\s*([\d.]+) s",
        "proof_pattern": r"# SZS output start",
    },
    "z3": {
        "binary": "z3",
        "tptp_cmd": ["z3", "tptp.timeout={timeout}000", "{file}"],  # z3 reads TPTP
        "smt_cmd": ["z3", "-T:{timeout}", "{file}"],
        "szs_pattern": r"% SZS status (\w+)",  # z3 TPTP mode
        "smt_result_map": {"unsat": "Theorem", "sat": "CounterSatisfiable",
                          "unknown": "Unknown", "timeout": "Timeout"},
        "time_pattern": None,  # measure externally
    },
    "cvc5": {
        "binary": "cvc5",
        "tptp_cmd": None,  # cvc5 doesn't read TPTP natively
        "smt_cmd": ["cvc5", "--lang=smt2", "--tlimit={timeout_ms}", "{file}"],
        "smt_result_map": {"unsat": "Theorem", "sat": "CounterSatisfiable",
                          "unknown": "Unknown", "timeout": "Timeout"},
        "time_pattern": None,
    },
    "iprover": {
        "binary": "iprover",
        "tptp_cmd": ["iprover", "--time_out_real", "{timeout}", "{file}"],
        "smt_cmd": None,
        "szs_pattern": r"% SZS status (\w+)",
        "time_pattern": r"% Running time:\s*([\d.]+)",
        "proof_pattern": r"% SZS output start",
    },
    "spass": {
        "binary": "SPASS",
        "tptp_cmd": ["SPASS", "-TPTP", "-TimeLimit={timeout}", "{file}"],
        "smt_cmd": None,
        "szs_pattern": r"SPASS beagle proves|SPASS beagle cannot",
        "spass_result_map": {"proves": "Theorem", "cannot": "CounterSatisfiable"},
        "time_pattern": r"SPASS-STOP.*?(\d+\.\d+)",
    },
}

# SZS status normalization
SZS_NORMALIZE = {
    "Theorem": "Theorem",
    "Unsatisfiable": "Theorem",  # for CNF problems
    "CounterSatisfiable": "CounterSatisfiable",
    "Satisfiable": "CounterSatisfiable",  # for CNF
    "Timeout": "Timeout",
    "ResourceOut": "Timeout",
    "MemoryOut": "Timeout",
    "GaveUp": "GaveUp",
    "Unknown": "Unknown",
    "Error": "Error",
    "unsat": "Theorem",
    "sat": "CounterSatisfiable",
    "unknown": "Unknown",
    "timeout": "Timeout",
}

# ============================================================
# Data Structures
# ============================================================

@dataclass
class ProblemInfo:
    """Metadata for a single benchmark problem."""
    problem_id: str
    category: str
    filepath_tptp: str
    filepath_smt: Optional[str]
    expected_szs: str
    expected_smt: str
    description: str = ""
    # Syntax statistics (computed)
    num_clauses: int = 0
    num_literals: int = 0
    max_clause_size: int = 0
    num_predicates: int = 0
    num_constants: int = 0
    num_variables: int = 0
    max_term_depth: int = 0
    is_epr: bool = True
    spc_class: str = ""

@dataclass
class ProverResult:
    """Result from a single prover on a single problem."""
    prover: str
    problem_id: str
    szs_status: str
    wall_time: float
    reported_time: Optional[float] = None
    proof_length: Optional[int] = None  # number of inferences
    raw_output: str = ""
    error: str = ""
    correct: Optional[bool] = None  # matches expected?

# ============================================================
# Problem Discovery
# ============================================================

def discover_problems(tptp_root: str, smt_root: str) -> list[ProblemInfo]:
    """Scan directories and build problem inventory."""
    problems = []
    tptp_path = Path(tptp_root)

    if not tptp_path.exists():
        print(f"ERROR: TPTP root not found: {tptp_root}")
        return problems

    for p_file in sorted(tptp_path.rglob("*.p")):
        pid = p_file.stem  # e.g., ODRL010-1
        category = p_file.parent.name  # e.g., Spatial

        # Parse expected status from file
        expected_szs, expected_smt, desc = parse_expected_status(p_file)

        # Find corresponding SMT-LIB file
        smt_file = find_smt_counterpart(pid, smt_root)

        problems.append(ProblemInfo(
            problem_id=pid,
            category=category,
            filepath_tptp=str(p_file),
            filepath_smt=smt_file,
            expected_szs=expected_szs,
            expected_smt=expected_smt,
            description=desc,
        ))

    return problems


def parse_expected_status(filepath: Path) -> tuple[str, str, str]:
    """Extract expected SZS status and description from TPTP file."""
    szs = "Unknown"
    smt = "unknown"
    desc = ""
    try:
        content = filepath.read_text()
        # Look for Status line
        m = re.search(r'%\s*Status\s*:\s*(\w+)', content)
        if m:
            szs = m.group(1)
        # Look for fof/cnf conjecture status hint
        if "Theorem" in content or "% SZS status" in content:
            if re.search(r'%.*Expected.*Theorem', content, re.IGNORECASE):
                szs = "Theorem"
        if re.search(r'%.*Expected.*CounterSat', content, re.IGNORECASE):
            szs = "CounterSatisfiable"
        # Map SZS to SMT
        smt = "unsat" if szs in ("Theorem", "Unsatisfiable") else "sat" if szs in ("CounterSatisfiable", "Satisfiable") else "unknown"
        # Description from first comment line
        for line in content.split('\n'):
            if line.startswith('%') and 'File' not in line and 'Status' not in line:
                desc = line.lstrip('% ').strip()
                if desc and len(desc) > 10:
                    break
    except Exception:
        pass
    return szs, smt, desc


def find_smt_counterpart(pid: str, smt_root: str) -> Optional[str]:
    """Find the SMT-LIB version of a TPTP problem."""
    smt_path = Path(smt_root)
    if not smt_path.exists():
        return None
    for smt_file in smt_path.rglob(f"{pid}.smt2"):
        return str(smt_file)
    return None

# ============================================================
# Prover Detection
# ============================================================

def detect_provers() -> dict:
    """Check which provers are available on PATH."""
    available = {}
    for name, config in PROVER_CONFIGS.items():
        binary = config["binary"]
        try:
            result = subprocess.run(
                ["which", binary], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                available[name] = config
                # Get version
                try:
                    if name == "vampire":
                        v = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=5)
                        ver = v.stdout.strip().split('\n')[0] if v.stdout else "?"
                    elif name == "eprover":
                        v = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=5)
                        ver = v.stdout.strip().split('\n')[0] if v.stdout else "?"
                    elif name == "z3":
                        v = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=5)
                        ver = v.stdout.strip() if v.stdout else "?"
                    elif name == "cvc5":
                        v = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=5)
                        ver = v.stdout.strip().split('\n')[0] if v.stdout else "?"
                    else:
                        ver = "detected"
                    available[name]["version"] = ver
                except Exception:
                    available[name]["version"] = "detected"
        except Exception:
            pass
    return available

# ============================================================
# Prover Execution
# ============================================================

def run_prover(prover_name: str, config: dict, problem: ProblemInfo,
               timeout: int) -> ProverResult:
    """Run a single prover on a single problem."""

    # Decide: TPTP or SMT-LIB input?
    # SMT solvers (Z3, CVC5) should prefer SMT-LIB files.
    # ATP provers (Vampire, E, iProver, SPASS) should prefer TPTP files.
    smt_native = prover_name in ("z3", "cvc5")

    if smt_native and config.get("smt_cmd") and problem.filepath_smt:
        cmd = [
            s.replace("{file}", problem.filepath_smt)
             .replace("{timeout}", str(timeout))
             .replace("{timeout_ms}", str(timeout * 1000))
            for s in config["smt_cmd"]
        ]
        input_format = "smt"
    elif config.get("tptp_cmd") and problem.filepath_tptp:
        cmd = [
            s.replace("{file}", problem.filepath_tptp)
             .replace("{timeout}", str(timeout))
             .replace("{timeout_ms}", str(timeout * 1000))
            for s in config["tptp_cmd"]
        ]
        input_format = "tptp"
    elif config.get("smt_cmd") and problem.filepath_smt:
        cmd = [
            s.replace("{file}", problem.filepath_smt)
             .replace("{timeout}", str(timeout))
             .replace("{timeout_ms}", str(timeout * 1000))
            for s in config["smt_cmd"]
        ]
        input_format = "smt"
    else:
        return ProverResult(
            prover=prover_name, problem_id=problem.problem_id,
            szs_status="NoInput", wall_time=0.0,
            error=f"No compatible input format for {prover_name}"
        )

    # Execute
    t0 = time.time()
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout + 5
        )
        wall_time = time.time() - t0
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.TimeoutExpired:
        wall_time = time.time() - t0
        return ProverResult(
            prover=prover_name, problem_id=problem.problem_id,
            szs_status="Timeout", wall_time=wall_time
        )
    except FileNotFoundError:
        return ProverResult(
            prover=prover_name, problem_id=problem.problem_id,
            szs_status="Error", wall_time=0.0, error="Binary not found"
        )

    # Extract SZS status
    szs_status = "Unknown"

    if input_format == "smt" and "smt_result_map" in config:
        # SMT-LIB output: first line is sat/unsat/unknown
        first_line = stdout.strip().split('\n')[0].strip().lower() if stdout else ""
        szs_status = config["smt_result_map"].get(first_line, "Unknown")
    elif "szs_pattern" in config:
        m = re.search(config["szs_pattern"], stdout)
        if m:
            raw = m.group(1) if m.lastindex else m.group(0)
            szs_status = SZS_NORMALIZE.get(raw, raw)
    elif "spass_result_map" in config:
        for key, val in config["spass_result_map"].items():
            if key in stdout:
                szs_status = val
                break

    # Extract reported time (if prover reports it)
    reported_time = None
    if config.get("time_pattern"):
        m = re.search(config["time_pattern"], stdout)
        if m:
            try:
                reported_time = float(m.group(1))
            except (ValueError, IndexError):
                pass

    # Count proof inferences (rough)
    proof_length = None
    if config.get("proof_pattern") and config["proof_pattern"] in stdout:
        # Count lines in proof output section
        proof_section = stdout.split(config["proof_pattern"])[-1] if config["proof_pattern"] in stdout else ""
        proof_length = len([l for l in proof_section.split('\n')
                          if l.strip() and not l.startswith('%')])

    # Normalize
    szs_status = SZS_NORMALIZE.get(szs_status, szs_status)

    # Check correctness
    correct = None
    if problem.expected_szs != "Unknown":
        expected_norm = SZS_NORMALIZE.get(problem.expected_szs, problem.expected_szs)
        correct = (szs_status == expected_norm)

    return ProverResult(
        prover=prover_name,
        problem_id=problem.problem_id,
        szs_status=szs_status,
        wall_time=wall_time,
        reported_time=reported_time,
        proof_length=proof_length,
        raw_output=stdout[:5000],  # truncate for storage
        error=stderr[:1000] if stderr else "",
        correct=correct,
    )

# ============================================================
# Syntax Statistics (EPR Characterization)
# ============================================================

def compute_syntax_stats(problem: ProblemInfo) -> ProblemInfo:
    """Compute TPTP-style syntax statistics from a .p file."""
    try:
        content = Path(problem.filepath_tptp).read_text()
    except Exception:
        return problem

    # Count fof/cnf clauses
    clauses = re.findall(r'(?:fof|cnf|tff)\s*\(', content)
    problem.num_clauses = len(clauses)

    # Count literals (very rough: count | in clauses + base)
    literals = content.count(' | ') + content.count(' & ') + problem.num_clauses
    problem.num_literals = literals

    # Extract predicates (capitalized terms before parentheses in formulas)
    predicates = set(re.findall(r'\b([a-z_]\w*)\s*\(', content))
    # Filter out fof/cnf/tff/include keywords
    predicates -= {'fof', 'cnf', 'tff', 'include', 'file'}
    problem.num_predicates = len(predicates)

    # Extract constants (terms that appear without variables)
    constants = set(re.findall(r'\b([a-z_]\w*)\b', content))
    constants -= predicates
    constants -= {'fof', 'cnf', 'tff', 'include', 'file', 'axiom', 'conjecture',
                  'hypothesis', 'negated_conjecture', 'plain', 'true', 'false'}
    problem.num_constants = len(constants)

    # Variables (capitalized single words in formulas)
    variables = set(re.findall(r'\b([A-Z]\w*)\b', content))
    variables -= {'X', 'Y', 'Z'}  # might be overcounting; keep unique
    problem.num_variables = len(variables)

    # EPR check: no function symbols of arity > 0 (rough)
    # If all terms are constants or variables, it's EPR
    func_apps = re.findall(r'\b[a-z_]\w*\s*\(\s*[a-z_]\w*\s*\(', content)
    problem.is_epr = len(func_apps) == 0
    problem.max_term_depth = 2 if func_apps else 1

    # SPC class
    if problem.expected_szs in ("Theorem", "Unsatisfiable"):
        problem.spc_class = "FOF_THM_EPR" if problem.is_epr else "FOF_THM_NEQ"
    else:
        problem.spc_class = "FOF_CSA_EPR" if problem.is_epr else "FOF_CSA_NEQ"

    return problem

# ============================================================
# Analysis
# ============================================================

def compute_difficulty_ratings(problems: list[ProblemInfo],
                               results: dict[str, list[ProverResult]],
                               provers: list[str]) -> dict[str, float]:
    """Compute TPTP-style difficulty ratings."""
    ratings = {}
    n_provers = len(provers)
    if n_provers == 0:
        return ratings

    for prob in problems:
        solved = sum(
            1 for p in provers
            if any(r.problem_id == prob.problem_id and
                   r.szs_status in ("Theorem", "CounterSatisfiable")
                   for r in results.get(p, []))
        )
        ratings[prob.problem_id] = round(1.0 - (solved / n_provers), 2)

    return ratings


def compute_agreement_matrix(problems: list[ProblemInfo],
                              results: dict[str, list[ProverResult]],
                              provers: list[str]) -> list[dict]:
    """Find problems where provers disagree."""
    disagreements = []
    for prob in problems:
        statuses = {}
        for p in provers:
            for r in results.get(p, []):
                if r.problem_id == prob.problem_id:
                    statuses[p] = r.szs_status
                    break
        # Check for genuine disagreement (not just timeout vs solved)
        definite = {k: v for k, v in statuses.items()
                   if v in ("Theorem", "CounterSatisfiable")}
        if len(set(definite.values())) > 1:
            disagreements.append({
                "problem": prob.problem_id,
                "category": prob.category,
                "statuses": statuses,
                "type": "CONTRADICTION"  # This is a big deal!
            })
        elif len(definite) > 0 and len(statuses) > len(definite):
            timeouts = {k for k, v in statuses.items()
                       if v in ("Timeout", "GaveUp", "Unknown")}
            if timeouts:
                disagreements.append({
                    "problem": prob.problem_id,
                    "category": prob.category,
                    "statuses": statuses,
                    "type": "PARTIAL"  # Some solved, some didn't
                })

    return disagreements

# ============================================================
# TPTP Header Generation
# ============================================================

TPTP_HEADER_TEMPLATE = """%--------------------------------------------------------------------------
% File     : {problem_id} : TPTP v9.0.0. Released v9.1.0.
% Domain   : Policy (ODRL)
% Problem  : {description}
% Version  : [Mus26] axioms.
% English  : {english}
% Refs     : [Mus26] Mustafa, D. (2026), Grounding ODRL Constraints:
%            Knowledge-Based Conflict Detection Across Dataspaces.
% Source   : [Mus26]
% Names    : {problem_id} [Mus26]
%
% Status   : {szs_status}
% Rating   : {rating} v9.1.0
% Syntax   : Number of formulae    : {num_clauses:>4}
%            Number of literals     : {num_literals:>4}
%            Maximal formula size   : {max_clause_size:>4}
%            Number of predicates   : {num_predicates:>4}
%            Number of constants    : {num_constants:>4}
%            Number of variables    : {num_variables:>4}
%            Maximal term depth     : {max_term_depth:>4}
% SPC      : {spc_class}
%
% Comments : Part of the ODRL KB-grounding benchmark suite.
%            Category: {category}
%            Semantic domain: {domain}
%--------------------------------------------------------------------------
"""

CATEGORY_TO_DOMAIN = {
    "Spatial": "Mereological (partOf)",
    "Purpose": "Taxonomic (subsumption)",
    "Language": "Taxonomic (subsumption)",
    "Nominal": "Nominal (identity)",
    "HasPart": "Mereological (hasPart)",
    "Neq": "All domains (complement)",
    "IsAnyOf": "All domains (union)",
    "IsAllOf": "All domains (intersection)",
    "IsNoneOf": "All domains (exclusion)",
    "OperatorPairs": "Cross-operator",
    "LogicalOr": "Composition (disjunction)",
    "LogicalXone": "Composition (exclusive)",
    "CrossDataspace": "Composition (conjunction)",
    "Alignment": "Cross-KB alignment",
    "AlignAdv": "Cross-KB alignment (adversarial)",
    "Runtime": "Runtime soundness",
    "Adversarial": "Adversarial edge cases",
    "AdvDeep": "Structural stress tests",
    "CompDeep": "Composition (nested)",
}

CATEGORY_TO_ENGLISH = {
    "Spatial": "Mereological conflict detection over GeoNames spatial hierarchy.",
    "Purpose": "Taxonomic conflict detection over W3C DPV purpose taxonomy.",
    "Language": "Taxonomic conflict detection over BCP 47 language hierarchy.",
    "Nominal": "Nominal domain where isA degenerates to equality.",
    "Alignment": "Cross-KB alignment preserving verdicts between standards.",
    "LogicalXone": "Exclusive composition requiring provable non-overlap.",
    "Runtime": "Runtime soundness bridging concept-level to execution-level.",
    "AdvDeep": "Structural KB stress test (chains, diamonds, singletons).",
}


def generate_tptp_header(problem: ProblemInfo, rating: float = 0.00) -> str:
    """Generate a TPTP-compliant header for a problem file."""
    domain = CATEGORY_TO_DOMAIN.get(problem.category, "General")
    english = CATEGORY_TO_ENGLISH.get(problem.category, problem.description)

    return TPTP_HEADER_TEMPLATE.format(
        problem_id=problem.problem_id,
        description=problem.description or f"{problem.category} benchmark",
        english=english,
        szs_status=problem.expected_szs,
        rating=f"{rating:.2f}",
        num_clauses=problem.num_clauses,
        num_literals=problem.num_literals,
        max_clause_size=problem.max_clause_size,
        num_predicates=problem.num_predicates,
        num_constants=problem.num_constants,
        num_variables=problem.num_variables,
        max_term_depth=problem.max_term_depth,
        spc_class=problem.spc_class,
        category=problem.category,
        domain=domain,
    )

# ============================================================
# Output Generation
# ============================================================

def write_summary_csv(problems, results, provers, ratings, filepath):
    """Write per-problem summary table."""
    with open(filepath, 'w', newline='') as f:
        w = csv.writer(f)
        header = ["Problem", "Category", "Expected", "Rating", "SPC"]
        for p in provers:
            header += [f"{p}_status", f"{p}_time", f"{p}_correct"]
        w.writerow(header)

        for prob in problems:
            row = [prob.problem_id, prob.category, prob.expected_szs,
                   ratings.get(prob.problem_id, "?"), prob.spc_class]
            for p in provers:
                r = next((r for r in results.get(p, [])
                         if r.problem_id == prob.problem_id), None)
                if r:
                    row += [r.szs_status, f"{r.wall_time:.3f}",
                           "✓" if r.correct else ("✗" if r.correct is False else "?")]
                else:
                    row += ["N/A", "N/A", "N/A"]
            w.writerow(row)


def write_cactus_csv(results, provers, filepath):
    """Write cactus plot data: for each prover, sorted solve times."""
    with open(filepath, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["prover", "problems_solved", "time"])
        for p in provers:
            solved = sorted([
                r.wall_time for r in results.get(p, [])
                if r.szs_status in ("Theorem", "CounterSatisfiable")
            ])
            for i, t in enumerate(solved, 1):
                w.writerow([p, i, f"{t:.4f}"])


def write_category_stats(problems, results, provers, filepath):
    """Write per-category performance breakdown."""
    cats = defaultdict(lambda: defaultdict(list))
    for prob in problems:
        for p in provers:
            r = next((r for r in results.get(p, [])
                     if r.problem_id == prob.problem_id), None)
            if r and r.szs_status in ("Theorem", "CounterSatisfiable"):
                cats[prob.category][p].append(r.wall_time)

    with open(filepath, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["Category", "Problems"] +
                   [f"{p}_solved" for p in provers] +
                   [f"{p}_avg_time" for p in provers])
        cat_counts = defaultdict(int)
        for prob in problems:
            cat_counts[prob.category] += 1

        for cat in sorted(cat_counts.keys()):
            row = [cat, cat_counts[cat]]
            for p in provers:
                times = cats[cat][p]
                row.append(len(times))
            for p in provers:
                times = cats[cat][p]
                row.append(f"{sum(times)/len(times):.4f}" if times else "N/A")
            w.writerow(row)

# ============================================================
# Console Output
# ============================================================

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  ODRL Benchmark Suite — Multi-Prover Evaluation Framework   ║
║  TPTP-Grade Analysis for Policy Reasoning Benchmarks        ║
╚══════════════════════════════════════════════════════════════╝
""")


def print_results_table(problems, results, provers):
    """Print a formatted results table to console."""
    # Header
    hdr = f"{'Problem':<16} {'Cat':<12} {'Exp':<10}"
    for p in provers:
        hdr += f" {p[:6]:>8} {'Time':>7}"
    print(hdr)
    print("─" * len(hdr))

    ok_count = defaultdict(int)
    total = len(problems)

    for prob in problems:
        line = f"{prob.problem_id:<16} {prob.category[:11]:<12} {prob.expected_szs:<10}"
        all_ok = True
        for p in provers:
            r = next((r for r in results.get(p, [])
                     if r.problem_id == prob.problem_id), None)
            if r:
                mark = "✓" if r.correct else ("✗" if r.correct is False else "?")
                status_short = r.szs_status[:8]
                line += f" {status_short:>8} {r.wall_time:>6.3f}s"
                if r.correct:
                    ok_count[p] += 1
                elif r.correct is False:
                    all_ok = False
            else:
                line += f" {'N/A':>8} {'N/A':>7}"
        print(line)

    print("─" * len(hdr))
    summary = f"{'TOTAL':<16} {'':<12} {total:<10}"
    for p in provers:
        summary += f" {ok_count[p]:>4}/{total:<3} {'':>7}"
    print(summary)

# ============================================================
# Main
# ============================================================

def main():
    print_banner()

    timeout = DEFAULT_TIMEOUT
    do_run = "--run" in sys.argv
    do_analyze = "--analyze" in sys.argv
    do_headers = "--headers" in sys.argv

    for i, arg in enumerate(sys.argv):
        if arg == "--timeout" and i + 1 < len(sys.argv):
            timeout = int(sys.argv[i + 1])

    # Discover problems
    print(f"[1/6] Discovering problems in {TPTP_ROOT}/ ...")
    problems = discover_problems(TPTP_ROOT, SMT_ROOT)
    print(f"       Found {len(problems)} problems in {len(set(p.category for p in problems))} categories")

    if not problems:
        print("ERROR: No problems found. Check TPTP_ROOT path.")
        return

    # Compute syntax statistics
    print(f"[2/6] Computing syntax statistics ...")
    for i, prob in enumerate(problems):
        problems[i] = compute_syntax_stats(prob)

    epr_count = sum(1 for p in problems if p.is_epr)
    print(f"       EPR problems: {epr_count}/{len(problems)}")

    # Detect provers
    print(f"[3/6] Detecting available provers ...")
    available_provers = detect_provers()
    prover_names = sorted(available_provers.keys())
    for name in prover_names:
        ver = available_provers[name].get("version", "?")
        print(f"       ✓ {name}: {ver}")
    if not prover_names:
        print("       WARNING: No provers detected on PATH")
        print("       Install provers and ensure they are on PATH")

    # Load existing results if analyzing
    results = defaultdict(list)

    if do_analyze:
        results_file = os.path.join(RESULTS_DIR, "evaluation.json")
        if os.path.exists(results_file):
            with open(results_file) as f:
                data = json.load(f)
                for entry in data:
                    r = ProverResult(**entry)
                    results[r.prover].append(r)
            prover_names = sorted(results.keys())
            print(f"       Loaded results for {len(prover_names)} provers")
        else:
            print(f"       ERROR: No results file found at {results_file}")
            return

    # Run provers
    if do_run and prover_names:
        print(f"[4/6] Running {len(prover_names)} provers × {len(problems)} problems "
              f"(timeout={timeout}s) ...")

        total_runs = len(prover_names) * len(problems)
        completed = 0

        for pname in prover_names:
            config = available_provers[pname]
            for prob in problems:
                completed += 1
                progress = f"[{completed}/{total_runs}]"
                print(f"       {progress} {pname:>8} ← {prob.problem_id:<16}", end="", flush=True)

                r = run_prover(pname, config, prob, timeout)
                results[pname].append(r)

                mark = "✓" if r.correct else ("✗" if r.correct is False else "?")
                print(f"  {r.szs_status:<16} {r.wall_time:>7.3f}s  {mark}")

        # Save raw results
        os.makedirs(RESULTS_DIR, exist_ok=True)
        all_results = []
        for pname in prover_names:
            for r in results[pname]:
                d = asdict(r)
                d.pop("raw_output", None)  # don't save full output
                all_results.append(d)

        with open(os.path.join(RESULTS_DIR, "evaluation.json"), 'w') as f:
            json.dump(all_results, f, indent=2)
        print(f"       Saved results to {RESULTS_DIR}/evaluation.json")
    elif do_run:
        print("[4/6] SKIPPED: No provers available")
    else:
        print("[4/6] SKIPPED: Use --run to execute provers")

    # Analysis
    print(f"[5/6] Analyzing results ...")

    if results:
        # Difficulty ratings
        ratings = compute_difficulty_ratings(problems, results, prover_names)

        # Agreement analysis
        disagreements = compute_agreement_matrix(problems, results, prover_names)

        # Print results table
        print()
        print_results_table(problems, results, prover_names)

        # Print disagreements
        if disagreements:
            print(f"\n⚠ DISAGREEMENTS FOUND: {len(disagreements)}")
            for d in disagreements:
                print(f"  {d['problem']:<16} ({d['category']}) — {d['type']}")
                for p, s in d['statuses'].items():
                    print(f"    {p:>10}: {s}")
        else:
            print(f"\n✓ Full agreement across all {len(prover_names)} provers")

        # Difficulty distribution
        if ratings:
            trivial = sum(1 for r in ratings.values() if r == 0.0)
            easy = sum(1 for r in ratings.values() if 0.0 < r <= 0.33)
            medium = sum(1 for r in ratings.values() if 0.33 < r <= 0.67)
            hard = sum(1 for r in ratings.values() if r > 0.67)
            print(f"\n  Difficulty distribution:")
            print(f"    Trivial (0.00):     {trivial}")
            print(f"    Easy (0.01-0.33):   {easy}")
            print(f"    Medium (0.34-0.67): {medium}")
            print(f"    Hard (0.68-1.00):   {hard}")

        # Write CSV outputs
        os.makedirs(RESULTS_DIR, exist_ok=True)
        write_summary_csv(problems, results, prover_names, ratings,
                         os.path.join(RESULTS_DIR, "summary.csv"))
        write_cactus_csv(results, prover_names,
                        os.path.join(RESULTS_DIR, "cactus.csv"))
        write_category_stats(problems, results, prover_names,
                           os.path.join(RESULTS_DIR, "category_stats.csv"))

        # Syntax stats
        with open(os.path.join(RESULTS_DIR, "syntax_stats.csv"), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(["Problem", "Category", "Clauses", "Literals",
                        "Predicates", "Constants", "Variables",
                        "MaxTermDepth", "IsEPR", "SPC"])
            for prob in problems:
                w.writerow([prob.problem_id, prob.category,
                           prob.num_clauses, prob.num_literals,
                           prob.num_predicates, prob.num_constants,
                           prob.num_variables, prob.max_term_depth,
                           prob.is_epr, prob.spc_class])

        # Difficulty ratings
        with open(os.path.join(RESULTS_DIR, "difficulty.csv"), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(["Problem", "Category", "Rating"])
            for prob in problems:
                w.writerow([prob.problem_id, prob.category,
                           ratings.get(prob.problem_id, "?")])

        print(f"\n  Output files in {RESULTS_DIR}/:")
        print(f"    summary.csv        — Per-problem results")
        print(f"    cactus.csv         — Cactus plot data")
        print(f"    category_stats.csv — Per-category breakdown")
        print(f"    syntax_stats.csv   — EPR characterization")
        print(f"    difficulty.csv     — TPTP difficulty ratings")

    # Generate TPTP headers
    if do_headers:
        print(f"\n[6/6] Generating TPTP headers ...")
        ratings = ratings if results else {}
        for prob in problems:
            header = generate_tptp_header(prob, ratings.get(prob.problem_id, 0.00))
            # Read existing file
            content = Path(prob.filepath_tptp).read_text()
            # Check if header already exists
            if "% File     :" in content:
                print(f"       SKIP {prob.problem_id} (header exists)")
                continue
            # Prepend header
            new_content = header + "\n" + content
            Path(prob.filepath_tptp).write_text(new_content)
            print(f"       ✓ {prob.problem_id}")
        print("       Done. Review generated headers before submission.")
    else:
        print(f"[6/6] SKIPPED: Use --headers to generate TPTP headers")

    print("\nDone.")


if __name__ == "__main__":
    main()