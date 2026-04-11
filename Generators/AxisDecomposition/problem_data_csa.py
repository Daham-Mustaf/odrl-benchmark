"""
problem_data_csa.py
===================
CSA benchmark problems: ODRL700-714 (15 problems).
Category: CSA/
Each problem flips the verdict of an existing THM problem — the
conjecture claims the WRONG verdict, so the problem is CounterSatisfiable.
The prover finds a countermodel showing the wrong verdict is refuted.

Status: CounterSatisfiable for all.
"""

PROBLEMS = [
    # ─────────────────────────────────────────────────────────────────
    # ODRL700 — flip ODRL300: claim compatible (wrong — actually conflict)
    # [v0,v600) and [v800,∞) — claim overlap exists (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL700",
        "subdir":      "CSA",
        "name":        "CSA SingleAxis: claim compatible for disjoint intervals (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "needs_density": False,
        "difficulty":  "Easy",
        "description": (
            "Flip of ODRL300: width lteq 600 vs gteq 800.\n"
            "Intervals (0,600) and [800,∞) are disjoint — Conflict.\n"
            "Wrong claim: ?[X]: overlap exists. Countermodel: no such X.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
""",
        "fof_conjecture": "?[X]: (in_lopen(X,v0,v600) & leq(v800,X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (>= x 800.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL701 — flip ODRL301: eq 600 vs eq 800 — claim compatible (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL701",
        "subdir":      "CSA",
        "name":        "CSA SingleAxis: claim eq values compatible when distinct (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "difficulty":  "Easy",
        "needs_density": False,
        "description": (
            "width eq 600 vs eq 800: {600} ∩ {800} = ∅ — Conflict.\n"
            "Wrong claim: ?[X]: X=v600 & X=v800. Countermodel: v600≠v800.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v600, v800)).
""",
        "fof_conjecture": "?[X]: (in_closed(X,v600,v600) & in_closed(X,v800,v800))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (= x 600.0))
(assert (= x 800.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL702 — flip ODRL421 Boundary co: claim compatible (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL702",
        "subdir":      "CSA",
        "name":        "CSA Boundary co: claim lteq∩gt compatible (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "difficulty":  "Easy",
        "needs_density": False,
        "description": (
            "Flip of ODRL421: lteq 600 vs gt 600.\n"
            "(0,600] ∩ (600,∞) = ∅ — Conflict.\n"
            "Wrong claim: overlap ?[X]: X≤600 & X>600.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "?[X]: (in_lopen(X,v0,v600) & less(v600,X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> x 600.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL703 — flip ODRL422 oc: claim lt∩gteq compatible (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL703",
        "subdir":      "CSA",
        "name":        "CSA Boundary oc: claim lt∩gteq compatible (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "difficulty":  "Easy",
        "needs_density": False,
        "description": (
            "Flip of ODRL422: lt 600 vs gteq 600.\n"
            "(0,600) ∩ [600,∞) = ∅ — Conflict.\n"
            "Wrong claim: overlap ?[X]: X<600 & X≥600.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "?[X]: (in_open(X,v0,v600) & leq(v600,X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (< x 600.0))
(assert (>= x 600.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL704 — flip ODRL423 oo: claim lt∩gt compatible (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL704",
        "subdir":      "CSA",
        "name":        "CSA Boundary oo: claim lt∩gt compatible (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "difficulty":  "Easy",
        "needs_density": False,
        "description": (
            "Flip of ODRL423: lt 600 vs gt 600.\n"
            "(0,600) ∩ (600,∞) = ∅ — Conflict.\n"
            "Wrong claim: overlap ?[X]: X<600 & X>600.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "?[X]: (in_open(X,v0,v600) & less(v600,X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (< x 600.0))
(assert (> x 600.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL705 — flip ODRL605: claim NOT disjoint cc (wrong — it IS disjoint)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL705",
        "subdir":      "CSA",
        "name":        "CSA ConflictCriterion: claim NOT disjoint cc (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "difficulty":  "Easy",
        "description": (
            "Flip of ODRL605: [v0,v5] vs [v6,v10] strictly separated.\n"
            "Wrong claim: ~disjoint(v0,v5,c,c,v6,v10,c,c).\n"
            "Countermodel: less(v5,v6) => disjoint holds.\n"
        ),
        "includes": ["ORD000-0.ax", "PREC000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "500"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,  axiom, val(v0)).
fof(val_v5,  axiom, val(v5)).
fof(val_v6,  axiom, val(v6)).
fof(val_v10, axiom, val(v10)).
fof(ord_v0_v5,  axiom, less(v0, v5)).
fof(ord_v5_v6,  axiom, less(v5, v6)).
fof(ord_v6_v10, axiom, less(v6, v10)).
fof(distinct, axiom, $distinct(v0, v5, v6, v10)).
""",
        "fof_conjecture": "~disjoint(v0, v5, closed, closed, v6, v10, closed, closed)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0)) (assert (<= x 500.0))
(assert (>= x 600.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL706 — flip ODRL361: claim 4D box compatible (wrong — width conflicts)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL706",
        "subdir":      "CSA",
        "name":        "CSA Composition 4D: claim compatible when width conflicts (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "difficulty":  "Medium",
        "description": (
            "Flip of ODRL361: width lteq 400 vs gteq 800 — Conflict.\n"
            "Wrong claim: overlap exists on all 4 axes.\n"
            "Countermodel: width contradiction kills the box.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
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
        odrl:operator odrl:gteq ; odrl:rightOperand "800"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:gteq ; odrl:rightOperand "100"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v100, axiom, val(v100)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v100,   axiom, less(v0, v100)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v100, v400, v600, v800)).
""",
        "fof_conjecture": (
            "?[X,Y]: (in_lopen(X,v0,v400) & leq(v800,X) &\n"
            "           in_lopen(Y,v0,v600) & leq(v100,Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 400.0)) (assert (>= x 800.0))
(assert (> y 0.0)) (assert (<= y 600.0)) (assert (>= y 100.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL707 — flip ODRL425 eq∩gteq compatible: claim eq∩gt compatible (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL707",
        "subdir":      "CSA",
        "name":        "CSA Boundary: claim eq∩gt compatible (wrong — boundary excluded)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "difficulty":  "Easy",
        "description": (
            "eq 600 vs gt 600: {600} ∩ (600,∞) = ∅ — Conflict.\n"
            "Wrong claim: ?[X]: X=600 & X>600. Countermodel: irreflexive.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "?[X]: (in_closed(X,v600,v600) & less(v600,X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (= x 600.0))
(assert (> x 600.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL708 — flip ODRL641: claim or_conflict=compatible (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL708",
        "subdir":      "CSA",
        "name":        "CSA Composition: claim or(conflict,conflict)=compatible (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "difficulty":  "Easy",
        "description": (
            "Flip of ODRL641: or_verdict(conflict,conflict)=conflict.\n"
            "Wrong claim: or_verdict(conflict,conflict)=compatible.\n"
            "Countermodel: violates or_conflict axiom.\n"
        ),
        "includes": ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": "",
        "fof_conjecture": "or_verdict(conflict, conflict) = compatible",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (not (= x x)))",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL709 — flip ODRL644: claim xone(compat,conflict)=conflict (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL709",
        "subdir":      "CSA",
        "name":        "CSA Composition: claim xone(compat,conflict)=conflict (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "difficulty":  "Easy",
        "description": (
            "Flip of ODRL644: xone_verdict(compatible,conflict)=compatible.\n"
            "Wrong claim: xone_verdict(compatible,conflict)=conflict.\n"
        ),
        "includes": ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": "",
        "fof_conjecture": "xone_verdict(compatible, conflict) = conflict",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (not (= x x)))",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL710 — flip ODRL631: claim completion_conflict requires U≥V (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL710",
        "subdir":      "CSA",
        "name":        "CSA Completion: claim conflict completion holds when U=V (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "difficulty":  "Easy",
        "description": (
            "Flip of ODRL637: ~completion_conflict(v600,v600,v0,v1200).\n"
            "Wrong claim: completion_conflict(v600,v600,...) holds.\n"
            "Requires less(v600,v600) — contradicts irreflexivity.\n"
        ),
        "includes": ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "completion_conflict(v600, v600, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const u Real)",
        "smt2_asserts": """\
(assert (= u 600.0))
(assert (< u 600.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL711 — flip ODRL652 box containment: claim conflict (wrong — it's compat)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL711",
        "subdir":      "CSA",
        "name":        "CSA BoxContainment: claim subs_verdict conflict when subsumes (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt": "unsat",
        "needs_density": False,
        "difficulty":  "Medium",
        "description": (
            "Flip of ODRL652: [v0,v400] ⊆ [v0,v600] => subs_verdict=compatible.\n"
            "Wrong claim: subs_verdict=conflict.\n"
            "Countermodel: axis_subsumes holds, so conflict is impossible.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax", "SUBS000-0.ax"],
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
      odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v400, v600)).
fof(subs_hint, axiom, axis_subsumes(v0, v400, v0, v600)).
""",
        "fof_conjecture": (
            "subs_verdict(v0, v400, present, v0, v600, present) = conflict"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0)) (assert (<= x 400.0))
(assert (not (<= x 600.0)))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL712 — flip ODRL610: claim wf(eq) NOT well-formed (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL712",
        "subdir":      "CSA",
        "name":        "CSA WellFormedness: claim wf(eq) not well-formed (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "difficulty":  "Easy",
        "description": (
            "Flip of ODRL610: wf(eq,v600,v0,v1200) holds.\n"
            "Wrong claim: ~wf(eq,v600,v0,v1200).\n"
            "Countermodel: v600 in [v0,v1200] so wf holds — negation impossible.\n"
        ),
        "includes": ["ORD000-0.ax", "WF000-0.ax", "AXIS000-0.ax"],
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
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "~wf(eq, v600, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const v Real)",
        "smt2_asserts": """\
(assert (= v 600.0))
(assert (not (and (>= v 0.0) (<= v 1200.0))))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL713 — flip ODRL626: claim in_closed(v400,v600,v600) (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL713",
        "subdir":      "CSA",
        "name":        "CSA Projection: claim v400 in point interval [v600,v600] (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,
        "difficulty":  "Easy",
        "description": (
            "Flip of ODRL626: in_closed(v600,v600,v600) holds but in_closed(v400,v600,v600) does not.\n"
            "Wrong claim: in_closed(v400,v600,v600).\n"
            "Countermodel: v400 != v600 so v400 not in {v600}.\n"
        ),
        "includes": ["ORD000-0.ax", "PROJ000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": """\
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v400, v600)).
""",
        "fof_conjecture": "in_closed(v400, v600, v600)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (= x 400.0))
(assert (= x 600.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL714 — flip ODRL635: claim box(compat,unknown)=conflict (wrong)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL714",
        "subdir":      "CSA",
        "name":        "CSA Completion: claim box(compatible,unknown)=conflict (wrong)",
        "verdict":     "CounterSatisfiable",
        "status_fof":  "CounterSatisfiable",
        "status_smt":  "unsat",
        "needs_density": False,   
        "difficulty":  "Easy",
        "description": (
            "Flip of ODRL635: box_verdict(compatible,unknown)=unknown.\n"
            "Wrong claim: box_verdict(compatible,unknown)=conflict.\n"
            "Countermodel: box_conflict requires at least one conflict.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": "",
        "fof_conjecture": "box_verdict(compatible, unknown) = conflict",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (not (= x x)))",
    },
]
