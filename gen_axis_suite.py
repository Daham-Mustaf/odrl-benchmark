#!/usr/bin/env python3
"""
gen_axis_suite.py — Generate and run axis decomposition benchmarks.

Produces two encodings per benchmark:
  1. TPTP FOF  → Problems/ODRL/AxisDecomposition/{Category}/ODRL{NNN}-1.p
  2. SMT-LIB   → Problems/ODRL/SelfContained/spatialAxis/ODRL{NNN}-1.smt2

Benchmark definitions live in benchmarks/*.py (one file per category).
This file contains ONLY the generators, runner, and CLI — it should
not need editing when adding new benchmark categories.

Usage:
    uv run python gen_axis_suite.py                        # generate all
    uv run python gen_axis_suite.py --category SingleAxis  # one category
    uv run python gen_axis_suite.py --dry-run              # preview only
    uv run python gen_axis_suite.py --run                  # generate + run
    uv run python gen_axis_suite.py --run --timeout 60     # custom timeout
    uv run python gen_axis_suite.py --run-only             # run without regen

Authors: Mustafa, D. & Sutcliffe, G.
Date:    2026-02-21
"""

import csv
import shutil
import subprocess
import time
import argparse
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from benchmarks import CATEGORY_GENERATORS, Benchmark, Category, Connective, Constraint, Op, SZS, Verdict


# ==========================================================================
# Code generators — Helpers
# ==========================================================================

def op_to_interval_comment(c: Constraint, domain_lo, domain_lo_open) -> str:
    """Human-readable interval for header comments."""
    lo = f"({domain_lo}" if domain_lo_open else f"[{domain_lo}"
    if domain_lo is None:
        lo = "(-∞"
    match c.op:
        case Op.EQ:   return f"[{c.value}, {c.value}]"
        case Op.LTEQ: return f"{lo}, {c.value}]"
        case Op.LT:   return f"{lo}, {c.value})"
        case Op.GTEQ: return f"[{c.value}, ∞)"
        case Op.GT:   return f"({c.value}, ∞)"


def smt2_op(op: Op, var: str, val: float) -> str:
    """SMT-LIB constraint expression."""
    match op:
        case Op.EQ:   return f"(= {var} {val})"
        case Op.LT:   return f"(< {var} {val})"
        case Op.LTEQ: return f"(<= {var} {val})"
        case Op.GT:   return f"(> {var} {val})"
        case Op.GTEQ: return f"(>= {var} {val})"


def val_name(v: float) -> str:
    """Named constant for a numeric value in FOF."""
    if v < 0:
        return f"neg{abs(int(v))}" if v == int(v) else f"neg{str(abs(v)).replace('.', '_')}"
    return f"v{int(v)}" if v == int(v) else f"v{str(v).replace('.', '_')}"


def fof_membership_expr(c: Constraint,
                        domain_lo: Optional[float],
                        domain_lo_open: bool,
                        domain_hi: Optional[float],
                        domain_hi_open: bool,
                        var: str = "X") -> str:
    """Return FOF expression for 'var ∈ [[c]]'.

    Handles bounded and unbounded intervals:
      - Bounded (both endpoints known) → Section A predicates
      - Unbounded (no upper/lower)     → raw leq/less from ORD000-0
    """
    vn = val_name(c.value)
    match c.op:
        case Op.EQ:
            return f"in_closed({var}, {vn}, {vn})"
        case Op.LTEQ:
            if domain_lo is not None:
                lo = val_name(domain_lo)
                return f"in_lopen({var}, {lo}, {vn})" if domain_lo_open else f"in_closed({var}, {lo}, {vn})"
            return f"leq({var}, {vn})"
        case Op.LT:
            if domain_lo is not None:
                lo = val_name(domain_lo)
                return f"in_open({var}, {lo}, {vn})" if domain_lo_open else f"in_ropen({var}, {lo}, {vn})"
            return f"less({var}, {vn})"
        case Op.GTEQ:
            if domain_hi is not None:
                hi = val_name(domain_hi)
                return f"in_ropen({var}, {vn}, {hi})" if domain_hi_open else f"in_closed({var}, {vn}, {hi})"
            return f"leq({vn}, {var})"
        case Op.GT:
            if domain_hi is not None:
                hi = val_name(domain_hi)
                return f"in_open({var}, {vn}, {hi})" if domain_hi_open else f"in_lopen({var}, {vn}, {hi})"
            return f"less({vn}, {var})"


