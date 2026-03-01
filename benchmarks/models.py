"""Shared data model for axis decomposition benchmarks."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Op(Enum):
    """ODRL dimensional comparison operators."""
    EQ   = "eq"
    LT   = "lt"
    LTEQ = "lteq"
    GT   = "gt"
    GTEQ = "gteq"


class Verdict(Enum):
    """Expected verdict for the benchmark."""
    CONFLICT   = "Conflict"
    COMPATIBLE = "Compatible"
    SUBSUMES   = "Subsumes"
    REFUTED    = "Refuted"


class SZS(Enum):
    """SZS status for TPTP."""
    THEOREM            = "Theorem"
    COUNTERSATISFIABLE = "CounterSatisfiable"


class Category(Enum):
    """Benchmark categories matching directory names."""
    SINGLE_AXIS    = "SingleAxis"
    BOX_2D         = "Box2D"
    BOX_3D         = "Box3D"
    COMPOSITION    = "Composition"
    CROSS_DOMAIN   = "CrossDomain"
    POLICY_QUALITY = "PolicyQuality"
    BOUNDARY       = "Boundary"
    LOGICAL_OR     = "LogicalOr"
    LOGICAL_XONE   = "LogicalXone"


class Connective(Enum):
    """ODRL LogicalConstraint connective type.

    AND — implicit (multiple odrl:constraint on one Rule) or odrl:and
    OR  — odrl:or  (at least one constraint must hold)
    XONE — odrl:xone (exactly one constraint must hold)
    """
    AND  = "and"
    OR   = "or"
    XONE = "xone"


@dataclass
class Constraint:
    """A single axis-specific constraint."""
    axis: str          # e.g. "width", "height", "latitude"
    op: Op             # comparison operator
    value: float       # right-operand value
    axis_iri: str = "" # e.g. "oax:absoluteSizeWidth"


@dataclass
class Benchmark:
    """A single benchmark problem.

    For SingleAxis: uses c1, c2 (one axis pair).
    For Box2D/Box3D: additionally uses c1_ax2/c2_ax2 (and c1_ax3/c2_ax3).
    The conjecture quantifies over one variable per axis.
    """
    number: int                    # ODRL number (300+)
    name: str                      # short identifier
    category: Category
    c1: Constraint                 # Policy A, axis 1
    c2: Constraint                 # Policy B, axis 1
    verdict: Verdict               # expected result
    szs: SZS                       # expected SZS status
    description: str               # one-liner
    difficulty: str = "Easy"       # Easy / Medium / Hard
    domain_lo: Optional[float] = None     # axis 1 lower bound (None = -inf)
    domain_lo_open: bool = True           # True = open at lo
    domain_hi: Optional[float] = None     # axis 1 upper bound (None = +inf)
    domain_hi_open: bool = False          # True = open at hi
    needs_density: bool = False           # include ORD001-0?
    policy_ttl: str = ""                  # ODRL policy snippet
    notes: str = ""                       # extra notes for header
    # --- Logical connectives (default AND = implicit multi-constraint) ---
    connective_a: 'Connective' = None     # Policy A connective (None = AND)
    connective_b: 'Connective' = None     # Policy B connective (None = AND)
    # --- Optional axis 2 (Box2D, Box3D) ---
    c1_ax2: Optional[Constraint] = None   # Policy A, axis 2
    c2_ax2: Optional[Constraint] = None   # Policy B, axis 2
    domain2_lo: Optional[float] = None
    domain2_lo_open: bool = True
    domain2_hi: Optional[float] = None
    domain2_hi_open: bool = False
    # --- Optional axis 3 (Box3D) ---
    c1_ax3: Optional[Constraint] = None   # Policy A, axis 3
    c2_ax3: Optional[Constraint] = None   # Policy B, axis 3
    domain3_lo: Optional[float] = None
    domain3_lo_open: bool = True
    domain3_hi: Optional[float] = None
    domain3_hi_open: bool = False
    # --- Optional axis 4 (Composition) ---
    c1_ax4: Optional[Constraint] = None   # Policy A, axis 4
    c2_ax4: Optional[Constraint] = None   # Policy B, axis 4
    domain4_lo: Optional[float] = None
    domain4_lo_open: bool = True
    domain4_hi: Optional[float] = None
    domain4_hi_open: bool = False