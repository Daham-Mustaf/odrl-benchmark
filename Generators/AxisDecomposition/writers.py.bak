"""
writers.py
==========
Writes .p (FOF/TPTP), .smt2 (SMT-LIB), and .ttl (Turtle) files
for the ODRL Axis Decomposition benchmark.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from header import problem_header, SMTHeader

def write_fof_problem(p: dict, out_dir: Path) -> Path:
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)
    # Includes are built as follows:
    #   1. start from p['includes'] if set, else a default of ORD000+AXIS000
    #      (+ ORD001 if needs_density)
    #   2. always add the category-specific axiom file for the problem's subdir
    #      if one exists and isn't already in the list
    CATEGORY_AXIOMS = {
        "Composition":       "COMP000-0.ax",
        "LogicalOr":         "COMP000-0.ax",
        "LogicalXone":       "COMP000-0.ax",
        "Completion":        "COMPL000-0.ax",
        "BoxContainment":    "SUBS000-0.ax",
        "ConflictCriterion": "PREC000-0.ax",
        "WellFormedness":    "WF000-0.ax",
        "Projection":        "PROJ000-0.ax",
    }
    inc_list = list(p.get("includes") or [])
    if not inc_list:
        inc_list = ["ORD000-0.ax"]
        if p.get("needs_density"):
            inc_list.append("ORD001-0.ax")
        inc_list.append("AXIS000-0.ax")
    cat_axiom = CATEGORY_AXIOMS.get(p.get("subdir"))
    if cat_axiom and cat_axiom not in inc_list:
        inc_list.append(cat_axiom)
    includes = "".join(f"include('Axioms/{ax}').\n" for ax in inc_list)
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

    smt_header = SMTHeader(
        file     = f"{p['id']}-1.smt2",
        domain   = "axis",
        title    = p["name"],
        version  = "1.0",
        refs     = ["axis2026"],
        comments = (
            f"Verdict: {p['verdict']}  "
            f"Category: {p['subdir']}  "
            f"Difficulty: {p.get('difficulty', 'Easy')}"
        ),
        status   = p["status_smt"],
    ).render()

    content = "\n".join([
        smt_header,
        f"(set-logic {logic})",
        decls,
        asserts,
        "(check-sat)",
        "(exit)",
        "",
    ])

    path = subdir / f"{p['id']}-1.smt2"
    path.write_text(content, encoding="utf-8")
    return path

def write_ttl_policy(p: dict, policies_dir: Path) -> Path:
    policies_dir.mkdir(parents=True, exist_ok=True)
    path = policies_dir / f"{p['id']}-policy.ttl"
    path.write_text(p["ttl"].strip() + "\n", encoding="utf-8")
    return path