def fof_named_constants(b: Benchmark) -> list[float]:
    """Collect all numeric values that need named FOF constants."""
    vals = set()
    # Axis 1
    if b.domain_lo is not None: vals.add(b.domain_lo)
    if b.domain_hi is not None: vals.add(b.domain_hi)
    vals.add(b.c1.value)
    vals.add(b.c2.value)
    # Axis 2
    if b.c1_ax2 is not None:
        if b.domain2_lo is not None: vals.add(b.domain2_lo)
        if b.domain2_hi is not None: vals.add(b.domain2_hi)
        vals.add(b.c1_ax2.value)
        vals.add(b.c2_ax2.value)
    # Axis 3
    if b.c1_ax3 is not None:
        if b.domain3_lo is not None: vals.add(b.domain3_lo)
        if b.domain3_hi is not None: vals.add(b.domain3_hi)
        vals.add(b.c1_ax3.value)
        vals.add(b.c2_ax3.value)
    # Axis 4
    if b.c1_ax4 is not None:
        if b.domain4_lo is not None: vals.add(b.domain4_lo)
        if b.domain4_hi is not None: vals.add(b.domain4_hi)
        vals.add(b.c1_ax4.value)
        vals.add(b.c2_ax4.value)
    return sorted(vals)


def ax1_expr(c: Constraint, b: Benchmark, var: str = "X") -> str:
    return fof_membership_expr(c, b.domain_lo, b.domain_lo_open,
                               b.domain_hi, b.domain_hi_open, var)

def ax2_expr(c: Constraint, b: Benchmark, var: str = "Y") -> str:
    return fof_membership_expr(c, b.domain2_lo, b.domain2_lo_open,
                               b.domain2_hi, b.domain2_hi_open, var)

def ax3_expr(c: Constraint, b: Benchmark, var: str = "Z") -> str:
    return fof_membership_expr(c, b.domain3_lo, b.domain3_lo_open,
                               b.domain3_hi, b.domain3_hi_open, var)

def ax4_expr(c: Constraint, b: Benchmark, var: str = "W") -> str:
    return fof_membership_expr(c, b.domain4_lo, b.domain4_lo_open,
                               b.domain4_hi, b.domain4_hi_open, var)


# ==========================================================================
# Code generators — TPTP FOF
# ==========================================================================

def _is_non_and(conn) -> bool:
    """True if connective is OR or XONE (not implicit AND)."""
    return conn is not None and conn != Connective.AND


def _combine_fof(exprs: list[str], connective) -> str:
    """Combine FOF axis expressions with a connective.

    AND:  e1 & e2 & e3
    OR:   e1 | e2 | e3
    XONE: (e1 & ~(e2) & ~(e3)) | (~(e1) & e2 & ~(e3)) | (~(e1) & ~(e2) & e3)
    """
    if connective is None or connective == Connective.AND:
        return " & ".join(exprs)
    elif connective == Connective.OR:
        return " | ".join(exprs)
    elif connective == Connective.XONE:
        n = len(exprs)
        terms = []
        for i in range(n):
            parts = [exprs[j] if j == i else f"~({exprs[j]})" for j in range(n)]
            terms.append("(" + " & ".join(parts) + ")")
        return " |\n              ".join(terms)
    raise ValueError(f"Unknown connective: {connective}")


def _connective_label(conn) -> str:
    """Human-readable label for header."""
    if conn is None or conn == Connective.AND:
        return "AND (implicit)"
    return f"odrl:{conn.value}"


