"""
problem_data_uns_ext.py
=======================
Additional UNS problems: ODRL765-766 (+2 problems).
Appended to problem_data_uns.py PROBLEMS list.

Both problems encode Remark 3.4: a single policy constraint whose
denotation is empty — the constraint is self-contradictory.

Contradiction mechanism:
  ODRL765: fresh witness w declared to satisfy both in_lopen(w,v0,v600)
           and leq(v800,w). These are incompatible:
             in_lopen -> leq(w,v600)
             leq(w,v600) + less(v600,v800) -> less(w,v800)
             leq(v800,w) -> less(v800,w) | v800=w
             less(w,v800) contradicts both -> ⊥

  ODRL766: fresh witness w declared equal to both v600 and v800.
           w=v600 & w=v800 -> v600=v800, but $distinct(v600,v800) -> ⊥
           This is the simplest possible UNS construction.
"""

PROBLEMS_EXT = [
    # ── Box2D intra-policy: width lteq 600 AND gteq 800 → empty ─────
    {
        "id":          "ODRL765",
        "subdir":      "UNS",
        "name":        "intra-policy Box2D: width lteq 600 AND gteq 800 empty",
        "verdict":     "Unsatisfiable",
        "status_fof":  "Unsatisfiable",
        "status_smt":  "unsat",
        "difficulty":  "Easy",
        "includes":    ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "Remark 3.4: width (0,600] ∩ [800,∞) = ∅.\n"
            "Single policy asserts width ≤ 600 AND ≥ 800 simultaneously.\n"
            "Contradiction via fresh witness w: in_lopen(w,v0,v600) forces\n"
            "leq(w,v600), and leq(v800,w) with less(v600,v800) gives less(w,v800)\n"
            "and less(v800,w) — irreflexivity closes the proof.\n"
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
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:gteq ; odrl:rightOperand "800"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
    ) ] ] .""",
        # Contradiction chain:
        #   in_lopen(w,v0,v600) unfolds to: less(v0,w) & leq(w,v600)
        #   leq(w,v600) means: less(w,v600) | w=v600
        #   less(v600,v800) is declared
        #   → less(w,v800) by transitivity (or less(v600,v800) directly)
        #   leq(v800,w) means: less(v800,w) | v800=w
        #   less(w,v800) + less(v800,w) → less(w,w) → contradicts irrefl
        #   less(w,v800) + v800=w → less(w,w) → contradicts irrefl
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
fof(wit_val,      axiom, val(w)).
fof(wit_in_lopen, axiom, in_lopen(w, v0, v600)).
fof(wit_leq,      axiom, leq(v800, w)).
""",
        "fof_conjecture": None,
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (>= x 800.0))""",
    },
    # ── intra-policy eq 600 AND eq 800 on same axis → empty ──────────
    {
        "id":          "ODRL766",
        "subdir":      "UNS",
        "name":        "intra-policy: eq 600 AND eq 800 on same axis empty",
        "verdict":     "Unsatisfiable",
        "status_fof":  "Unsatisfiable",
        "status_smt":  "unsat",
        "difficulty":  "Easy",
        "includes":    ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "Remark 3.4: single constraint eq 600 AND eq 800 on width.\n"
            "{600} ∩ {800} = ∅ — self-contradictory.\n"
            "Contradiction via fresh witness w=v600 and w=v800:\n"
            "by transitivity v600=v800, contradicting $distinct(v600,v800).\n"
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
        odrl:operator odrl:eq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:eq ; odrl:rightOperand "800"^^xsd:decimal ]
    ) ] ] .""",
        # Contradiction chain:
        #   w = v600  (axiom)
        #   w = v800  (axiom)
        #   → v600 = v800  (by transitivity of equality)
        #   $distinct(v600,v800) → v600 ≠ v800
        #   → contradiction ⊥
        "fof_extra_decls": """\
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v600, v800)).
fof(wit_eq1, axiom, w = v600).
fof(wit_eq2, axiom, w = v800).
""",
        "fof_conjecture": None,
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (= x 600.0))
(assert (= x 800.0))""",
    },
]