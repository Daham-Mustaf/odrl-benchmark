"""
problem_data_proj.py
====================
Projection benchmark problems: ODRL620-629 (10 problems).
Category M: Tests thm:projection and thm:aabb from PROJ000-0.ax.
Include pattern:
    include('Axioms/ORD000-0.ax').
    include('Axioms/PROJ000-0.ax').
    include('Axioms/AXIS000-0.ax').
    [include('Axioms/ORD001-0.ax').]  <- added by generator when needs_density=True

Problem overview:
  ODRL620 — 2D point in box2                           Theorem
  ODRL621 — 2D point outside box2 (axis 1 miss)        Theorem
  ODRL622 — 3D point in box3                           Theorem
  ODRL623 — 3D point outside box3 (axis 2 miss)        Theorem
  ODRL624 — box2_compatible: both axes overlap          Theorem
  ODRL625 — box2_conflict: one axis disjoint            Theorem
  ODRL626 — shape_point: X in [v,v] iff X=v            Theorem
  ODRL627 — shape_ropen: X in [InfD,V)                 Theorem
  ODRL628 — shape_open: X in (L,U)  [needs ORD001]     Theorem
  ODRL629 — shape_closed: unconstrained axis            Theorem

Fixes vs. original:
  ODRL627: name updated from "shape_lray_open" to "shape_ropen" to match
           the renamed axiom in PROJ000-0.ax v1.2.
  ODRL628: relation corrected from "compatible" to "conflict" for
           consistency with all other problems in this file.
           Note: needs_density=True; the generator must include
           ORD001-0.ax for this problem's .p file.
  ODRL629: name updated from "shape_full" to "shape_closed" to match
           the renamed axiom in PROJ000-0.ax v1.2.
           status_smt corrected from "sat" to "unsat"; the previous
           SMT just showed the domain is non-empty (unrelated to the
           conjecture). Replaced with negated-conjecture encoding:
           assert (0<=x<=1200) + assert NOT(0<=x<=1200) -> UNSAT,
           which correctly tests the universal FOF claim.
"""

PROBLEMS = [
    # ─────────────────────────────────────────────────────────────────
    # ODRL620 — 2D point in box2
    # ─────────────────────────────────────────────────────────────────
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

    # ─────────────────────────────────────────────────────────────────
    # ODRL621 — 2D point outside box2 (axis 1 miss)
    # ─────────────────────────────────────────────────────────────────
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

    # ─────────────────────────────────────────────────────────────────
    # ODRL622 — 3D point in box3
    # ─────────────────────────────────────────────────────────────────
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

    # ─────────────────────────────────────────────────────────────────
    # ODRL623 — 3D point outside box3 (axis 2 miss)
    # ─────────────────────────────────────────────────────────────────
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

    # ─────────────────────────────────────────────────────────────────
    # ODRL624 — box2_compatible: both axes overlap
    # ─────────────────────────────────────────────────────────────────
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
            "Both axes overlap: width [v0,v600]∩[v400,v800]=[v400,v600] != empty.\n"
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

    # ─────────────────────────────────────────────────────────────────
    # ODRL625 — box2_conflict: one axis disjoint kills box
    # ─────────────────────────────────────────────────────────────────
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
            "Width: [v0,v400]∩[v600,v800]=empty => box2_conflict.\n"
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

    # ─────────────────────────────────────────────────────────────────
    # ODRL626 — shape_point: in_closed(X,V,V) iff X=V
    # ─────────────────────────────────────────────────────────────────
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
        "smt2_asserts": """\
(assert (= x 600.0))
(assert (not (= x 600.0)))""",
    },

    # ─────────────────────────────────────────────────────────────────
    # ODRL627 — shape_ropen: in_ropen(X,InfD,V)
    #
    # FIX: name updated from "shape_lray_open" to "shape_ropen" to match
    #      the renamed axiom in PROJ000-0.ax v1.2.
    # ─────────────────────────────────────────────────────────────────
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

    # ─────────────────────────────────────────────────────────────────
    # ODRL628 — shape_open: in_open(X,L,U)
    #
    # FIX: relation corrected from "compatible" to "conflict" for
    #      consistency with all other problems in this file.
    # NOTE: needs_density=True — the generator must include ORD001-0.ax
    #       for this problem's .p file.  Without the density axiom,
    #       ?[X]: in_open(X,v400,v600) is unprovable (no FOL axiom
    #       guarantees a point strictly between v400 and v600 exists).
    # ─────────────────────────────────────────────────────────────────
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
            "Witness must be strictly between v400 and v600 — requires ORD001 density.\n"
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

    # ─────────────────────────────────────────────────────────────────
    # ODRL629 — shape_closed: unconstrained axis = full domain
    #
    # FIX 1: name updated from "shape_full" to "shape_closed" to match
    #        the renamed axiom in PROJ000-0.ax v1.2 (shape_full was
    #        removed as a duplicate; its content is now shape_closed).
    # FIX 2: status_smt corrected from "sat" to "unsat".
    #        The previous SMT just asserted (>= x 0) and (<= x 1200),
    #        showing only that the domain is non-empty — it did not test
    #        the FOF conjecture at all.
    #        The FOF conjecture is universal: ![X]: (0<=X<=1200) =>
    #        in_closed(X,v0,v1200).  The negated conjecture is:
    #        exists X: (0<=X<=1200) & NOT in_closed(X,v0,v1200)
    #        = exists X: (0<=X<=1200) & (X<0 | X>1200) -> UNSAT.
    # ─────────────────────────────────────────────────────────────────
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
        # Negated conjecture: exists X in [0,1200] that is NOT in in_closed(X,0,1200)
        # = exists X: (0<=X<=1200) & (X<0 | X>1200) -> UNSAT.
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0))
(assert (<= x 1200.0))
(assert (or (< x 0.0) (> x 1200.0)))""",
    },
]