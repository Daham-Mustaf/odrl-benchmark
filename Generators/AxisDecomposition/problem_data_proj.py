"""
problem_data_proj.py
====================
Projection benchmark problems: ODRL620-629 (10 problems).
Category: Projection (paper Def. 14 Box Denotation, Thm. 17 Projection).
Include pattern:
    include('Axioms/ORD000-0.ax').
    include('Axioms/PROJ000-0.ax').
    include('Axioms/AXIS000-0.ax').
    [include('Axioms/ORD001-0.ax').]  <- added by generator when needs_density=True

Problem overview:
  ODRL620 -- 2D point in box2                           Theorem
  ODRL621 -- 2D point outside box2 (axis 1 miss)        Theorem
  ODRL622 -- 3D point in box3                           Theorem
  ODRL623 -- 3D point outside box3 (axis 2 miss)        Theorem
  ODRL624 -- box2_compatible: both axes overlap         Theorem
  ODRL625 -- box2_conflict: one axis disjoint           Theorem
  ODRL626 -- shape_point: X in [v,v] iff X=v            Theorem
  ODRL627 -- shape_ropen: X in [InfD,V)                 Theorem
  ODRL628 -- shape_open: X in (L,U)  [needs ORD001]     Theorem
  ODRL629 -- shape_closed: unconstrained axis           Theorem

Change log (v1.1):
  - PROJ000-0.ax rewritten to define in_box2/6, in_box3/9,
    box2_compatible/8, box2_conflict/8 as biconditionals.  Previously
    PROJ000 defined box_member/box_member3, neither used by any problem
    here, while in_box2/in_box3/box2_compatible/box2_conflict were
    undeclared.  ODRL620-625 returned CounterSatisfiable under v1.0;
    they close under v1.1.
  - ODRL626 SMT replaced.  Original was (= x 600) AND (not (= x 600))
    which is P AND NOT P at value 600 (propositionally tautological).
    New SMT pins witness at v400 and asserts in_closed(v400, v600, v600)
    -- semantic: unsat because 400 != 600, sat if witness changed to 600
    or singleton bound changed to 400.  This actually tests the
    conjecture's interesting part (v400 NOT in {v600}).
  - ODRL628 needs_density=True; the generator must include ORD001-0.ax
    so ?[X]: in_open(X, v400, v600) is provable.  Z3 may time out on
    this case (existential under density axiom); Vampire and E should
    close it.
  - ODRL629 SMT note: the user-supplied (x in D) AND (x NOT in D)
    encoding is structurally tautological but encoding-correct for a
    universal claim that reduces to P => P after biconditional
    unfolding.  Same disposition as ODRL637 in Completion (kept) vs
    ODRL617 in WF (dropped).  Kept here since the user explicitly chose
    this design.
"""

PROBLEMS = [
    # =================================================================
    # ODRL620 -- 2D point in box2 -> Theorem (Compatible verdict)
    # FOL: closes via in_box2_def + in_closed_def + ord chain.
    # SMT: pin (x=300, y=400), negate box test; unsat because (300, 400)
    #      IS in [0,600] x [0,600].
    # =================================================================
    {
        "id":            "ODRL620",
        "subdir":        "Projection",
        "name":          "thm:projection 2D: point inside box2",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:projection: (v300,v400) in [v0,v600]x[v0,v600]\n"
            "iff v300 in [v0,v600] AND v400 in [v0,v600].\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v300,   axiom, less(v0, v300)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v300, v400, v600)).
""",
        "fof_conjecture": "in_box2(v300, v400, v0, v600, v0, v600)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (= x 300.0)) (assert (= y 400.0))
(assert (not (and (>= x 0.0) (<= x 600.0) (>= y 0.0) (<= y 600.0))))""",
    },

    # =================================================================
    # ODRL621 -- 2D point outside box2 -> Theorem (Conflict verdict)
    # FOL: closes via in_box2_def + in_closed_def + ord chain.
    # SMT: pin (x=800, y=400), assert box test; unsat because 800 > 600.
    # =================================================================
    {
        "id":            "ODRL621",
        "subdir":        "Projection",
        "name":          "thm:projection 2D: point outside box2 on axis 1",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:projection: v800 NOT in [v0,v600] => (v800,v400) NOT in box2.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v400, v600, v800)).
