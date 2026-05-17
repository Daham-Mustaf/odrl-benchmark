"""
problem_data_semcore.py
=======================
SemanticCore benchmark problems: ODRL500-513 (14 problems).
Category: SemanticCore/

Covers paper formal results not in other categories:
  lem:totality      -- non-emptiness of each operator denotation (5)
  lem:normalisation -- same-axis constraint intersection (2)
  thm:projection    -- box/per-axis membership biconditional (1)
  thm:aabb          -- all 4 bounded interval shapes (4)
  def:profile       -- well-formedness consequence: empty denotation (2)

Include pattern:
    include('Axioms/ORD000-0.ax').
    include('Axioms/AXIS000-0.ax').
    [include('Axioms/ORD001-0.ax').]  -- when needs_density=True
    [include('Axioms/PROJ000-0.ax').] -- when uses in_box2/in_box3

Change log (v1.1):
  - ODRL507 conjecture rewritten.  Previous version was P => P (literally
    identical antecedent and consequent), a propositional tautology
    provable from the empty axiom set; did not test thm:projection.
    New conjecture tests both directions of the paper's biconditional
    (box membership <=> per-axis membership) on a concrete instance.
    Requires PROJ000-0.ax in includes for the new test.  SMT updated
    to match (negation of biconditional, asserted unsat).

  - ODRL512 and ODRL513 descriptions clarified.  Previous labels said
    "def:profile (ii)" and "def:profile (iii)" but the conjectures test
    the geometric *consequence* (empty denotation), not the well-formedness
    predicate directly (which lives in WF000 / WellFormedness category).
    Labels updated to "geometric consequence of def:profile (ii)/(iii)".
    No code change to conjectures/SMTs.

  - All 14 problems aligned to the standard problem-dict shape used by
    every other problem_data_*.py module (includes, fof_extra_decls,
    fof_conjecture, smt2_logic, smt2_decls, smt2_asserts).
"""

# ----------------------------------------------------------------------
# Shared declaration blocks (matches the chains used in audit)
# ----------------------------------------------------------------------

_DECLS_2 = """\
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v600)).
"""

_DECLS_3 = """\
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v400, v600)).
"""

_DECLS_v0_v600 = """\
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
"""


def _ttl(op, val):
    return f"""\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator {op} ;
      odrl:rightOperand "{val}"^^xsd:decimal ] ] ."""


def _ttl_box():
    """TTL for ODRL507 -- 2D box policy (width AND height bounded)."""
    return """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ]
    ) ] ] ."""


# ----------------------------------------------------------------------
# Problem dictionaries
# ----------------------------------------------------------------------