def generate_fof(b: Benchmark) -> str:
    """Generate TPTP FOF problem file content."""
    lines = []

    # --- Header ---
    lines.append(f"%--------------------------------------------------------------------------")
    lines.append(f"% File     : ODRL{b.number}-1 : TPTP v0.2.0")
    lines.append(f"% Domain   : ODRL Spatial Axis Profile")
    lines.append(f"% Problem  : {b.description}")
    lines.append(f"% Expected : Theorem")
    lines.append(f"% Verdict  : {b.verdict.value}")
    lines.append(f"% Category : {b.category.value}")
    lines.append(f"% Difficulty: {b.difficulty}")
    lines.append(f"%")

    # Policy TTL
    lines.append(f"% ODRL Policy (Turtle):")
    for ttl_line in b.policy_ttl.splitlines():
        lines.append(ttl_line)
    lines.append(f"%")

    # Formal description
    i1 = op_to_interval_comment(b.c1, b.domain_lo, b.domain_lo_open)
    i2 = op_to_interval_comment(b.c2, b.domain_lo, b.domain_lo_open)
    if b.verdict in (Verdict.CONFLICT, Verdict.COMPATIBLE):
        lines.append(f"% Formal   : {b.c1.axis} {b.c1.op.value} {b.c1.value}  →  {i1}")
        lines.append(f"%            {b.c2.axis} {b.c2.op.value} {b.c2.value}  →  {i2}")
        sym = "∅" if b.verdict == Verdict.CONFLICT else "≠ ∅"
        lines.append(f"%            {i1} ∩ {i2} {sym}  →  {b.verdict.value}")
    else:
        sym = "⊆" if b.verdict == Verdict.SUBSUMES else "⊄"
        lines.append(f"% Formal   : {i1} {sym} {i2}")

    if b.notes:
        lines.append(f"% Notes    : {b.notes}")
    if _is_non_and(b.connective_a) or _is_non_and(b.connective_b):
        lines.append(f"% Connect. : Policy A = {_connective_label(b.connective_a)}")
        lines.append(f"%            Policy B = {_connective_label(b.connective_b)}")

    lines.append(f"%")
    lines.append(f"% Authors  : Mustafa, D. & Sutcliffe, G.")
    lines.append(f"% Date     : {date.today().isoformat()}")
    lines.append(f"% Gen      : gen_axis_suite.py")
    lines.append(f"%--------------------------------------------------------------------------")

    # --- Includes ---
    lines.append(f"include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').")
    if b.needs_density:
        lines.append(f"include('Axioms/Layer0-DomainKB/ORD001-0.ax').")
    lines.append(f"")

    # --- Named constants and pairwise ordering ---
    vals = fof_named_constants(b)
    lines.append(f"% ─── Named constants and ordering ─────────────────────────────────────")
    for v in vals:
        lines.append(f"fof(val_{val_name(v)}, axiom, val({val_name(v)})).")
    for i, v1 in enumerate(vals):
        for v2 in vals[i+1:]:
            if v1 < v2:
                lines.append(f"fof(ord_{val_name(v1)}_{val_name(v2)}, axiom, less({val_name(v1)}, {val_name(v2)})).")
    if len(vals) > 1:
        names = ", ".join(val_name(v) for v in vals)
        lines.append(f"fof(distinct, axiom, $distinct({names})).")
    lines.append(f"")

    # --- Conjecture ---
    # All conjectures are Theorem-provable (Vampire-friendly).
    # For multi-axis: quantify over one variable per axis (X, Y, Z, W).
    lines.append(f"% ─── Conjecture ──────────────────────────────────────────────────────")

    axis_exprs = []
    axis_exprs.append((ax1_expr(b.c1, b, "X"), ax1_expr(b.c2, b, "X"), "X"))
    if b.c1_ax2 is not None:
        axis_exprs.append((ax2_expr(b.c1_ax2, b, "Y"), ax2_expr(b.c2_ax2, b, "Y"), "Y"))
    if b.c1_ax3 is not None:
        axis_exprs.append((ax3_expr(b.c1_ax3, b, "Z"), ax3_expr(b.c2_ax3, b, "Z"), "Z"))
    if b.c1_ax4 is not None:
        axis_exprs.append((ax4_expr(b.c1_ax4, b, "W"), ax4_expr(b.c2_ax4, b, "W"), "W"))

    vars_str = ",".join(v for _, _, v in axis_exprs)
    a_exprs = [ea for ea, _, _ in axis_exprs]
    b_exprs = [eb for _, eb, _ in axis_exprs]

    # Determine connectives (None = AND)
    conn_a = b.connective_a
    conn_b = b.connective_b
    uses_logical = _is_non_and(conn_a) or _is_non_and(conn_b)

    if not uses_logical:
        # ── Legacy AND × AND format (backward-compatible) ──
        both_all = " &\n          ".join(f"{ea} & {eb}" for ea, eb, _ in axis_exprs)
        box_a = " & ".join(a_exprs)
        box_b = " & ".join(b_exprs)

        if b.verdict == Verdict.CONFLICT:
            lines.append(f"fof(odrl{b.number}, conjecture,")
            lines.append(f"    ~?[{vars_str}]: ({both_all})).")
        elif b.verdict == Verdict.COMPATIBLE:
            lines.append(f"fof(odrl{b.number}, conjecture,")
            lines.append(f"    ?[{vars_str}]: ({both_all})).")
        elif b.verdict == Verdict.SUBSUMES:
            lines.append(f"fof(odrl{b.number}, conjecture,")
            lines.append(f"    ![{vars_str}]: (({box_a}) => ({box_b}))).")
        elif b.verdict == Verdict.REFUTED:
            lines.append(f"fof(odrl{b.number}, conjecture,")
            lines.append(f"    ?[{vars_str}]: (({box_a}) & ~({box_b}))).")
    else:
        # ── Logical connective format (OR / XONE) ──
        box_a = _combine_fof(a_exprs, conn_a)
        box_b = _combine_fof(b_exprs, conn_b)

        if b.verdict == Verdict.CONFLICT:
            lines.append(f"fof(odrl{b.number}, conjecture,")
            lines.append(f"    ~?[{vars_str}]: (({box_a}) &")
            lines.append(f"          ({box_b}))).")
        elif b.verdict == Verdict.COMPATIBLE:
            lines.append(f"fof(odrl{b.number}, conjecture,")
            lines.append(f"    ?[{vars_str}]: (({box_a}) &")
            lines.append(f"          ({box_b}))).")
        elif b.verdict == Verdict.SUBSUMES:
            lines.append(f"fof(odrl{b.number}, conjecture,")
            lines.append(f"    ![{vars_str}]: (({box_a}) => ({box_b}))).")
        elif b.verdict == Verdict.REFUTED:
            lines.append(f"fof(odrl{b.number}, conjecture,")
            lines.append(f"    ?[{vars_str}]: (({box_a}) & ~({box_b}))).")

    lines.append(f"%--------------------------------------------------------------------------")
    return "\n".join(lines)