""",
        "fof_conjecture": "~in_box2(v800, v400, v0, v600, v0, v600)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (= x 800.0)) (assert (= y 400.0))
(assert (and (>= x 0.0) (<= x 600.0) (>= y 0.0) (<= y 600.0)))""",
    },

    # =================================================================
    # ODRL622 -- 3D point in box3 -> Theorem (Compatible verdict)
    # =================================================================
    {
        "id":            "ODRL622",
        "subdir":        "Projection",
        "name":          "thm:projection 3D: point inside box3",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:projection: (v300,v400,v200) in [v0,v600]^3.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeDepth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0, v200)).
fof(ord_v0_v300,   axiom, less(v0, v300)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v200, v300, v400, v600)).
""",
        "fof_conjecture": "in_box3(v300, v400, v200, v0, v600, v0, v600, v0, v600)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (= x 300.0)) (assert (= y 400.0)) (assert (= z 200.0))
(assert (not (and (>= x 0.0) (<= x 600.0)
                  (>= y 0.0) (<= y 600.0)
                  (>= z 0.0) (<= z 600.0))))""",
    },

    # =================================================================
    # ODRL623 -- 3D point outside box3 -> Theorem (Conflict verdict)
    # =================================================================
    {
        "id":            "ODRL623",
        "subdir":        "Projection",
        "name":          "thm:projection 3D: point outside box3 on axis 2",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:projection: v800 NOT in [v0,v600] on axis 2\n"
            "=> (v300,v800,v200) NOT in box3.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeDepth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200,   axiom, less(v0, v200)).
fof(ord_v0_v300,   axiom, less(v0, v300)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v200, v300, v600, v800)).
""",
        "fof_conjecture": "~in_box3(v300, v800, v200, v0, v600, v0, v600, v0, v600)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (= x 300.0)) (assert (= y 800.0)) (assert (= z 200.0))
(assert (and (>= x 0.0) (<= x 600.0)
             (>= y 0.0) (<= y 600.0)
             (>= z 0.0) (<= z 600.0)))""",
    },

    # =================================================================
    # ODRL624 -- box2_compatible: both axes overlap -> Theorem
    # FOL: closes via box2_compatible_def (4-clause leq conjunction).
    # SMT: existential test -- find (x, y) in both boxes.
    # =================================================================
    {
        "id":            "ODRL624",
        "subdir":        "Projection",
        "name":          "box2_compatible: both axes overlap",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "def:box-verdict: [v0,v600]x[v0,v600] compatible with [v400,v800]x[v400,v800]\n"
            "Both axes overlap: width [v0,v600] intersect [v400,v800] = [v400,v600] non-empty.\n"
        ),
        "ttl": """\
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
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
    ) ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:gteq ; odrl:rightOperand "400"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:gteq ; odrl:rightOperand "400"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v400, v600, v800)).
""",
        "fof_conjecture": "box2_compatible(v0, v600, v0, v600, v400, v800, v400, v800)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (>= x 0.0)) (assert (<= x 600.0))
(assert (>= y 0.0)) (assert (<= y 600.0))
(assert (>= x 400.0)) (assert (>= y 400.0))""",
    },

    # =================================================================
    # ODRL625 -- box2_conflict: one axis disjoint -> Theorem
    # FOL: closes via box2_conflict_def disjunction; width gap satisfied.
    # SMT: x in [0,400] AND x >= 600 -- empty since 400 < 600.
    # =================================================================
    {
        "id":            "ODRL625",
        "subdir":        "Projection",
        "name":          "box2_conflict: axis 1 disjoint kills box",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "def:box-verdict: [v0,v400]x[v0,v600] conflict with [v600,v800]x[v0,v600]\n"
            "Width: [v0,v400] intersect [v600,v800] = empty => box2_conflict.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
    ) ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v400, v600, v800)).
""",
        "fof_conjecture": "box2_conflict(v0, v400, v0, v600, v600, v800, v0, v600)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (>= x 0.0)) (assert (<= x 400.0))
