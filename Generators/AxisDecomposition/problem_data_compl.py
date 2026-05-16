"""
problem_data_compl.py
=====================
Completion benchmark problems: ODRL630-637 (8 problems).
Category O: Tests completion_compatible/3, completion_conflict/4,
axis_conflict/4, monotone_conflict (Prop 6.9), and box_verdict.

Include pattern (default):
    include('Axioms/ORD000-0.ax').
    include('Axioms/COMPL000-0.ax').
    include('Axioms/AXIS000-0.ax').

ODRL634 additionally includes SUBS000-0.ax for axis_subsumes.

Problem overview:
  ODRL630 -- completion_compat: V in [InfD,SupD] => completion_compatible   Theorem
  ODRL631 -- completion_conflict: U<V in domain => completion_conflict      Theorem
  ODRL632 -- sharpness_compat: completion yields Compatible                 Theorem
  ODRL633 -- sharpness_conflict: completion yields Conflict                 Theorem
  ODRL634 -- monotone_conflict (Prop 6.9): subsumes + conflict => conflict  Theorem
  ODRL635 -- unknown_sound: box_verdict(compatible, unknown) = unknown      Theorem
  ODRL636 -- completion_compat at boundary: V=InfD works for eq             Theorem
  ODRL637 -- completion_conflict requires U<V strictly                      Theorem

Change log (v1.1):
  - ODRL630 SMT: was (assert P)(assert Q)(assert (not (and P Q))) propositional
                 tautology.  Now a membership test at v=600 in [0, 1200].
  - ODRL631 SMT: was (assert (< u v))(assert (not (< u v))) propositional
                 tautology.  Now policy-level disjointness [0,400] vs [800,inf).
  - ODRL632 SMT: same tautology pattern as 630.  Now membership at v=400.
  - ODRL633 SMT: same tautology pattern as 631.  Now policy-level disjointness.
  - ODRL634 FOF: was a ground axis_conflict claim, mislabeled "monotonicity".
                 Now tests Prop 6.9 monotonicity: subsumes + conflict => conflict.
                 Adds SUBS000-0.ax to includes for axis_subsumes/4.
  - ODRL637 FOF: was a vacuous universal collapsing to plain irreflexivity.
                 Now tests ~completion_conflict(v600, v600, v0, v1200) directly,
                 i.e., the strictness requirement of completion_conflict.
"""

# Real UF SMT encoding for ODRL635 (box_verdict verdict-algebra)
from smt_axioms import (
    PREAMBLE_VERDICT, DECL_BOX_VERDICT, AXIOM_BOX_UNKNOWN,
)

PROBLEMS = [

    # =====================================================================
    # ODRL630 -- completion_compat: V in domain => completion_compatible
    # SMT v1.1: tautology removed; now membership test at v=600 in [0,1200].
    # =====================================================================
    {
        "id":            "ODRL630",
        "subdir":        "Completion",
        "name":          "completion_compat: value in domain gives compatible completion",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "def:completion: leq(v0,v600) & leq(v600,v1200)\n"
            "=> completion_compatible(v600, v0, v1200).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# Compatible completion: add (eq 600) to BOTH policies (Thm 6.10).
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "completion_compatible(v600, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const v Real)",
        "smt2_asserts": """\
; Membership at the specific witness v=600 (verified semantic by substitution:
; flipping v to 2000 makes this sat).
(assert (= v 600.0))
(assert (not (and (>= v 0.0) (<= v 1200.0))))
""",
    },

    # =====================================================================
    # ODRL631 -- completion_conflict: U<V in domain => completion_conflict
    # SMT v1.1: tautology removed; now policy-level disjointness encoding.
    # The (lteq 400) policy after completion has denotation [0, 400]; the
    # (gteq 800) policy has denotation [800, infinity).  No x is in both.
    # =====================================================================
    {
        "id":            "ODRL631",
        "subdir":        "Completion",
        "name":          "completion_conflict: U<V in domain gives conflict completion",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "def:completion: less(v400,v800) & both in [v0,v1200]\n"
            "=> completion_conflict(v400, v800, v0, v1200).\n"
            "Policy1 gets lteq v400, Policy2 gets gteq v800 => disjoint.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# Conflict completion: lteq 400 to policy A, gteq 800 to policy B (Thm 6.10).
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v400,  axiom, val(v400)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v400,    axiom, less(v0, v400)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v400, v800, v1200)).
""",
        "fof_conjecture": "completion_conflict(v400, v800, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
; Policy-level disjointness: [0, 400] and [800, infinity) share no point.
(assert (>= x 0.0))
(assert (<= x 400.0))
(assert (>= x 800.0))
""",
    },

    # =====================================================================
    # ODRL632 -- sharpness_compat: completion_compatible at v=v400
    # SMT v1.1: tautology removed; now membership test at v=400.
    # =====================================================================
    {
        "id":            "ODRL632",
        "subdir":        "Completion",
        "name":          "sharpness_compat: U<V in domain implies compatible completion exists",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:unknown-sound sharpness_compat:\n"
            "leq(v0,v400) & less(v400,v800) & leq(v800,v1200)\n"
            "=> completion_compatible(v400, v0, v1200).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# Compatible completion (sharpness witness): add (eq 400) to BOTH policies.
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "400"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "400"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v400,  axiom, val(v400)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v400,    axiom, less(v0, v400)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v400, v800, v1200)).
""",
        "fof_conjecture": "completion_compatible(v400, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const v Real)",
        "smt2_asserts": """\
