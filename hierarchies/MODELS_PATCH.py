# ============================================================
# MODELS_PATCH.py
# Add these values to your existing models.py
# ============================================================
#
# 1. Add to the Category enum:
#
#     NESTED_SET_OPS      = "NestedSetOperators"
#     QUANTIFIER_STRESS   = "QuantifierStress"
#     LARGE_COMPOSITION   = "LargeComposition"
#     EDGE_CASES_ADV      = "EdgeCases"
#     MULTIHOP_ADV        = "MultiHopAlignment"
#     NWAY_CONFLICT       = "NWayConflict"
#     NWAY_COMPOSED       = "NWayComposed"
#     SET_OPERATOR_STRESS = "SetOperatorStress"
#     COMBINED_COMPLEXITY = "CombinedComplexity"
#     ADVERSARIAL_OPS     = "AdversarialOperators"
#     XONE                = "XONESymmetricDiff"
#     OPERATOR_MONOTONE   = "OperatorMonotonicity"
#
# 2. KBProblem must accept these fields (already there if you used
#    the standard dataclass):
#
#     number:   int
#     name:     str
#     variant:  int          # 1 or 2
#     category: Category
#     szs:      SZS
#     includes: list[str]    # e.g. ["GEO000-0.ax", "ODRL000-0.ax"]
#     extra:    str          # inline axioms (empty string if none)
#     conjecture: str        # fof(...) conjecture formula
#     flip_conjecture: str   # alternative for CounterSat→Theorem, or ""
#     description: str       # one-liner
#     difficulty: str        # Easy/Medium/Hard/Very Hard/Extreme