(assert (>= x 600.0))""",
    },

    # =================================================================
    # ODRL626 -- shape_point: in_closed(X,V,V) iff X=V -> Theorem
    #
    # v1.1: SMT replaced.  Original was (= x 600) AND (not (= x 600)),
    # which is P AND NOT P at value 600 -- propositionally tautological
    # and doesn't test the claim's interesting part (v400 NOT in {v600}).
    # New SMT pins witness at v400 and asserts in_closed(v400, v600, v600);
    # unsat because 400 != 600.  Substitution test: witness=600 -> sat,
    # singleton bound 600->400 -> sat.  Now semantically load-bearing.
    # =================================================================
    {
        "id":            "ODRL626",
        "subdir":        "Projection",
        "name":          "thm:aabb shape_point: in_closed(X,V,V) iff X=V",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:aabb shape 1: point interval [v600,v600] contains only v600.\n"
            "in_closed(v600,v600,v600) holds; in_closed(v400,v600,v600) does not.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v400, v600)).
""",
        "fof_conjecture": (
            "in_closed(v600, v600, v600) & ~in_closed(v400, v600, v600)"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        # Pin witness at v400; assert in_closed(v400, v600, v600).
        # 400 in [600, 600] requires 400 = 600 -- unsat.
        "smt2_asserts": """\
(assert (= x 400.0))
(assert (and (>= x 600.0) (<= x 600.0)))""",
    },

    # =================================================================
    # ODRL627 -- shape_ropen: in_ropen(X,v0,v600) -> Theorem
    # FOL: closes via in_ropen_def (leq + less) + ord chain.
    # SMT: x in [0, 600) -- sat at e.g. x=300.
    # =================================================================
    {
        "id":            "ODRL627",
        "subdir":        "Projection",
        "name":          "thm:aabb shape_ropen: in_ropen(X,v0,v600)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:aabb shape_ropen (canonical shape 4): right-open left ray [v0,v600).\n"
            "v400 in [v0,v600); v600 NOT in [v0,v600).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v400, v600)).
""",
        "fof_conjecture": (
            "in_ropen(v400, v0, v600) & ~in_ropen(v600, v0, v600)"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0)) (assert (< x 600.0))""",
    },

    # =================================================================
    # ODRL628 -- shape_open: ?[X]: in_open(X, v400, v600) -> Theorem
    #
    # needs_density=True: generator must include ORD001-0.ax.  Without
    # density, no witness can be constructed from the finite ord chain.
    # Z3 may time out on this case (existential under quantified density);
    # Vampire and E should close it.
    # =================================================================
    {
        "id":            "ODRL628",
        "subdir":        "Projection",
        "name":          "thm:aabb shape_open: in_open(X,v400,v600)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": True,
        "description": (
            "thm:aabb shape_open (shape 9): open bounded (v400,v600).\n"
            "Witness must be strictly between v400 and v600 -- requires ORD001 density.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:gt ; odrl:rightOperand "400"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lt ; odrl:rightOperand "600"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v400, v600)).
""",
        "fof_conjecture": "?[X]: in_open(X, v400, v600)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 400.0)) (assert (< x 600.0))""",
    },

    # =================================================================
    # ODRL629 -- shape_closed: unconstrained axis = full domain -> Theorem
    #
    # FOL: universal claim (P => P after biconditional unfolding).
    # SMT note: the encoding (x in D) AND (x NOT in D) is structurally
    # tautological -- the unsat reflects the vacuous nature of the
    # universal claim after definition unfolding.  Same disposition as
    # ODRL637 in Completion (kept) rather than ODRL617 in WF (dropped).
    # =================================================================
    {
        "id":            "ODRL629",
        "subdir":        "Projection",
        "name":          "thm:aabb shape_closed: unconstrained axis is full domain",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:aabb shape_closed (canonical shape 2/10): full domain [v0,v1200].\n"
            "Every value in [v0,v1200] satisfies in_closed(X,v0,v1200).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "0"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": (
            "![X]: ((leq(v0,X) & leq(X,v1200)) => in_closed(X, v0, v1200))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0))
(assert (<= x 1200.0))
(assert (or (< x 0.0) (> x 1200.0)))""",
    },
]