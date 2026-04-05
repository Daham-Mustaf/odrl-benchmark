"""
writers.py
==========
Writes .p (FOF/TPTP), .smt2 (SMT-LIB), and .ttl (Turtle) files
for the ODRL Axis Decomposition benchmark.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from header import problem_header


def write_fof_problem(p: dict, out_dir: Path) -> Path:
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)

    includes = ""
    if p.get("needs_density"):
        includes += "include('Axioms/ORD001-0.ax').\n"
    includes += "include('Axioms/AXIS000-0.ax').\n"

    conj_id = p["id"].lower()
    conjecture_fof = (
        f"fof({conj_id}, conjecture,\n"
        f"    {p['fof_conjecture']}).\n"
    )

    fof_body = includes + "\n" + p["fof_extra_decls"] + conjecture_fof
    header = problem_header(p, "axis", "")

    content = (
        header
        + includes
        + "\n"
        + "% ─── Named constants and ordering "
        + "─" * 37 + "\n"
        + p["fof_extra_decls"]
        + "% ─── Conjecture "
        + "─" * 52 + "\n"
        + conjecture_fof
        + "%--------------------------------------------------------------------------\n"
    )

    path = subdir / f"{p['id']}-1.p"
    path.write_text(content, encoding="utf-8")
    return path


def write_smt2_problem(p: dict, out_dir: Path) -> Path:
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)

    logic   = p.get("smt2_logic", "QF_LRA")
    decls   = p.get("smt2_decls", "(declare-const x Real)")
    asserts = p["smt2_asserts"].strip()

    lines = [
        "; --------------------------------------------------------------------------",
        f"; File     : {p['id']}-1.smt2",
        "; Domain   : ODRL Spatial Axis Profile / Axis Decomposition",
        f"; Problem  : {p['name']}",
        f"; Expected : {p['status_smt']}",
        f"; Verdict  : {p['verdict']}",
        f"; Category : {p['subdir']}",
        f"; Difficulty: {p.get('difficulty', 'Easy')}",
        ";",
        "; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.",
        ";            arXiv:2602.19878.",
        ";            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.",
        "; --------------------------------------------------------------------------",
        f"(set-logic {logic})",
        decls,
        asserts,
        "(check-sat)",
        "(exit)",
        "",
    ]

    path = subdir / f"{p['id']}-1.smt2"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_ttl_policy(p: dict, policies_dir: Path) -> Path:
    policies_dir.mkdir(parents=True, exist_ok=True)
    path = policies_dir / f"{p['id']}-policy.ttl"
    path.write_text(p["ttl"].strip() + "\n", encoding="utf-8")
    return path