"""
problem_data_subs.py
====================
BoxContainment benchmark problems: ODRL650-657 (8 problems).
Category E: Tests axis_subsumes/4, subs_verdict/6, box_subs/2 from
SUBS000-0.ax (paper Def. 23 Box Containment).

Include pattern:
    include('Axioms/ORD000-0.ax').
    include('Axioms/AXIS000-0.ax').
    include('Axioms/SUBS000-0.ax').

Paper reference: def:box-containment (Def. 23)
Semantics:
  axis_subsumes(L1,U1,L2,U2): sem([L1,U1]) subseteq sem([L2,U2])
    Closed-interval form: leq(L2,L1) AND leq(U1,U2).
  subs_verdict(L1,U1,P1, L2,U2,P2):
    P1=absent or P2=absent              -> unknown
    both present + axis_subsumes        -> compatible  (C1 subseteq C2)
    both present + ~axis_subsumes       -> conflict    (C1 not subseteq C2)
  box_subs(V1,V2) - binary box-level combinator:
    (compatible,compatible)             -> compatible
    V1=conflict or V2=conflict          -> conflict
    otherwise                           -> unknown
  4-axis box: box_subs(box_subs(box_subs(S1,S2),S3),S4)

Problem overview:
  ODRL650 -- 1-axis Compatible:  lteq 600 subseteq lteq 800        Theorem
  ODRL651 -- 1-axis Conflict:    lteq 800 not-subseteq lteq 600    Theorem
  ODRL652 -- 4-axis box Compatible: all 4 axes A_k subseteq B_k    Theorem
  ODRL653 -- 4-axis box Conflict: width axis A not-subseteq B      Theorem
  ODRL654 -- C1 absent -> Unknown                                  Theorem
  ODRL655 -- C2 absent -> Unknown                                  Theorem
  ODRL656 -- Both absent -> Unknown                                Theorem
  ODRL657 -- 4-axis box, width absent -> Unknown                   Theorem

Change log (v1.1):
  - SUBS000-0.ax gains axis_subsumes_def biconditional, so ODRL650 and
    ODRL651 (which had no explicit axis_subsumes ground hint) now close
    as Theorem.  Previously CounterSatisfiable due to axis_subsumes being
    declared but undefined.
  - ODRL653 FOL conjecture upgraded from single-axis (which duplicated
    ODRL651) to a 4-axis box_subs chain that genuinely exercises Conflict
    propagation through box_subs_conflict.  Matches the description and
    provides distinct coverage from ODRL651.  SMT upgraded to match.
  - Ground hint axioms (hint_w, hint_h, etc. in ODRL652 and ODRL657, plus
    no_subs_hint in ODRL653) are kept as redundant facts.  Under v1.1 they
    are derivable from the biconditional + ord chain; keeping them lets
    saturation provers close faster on direct triggers.
"""

_SUBS_SMT_PLACEHOLDER = "(assert (not (= x x)))"

# Real UF SMT encodings for verdict-algebra problems (ODRL652-657)
from smt_axioms import (
    PREAMBLE_VERDICT, PREAMBLE_PRESENCE, PREAMBLE_BOUND_SORT,
    DECL_AXIS_SUBSUMES, DECL_SUBS_VERDICT, DECL_BOX_SUBS,
    AXIOM_SUBS_C1_ABSENT, AXIOM_SUBS_C2_ABSENT, AXIOM_SUBS_BOTH_ABSENT,
    AXIOM_SUBS_PRESENT_YES, AXIOM_SUBS_PRESENT_NO,
    AXIOM_BOX_SUBS_COMPAT, AXIOM_BOX_SUBS_CONFLICT, AXIOM_BOX_SUBS_UNKNOWN,
    declare_bounds,
)

