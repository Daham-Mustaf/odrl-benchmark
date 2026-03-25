"""
writers.py
==========
File writers for the FOIS 2026 deontic grounding benchmark.
Imports axiom content from axiom_data.py and problem definitions
from problem_data.py.

Exported functions:
  write_fof_problem(p, out_dir)   -> Path
  write_smt2_problem(p, out_dir)  -> Path

Imported by: gen_foundation_problems.py

Fix history:
  v1.5 — import corrected from gen_layer0_signature;
          version string and all axiom-count comments updated to reflect
          Ax5.1-5.11 + A1-A3 + B1-B3 (26 axioms, up from 20).
"""
import sys
import textwrap
from pathlib import Path
from datetime import date

# Import preamble from gen_layer0_signature so it never diverges from the
# generated GRND000-0.smt2 file.
sys.path.insert(0, str(Path(__file__).parent))
from gen_signature import generate_smt2 as _gen_smt2
from axiom_data import (
    FOF_AXIOM_DICT,
    SMT2_AXIOMS,
    SMT2_APPENDIX_SORTS,
    FOF_APPENDIX_DECLS,
)

VERSION = "1.5"
GENERATOR = f"gen_foundation_problems.py v{VERSION}"
SMT2_PREAMBLE = _gen_smt2()


# ============================================================================
# FOF WRITER
# ============================================================================

def write_fof_problem(p: dict, out_dir: Path) -> Path:
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / f"{p['id']}-1.p"

    conj = p.get("fof_conjecture")

    lines = [
        "%--------------------------------------------------------------------------",
        f"% File     : {p['id']}-1.p",
        "% Domain   : Deontic Ontology / ODRL Grounding",
        f"% Problem  : {p['name']}",
        f"% Status   : {p['status_fof']}",
        "% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026",
        f"% Policy   : Policies/{p['id']}-policy.ttl",
        f"% Generated: {date.today().isoformat()} by {GENERATOR}",
        "%",
    ]
    for line in textwrap.dedent(p["description"]).strip().splitlines():
        lines.append(f"% {line}")

    # TTL summary in header
    if p.get("ttl"):
        lines.append("%")
        lines.append("% ODRL Policy (Turtle) — see Policies/ for full file:")
        for ttl_line in p["ttl"].strip().splitlines():
            lines.append(f"% {ttl_line}")

    lines += [
        "%--------------------------------------------------------------------------",
        "",
        "% Layer 0: Signature (sorts, rfr/decl, position disjointness)",
        "include('Axioms/Layer0-Signature/GRND000-0.ax').",
        "",
        "% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)",
        *[FOF_AXIOM_DICT[ax] for ax in p.get("fof_axioms", [])],
        "",
        FOF_APPENDIX_DECLS,
        "%--------------------------------------------------------------------------",
        "% Ground instance (gamma)",
        "%--------------------------------------------------------------------------",
        p["fof_extra_decls"],
    ]

    if conj is not None:
        lines += [
            "%--------------------------------------------------------------------------",
            "% Conjecture",
            "%--------------------------------------------------------------------------",
            "fof(conjecture, conjecture,",
            f"    ( {conj} )).",
        ]

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ============================================================================
# SMT-LIB WRITER
# ============================================================================

def write_smt2_problem(p: dict, out_dir: Path) -> Path:
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / f"{p['id']}-1.smt2"

    conj = p.get("smt2_conjecture")

    lines = [
        "; --------------------------------------------------------------------------",
        f"; File     : {p['id']}-1.smt2",
        "; Domain   : Deontic Ontology / ODRL Grounding",
        f"; Problem  : {p['name']}",
        f"; Status   : {p['status_smt']}",
        "; Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026",
        f"; Policy   : Policies/{p['id']}-policy.ttl",
        f"; Generated: {date.today().isoformat()} by {GENERATOR}",
        ";",
    ]
    for line in textwrap.dedent(p["description"]).strip().splitlines():
        lines.append(f"; {line.lstrip('% ')}")

    # TTL summary in header
    if p.get("ttl"):
        lines.append(";")
        lines.append("; ODRL Policy (Turtle) — see Policies/ for full file:")
        for ttl_line in p["ttl"].strip().splitlines():
            lines.append(f"; {ttl_line}")

    lines += [
        "; --------------------------------------------------------------------------",
        "",
        "; === Layer 0 + Layer 1 preamble (embedded — SMT-LIB has no include) ===",
        "; === Source: Axioms/Layer0-Signature/GRND000-0.smt2 ===",
        SMT2_PREAMBLE,
        "; === Appendix A.0 additional sorts/predicates ===",
        SMT2_APPENDIX_SORTS,
        "",
        "; === Layer 1: Paper axioms (Ax5.1-5.11, A1-A3, B1-B3) ===",
        "; === Authoritative source: Axioms/Layer1-Deontic/GRND-AX-1.smt2 ===",
        "; === (SMT-LIB has no include directive — axioms embedded directly) ===",
        "",
    ]

    for name, formula in SMT2_AXIOMS:
        lines.append(f"; {name}")
        lines.append(formula)
        lines.append("")

    lines += [
        "; === Ground instance (gamma) ===",
        p["smt2_extra_decls"],
    ]

    if conj is not None:
        lines += [
            "; === Negated conjecture ===",
            conj,
            "",
        ]

    lines.append("(check-sat)")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path