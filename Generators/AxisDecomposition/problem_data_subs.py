"""
problem_data_subs.py
====================
BoxContainment benchmark problems: ODRL650-657 (8 problems).
Category E: Tests subs_verdict/6 and box_subs/2 from SUBS000-0.ax.
Include pattern:
    include('Axioms/ORD000-0.ax').
    include('Axioms/AXIS000-0.ax').
    include('Axioms/SUBS000-0.ax').

Paper reference: def:box-containment (arXiv:2602.19878)

Semantics:
  axis_subsumes(L1,H1,L2,H2): sem([L1,H1]) ⊆ sem([L2,H2])
    For lteq intervals (in_lopen(X,v0,H)): subsumes iff H1 ≤ H2

  subs_verdict(L1,H1,P1, L2,H2,P2):
    P1=absent or P2=absent              → unknown
    both present + axis_subsumes        → compatible  (C1 ⊆ C2)
    both present + ~axis_subsumes       → conflict    (C1 ⊄ C2)

  box_subs(V1,V2) — binary Kleene aggregation:
    (compatible,compatible)             → compatible
    V1=conflict or V2=conflict          → conflict
    otherwise                           → unknown
  For 4 axes: box_subs(box_subs(box_subs(S1,S2),S3),S4)

Problem overview:
  ODRL650 — 1-axis Compatible:  lteq 600 ⊆ lteq 800          Theorem
  ODRL651 — 1-axis Conflict:    lteq 800 ⊄ lteq 600          Theorem
  ODRL652 — 4-axis box Compatible: all axes A_k ⊆ B_k         Theorem
  ODRL653 — 4-axis box Conflict: width axis A ⊄ B             Theorem
  ODRL654 — C1 absent → Unknown                               Theorem
  ODRL655 — C2 absent → Unknown                               Theorem
  ODRL656 — Both absent → Unknown                             Theorem
  ODRL657 — 4-axis box, width absent → Unknown                Theorem

SMT encoding:
  ODRL650-651: LRA directly encodes the containment arithmetic.
    ODRL650 Compatible: negate = (assert (> 600.0 800.0)) → unsat  ✓
    ODRL651 Conflict:   negate = (assert (<= 800.0 600.0)) → unsat ✓
  ODRL652-657: subs_verdict/box_subs are uninterpreted — no QF_LRA encoding.
    SMT uses (assert (not (= x x))) as well-formedness placeholder.
    Meaningful verification is FOF Theorem status from Vampire/E.

box_subs chaining reduction (verified by hand):
  ODRL652: box_subs(C,box_subs(C,box_subs(C,C))) = compatible  ✓
  ODRL653: box_subs(CONFLICT,box_subs(C,box_subs(C,C))) = conflict  ✓
  ODRL657: box_subs(unknown,box_subs(C,box_subs(C,C))) = unknown  ✓
"""

_SUBS_SMT_PLACEHOLDER = "(assert (not (= x x)))"