# ==========================================================================
# Code generators — SMT-LIB
# ==========================================================================

def _smt2_domain_bounds(lines: list, var: str,
                        domain_lo, domain_lo_open,
                        domain_hi, domain_hi_open) -> None:
    """Assert domain bounds for one axis variable."""
    if domain_lo is not None:
        op = ">" if domain_lo_open else ">="
        lines.append(f"(assert ({op} {var} {domain_lo}))")
    if domain_hi is not None:
        op = "<" if domain_hi_open else "<="
        lines.append(f"(assert ({op} {var} {domain_hi}))")


def _smt2_combine(exprs: list[str], connective) -> str:
    """Combine SMT-LIB expressions with a connective.

    Returns a single S-expression (for use inside assert).
    """
    if connective is None or connective == Connective.AND:
        if len(exprs) == 1:
            return exprs[0]
        return f"(and {' '.join(exprs)})"
    elif connective == Connective.OR:
        if len(exprs) == 1:
            return exprs[0]
        return f"(or {' '.join(exprs)})"
    elif connective == Connective.XONE:
        # exactly one: (or (and c1 (not c2) ...) (and (not c1) c2 ...) ...)
        n = len(exprs)
        terms = []
        for i in range(n):
            parts = [exprs[j] if j == i else f"(not {exprs[j]})" for j in range(n)]
            terms.append(f"(and {' '.join(parts)})")
        return f"(or {' '.join(terms)})"
    raise ValueError(f"Unknown connective: {connective}")


