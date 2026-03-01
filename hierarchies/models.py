"""
    SET_OPERATOR_STRESS = "SetOperatorStress"
hierarchies/models.py
Dataclass and enums for ODRL KBGrounding benchmark generation.
Mirrors benchmarks/models.py (AxisDecomposition) but for hierarchy-based problems.
Each KBProblem produces:
  - one .p  file (TPTP FOF, run by Vampire)
  - one .smt2 file (SMT-LIB 2, run by Z3, self-contained)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ==========================================================================
# Enums
# ==========================================================================

class Category(Enum):
    SPATIAL          = "Spatial"           # ODRL010-095
    DAG_MULTI_PARENT = "DAGMultiParent"    # ODRL100-105
    NESTED_SET       = "NestedSetOperators"# ODRL110-114
    QUANTIFIER_STRESS= "QuantifierStress"  # ODRL120-123
    LARGE_COMPOSITION= "LargeComposition"  # ODRL130-132
    EDGE_CASES       = "EdgeCases"         # ODRL140-145
    MULTI_HOP_ALIGN  = "MultiHopAlignment" # ODRL150-159
    N_WAY_CONFLICT   = "NWayConflict"      # ODRL160-165
    N_WAY_COMPOSED   = "NWayComposed"      # ODRL170-175
    ADVERSARIAL      = "AdversarialOperators" # ODRL220-225
    XONE_SYMM        = "XONESymmetricDiff" # ODRL230-237
    MONOTONICITY     = "OperatorMonotonicity" # ODRL250-254
    COMBINED         = "CombinedComplexity"# ODRL210-215
    RUNTIME          = "Runtime"           # ODRL090-095


class Verdict(Enum):
    COMPATIBLE   = "Compatible"
    CONFLICT     = "Conflict"
    UNKNOWN      = "Unknown"
    SUBSUMES     = "Subsumption"
    REFUTED      = "Refuted"
    CONSISTENT   = "Consistent"
    INCONSISTENT = "Inconsistent"
    TAUTOLOGICAL = "Tautological"
    DERIVABLE    = "Derivable"


class SZS(Enum):
    """Expected SZS status for Vampire."""
    THEOREM              = "Theorem"
    COUNTERSATISFIABLE   = "CounterSatisfiable"
    CONTRADICTORY_AXIOMS = "ContradictoryAxioms"
    SATISFIABLE          = "Satisfiable"


class Op(Enum):
    """ODRL hierarchy-dependent operators."""
    EQ         = "eq"
    NEQ        = "neq"
    IS_A       = "isA"
    IS_PART_OF = "isPartOf"
    HAS_PART   = "hasPart"
    IS_ANY_OF  = "isAnyOf"
    IS_ALL_OF  = "isAllOf"
    IS_NONE_OF = "isNoneOf"


class KB(Enum):
    """Available Layer 0 knowledge bases."""
    GEO          = "GEO"
    DPV          = "DPV"
    DPV_NAIVE    = "DPV_NAIVE"
    LANG         = "LANG"
    ISO          = "ISO"
    ALIGN_DATA   = "ALIGN_DATA"
    ALIGN_THEORY = "ALIGN_THEORY"
    RUNTIME      = "RUNTIME"
    DEMO         = "DEMO"


# Include paths for .p files
KB_INCLUDE = {
    KB.GEO:          "include('Axioms/Layer0-DomainKB/GEO000-0.ax').",
    KB.DPV:          "include('Axioms/Layer0-DomainKB/DPV000-0.ax').",
    KB.DPV_NAIVE:    "include('Axioms/Layer0-DomainKB/DPV-NAIVE.ax').",
    KB.LANG:         "include('Axioms/Layer0-DomainKB/LANG000-0.ax').",
    KB.ISO:          "include('Axioms/Layer0-DomainKB/ISO3166-0.ax').",
    KB.ALIGN_DATA:   "include('Axioms/Alignment/ALIGN-GEO-ISO.ax').",
    KB.ALIGN_THEORY: "include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').",
    KB.RUNTIME:      "include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').",
    KB.DEMO:         "include('Axioms/Layer0-DomainKB/DEMO-0.ax').",
}

# ODRL000-0.ax is always included
ODRL_INCLUDE = "include('Axioms/Layer1-ODRLCore/ODRL000-0.ax')."


# ==========================================================================
# Constraint helper
# ==========================================================================

@dataclass
class Constraint:
    """Single ODRL constraint: (operand, op, value)."""
    operand: str       # e.g. "spatial", "hasPurpose", "language"
    op: Op
    value: str         # e.g. "europe", "commercialResearch"
    # For set-valued operators (isAnyOf, isAllOf, isNoneOf):
    values: list[str] = field(default_factory=list)
    list_id: str = ""  # TPTP list constant, e.g. "regions020"


# ==========================================================================
# KBProblem dataclass
# ==========================================================================

@dataclass
class KBProblem:
    """
    One KBGrounding benchmark problem.

    Produces both a .p (TPTP) and a .smt2 (SMT-LIB 2) file.

    Fields
    ------
    number      : int            ODRL problem number (e.g., 10 → ODRL010)
    variant     : int            Variant number (almost always 1)
    name        : str            Short name for CSV / concordance table
    category    : Category       Determines output subdirectory
    verdict     : Verdict        Expected semantic verdict
    szs         : SZS            Expected Vampire SZS status
    kbs         : list[KB]       Layer 0 KBs to include (GEO, DPV, etc.)
    c1          : Constraint     Constraint from policy A (permission/offer)
    c2          : Constraint     Constraint from policy B (prohibition/request)
    conjecture_fof  : str        Complete fof(odrlNNN, conjecture, ...) line(s)
    conjecture_smt2 : str        SMT2 assert + check-sat (negated conjecture)
    inline_axioms   : str        Extra FOF axioms for self-contained problems
    inline_smt2_kb  : str        SMT2 KB declarations for self-contained problems
    policy_ttl      : str        ODRL Turtle snippet for header comment
    description     : str        One-line problem description
    formal          : str        Formal denotation analysis for header
    paper_ref       : str        Paper definition/lemma reference
    difficulty      : str        Trivial / Easy / Medium / Hard / Very Hard
    notes           : str        Additional comments for header
    """
    number:          int
    name:            str
    category:        Category
    verdict:         Verdict
    szs:             SZS
    kbs:             list[KB]
    c1:              Optional[Constraint]
    c2:              Optional[Constraint]
    conjecture_fof:  str
    conjecture_smt2: str          # full SMT2 block: declares + asserts + check-sat
    description:     str
    formal:          str = ""
    paper_ref:       str = ""
    difficulty:      str = "Medium"
    policy_ttl:      str = ""
    notes:           str = ""
    inline_axioms:   str = ""     # extra FOF axioms (inlined, not via include)
    inline_smt2_kb:  str = ""     # SMT2 KB fragment for self-contained .smt2

    variant:         int = 1