"""
hierarchies/__init__.py  (UPDATED)
Registry of all KBGrounding category generators.
"""
from .models import Category, KBProblem

# ── Existing categories (cat01–cat09) ────────────────────────────────────
from .cat01_spatial            import spatial_basic
from .cat02_set_valued         import set_valued
from .cat03_subsumption        import subsumption
from .cat04_composition        import composition
from .cat05_edge_cases         import edge_cases
from .cat06_dag                import dag_multi_parent
from .cat07_tautology_redundancy import tautology_redundancy
from .cat08_alignment          import alignment
from .cat09_runtime            import runtime

# ── New categories (cat10–cat21) ─────────────────────────────────────────
from .cat10_nested_set_ops     import nested_set_ops
from .cat11_quantifier_stress  import quantifier_stress
from .cat12_large_composition  import large_composition
from .cat13_edge_cases_adv     import edge_cases_adv
from .cat14_multihop_adv       import multihop_adv
from .cat15_nway_conflict      import nway_conflict
from .cat16_nway_composed      import nway_composed
from .cat17_set_operator_stress import set_operator_stress
from .cat18_combined_complexity import combined_complexity
from .cat19_to_21 import (
    adversarial_operators,
    xone,
    operator_monotonicity,
)


def spatial_all() -> list[KBProblem]:
    """All Spatial: cat01–cat09 combined."""
    return (spatial_basic() + set_valued() + subsumption()
            + composition() + edge_cases() + tautology_redundancy()
            + runtime())


CATEGORY_GENERATORS: dict[Category, callable] = {
    # ── Existing ─────────────────────────────────────────────────────
    Category.SPATIAL:              spatial_all,
    Category.DAG_MULTI_PARENT:     dag_multi_parent,
    Category.MULTI_HOP_ALIGN:      alignment,
    Category.RUNTIME:              runtime,

    # ── New: Advanced Suite (Categories 10–16) ────────────────────────
    Category.NESTED_SET:       nested_set_ops,
    Category.QUANTIFIER_STRESS:    quantifier_stress,
    Category.LARGE_COMPOSITION:    large_composition,
    Category.EDGE_CASES:       edge_cases_adv,
    Category.MULTI_HOP_ALIGN:         multihop_adv,
    Category.N_WAY_CONFLICT:        nway_conflict,
    Category.N_WAY_COMPOSED:        nway_composed,

    # ── New: Extreme Suite (Categories 17–21) ─────────────────────────
    Category.COMBINED:  set_operator_stress,
    Category.COMBINED:  combined_complexity,
    Category.ADVERSARIAL:      adversarial_operators,
    Category.XONE_SYMM:                 xone,
    Category.MONOTONICITY:    operator_monotonicity,
}

__all__ = ["CATEGORY_GENERATORS", "Category", "KBProblem"]