def _smt2_negate(exprs: list[str], connective) -> str:
    """Negate a combined expression (De Morgan).

    ~AND(a,b,c) = OR(~a,~b,~c)
    ~OR(a,b,c)  = AND(~a,~b,~c)
    ~XONE(...)  = NOT(xone-encoding)
    """
    negs = [f"(not {e})" for e in exprs]
    if connective is None or connective == Connective.AND:
        if len(negs) == 1:
            return negs[0]
        return f"(or {' '.join(negs)})"
    elif connective == Connective.OR:
        if len(negs) == 1:
            return negs[0]
        return f"(and {' '.join(negs)})"
    elif connective == Connective.XONE:
        return f"(not {_smt2_combine(exprs, connective)})"
    raise ValueError(f"Unknown connective: {connective}")


def generate_smt2(b: Benchmark) -> str:
    """Generate SMT-LIB problem file content.

    Encoding by verdict:
      Conflict/Compatible:
        assert domain ∧ policy_A(conn_a) ∧ policy_B(conn_b)
        → sat=Compatible, unsat=Conflict

      Subsumes/Refuted:
        assert domain ∧ policy_A(conn_a)  (point ∈ box_A)
        assert ¬policy_B(conn_b)          (point ∉ box_B — De Morgan)
        → unsat=Subsumes, sat=Refuted
    """
    lines = []

    # --- Header ---
    lines.append(f"; --------------------------------------------------------------------------")
    lines.append(f"; File     : ODRL{b.number}-1.smt2")
    lines.append(f"; Domain   : ODRL Spatial Axis Profile")
    lines.append(f"; Problem  : {b.description}")
    lines.append(f"; Expected : {'unsat' if b.szs == SZS.THEOREM else 'sat'}")
    lines.append(f"; Verdict  : {b.verdict.value}")
    lines.append(f"; Category : {b.category.value}")
    if _is_non_and(b.connective_a) or _is_non_and(b.connective_b):
        lines.append(f"; Connect. : A={_connective_label(b.connective_a)}, B={_connective_label(b.connective_b)}")
    lines.append(f";")
    lines.append(f"; ODRL Policy (Turtle):")
    for ttl_line in b.policy_ttl.splitlines():
        lines.append(f";{ttl_line.lstrip('%')}")
    lines.append(f";")
    lines.append(f"; Gen      : gen_axis_suite.py")
    lines.append(f"; --------------------------------------------------------------------------")
    lines.append(f"(set-logic QF_LRA)")

    # --- Declare variables ---
    lines.append(f"(declare-const x Real)")
    if b.c1_ax2 is not None:
        lines.append(f"(declare-const y Real)")
    if b.c1_ax3 is not None:
        lines.append(f"(declare-const z Real)")
    if b.c1_ax4 is not None:
        lines.append(f"(declare-const w Real)")
    lines.append(f"")

    # Collect axes: (c1, c2, var, domain_lo, lo_open, domain_hi, hi_open)
    axes = [(b.c1, b.c2, "x",
             b.domain_lo, b.domain_lo_open, b.domain_hi, b.domain_hi_open)]
    if b.c1_ax2 is not None:
        axes.append((b.c1_ax2, b.c2_ax2, "y",
                     b.domain2_lo, b.domain2_lo_open, b.domain2_hi, b.domain2_hi_open))
    if b.c1_ax3 is not None:
        axes.append((b.c1_ax3, b.c2_ax3, "z",
                     b.domain3_lo, b.domain3_lo_open, b.domain3_hi, b.domain3_hi_open))
    if b.c1_ax4 is not None:
        axes.append((b.c1_ax4, b.c2_ax4, "w",
                     b.domain4_lo, b.domain4_lo_open, b.domain4_hi, b.domain4_hi_open))

    conn_a = b.connective_a
    conn_b = b.connective_b
    uses_logical = _is_non_and(conn_a) or _is_non_and(conn_b)

    if not uses_logical:
        # ── Legacy AND × AND (backward-compatible output) ──
        if b.verdict in (Verdict.CONFLICT, Verdict.COMPATIBLE):
            for i, (c1, c2, var, dlo, dlo_o, dhi, dhi_o) in enumerate(axes):
                if i > 0:
                    lines.append(f"")
                lines.append(f"; --- Axis {i+1}: {c1.axis} ---")
                _smt2_domain_bounds(lines, var, dlo, dlo_o, dhi, dhi_o)
                lines.append(f"; {c1.axis}: {c1.op.value} {c1.value}  ∧  {c2.op.value} {c2.value}")
                lines.append(f"(assert {smt2_op(c1.op, var, c1.value)})")
                lines.append(f"(assert {smt2_op(c2.op, var, c2.value)})")
        elif b.verdict in (Verdict.SUBSUMES, Verdict.REFUTED):
            for i, (c1, c2, var, dlo, dlo_o, dhi, dhi_o) in enumerate(axes):
                if i > 0:
                    lines.append(f"")
                lines.append(f"; --- Axis {i+1}: {c1.axis} (∈ box_A) ---")
                _smt2_domain_bounds(lines, var, dlo, dlo_o, dhi, dhi_o)
                lines.append(f"(assert {smt2_op(c1.op, var, c1.value)})")
            lines.append(f"")
            lines.append(f"; --- ¬(∈ box_B): De Morgan disjunction ---")
            negations = [f"(not {smt2_op(c2.op, var, c2.value)})"
                         for _, c2, var, *_ in axes]
            if len(negations) == 1:
                lines.append(f"(assert {negations[0]})")
            else:
                or_body = " ".join(negations)
                lines.append(f"(assert (or {or_body}))")
    else:
        # ── Logical connective format (OR / XONE) ──
        # Domain bounds always asserted individually
        for i, (c1, c2, var, dlo, dlo_o, dhi, dhi_o) in enumerate(axes):
            if i > 0:
                lines.append(f"")
            lines.append(f"; --- Axis {i+1}: {c1.axis} (domain) ---")
            _smt2_domain_bounds(lines, var, dlo, dlo_o, dhi, dhi_o)

        # Collect raw constraint expressions per policy
        a_smt = [smt2_op(c1.op, var, c1.value) for c1, _, var, *_ in axes]
        b_smt = [smt2_op(c2.op, var, c2.value) for _, c2, var, *_ in axes]

        if b.verdict in (Verdict.CONFLICT, Verdict.COMPATIBLE):
            lines.append(f"")
            lines.append(f"; --- Policy A ({_connective_label(conn_a)}) ---")
            lines.append(f"(assert {_smt2_combine(a_smt, conn_a)})")
            lines.append(f"; --- Policy B ({_connective_label(conn_b)}) ---")
            lines.append(f"(assert {_smt2_combine(b_smt, conn_b)})")
        elif b.verdict in (Verdict.SUBSUMES, Verdict.REFUTED):
            lines.append(f"")
            lines.append(f"; --- ∈ Policy A ({_connective_label(conn_a)}) ---")
            lines.append(f"(assert {_smt2_combine(a_smt, conn_a)})")
            lines.append(f"; --- ¬(∈ Policy B): negated {_connective_label(conn_b)} ---")
            lines.append(f"(assert {_smt2_negate(b_smt, conn_b)})")

    lines.append(f"")
    lines.append(f"; Result: {'unsat' if b.szs == SZS.THEOREM else 'sat'} → {b.verdict.value}")
    lines.append(f"(check-sat)")
    lines.append(f"(exit)")
    return "\n".join(lines)