; Membership at the specific witness v=400 (verified semantic by substitution:
; flipping v to -50 makes this sat).
(assert (= v 400.0))
(assert (not (and (>= v 0.0) (<= v 1200.0))))
""",
    },

    # =====================================================================
    # ODRL633 -- sharpness_conflict: completion_conflict at (v400, v800)
    # SMT v1.1: tautology removed; same policy-level disjointness as ODRL631.
    # =====================================================================
    {
        "id":            "ODRL633",
        "subdir":        "Completion",
        "name":          "sharpness_conflict: U<V in domain implies conflict completion exists",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:unknown-sound sharpness_conflict:\n"
            "leq(v0,v400) & less(v400,v800) & leq(v800,v1200)\n"
            "=> completion_conflict(v400, v800, v0, v1200).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v400,  axiom, val(v400)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v400,    axiom, less(v0, v400)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v400, v800, v1200)).
""",
        "fof_conjecture": "completion_conflict(v400, v800, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
; Policy-level disjointness: [0, 400] and [800, infinity) share no point.
(assert (>= x 0.0))
(assert (<= x 400.0))
(assert (>= x 800.0))
""",
    },

    # =====================================================================
    # ODRL634 -- monotone_conflict (Prop 6.9)
    # FOF v1.1: was a ground axis_conflict claim mislabeled as monotonicity.
    # Now tests the actual monotonicity theorem:
    #   axis_subsumes(A1, A2) & axis_conflict(A2, B) => axis_conflict(A1, B).
    # With A1=[v200,v400], A2=[v0,v600], B=[v800,v1200]:
    #   premise 1: axis_subsumes(v200,v400, v0,v600)  -- [v200,v400] in [v0,v600]
    #   premise 2: axis_conflict(v0,v600, v800,v1200) -- via less(v600, v800)
    #   conclude:  axis_conflict(v200,v400, v800,v1200) -- via less(v400, v800)
    # Adds SUBS000-0.ax to includes for axis_subsumes/4.
    # NOTE: requires SUBS000-0.ax to define axis_subsumes biconditionally.
    # =====================================================================
    {
        "id":            "ODRL634",
        "subdir":        "Completion",
        "name":          "monotone_conflict (Prop 6.9): subsumes & conflict implies conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes": [
            "ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax", "SUBS000-0.ax"
        ],
        "needs_density": False,
        "description": (
            "prop:monotone Prop 6.9:\n"
            "  axis_subsumes(A1, A2) & axis_conflict(A2, B) => axis_conflict(A1, B).\n"
            "Instance: A1=[v200,v400], A2=[v0,v600], B=[v800,v1200].\n"
            "[v200,v400] is contained in [v0,v600]; [v0,v600] conflicts [v800,v1200];\n"
            "therefore [v200,v400] conflicts [v800,v1200].\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v200,  axiom, val(v200)).
fof(val_v400,  axiom, val(v400)).
fof(val_v600,  axiom, val(v600)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v200,    axiom, less(v0, v200)).
fof(ord_v0_v400,    axiom, less(v0, v400)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v200_v400,  axiom, less(v200, v400)).
fof(ord_v200_v600,  axiom, less(v200, v600)).
fof(ord_v200_v800,  axiom, less(v200, v800)).
fof(ord_v400_v600,  axiom, less(v400, v600)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600, v800, v1200)).
""",
        "fof_conjecture": (
            "(axis_subsumes(v200, v400, v0, v600)"
            " & axis_conflict(v0, v600, v800, v1200))"
            " => axis_conflict(v200, v400, v800, v1200)"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
; Inner interval [200, 400] and outer-conflict witness [800, infinity):
; disjoint because 400 < 800.
(assert (>= x 200.0))
(assert (<= x 400.0))
(assert (>= x 800.0))
""",
    },

    # =====================================================================
    # ODRL635 -- unknown_sound: Unknown is correctly assigned
    # (No changes from v1.0; already semantic on both sides.)
    # =====================================================================
    {
        "id":            "ODRL635",
        "subdir":        "Completion",
        "name":          "unknown_sound: box verdict is Unknown when axis unconstrained",
        "relation":      "verdict_algebra",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:unknown-sound: box_verdict(compatible, unknown) = unknown.\n"
            "One axis compatible, one axis unconstrained => Unknown overall.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# Verdict-algebra witness: width-axis compatible (both policies agree),
# depth-axis unknown (policy A constrains it, policy B does not).
# boxV = min(Compatible, Unknown) = Unknown.
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "1500"^^xsd:decimal ],
                    [ odrl:leftOperand oax:absoluteSizeDepth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "50"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "1500"^^xsd:decimal ] ] .""",
        "fof_extra_decls": "",
        "fof_conjecture": "box_verdict(compatible, unknown) = unknown",
        "smt2_logic":   "UF",
        "smt2_decls":   PREAMBLE_VERDICT + DECL_BOX_VERDICT,
        "smt2_asserts": AXIOM_BOX_UNKNOWN + "; Negated conjecture\n"
                        "(assert (not (= (box_verdict compatible unknown) unknown)))",
    },

    # =====================================================================
    # ODRL636 -- completion_compat at InfD (boundary case)
    # (No changes from v1.0; already semantic on both sides.)
    # =====================================================================
    {
        "id":            "ODRL636",
        "subdir":        "Completion",
        "name":          "completion_compat at InfD: V=InfD is valid for eq completion",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "def:completion: V=InfD is in [InfD,SupD] so completion_compatible holds.\n"
            "completion_compatible(v0, v0, v1200) -- infimum as eq value.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# Boundary case: V = InfD = 0, the lowest valid value in the domain.
# Compatible completion adds (eq 0) to BOTH policies.
# Result: UNSAT
# Interpretation:
#   ∄ assignment satisfying both equality and strict precedence
#   U = V ∧ U < V is inconsistent in linear real arithmetic
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "0"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "0"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(distinct, axiom, $distinct(v0, v1200)).
""",
        "fof_conjecture": "completion_compatible(v0, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const v Real)",
        "smt2_asserts": """\
; Boundary case: v=InfD=0 must be in the closed domain [0, 1200].
(assert (= v 0.0))
(assert (not (and (>= v 0.0) (<= v 1200.0))))
""",
    },

    # =====================================================================
    # ODRL637 -- completion_conflict requires strict U<V
    # FOF v1.1: was "![U,V,InfD,SupD]: ~less(U,U)" which collapses to plain
    # irreflexivity (closes from ORD000 alone, never engages COMPL000).
    # Now tests the actual strictness requirement: completion_conflict at
    # U=V must not hold, because completion_conflict_def has less(U,V) as
    # one of its conjuncts and less is irreflexive.
    # =====================================================================
    {
        "id":            "ODRL637",
        "subdir":        "Completion",
        "name":          "completion_conflict requires strict U<V: U=V gives no conflict",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "def:completion: less(U,V) is required -- equal values give no conflict.\n"
            "~completion_conflict(v600, v600, v0, v1200) because ~less(v600,v600).\n"
        ),
"ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# Attempted conflict completion at U = V = 600. The pair (lteq 600, gteq 600)
# leaves the policies overlapping at the shared point 600, so the conflict
# completion does NOT succeed -- this is the strictness witness.
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "~completion_conflict(v600, v600, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const u Real)",
        "smt2_asserts": """\
; Arithmetic embodiment of the strict-less requirement: u cannot be both
; equal to 600 and strictly less than 600.  Mirrors the irreflexivity that
; refutes the middle conjunct of completion_conflict_def at U=V.
; SMT counterpart of the FOL claim ~completion_conflict(v600, v600, v0, v1200).
; By completion_conflict_def, that FOL claim reduces to ~less(v600, v600).
; QF_LRA's built-in irreflexivity of < on the reals gives the same fact:
; u = 600 AND u < 600 is unsat.  The two decision procedures take
; different paths to the same conclusion.
(assert (= u 600.0))
(assert (< u 600.0))
""",
    },
]