PROBLEMS = [

    # =================================================================
    # lem:totality (5 problems) -- each operator denotation is non-empty
    # =================================================================

    {
        "id":            "ODRL500",
        "subdir":        "SemanticCore",
        "name":          "lem:totality -- lteq denotation is non-empty",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "lem:totality applied to lteq: denotation (v0, v600] is non-empty.\n"
            "Witness: any X with less(v0, X) and leq(X, v600); e.g., X = v200.\n"
        ),
        "ttl": _ttl("odrl:lteq", "600"),
        "fof_extra_decls": _DECLS_2,
        "fof_conjecture":  "?[X]: in_lopen(X, v0, v600)",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (> x 0.0))\n(assert (<= x 600.0))",
    },

    {
        "id":            "ODRL501",
        "subdir":        "SemanticCore",
        "name":          "lem:totality -- gteq denotation is non-empty",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "lem:totality applied to gteq: denotation [v200, +inf) is non-empty.\n"
            "Witness: any X with leq(v200, X); X = v200 itself satisfies.\n"
        ),
        "ttl": _ttl("odrl:gteq", "200"),
        "fof_extra_decls": _DECLS_2,
        "fof_conjecture":  "?[X]: leq(v200, X)",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (>= x 200.0))",
    },

    {
        "id":            "ODRL502",
        "subdir":        "SemanticCore",
        "name":          "lem:totality -- lt denotation is non-empty",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "lem:totality applied to lt: denotation (v0, v600) is non-empty.\n"
            "Witness: any X with less(v0, X) and less(X, v600); e.g., X = v200.\n"
        ),
        "ttl": _ttl("odrl:lt", "600"),
        "fof_extra_decls": _DECLS_2,
        "fof_conjecture":  "?[X]: in_open(X, v0, v600)",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (> x 0.0))\n(assert (< x 600.0))",
    },

    {
        "id":            "ODRL503",
        "subdir":        "SemanticCore",
        "name":          "lem:totality -- gt denotation is non-empty",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "lem:totality applied to gt: denotation (v200, +inf) is non-empty.\n"
            "Witness: any X with less(v200, X); e.g., X = v600.\n"
        ),
        "ttl": _ttl("odrl:gt", "200"),
        "fof_extra_decls": _DECLS_2,
        "fof_conjecture":  "?[X]: less(v200, X)",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (> x 200.0))",
    },

    {
        "id":            "ODRL504",
        "subdir":        "SemanticCore",
        "name":          "lem:totality -- eq denotation is non-empty",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "lem:totality applied to eq: denotation {v200} is non-empty.\n"
            "Witness: X = v200 satisfies in_closed(X, v200, v200).\n"
        ),
        "ttl": _ttl("odrl:eq", "200"),
        "fof_extra_decls": _DECLS_2,
        "fof_conjecture":  "?[X]: in_closed(X, v200, v200)",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (= x 200.0))",
    },

    # =================================================================
    # lem:normalisation (2 problems) -- same-axis constraint intersection
    # =================================================================

    {
        "id":            "ODRL505",
        "subdir":        "SemanticCore",
        "name":          "lem:normalisation -- same-axis lteq intersection reduces to tighter bound",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "lem:normalisation: two lteq constraints on the same axis intersect\n"
            "to the tighter bound: (v0, v400] cap (v0, v600] = (v0, v400].\n"
            "Witness: any X with less(v0, X) and leq(X, v400); e.g., X = v200.\n"
        ),
        "ttl": _ttl("odrl:lteq", "400"),
        "fof_extra_decls": _DECLS_3,
        "fof_conjecture":  "?[X]: (in_lopen(X, v0, v400) & in_lopen(X, v0, v600))",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (> x 0.0))\n(assert (<= x 400.0))\n(assert (<= x 600.0))",
    },

    {
        "id":            "ODRL506",
        "subdir":        "SemanticCore",
        "name":          "lem:normalisation -- conflicting same-axis constraints yield empty denotation",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "lem:normalisation: conflicting same-axis constraints yield empty\n"
            "denotation. (v0, v200] cap [v400, +inf) = empty since v200 < v400.\n"
            "Closes via in_lopen unfold + leq + transitivity contradicting\n"
            "less irreflexivity.\n"
        ),
        "ttl": _ttl("odrl:lteq", "200"),
        "fof_extra_decls": _DECLS_3,
        "fof_conjecture":  "![X]: ~(in_lopen(X, v0, v200) & leq(v400, X))",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (> x 0.0))\n(assert (<= x 200.0))\n(assert (>= x 400.0))",
    },

    # =================================================================
    # thm:projection (1 problem) -- box / per-axis membership biconditional
    # =================================================================
    # v1.1: rewritten.  Previous conjecture was P => P (vacuously true).
    # New conjecture tests both directions of the paper's iff on a concrete
    # instance.  Requires PROJ000-0.ax for in_box2_def biconditional.

    {
        "id":            "ODRL507",
        "subdir":        "SemanticCore",
        "name":          "thm:projection -- box <=> per-axis membership (concrete instance)",
        "relation":      "verdict_algebra",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax", "PROJ000-0.ax"],
        "description": (
            "thm:projection at concrete point (v200, v200) over box\n"
            "[v0, v600] x [v0, v400]:\n"
            "  in_box2(v200, v200, v0, v600, v0, v400)\n"
            "  <=> (in_closed(v200, v0, v600) & in_closed(v200, v0, v400)).\n"
            "Tests both directions of the paper's biconditional.\n"
            "FOL closes via in_box2_def (PROJ000) + in_closed_def (AXIS000).\n"
            "SMT: negation of the iff is empty.\n"
        ),
        "ttl": _ttl_box(),
        "fof_extra_decls": _DECLS_3,
        "fof_conjecture": (
            "in_box2(v200, v200, v0, v600, v0, v400)\n"
            "  <=> (in_closed(v200, v0, v600) & in_closed(v200, v0, v400))"
        ),
        "smt2_logic":   "QF_LRA",
        "smt2_decls":   "(declare-const x Real)\n(declare-const y Real)",
        # x=200, y=200; membership in box iff (200 in [0,600]) AND (200 in [0,400]).
        # Both are true.  Negation of iff = (LHS != RHS) is empty.
        # Encode membership via interval bounds; iff equivalence to per-axis test.
        # Negation: (x in box) XOR (x_in_axis_w AND y_in_axis_h)
        # Witness x=y=200: all conditions hold, no XOR satisfaction -> unsat.
        "smt2_asserts": (
            "(assert (= x 200.0)) (assert (= y 200.0))\n"
            "; box membership: x in [0,600], y in [0,400]\n"
            "; per-axis:       x in [0,600] AND y in [0,400] (identical bounds)\n"
            "; negation of iff: box_mem != per_axis_mem -- empty at (200, 200)\n"
            "(assert (not\n"
            "  (= (and (>= x 0.0) (<= x 600.0) (>= y 0.0) (<= y 400.0))\n"
            "     (and (and (>= x 0.0) (<= x 600.0))\n"
            "          (and (>= y 0.0) (<= y 400.0))))))"
        ),
    },

    # =================================================================
    # thm:aabb (4 problems) -- four bounded interval shapes are non-empty
    # =================================================================

    {
        "id":            "ODRL508",
        "subdir":        "SemanticCore",
        "name":          "thm:aabb -- closed bounded interval [l,u] is non-empty",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "thm:aabb closed-closed shape: bounded interval [v200, v400] is\n"
            "non-empty.  Witness X = v200 (or v400, or anywhere in between).\n"
        ),
        "ttl": _ttl("odrl:gteq", "200"),
        "fof_extra_decls": _DECLS_3,
        "fof_conjecture":  "?[X]: (leq(v200, X) & in_lopen(X, v0, v400))",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (>= x 200.0))\n(assert (<= x 400.0))",
    },

    {
        "id":            "ODRL509",
        "subdir":        "SemanticCore",
        "name":          "thm:aabb -- half-open right-closed (l, u] is non-empty",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "thm:aabb half-open right-closed shape: (v200, v400] is non-empty.\n"
            "Witness X with less(v200, X) and leq(X, v400); e.g., X = v400.\n"
        ),
        "ttl": _ttl("odrl:gt", "200"),
        "fof_extra_decls": _DECLS_3,
        "fof_conjecture":  "?[X]: (less(v200, X) & in_lopen(X, v0, v400))",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (> x 200.0))\n(assert (<= x 400.0))",
    },

    {
        "id":            "ODRL510",
        "subdir":        "SemanticCore",
        "name":          "thm:aabb -- half-open left-closed [l, u) is non-empty",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "thm:aabb half-open left-closed shape: [v200, v400) is non-empty.\n"
            "Witness X with leq(v200, X) and less(X, v400); e.g., X = v200.\n"
        ),
        "ttl": _ttl("odrl:gteq", "200"),
        "fof_extra_decls": _DECLS_3,
        "fof_conjecture":  "?[X]: (leq(v200, X) & in_open(X, v0, v400))",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (>= x 200.0))\n(assert (< x 400.0))",
    },

    {
        "id":            "ODRL511",
        "subdir":        "SemanticCore",
        "name":          "thm:aabb -- open bounded interval (l, u) is non-empty (density)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": True,
        "includes":      ["ORD000-0.ax", "ORD001-0.ax", "AXIS000-0.ax"],
        "description": (
            "thm:aabb open-open shape: (v200, v400) is non-empty.  Requires\n"
            "ORD001 density: no named constant lies strictly between v200 and\n"
            "v400, so the existential witness must come from density.\n"
        ),
        "ttl": _ttl("odrl:gt", "200"),
        "fof_extra_decls": _DECLS_3,
        "fof_conjecture":  "?[X]: (less(v200, X) & in_open(X, v0, v400))",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (> x 200.0))\n(assert (< x 400.0))",
    },

    # =================================================================
    # def:profile consequences (2 problems) -- geometric consequence of WF
    # =================================================================
    # v1.1: descriptions clarified.  These test the *geometric consequence*
    # of def:profile (ii)/(iii) -- i.e., that the denotation is empty when
    # the WF predicate would reject the constraint.  Testing the WF
    # predicate directly is what the WellFormedness category does (WF000).

    {
        "id":            "ODRL512",
        "subdir":        "SemanticCore",
        "name":          "Geometric consequence of def:profile (ii) -- lt at domain inf has empty denotation",
        "relation":      "verdict_algebra",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "Geometric consequence of def:profile (ii): a constraint (lt, v0)\n"
            "on domain (v0, +inf) has empty denotation, since no X satisfies\n"
            "less(v0, X) AND less(X, v0).  Closes via in_open unfold +\n"
            "less irreflexivity (transitivity gives less(v0, v0)).\n"
            "Note: def:profile (ii) rejects this constraint as ill-formed.\n"
            "WF000 / WellFormedness category tests the WF predicate directly.\n"
            "This problem tests the geometric consequence (empty denotation).\n"
        ),
        "ttl": _ttl("odrl:lt", "0"),
        "fof_extra_decls": _DECLS_2,
        "fof_conjecture":  "![X]: ~in_open(X, v0, v0)",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        # P AND NOT P at value 0 -- same disposition as ODRL614/637/762
        # (irreflexivity-at-a-point), accepted as semantic in the
        # value-dependent sense.
        "smt2_asserts":    "(assert (> x 0.0))\n(assert (< x 0.0))",
    },

    {
        "id":            "ODRL513",
        "subdir":        "SemanticCore",
        "name":          "Geometric consequence of def:profile (iii) -- gt at effective upper bound has empty denotation",
        "relation":      "verdict_algebra",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "Geometric consequence of def:profile (iii): when the effective\n"
            "upper bound is v600, a constraint (gt, v600) combined with the\n"
            "domain (v0, v600] has empty denotation, since no X satisfies\n"
            "less(v600, X) AND leq(X, v600).\n"
            "Note: see ODRL512 comment.  This tests the geometric consequence;\n"
            "WF000 / WellFormedness tests the WF predicate.\n"
        ),
        "ttl": _ttl("odrl:gt", "600"),
        "fof_extra_decls": _DECLS_v0_v600,
        "fof_conjecture":  "![X]: ~(less(v600, X) & in_lopen(X, v0, v600))",
        "smt2_logic":      "QF_LRA",
        "smt2_decls":      "(declare-const x Real)",
        "smt2_asserts":    "(assert (> x 600.0))\n(assert (<= x 600.0))",
    },
]