# ==========================================================================
# File writer
# ==========================================================================

def write_benchmark(b: Benchmark, base_dir: Path, dry_run: bool = False):
    """Write both encodings for a benchmark."""
    fof_dir = base_dir / "Problems" / "ODRL" / "AxisDecomposition" / b.category.value
    fof_path = fof_dir / f"ODRL{b.number}-1.p"
    smt_dir = base_dir / "Problems" / "ODRL" / "SelfContained" / "spatialAxis"
    smt_path = smt_dir / f"ODRL{b.number}-1.smt2"

    if dry_run:
        print(f"  [DRY] {fof_path.relative_to(base_dir)}")
        print(f"  [DRY] {smt_path.relative_to(base_dir)}")
        return

    fof_dir.mkdir(parents=True, exist_ok=True)
    smt_dir.mkdir(parents=True, exist_ok=True)
    fof_path.write_text(generate_fof(b) + "\n")
    smt_path.write_text(generate_smt2(b) + "\n")
    print(f"  ✓ {fof_path.relative_to(base_dir)}")
    print(f"  ✓ {smt_path.relative_to(base_dir)}")


# ==========================================================================
# Runner
# ==========================================================================

@dataclass
class ProverResult:
    benchmark: int
    name: str
    prover: str
    encoding: str
    expected: str
    actual: str
    match: bool
    time_s: float
    error: str = ""


