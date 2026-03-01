"""
hierarchies/writer.py
Produces .p (TPTP) and .smt2 (SMT-LIB 2) files from KBProblem instances.
Header format mirrors the established ODRL benchmark style (ODRL105-1.p).
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from .models import KB, KB_INCLUDE, ODRL_INCLUDE, KBProblem, SZS


# ==========================================================================
# TPTP (.p) writer
# ==========================================================================

def generate_tptp(p: KBProblem) -> str:
    """Produce the full content of ODRLNNN-V.p"""
    num    = str(p.number).zfill(3)
    fname  = f"ODRL{num}-{p.variant}.p"
    today  = date.today().isoformat()
    lines  = []

    # ── Header ──────────────────────────────────────────────────────────
    lines.append("%--------------------------------------------------------------------------")
    lines.append(f"% File     : {fname} : TPTP v0.1.0.")
    lines.append(f"% Domain   : ODRL Policy Conflict Detection")
    lines.append(f"% Problem  : {p.description}")
    lines.append(f"% Expected : {p.szs.value}")
    lines.append(f"% Verdict  : {p.verdict.value}")
    lines.append(f"% Paper    : {p.paper_ref}")
    lines.append(f"%")

    # ── ODRL Policy (Turtle) ─────────────────────────────────────────────
    lines.append(f"% ODRL Policy (Turtle):")
    if p.policy_ttl:
        for ttl_line in p.policy_ttl.splitlines():
            lines.append(ttl_line if ttl_line.startswith("%") else f"%   {ttl_line}")
    else:
        lines.append(f"%   (see problem description)")
    lines.append(f"%")

    # ── Formal analysis ──────────────────────────────────────────────────
    if p.formal:
        lines.append(f"% Formal:")
        for fl in p.formal.splitlines():
            lines.append(fl if fl.startswith("%") else f"%   {fl}")
        lines.append(f"%")

    # ── Notes ────────────────────────────────────────────────────────────
    if p.notes:
        lines.append(f"% Notes    : {p.notes}")

    lines.append(f"% Difficulty: {p.difficulty}")
    lines.append(f"% Authors  : Mustafa, D. & Sutcliffe, G.")
    lines.append(f"% Date     : {today}")
    lines.append(f"% Gen      : gen_hierarchy_suite.py")
    lines.append(f"%--------------------------------------------------------------------------")

    # ── Includes ─────────────────────────────────────────────────────────
    lines.append(ODRL_INCLUDE)
    for kb in p.kbs:
        lines.append(KB_INCLUDE[kb])

    # ── Inline axioms (self-contained problems or derivability tests) ────
    if p.inline_axioms:
        lines.append(f"% ─── Problem-specific axioms ─────────────────────────────────────")
        lines.append(p.inline_axioms)

    # ── Conjecture ───────────────────────────────────────────────────────
    lines.append(f"% ─── Conjecture ──────────────────────────────────────────────────────")
    lines.append(p.conjecture_fof)
    lines.append(f"%--------------------------------------------------------------------------")

    return "\n".join(lines) + "\n"


# ==========================================================================
# SMT-LIB 2 (.smt2) writer
# ==========================================================================

def _tptp_to_smt2_header_comment(line: str) -> str:
    """Convert a % comment line to ; comment line."""
    if line.startswith("%"):
        return ";" + line[1:]
    return "; " + line


def generate_smt2(p: KBProblem) -> str:
    """Produce the full content of ODRLNNN-V.smt2"""
    num    = str(p.number).zfill(3)
    fname  = f"ODRL{num}-{p.variant}.smt2"
    today  = date.today().isoformat()
    # SMT2 expected: unsat = Theorem-equivalent, sat = CounterSat-equivalent
    smt2_expected = "unsat" if p.szs == SZS.THEOREM else "sat"

    lines = []

    # ── Header (mirrors .p but with ; comments) ──────────────────────────
    lines.append("; --------------------------------------------------------------------------")
    lines.append(f"; File     : {fname}")
    lines.append(f"; Domain   : ODRL Policy Conflict Detection")
    lines.append(f"; Problem  : {p.description}")
    lines.append(f"; Expected : {smt2_expected}")
    lines.append(f"; Verdict  : {p.verdict.value}")
    lines.append(f"; Paper    : {p.paper_ref}")
    lines.append(f";")

    # ── ODRL Policy (Turtle) ─────────────────────────────────────────────
    lines.append(f"; ODRL Policy (Turtle):")
    if p.policy_ttl:
        for ttl_line in p.policy_ttl.splitlines():
            # convert % → ;
            clean = ttl_line.lstrip("%").rstrip()
            lines.append(f";{clean}" if clean else ";")
    else:
        lines.append(f";   (see problem description)")
    lines.append(f";")

    # ── Formal analysis ──────────────────────────────────────────────────
    if p.formal:
        lines.append(f"; Formal:")
        for fl in p.formal.splitlines():
            # strip leading % or spaces, then re-indent uniformly
            clean = fl.lstrip("% ").rstrip()
            lines.append(f";   {clean}" if clean else ";")
        lines.append(f";")

    if p.notes:
        lines.append(f"; Notes    : {p.notes}")

    lines.append(f"; Difficulty: {p.difficulty}")
    lines.append(f"; Authors  : Mustafa, D. & Sutcliffe, G.")
    lines.append(f"; Date     : {today}")
    lines.append(f"; Gen      : gen_hierarchy_suite.py")
    lines.append(f"; --------------------------------------------------------------------------")
    lines.append(f"")

    # ── KB preamble (self-contained) ─────────────────────────────────────
    if p.inline_smt2_kb:
        lines.append(p.inline_smt2_kb)
        lines.append(f"")

    # ── Conjecture (already a complete SMT2 block) ────────────────────────
    lines.append(f"; ─── Conjecture (negated for refutation) ────────────────────────────")
    lines.append(p.conjecture_smt2)
    lines.append(f"; --------------------------------------------------------------------------")

    return "\n".join(lines) + "\n"


# ==========================================================================
# File I/O
# ==========================================================================

def write_problem(p: KBProblem, base_dir: Path, dry_run: bool = False) -> tuple[Path, Path]:
    """
    Write both encodings. Returns (tptp_path, smt2_path).

    Layout:
      Problems/ODRL/KBGrounding/{category}/ODRLNNN-V.p
      Problems/ODRL/KBGrounding/{category}/ODRLNNN-V.smt2
    """
    num     = str(p.number).zfill(3)
    variant = p.variant
    cat_dir = base_dir / "Problems" / "ODRL" / "KBGrounding" / p.category.value

    tptp_path = cat_dir / f"ODRL{num}-{variant}.p"
    smt2_path = cat_dir / f"ODRL{num}-{variant}.smt2"

    if dry_run:
        print(f"  [DRY] {tptp_path.relative_to(base_dir)}")
        print(f"  [DRY] {smt2_path.relative_to(base_dir)}")
        return tptp_path, smt2_path

    cat_dir.mkdir(parents=True, exist_ok=True)
    tptp_path.write_text(generate_tptp(p))
    smt2_path.write_text(generate_smt2(p))

    print(f"  ✓ {tptp_path.relative_to(base_dir)}")
    print(f"  ✓ {smt2_path.relative_to(base_dir)}")
    return tptp_path, smt2_path