PROBLEMS = [
    # ──────────────────────────────────────────────────────────────────
    # ODRL650 — 1-axis containment: lteq 600 ⊆ lteq 800 → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL650",
        "subdir":        "BoxContainment",
        "name":          "1-axis containment: lteq 600 subsumes lteq 800 → Compatible",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width: (0,600] ⊆ (0,800]  →  axis_subsumes(v0,v600,v0,v800)\n"
            "subs_verdict(v0,v600,present,v0,v800,present) = compatible\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand  oax:absoluteSizeWidth ;
      odrl:operator     odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand  oax:absoluteSizeWidth ;
      odrl:operator     odrl:lteq ;
      odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
""",
        "fof_conjecture": (
            "subs_verdict(v0,v600,present,v0,v800,present) = compatible"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const h1 Real)\n(declare-const h2 Real)",
        # Negate containment: h1=600, h2=800, claim 600 > 800 → unsat
        "smt2_asserts": """\
(assert (= h1 600.0))
(assert (= h2 800.0))
(assert (not (<= h1 h2)))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL651 — 1-axis containment: lteq 800 ⊄ lteq 600 → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL651",
        "subdir":        "BoxContainment",
        "name":          "1-axis containment: lteq 800 does not subsume lteq 600 → Conflict",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width: (0,800] ⊄ (0,600]  →  ~axis_subsumes(v0,v800,v0,v600)\n"
            "subs_verdict(v0,v800,present,v0,v600,present) = conflict\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand  oax:absoluteSizeWidth ;
      odrl:operator     odrl:lteq ;
      odrl:rightOperand "800"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand  oax:absoluteSizeWidth ;
      odrl:operator     odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
""",
        "fof_conjecture": (
            "subs_verdict(v0,v800,present,v0,v600,present) = conflict"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const h1 Real)\n(declare-const h2 Real)",
        # Negate non-containment: h1=800, h2=600, claim 800 ≤ 600 → unsat
        "smt2_asserts": """\
(assert (= h1 800.0))
(assert (= h2 600.0))
(assert (<= h1 h2))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL652 — 4-axis box containment: all A_k ⊆ B_k → Compatible
    # Width:  (0,600] ⊆ (0,800]  ✓  less(v600,v800)
    # Height: (0,400] ⊆ (0,800]  ✓  less(v400,v800)
    # Depth:  (0,16]  ⊆ (0,32]   ✓  less(v16,v32)
    # Alt:    (0,150] ⊆ (0,300]  ✓  less(v150,v300)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL652",
        "subdir":        "BoxContainment",
        "name":          "4-axis box containment: all axes A subsumes B → Compatible",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  (0,600] ⊆ (0,800]  Compatible  less(v600,v800)\n"
            "Height: (0,400] ⊆ (0,800]  Compatible  less(v400,v800)\n"
            "Depth:  (0,16]  ⊆ (0,32]   Compatible  less(v16,v32)\n"
            "Alt:    (0,150] ⊆ (0,300]  Compatible  less(v150,v300)\n"
            "box_subs(box_subs(box_subs(C,C),C),C) = compatible [def:box-containment]\n"
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
        odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeDepth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "16"^^xsd:decimal ]
      [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
        odrl:operator odrl:lteq ; odrl:rightOperand "150"^^xsd:decimal ]
    ) ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "800"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "800"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeDepth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "32"^^xsd:decimal ]
      [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
        odrl:operator odrl:lteq ; odrl:rightOperand "300"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v16,  axiom, val(v16)).
