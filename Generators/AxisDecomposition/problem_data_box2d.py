"""
problem_data_box2d.py
=====================
Box2D benchmark problems: ODRL320-332 (13 problems).

Category B: Two-axis box verdict aggregation.
Tests def:box-verdict Kleene conjunction and def:box-containment
across width and height axes.
All problems use absoluteSize with D_k = (0, ∞) for both axes.

Verdict algebra (paper: def:box-verdict):
  Rule 1: box_verdict(conflict,   compatible) = conflict
  Rule 2: box_verdict(compatible, compatible) = compatible

Box containment (paper: def:box-containment):
  Compatible: A ⊆ B on all axes
  Conflict:   A ⊄ B on some axis (escape witness exists)

Conjecture structure:
  conflict/Compatible:    ?[X,Y]: (A_w(X) & B_w(X) & A_h(Y) & B_h(Y))
  conflict/Conflict:     ~?[X,Y]: (A_w(X) & B_w(X) & A_h(Y) & B_h(Y))
  subsumption/Compatible: ![X,Y]: (A(X,Y) => B(X,Y))
  subsumption/Conflict:    ?[X,Y]: (A(X,Y) & ~B(X,Y))

Interval predicates (paper: def:interval-denotation, D_k = (0,∞)):
  lteq v → in_lopen(X, v0, v)    encodes (0, v]
  gteq v → leq(v, X)             encodes [v, ∞)
  lt   v → in_open(X, v0, v)     encodes (0, v)
  gt   v → less(v, X)            encodes (v, ∞)
  eq   v → in_closed(X, v, v)    encodes {v}

TTL encoding: explicit odrl:and for AND-composition per ODRL 2.2 §4.3.
  Categories H/I use odrl:or / odrl:xone respectively.

Include pattern:
  Discrete domain : include('Axioms/AXIS000-0.ax').
  Continuous      : include('Axioms/ORD001-0.ax').   ← BEFORE AXIS000
                    include('Axioms/AXIS000-0.ax').

SMT2: two variables x (width), y (height), both Real > 0.
      Comments use ; not %.

TTL prefix: drk: <http://w3id.org/drk/ontology/>
"""