def run_z3(smt_path: Path, timeout: int = 30) -> tuple[str, float, str]:
    try:
        start = time.time()
        proc = subprocess.run(["z3", str(smt_path)],
                              capture_output=True, text=True, timeout=timeout)
        elapsed = time.time() - start
        output = proc.stdout.strip()
        if output in ("sat", "unsat", "unknown"):
            return output, elapsed, ""
        return "error", elapsed, (proc.stderr.strip() or output)[:200]
    except FileNotFoundError:
        return "error", 0.0, "z3 not found in PATH"
    except subprocess.TimeoutExpired:
        return "timeout", float(timeout), ""


def run_vampire(fof_path: Path, include_dir: Path,
                timeout: int = 30) -> tuple[str, float, str]:
    try:
        start = time.time()
        proc = subprocess.run(
            ["vampire", "--input_syntax", "tptp",
             "--include", str(include_dir),
             "--time_limit", str(timeout),
             str(fof_path)],
            capture_output=True, text=True, timeout=timeout + 10)
        elapsed = time.time() - start
        for line in proc.stdout.splitlines():
            if "SZS status" in line:
                status = line.split("SZS status")[1].strip().split()[0]
                return status, elapsed, ""
        return "error", elapsed, proc.stderr.strip()[:200] or "No SZS status in output"
    except FileNotFoundError:
        return "error", 0.0, "vampire not found in PATH"
    except subprocess.TimeoutExpired:
        return "timeout", float(timeout), ""


def expected_z3(b: Benchmark) -> str:
    return "unsat" if b.szs == SZS.THEOREM else "sat"

def expected_vampire(b: Benchmark) -> str:
    return "Theorem"


def run_benchmarks(benchmarks: list[Benchmark], base: Path,
                   timeout: int = 30) -> list[ProverResult]:
    results = []
    include_dir = base / "Problems" / "ODRL"
    has_z3 = shutil.which("z3") is not None
    has_vampire = shutil.which("vampire") is not None
    if not has_z3: print("  ⚠  z3 not found — skipping SMT-LIB benchmarks")
    if not has_vampire: print("  ⚠  vampire not found — skipping FOF benchmarks")

    for b in benchmarks:
        if has_z3:
            smt_path = (base / "Problems" / "ODRL" / "SelfContained"
                        / "spatialAxis" / f"ODRL{b.number}-1.smt2")
            if smt_path.exists():
                exp = expected_z3(b)
                actual, elapsed, err = run_z3(smt_path, timeout)
                match = (actual == exp)
                sym = "✓" if match else "✗"
                print(f"  {sym} ODRL{b.number} z3: {actual} "
                      f"(expected {exp}) [{elapsed:.2f}s]"
                      f"{' ERROR: ' + err if err else ''}")
                results.append(ProverResult(b.number, b.name, "z3", "smt2",
                                            exp, actual, match, elapsed, err))

        if has_vampire:
            fof_path = (base / "Problems" / "ODRL" / "AxisDecomposition"
                        / b.category.value / f"ODRL{b.number}-1.p")
            if fof_path.exists():
                exp = expected_vampire(b)
                actual, elapsed, err = run_vampire(fof_path, include_dir, timeout)
                match = (actual == exp)
                sym = "✓" if match else "✗"
                print(f"  {sym} ODRL{b.number} vampire: {actual} "
                      f"(expected {exp}) [{elapsed:.2f}s]"
                      f"{' ERROR: ' + err if err else ''}")
                results.append(ProverResult(b.number, b.name, "vampire", "fof",
                                            exp, actual, match, elapsed, err))
    return results