fof(val_v32,  axiom, val(v32)).
fof(val_v150, axiom, val(v150)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v16,    axiom, less(v0,   v16)).
fof(ord_v0_v32,    axiom, less(v0,   v32)).
fof(ord_v0_v150,   axiom, less(v0,   v150)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v16_v32,   axiom, less(v16,  v32)).
fof(ord_v16_v150,  axiom, less(v16,  v150)).
fof(ord_v16_v300,  axiom, less(v16,  v300)).
fof(ord_v16_v400,  axiom, less(v16,  v400)).
fof(ord_v16_v600,  axiom, less(v16,  v600)).
fof(ord_v16_v800,  axiom, less(v16,  v800)).
fof(ord_v32_v150,  axiom, less(v32,  v150)).
fof(ord_v32_v300,  axiom, less(v32,  v300)).
fof(ord_v32_v400,  axiom, less(v32,  v400)).
fof(ord_v32_v600,  axiom, less(v32,  v600)).
fof(ord_v32_v800,  axiom, less(v32,  v800)).
fof(ord_v150_v300, axiom, less(v150, v300)).
fof(ord_v150_v400, axiom, less(v150, v400)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v800, axiom, less(v150, v800)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v16, v32, v150, v300, v400, v600, v800)).
""",
        "fof_conjecture": (
            "box_subs(\n"
            "    box_subs(\n"
            "      box_subs(\n"
            "        subs_verdict(v0,v600,present,v0,v800,present),\n"
            "        subs_verdict(v0,v400,present,v0,v800,present)),\n"
            "      subs_verdict(v0,v16,present,v0,v32,present)),\n"
            "    subs_verdict(v0,v150,present,v0,v300,present))\n"
            "  = compatible"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _SUBS_SMT_PLACEHOLDER,
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL653 — 4-axis box: width axis A ⊄ B → Conflict
    # Width:  (0,800] ⊄ (0,600]  Conflict  ← escape: ~less(v800,v600)
    # Height: (0,400] ⊆ (0,800]  Compatible
    # Depth:  (0,16]  ⊆ (0,32]   Compatible
    # Alt:    (0,150] ⊆ (0,300]  Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL653",
        "subdir":        "BoxContainment",
        "name":          "4-axis box containment: width axis escapes → Conflict",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  (0,800] ⊄ (0,600]  Conflict  ← escape axis\n"
            "Height: (0,400] ⊆ (0,800]  Compatible\n"
            "Depth:  (0,16]  ⊆ (0,32]   Compatible\n"
            "Alt:    (0,150] ⊆ (0,300]  Compatible\n"
            "box_subs chained: one Conflict → overall Conflict\n"
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
        odrl:operator odrl:lteq ; odrl:rightOperand "800"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeDepth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "16"^^xsd:decimal ]
      [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
        odrl:operator odrl:lteq ; odrl:rightOperand "150"^^xsd:decimal ]
    ) ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "800"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeDepth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "32"^^xsd:decimal ]
      [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
        odrl:operator odrl:lteq ; odrl:rightOperand "300"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v16,  axiom, val(v16)).
fof(val_v32,  axiom, val(v32)).
fof(val_v150, axiom, val(v150)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v16,    axiom, less(v0,   v16)).
fof(ord_v0_v32,    axiom, less(v0,   v32)).
fof(ord_v0_v150,   axiom, less(v0,   v150)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v16_v32,   axiom, less(v16,  v32)).
fof(ord_v16_v150,  axiom, less(v16,  v150)).
fof(ord_v16_v300,  axiom, less(v16,  v300)).
fof(ord_v16_v400,  axiom, less(v16,  v400)).
fof(ord_v16_v600,  axiom, less(v16,  v600)).
fof(ord_v16_v800,  axiom, less(v16,  v800)).
fof(ord_v32_v150,  axiom, less(v32,  v150)).
fof(ord_v32_v300,  axiom, less(v32,  v300)).
fof(ord_v32_v400,  axiom, less(v32,  v400)).
fof(ord_v32_v600,  axiom, less(v32,  v600)).
fof(ord_v32_v800,  axiom, less(v32,  v800)).
fof(ord_v150_v300, axiom, less(v150, v300)).
fof(ord_v150_v400, axiom, less(v150, v400)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v800, axiom, less(v150, v800)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v16, v32, v150, v300, v400, v600, v800)).
""",
        # Width: less(v600,v800) so ~axis_subsumes(v0,v800,v0,v600) → conflict
        "fof_conjecture": (
            "box_subs(\n"
            "    box_subs(\n"
            "      box_subs(\n"
            "        subs_verdict(v0,v800,present,v0,v600,present),\n"
            "        subs_verdict(v0,v400,present,v0,v800,present)),\n"
            "      subs_verdict(v0,v16,present,v0,v32,present)),\n"
            "    subs_verdict(v0,v150,present,v0,v300,present))\n"
            "  = conflict"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _SUBS_SMT_PLACEHOLDER,
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL654 — C1 absent on width axis → Unknown
    # policyA has no width constraint (P1=absent)
    # subs_c1_absent: subs_verdict(L1,H1,absent,L2,H2,present) = unknown
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL654",
        "subdir":        "BoxContainment",
        "name":          "C1 absent on width axis → Unknown",
        "relation":      "subsumption",
        "verdict":       "Unknown",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "C1 does not constrain width (P1=absent).\n"
            "Unknown-when-absent: intended scope of C1 not known.\n"
            "subs_verdict(v0,v600,absent,v0,v800,present) = unknown\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand  oax:absoluteSizeWidth ;
      odrl:operator     odrl:lteq ;
      odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
""",
        "fof_conjecture": (
            "subs_verdict(v0,v600,absent,v0,v800,present) = unknown"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _SUBS_SMT_PLACEHOLDER,
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL655 — C2 absent on width axis → Unknown
    # policyB has no width constraint (P2=absent)
    # subs_c2_absent: subs_verdict(L1,H1,present,L2,H2,absent) = unknown
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL655",
        "subdir":        "BoxContainment",
        "name":          "C2 absent on width axis → Unknown",
        "relation":      "subsumption",
        "verdict":       "Unknown",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "C2 does not constrain width (P2=absent).\n"
            "Unknown-when-absent: intended scope of C2 not known.\n"
            "subs_verdict(v0,v600,present,v0,v800,absent) = unknown\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand  oax:absoluteSizeWidth ;
      odrl:operator     odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
""",
        "fof_conjecture": (
            "subs_verdict(v0,v600,present,v0,v800,absent) = unknown"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _SUBS_SMT_PLACEHOLDER,
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL656 — Both absent on width axis → Unknown
    # Neither policy constrains width
    # subs_both_absent: subs_verdict(L1,H1,absent,L2,H2,absent) = unknown
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL656",
        "subdir":        "BoxContainment",
        "name":          "Both absent on width axis → Unknown",
        "relation":      "subsumption",
        "verdict":       "Unknown",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Neither C1 nor C2 constrains width (both absent).\n"
            "subs_verdict(v0,v600,absent,v0,v800,absent) = unknown\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
""",
        "fof_conjecture": (
            "subs_verdict(v0,v600,absent,v0,v800,absent) = unknown"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _SUBS_SMT_PLACEHOLDER,
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL657 — 4-axis box: width C1 absent + 3 compatible → Unknown
    # Width:  C1 absent → subs_verdict = unknown
    # Height: (0,400] ⊆ (0,800]  Compatible
    # Depth:  (0,16]  ⊆ (0,32]   Compatible
    # Alt:    (0,150] ⊆ (0,300]  Compatible
    # box_subs chaining:
    #   box_subs(unknown, compatible) = unknown  (not both-compat, no conflict)
    #   → box_subs(unknown, compatible) = unknown
    #   → box_subs(unknown, compatible) = unknown
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL657",
        "subdir":        "BoxContainment",
        "name":          "4-axis box: absent width axis propagates Unknown",
        "relation":      "subsumption",
        "verdict":       "Unknown",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  C1 absent → subs_verdict = unknown\n"
            "Height: (0,400] ⊆ (0,800]  Compatible\n"
            "Depth:  (0,16]  ⊆ (0,32]   Compatible\n"
            "Alt:    (0,150] ⊆ (0,300]  Compatible\n"
            "box_subs(box_subs(box_subs(unknown,C),C),C) = unknown\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeDepth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "16"^^xsd:decimal ]
      [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
        odrl:operator odrl:lteq ; odrl:rightOperand "150"^^xsd:decimal ]
    ) ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "800"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "800"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeDepth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "32"^^xsd:decimal ]
      [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
        odrl:operator odrl:lteq ; odrl:rightOperand "300"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v16,  axiom, val(v16)).
fof(val_v32,  axiom, val(v32)).
fof(val_v150, axiom, val(v150)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v16,    axiom, less(v0,   v16)).
fof(ord_v0_v32,    axiom, less(v0,   v32)).
fof(ord_v0_v150,   axiom, less(v0,   v150)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v16_v32,   axiom, less(v16,  v32)).
fof(ord_v16_v150,  axiom, less(v16,  v150)).
fof(ord_v16_v300,  axiom, less(v16,  v300)).
fof(ord_v16_v400,  axiom, less(v16,  v400)).
fof(ord_v16_v800,  axiom, less(v16,  v800)).
fof(ord_v32_v150,  axiom, less(v32,  v150)).
fof(ord_v32_v300,  axiom, less(v32,  v300)).
fof(ord_v32_v400,  axiom, less(v32,  v400)).
fof(ord_v32_v800,  axiom, less(v32,  v800)).
fof(ord_v150_v300, axiom, less(v150, v300)).
fof(ord_v150_v400, axiom, less(v150, v400)).
fof(ord_v150_v800, axiom, less(v150, v800)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct, axiom, $distinct(v0, v16, v32, v150, v300, v400, v800)).
""",
        # Width axis: C1 absent (policyA has no width constraint)
        # Placeholder bounds v0,v800 used for absent axis — values irrelevant.
        "fof_conjecture": (
            "box_subs(\n"
            "    box_subs(\n"
            "      box_subs(\n"
            "        subs_verdict(v0,v800,absent,v0,v800,present),\n"
            "        subs_verdict(v0,v400,present,v0,v800,present)),\n"
            "      subs_verdict(v0,v16,present,v0,v32,present)),\n"
            "    subs_verdict(v0,v150,present,v0,v300,present))\n"
            "  = unknown"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _SUBS_SMT_PLACEHOLDER,
    },
]