PROBLEMS = [

    # ------------------------------------------------------------------
    # ODRL320 — BSB: width conflict × height compatible → box Conflict
    # Paper: def:box-verdict Rule 1, thm:projection, ex:bsb
    # Width:  (0,600] ∩ [1200,∞) = ∅  Conflict
    # Height: (0,600] ∩ [400,∞)  ≠ ∅  Compatible
    # box_verdict(Conflict, Compatible) = Conflict  [Rule 1]
    # ------------------------------------------------------------------
    {
        "id":            "ODRL320",
        "subdir":        "Box2D",
        "name":          "BSB: width conflict × height compatible → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  lteq 600 → (0,600]   ∩   gteq 1200 → [1200,∞) = ∅  Conflict\n"
            "Height: lteq 600 → (0,600]   ∩   gteq  400 → [400,∞)  ≠ ∅  Compatible\n"
            "box_verdict(Conflict, Compatible) = Conflict  [def:box-verdict Rule 1]\n"
            "Paper running example (BSB scenario, ex:bsb)."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyBSB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyMuseum a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "1200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,         axiom, val(v0)).
fof(val_v400,       axiom, val(v400)).
fof(val_v600,       axiom, val(v600)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v400,    axiom, less(v0,   v400)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v400_v600,  axiom, less(v400, v600)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct,       axiom, $distinct(v0, v400, v600, v1200)).
""",
        "fof_conjecture": (
            "~?[X,Y]: (in_lopen(X, v0, v600) & leq(v1200, X) &\n"
            "           in_lopen(Y, v0, v600) & leq(v400,  Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 1200.0))
(assert (> y 0.0))
(assert (<= y 600.0))
(assert (>= y 400.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL321 — Both axes conflict → box Conflict
    # Paper: def:box-verdict Rule 1
    # Width:  (0,600] ∩ [800,∞) = ∅  Conflict
    # Height: (0,300] ∩ [500,∞) = ∅  Conflict
    # ------------------------------------------------------------------
    {
        "id":            "ODRL321",
        "subdir":        "Box2D",
        "name":          "Both axes conflict → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width:  lteq 600 → (0,600]  ∩  gteq 800 → [800,∞) = ∅  Conflict\n"
            "Height: lteq 300 → (0,300]  ∩  gteq 500 → [500,∞) = ∅  Conflict\n"
            "box_verdict(Conflict, Conflict) = Conflict  [def:box-verdict Rule 1]"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "500"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v300,      axiom, val(v300)).
fof(val_v500,      axiom, val(v500)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct,      axiom, $distinct(v0, v300, v500, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y]: (in_lopen(X, v0, v600) & leq(v800, X) &\n"
            "           in_lopen(Y, v0, v300) & leq(v500, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 800.0))
(assert (> y 0.0))
(assert (<= y 300.0))
(assert (>= y 500.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL322 — Width compatible × height conflict → box Conflict
    # Paper: def:box-verdict Rule 1 (commutativity)
    # Width:  [200,800] ≠ ∅  Compatible
    # Height: (0,300] ∩ [500,∞) = ∅  Conflict
    # ------------------------------------------------------------------
    {
        "id":            "ODRL322",
        "subdir":        "Box2D",
        "name":          "Width compatible × height conflict → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible\n"
            "Height: lteq 300 → (0,300]  ∩  gteq 500 → [500,∞) = ∅               Conflict\n"
            "box_verdict(Compatible, Conflict) = Conflict  [def:box-verdict Rule 1]\n"
            "Tests commutativity: conflict on any axis kills the box."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "500"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v300,      axiom, val(v300)).
fof(val_v500,      axiom, val(v500)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(distinct,      axiom, $distinct(v0, v200, v300, v500, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y]: (in_lopen(X, v0, v800) & leq(v200, X) &\n"
            "           in_lopen(Y, v0, v300) & leq(v500, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 800.0))
(assert (>= x 200.0))
(assert (> y 0.0))
(assert (<= y 300.0))
(assert (>= y 500.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL323 — Both axes compatible → box Compatible
    # Paper: def:box-verdict Rule 2
    # Width:  [200,800] ≠ ∅  Compatible
    # Height: [100,600] ≠ ∅  Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL323",
        "subdir":        "Box2D",
        "name":          "Both axes compatible → box Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width:  lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible\n"
            "Height: lteq 600 → (0,600]  ∩  gteq 100 → [100,∞) = [100,600] ≠ ∅  Compatible\n"
            "box_verdict(Compatible, Compatible) = Compatible  [def:box-verdict Rule 2]\n"
            "Witness: (X=v200, Y=v100)."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v100,      axiom, val(v100)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v100,   axiom, less(v0,   v100)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct,      axiom, $distinct(v0, v100, v200, v600, v800)).
""",
        "fof_conjecture": (
            "?[X,Y]: (in_lopen(X, v0, v800) & leq(v200, X) &\n"
            "          in_lopen(Y, v0, v600) & leq(v100, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 800.0))
(assert (>= x 200.0))
(assert (> y 0.0))
(assert (<= y 600.0))
(assert (>= y 100.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL324 — Width eq inside lteq, height overlap → Compatible
    # Paper: def:box-verdict Rule 2, def:interval-denotation (eq)
    # Width:  {600} ∩ (0,800] = {600} ≠ ∅  Compatible
    # Height: [200,600] ≠ ∅                  Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL324",
        "subdir":        "Box2D",
        "name":          "Width eq inside lteq, height overlap → box Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width:  eq 600  → {600}     ∩  lteq 800 → (0,800] = {600} ≠ ∅  Compatible\n"
            "Height: gteq 200 → [200,∞)  ∩  lteq 600 → (0,600] = [200,600] ≠ ∅  Compatible\n"
            "box_verdict(Compatible, Compatible) = Compatible  [def:box-verdict Rule 2]\n"
            "Witness: (X=v600, Y=v200)."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:eq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct,      axiom, $distinct(v0, v200, v600, v800)).
""",
        "fof_conjecture": (
            "?[X,Y]: (in_closed(X, v600, v600) & in_lopen(X, v0, v800) &\n"
            "          leq(v200, Y) & in_lopen(Y, v0, v600))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 600.0))
(assert (<= x 800.0))
(assert (> y 0.0))
(assert (>= y 200.0))
(assert (<= y 600.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL325 — Both axes touch → single-point box Compatible
    # Paper: def:box-verdict Rule 2, thm:criterion (cc: u=l, not disjoint)
    # Width:  {600} ≠ ∅  Compatible (touching)
    # Height: {400} ≠ ∅  Compatible (touching)
    # ------------------------------------------------------------------
    {
        "id":            "ODRL325",
        "subdir":        "Box2D",
        "name":          "Both axes touch at boundary → single-point box Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  lteq 600 → (0,600]  ∩  gteq 600 → [600,∞) = {600} ≠ ∅  Compatible\n"
            "Height: lteq 400 → (0,400]  ∩  gteq 400 → [400,∞) = {400} ≠ ∅  Compatible\n"
            "box_verdict(Compatible, Compatible) = Compatible  [def:box-verdict Rule 2]\n"
            "Witness: (X=v600, Y=v400). Box intersection is a single point."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v400, v600)).
""",
        "fof_conjecture": (
            "?[X,Y]: (in_lopen(X, v0, v600) & leq(v600, X) &\n"
            "          in_lopen(Y, v0, v400) & leq(v400, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 600.0))
(assert (> y 0.0))
(assert (<= y 400.0))
(assert (>= y 400.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL326 — Width touches (Compatible), height conflicts → box Conflict
    # Paper: def:box-verdict Rule 1
    # Width:  {600} ≠ ∅  Compatible (touching at 600)
    # Height: (0,300] ∩ [500,∞) = ∅  Conflict
    # NOTE: width is Compatible — height conflict kills the box
    # ------------------------------------------------------------------
    {
        "id":            "ODRL326",
        "subdir":        "Box2D",
        "name":          "Width touches (compatible), height conflicts → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  lteq 600 → (0,600]  ∩  gteq 600 → [600,∞) = {600} ≠ ∅  Compatible\n"
            "Height: lteq 300 → (0,300]  ∩  gteq 500 → [500,∞) = ∅           Conflict\n"
            "box_verdict(Compatible, Conflict) = Conflict  [def:box-verdict Rule 1]\n"
            "Width touches at 600 (Compatible) — height conflict kills the box."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "500"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v300,      axiom, val(v300)).
fof(val_v500,      axiom, val(v500)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(distinct,      axiom, $distinct(v0, v300, v500, v600)).
""",
        "fof_conjecture": (
            "~?[X,Y]: (in_lopen(X, v0, v600) & leq(v600, X) &\n"
            "           in_lopen(Y, v0, v300) & leq(v500, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 600.0))
(assert (> y 0.0))
(assert (<= y 300.0))
(assert (>= y 500.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL327 — Both axes open intervals, overlapping → Compatible (density)
    # Paper: def:box-verdict Rule 2, lem:totality, ORD001-0.ax
    # Width:  (200,800) ≠ ∅  Compatible
    # Height: (100,500) ≠ ∅  Compatible
    # Witnesses inside open intervals → requires density
    # INCLUDE ORDER: ORD001 BEFORE AXIS000
    # ------------------------------------------------------------------
    {
        "id":            "ODRL327",
        "subdir":        "Box2D",
        "name":          "Both axes open intervals, overlapping → box Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": True,
        "description": (
            "Width:  gt 200 → (200,∞)  ∩  lt 800 → (0,800) = (200,800) ≠ ∅  Compatible\n"
            "Height: gt 100 → (100,∞)  ∩  lt 500 → (0,500) = (100,500) ≠ ∅  Compatible\n"
            "box_verdict(Compatible, Compatible) = Compatible  [def:box-verdict Rule 2]\n"
            "Both witnesses lie inside open intervals → requires ORD001-0.ax (density)."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "100"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "500"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v100,      axiom, val(v100)).
fof(val_v200,      axiom, val(v200)).
fof(val_v500,      axiom, val(v500)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v100,   axiom, less(v0,   v100)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(distinct,      axiom, $distinct(v0, v100, v200, v500, v800)).
""",
        "fof_conjecture": (
            "?[X,Y]: (less(v200, X) & in_open(X, v0, v800) &\n"
            "          less(v100, Y) & in_open(Y, v0, v500))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (> x 200.0))
(assert (< x 800.0))
(assert (> y 0.0))
(assert (> y 100.0))
(assert (< y 500.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL328 — Width open/closed boundary conflict × height compatible → Conflict
    # Paper: def:box-verdict Rule 1, thm:criterion (oc case)
    # Width:  (0,600) ∩ [600,∞) = ∅  Conflict (oc: X<600 & X≥600)
    # Height: [200,800] ≠ ∅            Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL328",
        "subdir":        "Box2D",
        "name":          "Width open/closed boundary conflict × height compatible → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Hard",
        "needs_density": False,
        "description": (
            "Width:  lt 600  → (0,600)   ∩  gteq 600 → [600,∞) = ∅  Conflict (oc case)\n"
            "Height: lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible\n"
            "box_verdict(Conflict, Compatible) = Conflict  [def:box-verdict Rule 1]\n"
            "Width: order contradiction (X<600 & X≥600), no density needed.\n"
            "Tests open-boundary conflict on one axis kills the box."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct,      axiom, $distinct(v0, v200, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y]: (in_open(X, v0, v600) & leq(v600, X) &\n"
            "           in_lopen(Y, v0, v800) & leq(v200, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (< x 600.0))
(assert (>= x 600.0))
(assert (> y 0.0))
(assert (<= y 800.0))
(assert (>= y 200.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL329 — Narrow width strip × wide height → Compatible
    # Paper: def:box-verdict Rule 2
    # Width:  [500,510] ≠ ∅  Compatible
    # Height: [100,900] ≠ ∅  Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL329",
        "subdir":        "Box2D",
        "name":          "Narrow width strip × wide height → box Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width:  gteq 500 → [500,∞)  ∩  lteq 510 → (0,510] = [500,510] ≠ ∅  Compatible\n"
            "Height: gteq 100 → [100,∞)  ∩  lteq 900 → (0,900] = [100,900] ≠ ∅  Compatible\n"
            "box_verdict(Compatible, Compatible) = Compatible  [def:box-verdict Rule 2]\n"
            "Witnesses: (X=v500, Y=v100). Tests narrow but non-empty intersection."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "500"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "510"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "900"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v100,      axiom, val(v100)).
fof(val_v500,      axiom, val(v500)).
fof(val_v510,      axiom, val(v510)).
fof(val_v900,      axiom, val(v900)).
fof(ord_v0_v100,   axiom, less(v0,   v100)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v510,   axiom, less(v0,   v510)).
fof(ord_v0_v900,   axiom, less(v0,   v900)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v510, axiom, less(v100, v510)).
fof(ord_v100_v900, axiom, less(v100, v900)).
fof(ord_v500_v510, axiom, less(v500, v510)).
fof(ord_v500_v900, axiom, less(v500, v900)).
fof(ord_v510_v900, axiom, less(v510, v900)).
fof(distinct,      axiom, $distinct(v0, v100, v500, v510, v900)).
""",
        "fof_conjecture": (
            "?[X,Y]: (leq(v500, X) & in_lopen(X, v0, v510) &\n"
            "          leq(v100, Y) & in_lopen(Y, v0, v900))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (>= x 500.0))
(assert (<= x 510.0))
(assert (> y 0.0))
(assert (>= y 100.0))
(assert (<= y 900.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL330 — Width near-miss (gap=1) × height compatible → Conflict
    # Paper: def:box-verdict Rule 1, thm:criterion (cc: 599 < 601)
    # Width:  (0,599] ∩ [601,∞) = ∅  Conflict
    # Height: [200,800] ≠ ∅            Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL330",
        "subdir":        "Box2D",
        "name":          "Width near-miss (gap=1) × height compatible → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  lteq 599 → (0,599]  ∩  gteq 601 → [601,∞) = ∅  Conflict\n"
            "        cc case: u1=599 closed, l2=601 closed, 599 < 601 → disjoint\n"
            "Height: lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible\n"
            "box_verdict(Conflict, Compatible) = Conflict  [def:box-verdict Rule 1]\n"
            "Tests gap of 1 unit on width kills the box."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "599"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "601"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,         axiom, val(v0)).
fof(val_v200,       axiom, val(v200)).
fof(val_v599,       axiom, val(v599)).
fof(val_v601,       axiom, val(v601)).
fof(val_v800,       axiom, val(v800)).
fof(ord_v0_v200,    axiom, less(v0,   v200)).
fof(ord_v0_v599,    axiom, less(v0,   v599)).
fof(ord_v0_v601,    axiom, less(v0,   v601)).
fof(ord_v0_v800,    axiom, less(v0,   v800)).
fof(ord_v200_v599,  axiom, less(v200, v599)).
fof(ord_v200_v601,  axiom, less(v200, v601)).
fof(ord_v200_v800,  axiom, less(v200, v800)).
fof(ord_v599_v601,  axiom, less(v599, v601)).
fof(ord_v599_v800,  axiom, less(v599, v800)).
fof(ord_v601_v800,  axiom, less(v601, v800)).
fof(distinct,       axiom, $distinct(v0, v200, v599, v601, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y]: (in_lopen(X, v0, v599) & leq(v601, X) &\n"
            "           in_lopen(Y, v0, v800) & leq(v200, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 599.0))
(assert (>= x 601.0))
(assert (> y 0.0))
(assert (<= y 800.0))
(assert (>= y 200.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL331 — 2D box subsumption: both axes A ⊆ B → Compatible
    # Paper: def:box-containment (Compatible case)
    # Width:  (0,600]  ⊆ (0,1200]
    # Height: (0,400]  ⊆ (0,800]
    # FOF: ∀X,Y. (A_w(X) & A_h(Y)) → (B_w(X) & B_h(Y))
    # SMT: ∄(x,y). x∈A_w & y∈A_h & (x∉B_w | y∉B_h) → unsat
    # ------------------------------------------------------------------
    {
        "id":            "ODRL331",
        "subdir":        "Box2D",
        "name":          "2D box A ⊆ B on both axes → Compatible",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width:  lteq 600  → (0,600]  ⊆  (0,1200] ← lteq 1200  Compatible\n"
            "Height: lteq 400  → (0,400]  ⊆  (0,800]  ← lteq 800   Compatible\n"
            "box_containment: A ⊆ B on all axes → Compatible  [def:box-containment]\n"
            "SMT: no escape witness in either axis → unsat."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "1200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,         axiom, val(v0)).
fof(val_v400,       axiom, val(v400)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v400,    axiom, less(v0,   v400)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v800,    axiom, less(v0,   v800)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v400_v600,  axiom, less(v400, v600)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct,       axiom, $distinct(v0, v400, v600, v800, v1200)).
""",
        "fof_conjecture": (
            "![X,Y]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400)) =>\n"
            "          (in_lopen(X, v0, v1200) & in_lopen(Y, v0, v800)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (> y 0.0))
(assert (<= y 400.0))
(assert (not (and (<= x 1200.0) (<= y 800.0))))""",
    },

    # ------------------------------------------------------------------
    # ODRL332 — 2D box subsumption: width A ⊄ B → Conflict
    # Paper: def:box-containment (Conflict case)
    # Width:  (0,1200] ⊄ (0,600]  escape witness X=v800
    # Height: (0,800]  ⊆ (0,1200] (compatible axis does not save it)
    # FOF: ∃X,Y. (A_w(X) & A_h(Y)) & ~(B_w(X) & B_h(Y))
    # SMT: find escape witness → sat
    # ------------------------------------------------------------------
    {
        "id":            "ODRL332",
        "subdir":        "Box2D",
        "name":          "2D box A ⊄ B on width axis → Conflict",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width:  lteq 1200 → (0,1200] ⊄ (0,600] ← lteq 600  Conflict\n"
            "        Escape witness: X=v800 ∈ (0,1200] but v800 ∉ (0,600]\n"
            "Height: lteq 800  → (0,800]  ⊆ (0,1200] ← lteq 1200 Compatible\n"
            "box_containment: width escape → Conflict  [def:box-containment]\n"
            "SMT: escape witness (x=800, any y∈A_h) → sat."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "1200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "1200"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v800,    axiom, less(v0,   v800)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v800, v1200)).
""",
        "fof_conjecture": (
            "?[X,Y]: ((in_lopen(X, v0, v1200) & in_lopen(Y, v0, v800)) &\n"
            "          ~(in_lopen(X, v0, v600) & in_lopen(Y, v0, v1200)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 1200.0))
(assert (> y 0.0))
(assert (<= y 800.0))
(assert (not (and (<= x 600.0) (<= y 1200.0))))""",
    },

]


PROBLEMS_EXT = [

    # ------------------------------------------------------------------
    # ODRL333 — prop:monotone directly  [Proposition 4.22]
    # Paper: prop:monotone, lem:conflict-propagation, Section B predicates
    # [200,600] ⊆ [0,800]  (axis_subsumes — narrower contained in wider)
    # [0,800] ∩ [900,1200] = ∅  (axis_conflict — wider already conflicts)
    # Therefore: [200,600] ∩ [900,1200] = ∅  (monotone propagation)
    # Uses axis_subsumes/4 and axis_conflict/4 from AXIS000-0.ax Section B
    # No new axioms needed.
    # ------------------------------------------------------------------
    {
        "id":            "ODRL333",
        "subdir":        "Box2D",
        "name":          "prop:monotone: narrowing an axis propagates Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "axis_subsumes(v200,v600, v0,v800):  [200,600] ⊆ [0,800]\n"
            "axis_conflict(v0,v800, v900,v1200): [0,800] ∩ [900,1200] = ∅\n"
            "Therefore: axis_conflict(v200,v600, v900,v1200)  [prop:monotone]\n"
            "Tests Section B predicates directly. No geometry primitives."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "900"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "1200"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,          axiom, val(v0)).
fof(val_v200,        axiom, val(v200)).
fof(val_v600,        axiom, val(v600)).
fof(val_v800,        axiom, val(v800)).
fof(val_v900,        axiom, val(v900)).
fof(val_v1200,       axiom, val(v1200)).
fof(ord_v0_v200,     axiom, less(v0,   v200)).
fof(ord_v0_v600,     axiom, less(v0,   v600)).
fof(ord_v0_v800,     axiom, less(v0,   v800)).
fof(ord_v0_v900,     axiom, less(v0,   v900)).
fof(ord_v0_v1200,    axiom, less(v0,   v1200)).
fof(ord_v200_v600,   axiom, less(v200, v600)).
fof(ord_v200_v800,   axiom, less(v200, v800)).
fof(ord_v200_v900,   axiom, less(v200, v900)).
fof(ord_v200_v1200,  axiom, less(v200, v1200)).
fof(ord_v600_v800,   axiom, less(v600, v800)).
fof(ord_v600_v900,   axiom, less(v600, v900)).
fof(ord_v600_v1200,  axiom, less(v600, v1200)).
fof(ord_v800_v900,   axiom, less(v800, v900)).
fof(ord_v800_v1200,  axiom, less(v800, v1200)).
fof(ord_v900_v1200,  axiom, less(v900, v1200)).
fof(distinct, axiom, $distinct(v0, v200, v600, v800, v900, v1200)).
""",
        "fof_conjecture": (
            "(axis_subsumes(v200, v600, v0, v800) &\n"
            "  axis_conflict(v0, v800, v900, v1200))\n"
            "=> axis_conflict(v200, v600, v900, v1200)"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
; Negation of conclusion: x in [200,600] AND x in [900,1200]
(assert (>= x 200.0))
(assert (<= x 600.0))
(assert (>= x 900.0))
(assert (<= x 1200.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL334 — box_verdict called directly: genuine Kleene Rule 1
    # Paper: def:box-verdict Rule 1
    # Forces Vampire to use Section D axioms, not interval arithmetic.
    # No ordering constants needed — tests the verdict algebra directly.
    # box_verdict(conflict, compatible) = conflict  [def:box-verdict Rule 1]
    # SMT2: Kleene encoding — conflict=0.0, compatible=2.0, min=box_verdict
    # ------------------------------------------------------------------
    {
        "id":            "ODRL334",
        "subdir":        "Box2D",
        "name":          "box_verdict(conflict, compatible) = conflict: Kleene Rule 1 direct",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "box_verdict(conflict, compatible) = conflict  [def:box-verdict Rule 1]\n"
            "Forces Vampire to fire Section D axiom box_conflict directly.\n"
            "No ordering constants needed — pure verdict algebra test.\n"
            "SMT2: Kleene min encoding — min(0,2)=0 → negation unsat."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": "",
        "fof_conjecture": "box_verdict(conflict, compatible) = conflict",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "",
        "smt2_asserts": """\
; Kleene ordering: conflict=0.0 < unknown=1.0 < compatible=2.0
; box_verdict(V1,V2) = min(V1,V2) under this ordering
; Negation: min(conflict=0.0, compatible=2.0) != conflict=0.0
(assert (not (= (ite (<= 0.0 2.0) 0.0 2.0) 0.0)))""",
    },

]

PROBLEMS = PROBLEMS + PROBLEMS_EXT