PROBLEMS = [

    # =================================================================
    # ODRL650 - 1-axis containment: lteq 600 subseteq lteq 800 -> Compatible
    # FOL: closes via axis_subsumes_def biconditional in SUBS000 v1.1.
    # (Did not close in v1.0: axis_subsumes was undefined.)
    # =================================================================
    {
        "id":            "ODRL650",
        "subdir":        "BoxContainment",
        "name":          "1-axis containment: lteq 600 subsumed-by lteq 800 -> Compatible",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width: (0,600] subseteq (0,800]  ->  axis_subsumes(v0,v600,v0,v800)\n"
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
        # Negation of containment: assert h1=600, h2=800, claim 600 > 800.
        # Semantic: changing h1 to 1000 flips to sat.
        "smt2_asserts": """\
(assert (= h1 600.0))
(assert (= h2 800.0))
(assert (not (<= h1 h2)))""",
    },

    # =================================================================
    # ODRL651 - 1-axis containment: lteq 800 not-subseteq lteq 600 -> Conflict
    # FOL: closes via axis_subsumes_def + irreflexivity of less.
    # =================================================================
    {
        "id":            "ODRL651",
        "subdir":        "BoxContainment",
        "name":          "1-axis containment: lteq 800 not subsumed-by lteq 600 -> Conflict",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width: (0,800] not subseteq (0,600]  ->  ~axis_subsumes(v0,v800,v0,v600)\n"
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
        "smt2_asserts": """\
(assert (= h1 800.0))
(assert (= h2 600.0))
(assert (<= h1 h2))""",
    },

    # =================================================================
    # ODRL652 - 4-axis box containment: all A_k subseteq B_k -> Compatible
    # box_subs_compat triggers 3 times (binary chain over 4 axes).
    # =================================================================
    {
        "id":            "ODRL652",
        "subdir":        "BoxContainment",
        "name":          "4-axis box containment: all axes A subsumed-by B -> Compatible",
        "relation":      "verdict_algebra",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  (0,600] subseteq (0,800]  Compatible  less(v600,v800)\n"
            "Height: (0,400] subseteq (0,800]  Compatible  less(v400,v800)\n"
            "Depth:  (0,16]  subseteq (0,32]   Compatible  less(v16,v32)\n"
            "Alt:    (0,150] subseteq (0,300]  Compatible  less(v150,v300)\n"
            "box_subs(box_subs(box_subs(C,C),C),C) = compatible [Def. 23]\n"
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
        # Note: hint_w/h/d/a are redundant under SUBS000 v1.1
        # (axis_subsumes_def derives them from the ord chain).  Kept for
        # saturation-prover speed.
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
fof(hint_w, axiom, axis_subsumes(v0,v600,v0,v800)).
fof(hint_h, axiom, axis_subsumes(v0,v400,v0,v800)).
fof(hint_d, axiom, axis_subsumes(v0,v16,v0,v32)).
fof(hint_a, axiom, axis_subsumes(v0,v150,v0,v300)).
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
        "smt2_logic":   "UF",
        "smt2_decls":   PREAMBLE_VERDICT + PREAMBLE_PRESENCE + PREAMBLE_BOUND_SORT + DECL_AXIS_SUBSUMES + DECL_SUBS_VERDICT + DECL_BOX_SUBS + declare_bounds(["v0", "v16", "v32", "v150", "v300", "v400", "v600", "v800"]),
        "smt2_asserts": AXIOM_SUBS_PRESENT_YES + AXIOM_SUBS_PRESENT_NO + AXIOM_BOX_SUBS_COMPAT + AXIOM_BOX_SUBS_CONFLICT + AXIOM_BOX_SUBS_UNKNOWN + "; axis_subsumes ground hints (positive on all 4 axes)\n"
                          "(assert (axis_subsumes v0 v600 v0 v800))\n"
                          "(assert (axis_subsumes v0 v400 v0 v800))\n"
                          "(assert (axis_subsumes v0 v16  v0 v32))\n"
                          "(assert (axis_subsumes v0 v150 v0 v300))\n"
                          "; Negated conjecture: 4-axis box_subs chain != compatible\n"
                          "(assert (not (=\n"
                          "  (box_subs\n"
                          "    (box_subs\n"
                          "      (box_subs\n"
                          "        (subs_verdict v0 v600 present v0 v800 present)\n"
                          "        (subs_verdict v0 v400 present v0 v800 present))\n"
                          "      (subs_verdict v0 v16 present v0 v32 present))\n"
                          "    (subs_verdict v0 v150 present v0 v300 present))\n"
                          "  compatible)))",
    },

    # =================================================================
    # ODRL653 - 4-axis box containment: width axis escapes -> Conflict
    #
    # v1.1 FOL upgrade: was a single-axis test (duplicating ODRL651's
    # conjecture).  Now a proper 4-axis chain with one Conflict input,
    # exercising box_subs_conflict propagation through 3 box_subs nodes.
    # SMT upgraded to match.
    # =================================================================
    {
        "id":            "ODRL653",
        "subdir":        "BoxContainment",
        "name":          "4-axis box containment: width axis escapes -> Conflict",
        "relation":      "verdict_algebra",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  (0,800] not subseteq (0,600]  Conflict   <- escape axis\n"
            "Height: (0,400] subseteq (0,800]  Compatible\n"
            "Depth:  (0,16]  subseteq (0,32]   Compatible\n"
            "Alt:    (0,150] subseteq (0,300]  Compatible\n"
            "box_subs chain: any Conflict input -> Conflict overall\n"
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
        # Hints: no_subs_hint for width (negative); positive hints for the
        # other 3 axes.  All redundant under SUBS000 v1.1, kept for speed.
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
fof(no_subs_hint, axiom, ~axis_subsumes(v0, v800, v0, v600)).
fof(hint_h, axiom, axis_subsumes(v0,v400,v0,v800)).
fof(hint_d, axiom, axis_subsumes(v0,v16,v0,v32)).
fof(hint_a, axiom, axis_subsumes(v0,v150,v0,v300)).
""",
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
        "smt2_logic":   "UF",
        "smt2_decls":   PREAMBLE_VERDICT + PREAMBLE_PRESENCE + PREAMBLE_BOUND_SORT + DECL_AXIS_SUBSUMES + DECL_SUBS_VERDICT + DECL_BOX_SUBS + declare_bounds(["v0", "v16", "v32", "v150", "v300", "v400", "v600", "v800"]),
        "smt2_asserts": AXIOM_SUBS_PRESENT_YES + AXIOM_SUBS_PRESENT_NO + AXIOM_BOX_SUBS_COMPAT + AXIOM_BOX_SUBS_CONFLICT + AXIOM_BOX_SUBS_UNKNOWN + "; axis_subsumes ground hints (negative on width, positive on others)\n"
                          "(assert (not (axis_subsumes v0 v800 v0 v600)))\n"
                          "(assert (axis_subsumes v0 v400 v0 v800))\n"
                          "(assert (axis_subsumes v0 v16  v0 v32))\n"
                          "(assert (axis_subsumes v0 v150 v0 v300))\n"
                          "; Negated conjecture: 4-axis box_subs chain != conflict\n"
                          "(assert (not (=\n"
                          "  (box_subs\n"
                          "    (box_subs\n"
                          "      (box_subs\n"
                          "        (subs_verdict v0 v800 present v0 v600 present)\n"
                          "        (subs_verdict v0 v400 present v0 v800 present))\n"
                          "      (subs_verdict v0 v16 present v0 v32 present))\n"
                          "    (subs_verdict v0 v150 present v0 v300 present))\n"
                          "  conflict)))",
    },

    # =================================================================
    # ODRL654 - C1 absent on width axis -> Unknown
    # subs_c1_absent (forward only) suffices since no axis_subsumes is needed.
    # =================================================================
    {
        "id":            "ODRL654",
        "subdir":        "BoxContainment",
        "name":          "C1 absent on width axis -> Unknown",
        "relation":      "verdict_algebra",
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
        "smt2_logic":   "UF",
        "smt2_decls":   PREAMBLE_VERDICT + PREAMBLE_PRESENCE + PREAMBLE_BOUND_SORT + DECL_SUBS_VERDICT + declare_bounds(["v0", "v600", "v800"]),
        "smt2_asserts": AXIOM_SUBS_C1_ABSENT + "; Negated conjecture\n"
                          "(assert (not (= (subs_verdict v0 v600 absent v0 v800 present) unknown)))",
    },

    # =================================================================
    # ODRL655 - C2 absent on width axis -> Unknown
    # =================================================================
    {
        "id":            "ODRL655",
        "subdir":        "BoxContainment",
        "name":          "C2 absent on width axis -> Unknown",
        "relation":      "verdict_algebra",
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
        "smt2_logic":   "UF",
        "smt2_decls":   PREAMBLE_VERDICT + PREAMBLE_PRESENCE + PREAMBLE_BOUND_SORT + DECL_SUBS_VERDICT + declare_bounds(["v0", "v600", "v800"]),
        "smt2_asserts": AXIOM_SUBS_C2_ABSENT + "; Negated conjecture\n"
                          "(assert (not (= (subs_verdict v0 v600 present v0 v800 absent) unknown)))",
    },

    # =================================================================
    # ODRL656 - Both absent on width axis -> Unknown
    # =================================================================
    {
        "id":            "ODRL656",
        "subdir":        "BoxContainment",
        "name":          "Both absent on width axis -> Unknown",
        "relation":      "verdict_algebra",
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
        "smt2_logic":   "UF",
        "smt2_decls":   PREAMBLE_VERDICT + PREAMBLE_PRESENCE + PREAMBLE_BOUND_SORT + DECL_SUBS_VERDICT + declare_bounds(["v0", "v600", "v800"]),
        "smt2_asserts": AXIOM_SUBS_BOTH_ABSENT + "; Negated conjecture\n"
                          "(assert (not (= (subs_verdict v0 v600 absent v0 v800 absent) unknown)))",
    },

    # =================================================================
    # ODRL657 - 4-axis box: width C1 absent + 3 compatible -> Unknown
    # box_subs_unknown triggers 3 times (any non-conflict, non-all-compatible
    # chain reduces to Unknown).
    # =================================================================
    {
        "id":            "ODRL657",
        "subdir":        "BoxContainment",
        "name":          "4-axis box: absent width axis propagates Unknown",
        "relation":      "verdict_algebra",
        "verdict":       "Unknown",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  C1 absent -> subs_verdict = unknown\n"
            "Height: (0,400] subseteq (0,800]  Compatible\n"
            "Depth:  (0,16]  subseteq (0,32]   Compatible\n"
            "Alt:    (0,150] subseteq (0,300]  Compatible\n"
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
        # Placeholder bounds v0,v800 used for absent axis -- values irrelevant.
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
        "smt2_logic":   "UF",
        "smt2_decls":   PREAMBLE_VERDICT + PREAMBLE_PRESENCE + PREAMBLE_BOUND_SORT + DECL_AXIS_SUBSUMES + DECL_SUBS_VERDICT + DECL_BOX_SUBS + declare_bounds(["v0", "v16", "v32", "v150", "v300", "v400", "v800"]),
        "smt2_asserts": AXIOM_SUBS_C1_ABSENT + AXIOM_SUBS_PRESENT_YES + AXIOM_SUBS_PRESENT_NO + AXIOM_BOX_SUBS_COMPAT + AXIOM_BOX_SUBS_CONFLICT + AXIOM_BOX_SUBS_UNKNOWN + "; axis_subsumes ground hints for the 3 present axes\n"
                          "(assert (axis_subsumes v0 v400 v0 v800))\n"
                          "(assert (axis_subsumes v0 v16  v0 v32))\n"
                          "(assert (axis_subsumes v0 v150 v0 v300))\n"
                          "; Negated conjecture: 4-axis chain (width absent) != unknown\n"
                          "(assert (not (=\n"
                          "  (box_subs\n"
                          "    (box_subs\n"
                          "      (box_subs\n"
                          "        (subs_verdict v0 v800 absent  v0 v800 present)\n"
                          "        (subs_verdict v0 v400 present v0 v800 present))\n"
                          "      (subs_verdict v0 v16 present v0 v32 present))\n"
                          "    (subs_verdict v0 v150 present v0 v300 present))\n"
                          "  unknown)))",
    },
]