def write_results_csv(results: list[ProverResult], output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["benchmark", "name", "prover", "encoding",
                          "expected", "actual", "match", "time_s", "error"])
        for r in results:
            writer.writerow([f"ODRL{r.benchmark}", r.name, r.prover, r.encoding,
                             r.expected, r.actual, r.match, f"{r.time_s:.3f}", r.error])
    print(f"\n  Results → {output_path}")


def print_concordance(results: list[ProverResult]):
    by_bench: dict[int, dict[str, ProverResult]] = {}
    for r in results:
        by_bench.setdefault(r.benchmark, {})[r.prover] = r

    agree = disagree = partial = 0
    print(f"\n{'='*60}")
    print(f"  CONCORDANCE SUMMARY")
    print(f"{'='*60}")

    for num in sorted(by_bench):
        z3_r = by_bench[num].get("z3")
        vamp_r = by_bench[num].get("vampire")
        z3_ok = z3_r.match if z3_r else None
        vamp_ok = vamp_r.match if vamp_r else None
        z3_str = z3_r.actual if z3_r else "-"
        vamp_str = vamp_r.actual if vamp_r else "-"

        if z3_ok is None or vamp_ok is None:
            partial += 1; sym = "◐"
        elif z3_ok and vamp_ok:
            agree += 1; sym = "✓"
        elif z3_ok == vamp_ok:
            agree += 1; sym = "?"
        else:
            disagree += 1; sym = "✗"

        print(f"  {sym} ODRL{num}: z3={z3_str:12s}  vampire={vamp_str:20s}")

    total = agree + disagree + partial
    print(f"\n  Agreement: {agree}/{total}  "
          f"Disagreement: {disagree}/{total}  "
          f"Partial: {partial}/{total}")
    if disagree == 0 and partial == 0:
        print(f"  ✓ 100% concordance between Z3 and Vampire")
    elif disagree > 0:
        print(f"  ✗ DISAGREEMENTS FOUND — investigate manually")


# ==========================================================================
# Main
# ==========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate and run axis decomposition benchmarks")
    parser.add_argument("--category", type=str, default=None,
                        help="Generate/run only one category (e.g. SingleAxis)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run", action="store_true",
                        help="Generate + run both provers")
    parser.add_argument("--run-only", action="store_true",
                        help="Run on existing files (skip generation)")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--base-dir", type=str, default=".")
    args = parser.parse_args()
    base = Path(args.base_dir)

    # Select categories
    if args.category:
        cat = Category(args.category)
        if cat not in CATEGORY_GENERATORS:
            print(f"Error: {cat.value} not implemented. "
                  f"Available: {', '.join(c.value for c in CATEGORY_GENERATORS)}")
            return
        cats = {cat: CATEGORY_GENERATORS[cat]}
    else:
        cats = CATEGORY_GENERATORS

    # Collect all benchmarks
    all_benchmarks = []
    for gen_fn in cats.values():
        all_benchmarks.extend(gen_fn())

    # === Generate ===
    if not args.run_only:
        total = 0
        for cat, gen_fn in cats.items():
            benchmarks = gen_fn()
            print(f"\n=== Generating {cat.value} ({len(benchmarks)} benchmarks) ===")
            for b in benchmarks:
                write_benchmark(b, base, dry_run=args.dry_run)
                total += 1
        print(f"\n{'[DRY RUN] ' if args.dry_run else ''}"
              f"Generated {total} benchmarks → {total * 2} files")

    # === Run ===
    if args.run or args.run_only:
        if args.dry_run:
            print("\n  Cannot --run with --dry-run")
            return
        print(f"\n{'='*60}")
        print(f"  RUNNING PROVERS (timeout={args.timeout}s)")
        print(f"{'='*60}")

        results = run_benchmarks(all_benchmarks, base, timeout=args.timeout)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = base / "results" / "axis" / f"axis_benchmark_{timestamp}.csv"
        write_results_csv(results, csv_path)
        print_concordance(results)

        total_r = len(results)
        matches = sum(1 for r in results if r.match)
        errors = sum(1 for r in results if r.error)
        print(f"\n  Total runs: {total_r}  Pass: {matches}  "
              f"Fail: {total_r - matches}  Errors: {errors}")


if __name__ == "__main__":
    main()