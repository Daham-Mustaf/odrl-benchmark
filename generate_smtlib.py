#!/usr/bin/env python3
"""
Generate SMT-LIB2 encodings for all TPTP-ODRL benchmarks and run Z3.
Produces comparison table: Vampire (SZS) vs Z3 (sat/unsat).

Usage:
    python3 generate_smtlib.py              # generate all .smt2 files
    python3 generate_smtlib.py --run        # generate + run z3 on all
    python3 generate_smtlib.py --run --cvc5 # also run cvc5 if available
"""

import os
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
SMT_DIR = os.path.join(BASE, "SMT/ODRL/KBGrounding")

# ============================================================
# Layer 0: Domain Knowledge Bases
# ============================================================

PREAMBLE = """\
(set-logic UF)
(declare-sort Entity 0)
"""

GEO_KB = """\
; === Layer 0: GeoNames Spatial KB ===
(declare-fun partOf (Entity Entity) Bool)
(declare-const europe Entity)
(declare-const france Entity)
(declare-const germany Entity)
(declare-const bavaria Entity)

(assert (forall ((x Entity)) (partOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (partOf x y) (partOf y z)) (partOf x z))))
(assert (partOf france europe))
(assert (partOf germany europe))
(assert (partOf bavaria germany))
(assert (not (partOf germany france)))
(assert (not (partOf france germany)))
"""

DPV_KB = """\
; === Layer 0: DPV Purpose Taxonomy (DAG) ===
(declare-fun subClassOf (Entity Entity) Bool)
(declare-const purpose_top Entity)
(declare-const commercialPurpose Entity)
(declare-const nonCommercialPurpose Entity)
(declare-const researchAndDevelopment Entity)
(declare-const marketing Entity)
(declare-const academicResearch Entity)
(declare-const scientificResearch Entity)
(declare-const commercialResearch Entity)
(declare-const nonCommercialResearch Entity)
(declare-const advertising Entity)
(declare-const directMarketing Entity)

(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))

; Top-level
(assert (subClassOf commercialPurpose purpose_top))
(assert (subClassOf nonCommercialPurpose purpose_top))
(assert (subClassOf researchAndDevelopment purpose_top))
(assert (subClassOf marketing purpose_top))

; R&D children
(assert (subClassOf academicResearch researchAndDevelopment))
(assert (subClassOf scientificResearch researchAndDevelopment))
(assert (subClassOf commercialResearch researchAndDevelopment))
(assert (subClassOf nonCommercialResearch researchAndDevelopment))

; Multi-parent (DAG)
(assert (subClassOf commercialResearch commercialPurpose))
(assert (subClassOf nonCommercialResearch nonCommercialPurpose))

; Marketing children
(assert (subClassOf advertising marketing))
(assert (subClassOf directMarketing marketing))

; Disjointness
(assert (not (subClassOf commercialPurpose nonCommercialPurpose)))
(assert (not (subClassOf nonCommercialPurpose commercialPurpose)))
(assert (not (subClassOf marketing nonCommercialPurpose)))
(assert (not (subClassOf advertising nonCommercialPurpose)))
(assert (not (subClassOf nonCommercialResearch commercialPurpose)))
"""

# Language constants + facts (no subClassOf declaration — for use with DPV_KB)
LNG_KB_FACTS = """\
; === Layer 0: BCP 47 Language Tags (facts only) ===
(declare-const de Entity)
(declare-const de_AT Entity)
(declare-const de_CH Entity)
(declare-const en Entity)
(declare-const en_US Entity)
(declare-const en_GB Entity)
(declare-const fr Entity)
(declare-const ar Entity)
(declare-const arb Entity)
(declare-const arz Entity)

; German variants
(assert (subClassOf de_AT de))
(assert (subClassOf de_CH de))
; English variants
(assert (subClassOf en_US en))
(assert (subClassOf en_GB en))
; Arabic macrolanguage
(assert (subClassOf arb ar))
(assert (subClassOf arz ar))

; Cross-branch disjointness
(assert (not (subClassOf de en)))
(assert (not (subClassOf en de)))
(assert (not (subClassOf de fr)))
(assert (not (subClassOf fr de)))
(assert (not (subClassOf en fr)))
(assert (not (subClassOf fr en)))
(assert (not (subClassOf de ar)))
(assert (not (subClassOf ar de)))
(assert (not (subClassOf en ar)))
(assert (not (subClassOf ar en)))
(assert (not (subClassOf fr ar)))
(assert (not (subClassOf ar fr)))
"""

# Standalone LNG KB (includes subClassOf declaration for language-only problems)
LNG_KB = """\
; === Layer 0: BCP 47 Language Tags ===
(declare-fun subClassOf (Entity Entity) Bool)
(declare-const de Entity)
(declare-const de_AT Entity)
(declare-const de_CH Entity)
(declare-const en Entity)
(declare-const en_US Entity)
(declare-const en_GB Entity)
(declare-const fr Entity)
(declare-const ar Entity)
(declare-const arb Entity)
(declare-const arz Entity)

(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))

(assert (subClassOf de_AT de))
(assert (subClassOf de_CH de))
(assert (subClassOf en_US en))
(assert (subClassOf en_GB en))
(assert (subClassOf arb ar))
(assert (subClassOf arz ar))

(assert (not (subClassOf de en)))
(assert (not (subClassOf en de)))
(assert (not (subClassOf de fr)))
(assert (not (subClassOf fr de)))
(assert (not (subClassOf en fr)))
(assert (not (subClassOf fr en)))
(assert (not (subClassOf de ar)))
(assert (not (subClassOf ar de)))
(assert (not (subClassOf en ar)))
(assert (not (subClassOf ar en)))
(assert (not (subClassOf fr ar)))
(assert (not (subClassOf ar fr)))
"""

# ============================================================
# Layer 1: ODRL Core structure
# ============================================================

LAYER1 = """\
; === Layer 1: ODRL Core ===
(declare-fun has_operand (Entity Entity) Bool)
(declare-fun has_operator (Entity Entity) Bool)
(declare-fun has_value (Entity Entity) Bool)
(declare-fun in_denotation (Entity Entity) Bool)

(declare-const op_eq Entity)
(declare-const op_isPartOf Entity)
(declare-const op_isA Entity)
(declare-const op_isAnyOf Entity)
(declare-const op_isAllOf Entity)
(declare-const op_isNoneOf Entity)

(declare-fun mereological (Entity) Bool)
(declare-fun taxonomic (Entity) Bool)
(declare-const spatial Entity)
(declare-const purpose Entity)
(declare-const language Entity)
(assert (mereological spatial))
(assert (taxonomic purpose))
(assert (taxonomic language))
"""

# ============================================================
# Layer 2: Grounding rules (modular by operator)
# ============================================================

GROUND_EQ = """\
; --- eq: bidirectional ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_eq) (has_value c v) (= x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_eq) (has_value c v))
        (= x v))))
"""

GROUND_ISPARTOF = """\
; --- isPartOf: bidirectional ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isPartOf) (has_value c v)
             (mereological l) (partOf x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l)
             (has_operator c op_isPartOf) (has_value c v) (mereological l))
        (partOf x v))))
"""

GROUND_ISA = """\
; --- isA: bidirectional ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isA) (has_value c v)
             (taxonomic l) (subClassOf x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l)
             (has_operator c op_isA) (has_value c v) (taxonomic l))
        (subClassOf x v))))
"""

GROUND_ISANYOF_TAX = """\
; --- isAnyOf: if-direction only (taxonomic) ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isAnyOf) (has_value c v)
             (taxonomic l) (subClassOf x v))
        (in_denotation x c))))
"""

GROUND_ISANYOF_MEREO = """\
; --- isAnyOf: if-direction only (mereological) ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isAnyOf) (has_value c v)
             (mereological l) (partOf x v))
        (in_denotation x c))))
"""

GROUND_ISALLOF_TAX_ONLY = """\
; --- isAllOf: only-if (taxonomic) ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l)
             (has_operator c op_isAllOf) (has_value c v) (taxonomic l))
        (subClassOf x v))))
"""

GROUND_ISALLOF_MEREO_ONLY = """\
; --- isAllOf: only-if (mereological) ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l)
             (has_operator c op_isAllOf) (has_value c v) (mereological l))
        (partOf x v))))
"""

GROUND_ISNONEOF_TAX_ONLY = """\
; --- isNoneOf: only-if (taxonomic) ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l)
             (has_operator c op_isNoneOf) (has_value c v) (taxonomic l))
        (not (subClassOf x v)))))
"""

GROUND_ISNONEOF_MEREO_ONLY = """\
; --- isNoneOf: only-if (mereological) ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l)
             (has_operator c op_isNoneOf) (has_value c v) (mereological l))
        (not (partOf x v)))))
"""

# ============================================================
# Problem definitions
# ============================================================

def constraint(name, operand, operator, value):
    """Generate constraint assertions."""
    return f"""(assert (has_operand {name} {operand}))
(assert (has_operator {name} {operator}))
(assert (has_value {name} {value}))"""

def constraint_multi_value(name, operand, operator, values):
    """Generate constraint with multiple values."""
    lines = [f"(assert (has_operand {name} {operand}))",
             f"(assert (has_operator {name} {operator}))"]
    for v in values:
        lines.append(f"(assert (has_value {name} {v}))")
    return "\n".join(lines)

def conjecture_compatible(c1, c2):
    """Negated compatibility: ¬∃X(denot(X,c1) ∧ denot(X,c2))"""
    return f"""(assert (not (exists ((x Entity))
    (and (in_denotation x {c1}) (in_denotation x {c2})))))"""

def conjecture_conflict(c1, c2):
    """Negated conflict: ¬¬∃X(...) = ∃X(denot(X,c1) ∧ denot(X,c2))"""
    return f"""(assert (exists ((x Entity))
    (and (in_denotation x {c1}) (in_denotation x {c2}))))"""

def conjecture_cross_compatible(c1, c2, c3, c4):
    """Negated cross-dataspace compatibility."""
    return f"""(assert (not (and
    (exists ((x Entity)) (and (in_denotation x {c1}) (in_denotation x {c2})))
    (exists ((y Entity)) (and (in_denotation y {c3}) (in_denotation y {c4}))))))"""

def conjecture_triple_compatible(c1, c2, c3, c4, c5, c6):
    """Negated three-operand compatibility."""
    return f"""(assert (not (and
    (exists ((x Entity)) (and (in_denotation x {c1}) (in_denotation x {c2})))
    (exists ((y Entity)) (and (in_denotation y {c3}) (in_denotation y {c4})))
    (exists ((z Entity)) (and (in_denotation z {c5}) (in_denotation z {c6}))))))"""

# isAllOf if-direction (grounded per-problem)
def isallof_if_taxonomic(cname, values, operand="purpose"):
    """Grounded isAllOf if-direction for specific values."""
    conj = " ".join(f"(subClassOf x {v})" for v in values)
    return f"""(assert (forall ((x Entity))
    (=> (and {conj} (taxonomic {operand}))
        (in_denotation x {cname}))))"""

# isNoneOf if-direction (grounded per-problem)
def isnoneof_if_taxonomic(cname, values, operand="purpose"):
    """Grounded isNoneOf if-direction for specific values."""
    conj = " ".join(f"(not (subClassOf x {v}))" for v in values)
    return f"""(assert (forall ((x Entity))
    (=> (and {conj} (taxonomic {operand}))
        (in_denotation x {cname}))))"""

# isAnyOf only-if (grounded disjunction per-problem — for conflict proofs)
def isanyof_onlyif_taxonomic(cname, values):
    """Grounded isAnyOf only-if: in_denotation → subClassOf to SOME value."""
    disj = " ".join(f"(subClassOf x {v})" for v in values)
    return f"""(assert (forall ((x Entity))
    (=> (in_denotation x {cname}) (or {disj}))))"""


# ============================================================
# Problem catalog
# ============================================================

PROBLEMS = []

def add(pid, subdir, desc, kbs, grounding, declarations, constraints, conjecture, expected_smt, expected_szs):
    PROBLEMS.append({
        "id": pid, "subdir": subdir, "desc": desc,
        "kbs": kbs, "grounding": grounding,
        "declarations": declarations, "constraints": constraints,
        "conjecture": conjecture,
        "expected_smt": expected_smt, "expected_szs": expected_szs
    })

# --- Spatial (Layer 0 sanity) ---

add("ODRL010-1", "Spatial",
    "Layer 0 transitivity: partOf(bavaria, europe)",
    [GEO_KB], [],
    "", "",
    "(assert (not (partOf bavaria europe)))",
    "unsat", "Theorem")

add("ODRL011-1", "Spatial",
    "Layer 0 negative: ~partOf(germany, france)",
    [GEO_KB], [],
    "", "",
    "(assert (partOf germany france))",
    "unsat", "Theorem")

# --- Spatial (full stack) ---

SPATIAL_GROUNDING = [GROUND_EQ, GROUND_ISPARTOF]

add("ODRL012-1", "Spatial",
    "Spatial compatible: france ⊑ europe",
    [GEO_KB], SPATIAL_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "spatial", "op_isPartOf", "europe") + "\n" +
    constraint("c2", "spatial", "op_eq", "france"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

add("ODRL013-1", "Spatial",
    "Spatial conflict: germany ⊄ france",
    [GEO_KB], SPATIAL_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "spatial", "op_isPartOf", "france") + "\n" +
    constraint("c2", "spatial", "op_eq", "germany"),
    conjecture_conflict("c1", "c2"),
    "unsat", "Theorem")

add("ODRL014-1", "Spatial",
    "Spatial compatible: bavaria → germany → europe",
    [GEO_KB], SPATIAL_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "spatial", "op_isPartOf", "europe") + "\n" +
    constraint("c2", "spatial", "op_eq", "bavaria"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

add("ODRL015-1", "Spatial",
    "Spatial Unknown: missing ~partOf(bavaria, france)",
    [GEO_KB], SPATIAL_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "spatial", "op_isPartOf", "france") + "\n" +
    constraint("c2", "spatial", "op_eq", "bavaria"),
    conjecture_conflict("c1", "c2"),
    "sat", "CounterSatisfiable")

# --- Purpose: isA ---

PURPOSE_GROUNDING = [GROUND_EQ, GROUND_ISA]

add("ODRL020-1", "Purpose",
    "Taxonomic compatible: nonCommResearch ⊑ nonCommPurpose",
    [DPV_KB], PURPOSE_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_isA", "nonCommercialPurpose") + "\n" +
    constraint("c2", "purpose", "op_eq", "nonCommercialResearch"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

add("ODRL021-1", "Purpose",
    "Taxonomic Unknown: scientificResearch ⊄ nonCommPurpose",
    [DPV_KB], PURPOSE_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_isA", "nonCommercialPurpose") + "\n" +
    constraint("c2", "purpose", "op_eq", "scientificResearch"),
    conjecture_compatible("c1", "c2"),
    "sat", "CounterSatisfiable")

add("ODRL022-1", "Purpose",
    "DAG multi-parent: commResearch ⊑ commPurpose",
    [DPV_KB], PURPOSE_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_isA", "commercialPurpose") + "\n" +
    constraint("c2", "purpose", "op_eq", "commercialResearch"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

add("ODRL023-1", "Purpose",
    "Cross-branch conflict: advertising ⊄ nonCommPurpose",
    [DPV_KB], PURPOSE_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_isA", "nonCommercialPurpose") + "\n" +
    constraint("c2", "purpose", "op_eq", "advertising"),
    conjecture_conflict("c1", "c2"),
    "unsat", "Theorem")

# --- Purpose: isAnyOf ---

ANYOF_GROUNDING = [GROUND_EQ, GROUND_ISANYOF_TAX]

add("ODRL024-1", "Purpose",
    "isAnyOf compatible: advertising ⊑ marketing",
    [DPV_KB], ANYOF_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint_multi_value("c1", "purpose", "op_isAnyOf",
                           ["nonCommercialPurpose", "marketing"]) + "\n" +
    constraint("c2", "purpose", "op_eq", "advertising"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

add("ODRL025-1", "Purpose",
    "isAnyOf Unknown: commResearch not reachable",
    [DPV_KB], ANYOF_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint_multi_value("c1", "purpose", "op_isAnyOf",
                           ["nonCommercialPurpose", "marketing"]) + "\n" +
    constraint("c2", "purpose", "op_eq", "commercialResearch"),
    conjecture_compatible("c1", "c2"),
    "sat", "CounterSatisfiable")

# --- Purpose: isAllOf ---

ALLOF_GROUNDING = [GROUND_EQ, GROUND_ISALLOF_TAX_ONLY]

add("ODRL026-1", "Purpose",
    "isAllOf compatible: commResearch ⊑ R&D ∩ commPurpose",
    [DPV_KB], ALLOF_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint_multi_value("c1", "purpose", "op_isAllOf",
                           ["researchAndDevelopment", "commercialPurpose"]) + "\n" +
    isallof_if_taxonomic("c1", ["researchAndDevelopment", "commercialPurpose"]) + "\n" +
    constraint("c2", "purpose", "op_eq", "commercialResearch"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

add("ODRL027-1", "Purpose",
    "isAllOf Unknown: scientificResearch ⊄ R&D ∩ nonCommPurpose",
    [DPV_KB], ALLOF_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint_multi_value("c1", "purpose", "op_isAllOf",
                           ["researchAndDevelopment", "nonCommercialPurpose"]) + "\n" +
    isallof_if_taxonomic("c1", ["researchAndDevelopment", "nonCommercialPurpose"]) + "\n" +
    constraint("c2", "purpose", "op_eq", "scientificResearch"),
    conjecture_compatible("c1", "c2"),
    "sat", "CounterSatisfiable")

# --- Purpose: isNoneOf ---

NONEOF_GROUNDING = [GROUND_EQ, GROUND_ISNONEOF_TAX_ONLY]

add("ODRL028-1", "Purpose",
    "isNoneOf compatible: nonCommResearch ∉ {commPurpose}",
    [DPV_KB], NONEOF_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_isNoneOf", "commercialPurpose") + "\n" +
    isnoneof_if_taxonomic("c1", ["commercialPurpose"]) + "\n" +
    constraint("c2", "purpose", "op_eq", "nonCommercialResearch"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

add("ODRL029-1", "Purpose",
    "isNoneOf conflict: commResearch ∈ {commPurpose}",
    [DPV_KB], NONEOF_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_isNoneOf", "commercialPurpose") + "\n" +
    constraint("c2", "purpose", "op_eq", "commercialResearch"),
    conjecture_conflict("c1", "c2"),
    "unsat", "Theorem")

# --- Cross-Dataspace ---

CROSS_GROUNDING = [GROUND_EQ, GROUND_ISPARTOF, GROUND_ISA]

add("ODRL030-1", "CrossKB",
    "Cross-DS compatible: spatial + purpose both align",
    [GEO_KB, DPV_KB], CROSS_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)\n(declare-const c3 Entity)\n(declare-const c4 Entity)",
    constraint("c1", "spatial", "op_isPartOf", "europe") + "\n" +
    constraint("c3", "purpose", "op_isA", "researchAndDevelopment") + "\n" +
    constraint("c2", "spatial", "op_eq", "france") + "\n" +
    constraint("c4", "purpose", "op_eq", "academicResearch"),
    conjecture_cross_compatible("c1", "c2", "c3", "c4"),
    "unsat", "Theorem")

add("ODRL031-1", "CrossKB",
    "Cross-DS blocked: spatial OK, purpose conflicts",
    [GEO_KB, DPV_KB], CROSS_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)\n(declare-const c3 Entity)\n(declare-const c4 Entity)",
    constraint("c1", "spatial", "op_isPartOf", "europe") + "\n" +
    constraint("c3", "purpose", "op_isA", "nonCommercialPurpose") + "\n" +
    constraint("c2", "spatial", "op_eq", "bavaria") + "\n" +
    constraint("c4", "purpose", "op_eq", "advertising"),
    conjecture_cross_compatible("c1", "c2", "c3", "c4"),
    "sat", "CounterSatisfiable")

add("ODRL032-1", "CrossKB",
    "Cross-DS diagnosis: purpose is the blocking operand",
    [GEO_KB, DPV_KB], CROSS_GROUNDING,
    "(declare-const c3 Entity)\n(declare-const c4 Entity)",
    constraint("c3", "purpose", "op_isA", "nonCommercialPurpose") + "\n" +
    constraint("c4", "purpose", "op_eq", "advertising"),
    conjecture_conflict("c3", "c4"),
    "unsat", "Theorem")

add("ODRL033-1", "CrossKB",
    "Cross-DS double Unknown: both dimensions undecidable",
    [GEO_KB, DPV_KB], CROSS_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)\n(declare-const c3 Entity)\n(declare-const c4 Entity)",
    constraint("c1", "spatial", "op_isPartOf", "france") + "\n" +
    constraint("c3", "purpose", "op_isA", "nonCommercialPurpose") + "\n" +
    constraint("c2", "spatial", "op_eq", "bavaria") + "\n" +
    constraint("c4", "purpose", "op_eq", "scientificResearch"),
    conjecture_cross_compatible("c1", "c2", "c3", "c4"),
    "sat", "CounterSatisfiable")

# --- Adversarial: attack tests ---

# ATK-1: Reflexive self-overlap (eq X vs eq X)
add("ODRL040-1", "Adversarial",
    "ATTACK: Reflexive self-overlap (eq X vs eq X)",
    [DPV_KB], [GROUND_EQ],
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_eq", "academicResearch") + "\n" +
    constraint("c2", "purpose", "op_eq", "academicResearch"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

# ATK-2: Cross-operator composition (isA × isAnyOf)
add("ODRL041-1", "Adversarial",
    "ATTACK: Cross-operator overlap (isA vs isAnyOf)",
    [DPV_KB], [GROUND_EQ, GROUND_ISA, GROUND_ISANYOF_TAX],
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_isA", "researchAndDevelopment") + "\n" +
    constraint_multi_value("c2", "purpose", "op_isAnyOf",
                           ["commercialPurpose", "marketing"]),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

# ATK-3: isNoneOf vs isA — forced contradiction via only-if composition
add("ODRL042-1", "Adversarial",
    "ATTACK: isNoneOf vs isA — forced contradiction",
    [DPV_KB], [GROUND_EQ, GROUND_ISA, GROUND_ISNONEOF_TAX_ONLY],
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_isA", "researchAndDevelopment") + "\n" +
    constraint("c2", "purpose", "op_isNoneOf", "researchAndDevelopment"),
    conjecture_conflict("c1", "c2"),
    "unsat", "Theorem")

# ATK-4: Phantom entity via impossible isAllOf
add("ODRL043-1", "Adversarial",
    "ATTACK: Phantom entity — impossible isAllOf intersection",
    [DPV_KB], [GROUND_EQ, GROUND_ISALLOF_TAX_ONLY],
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint_multi_value("c1", "purpose", "op_isAllOf",
                           ["commercialPurpose", "nonCommercialPurpose"]) + "\n" +
    isallof_if_taxonomic("c1", ["commercialPurpose", "nonCommercialPurpose"]) + "\n" +
    constraint("c2", "purpose", "op_eq", "commercialResearch"),
    conjecture_compatible("c1", "c2"),
    "sat", "CounterSatisfiable")

# ATK-5: Operand type mismatch — isPartOf on taxonomic operand
# Need GEO_KB to declare partOf, even though the attack is about purpose
add("ODRL044-1", "Adversarial",
    "ATTACK: Type guard — isPartOf on taxonomic operand",
    [GEO_KB, DPV_KB], [GROUND_EQ, GROUND_ISPARTOF],
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_isPartOf", "researchAndDevelopment") + "\n" +
    constraint("c2", "purpose", "op_eq", "academicResearch"),
    conjecture_compatible("c1", "c2"),
    "sat", "CounterSatisfiable")

# ATK-6a: isNoneOf + KB gap — false Unknown (missing negative fact)
add("ODRL045-1", "Adversarial",
    "ATTACK: isNoneOf KB gap — false Unknown (conservative)",
    [DPV_KB], [GROUND_EQ, GROUND_ISNONEOF_TAX_ONLY],
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_isNoneOf", "commercialPurpose") + "\n" +
    isnoneof_if_taxonomic("c1", ["commercialPurpose"]) + "\n" +
    constraint("c2", "purpose", "op_eq", "scientificResearch"),
    conjecture_compatible("c1", "c2"),
    "sat", "CounterSatisfiable")

# ATK-6b: Same as ATK-6a but with KB enrichment — resolves to Compatible
DPV_KB_ENRICHED = DPV_KB + """
; === KB ENRICHMENT: missing negative fact ===
(assert (not (subClassOf scientificResearch commercialPurpose)))
"""

add("ODRL045-2", "Adversarial",
    "ATTACK RESOLUTION: isNoneOf + enriched KB — false Unknown fixed",
    [DPV_KB_ENRICHED], [GROUND_EQ, GROUND_ISNONEOF_TAX_ONLY],
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "purpose", "op_isNoneOf", "commercialPurpose") + "\n" +
    isnoneof_if_taxonomic("c1", ["commercialPurpose"]) + "\n" +
    constraint("c2", "purpose", "op_eq", "scientificResearch"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

# --- Language domain (BCP 47) ---

LANGUAGE_GROUNDING = [GROUND_EQ, GROUND_ISA]

# ODRL050: BSB permits German, Austrian library requests de-AT → compatible
add("ODRL050-1", "Language",
    "Language compatible: de_AT ⊑ de (regional refinement)",
    [LNG_KB], LANGUAGE_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "language", "op_isA", "de") + "\n" +
    constraint("c2", "language", "op_eq", "de_AT"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

# ODRL051: HK permits German, Louvre requests French → conflict
add("ODRL051-1", "Language",
    "Language conflict: fr ⊄ de (cross-branch disjoint)",
    [LNG_KB], LANGUAGE_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "language", "op_isA", "de") + "\n" +
    constraint("c2", "language", "op_eq", "fr"),
    conjecture_conflict("c1", "c2"),
    "unsat", "Theorem")

# ODRL052: HK permits {de, en}, Louvre requests fr → conflict (union doesn't cover)
add("ODRL052-1", "Language",
    "Language isAnyOf conflict: fr ∉ {de, en}↓",
    [LNG_KB], [GROUND_EQ, GROUND_ISANYOF_TAX],
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint_multi_value("c1", "language", "op_isAnyOf", ["de", "en"]) + "\n" +
    isanyof_onlyif_taxonomic("c1", ["de", "en"]) + "\n" +
    constraint("c2", "language", "op_eq", "fr"),
    conjecture_conflict("c1", "c2"),
    "unsat", "Theorem")

# ODRL053: BSB Arabic collection, Egyptian Arabic request → compatible
add("ODRL053-1", "Language",
    "Language compatible: arz ⊑ ar (macrolanguage)",
    [LNG_KB], LANGUAGE_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint("c1", "language", "op_isA", "ar") + "\n" +
    constraint("c2", "language", "op_eq", "arz"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

# ODRL054: HK permits {de, en}, British Museum requests en_GB → compatible
add("ODRL054-1", "Language",
    "Language isAnyOf compatible: en_GB ⊑ en ∈ {de, en}↓",
    [LNG_KB], [GROUND_EQ, GROUND_ISANYOF_TAX],
    "(declare-const c1 Entity)\n(declare-const c2 Entity)",
    constraint_multi_value("c1", "language", "op_isAnyOf", ["de", "en"]) + "\n" +
    constraint("c2", "language", "op_eq", "en_GB"),
    conjecture_compatible("c1", "c2"),
    "unsat", "Theorem")

# ODRL055: Three-KB cross-dataspace (spatial + purpose + language)
TRIPLE_GROUNDING = [GROUND_EQ, GROUND_ISPARTOF, GROUND_ISA]

add("ODRL055-1", "Language",
    "Three-KB cross-dataspace: language blocks (fr ⊄ de)",
    [GEO_KB, DPV_KB, LNG_KB_FACTS], TRIPLE_GROUNDING,
    "(declare-const c1 Entity)\n(declare-const c2 Entity)\n" +
    "(declare-const c3 Entity)\n(declare-const c4 Entity)\n" +
    "(declare-const c5 Entity)\n(declare-const c6 Entity)",
    constraint("c1", "spatial", "op_isPartOf", "europe") + "\n" +
    constraint("c3", "purpose", "op_isA", "nonCommercialPurpose") + "\n" +
    constraint("c5", "language", "op_isA", "de") + "\n" +
    constraint("c2", "spatial", "op_eq", "france") + "\n" +
    constraint("c4", "purpose", "op_eq", "scientificResearch") + "\n" +
    constraint("c6", "language", "op_eq", "fr"),
    conjecture_triple_compatible("c1", "c2", "c3", "c4", "c5", "c6"),
    "sat", "CounterSatisfiable")

# ODRL056: Diagnostic — language is the blocking operand
add("ODRL056-1", "Language",
    "Diagnostic: language is the blocking operand (fr ⊄ de)",
    [LNG_KB], LANGUAGE_GROUNDING,
    "(declare-const c5 Entity)\n(declare-const c6 Entity)",
    constraint("c5", "language", "op_isA", "de") + "\n" +
    constraint("c6", "language", "op_eq", "fr"),
    conjecture_conflict("c5", "c6"),
    "unsat", "Theorem")


# ============================================================
# File generation
# ============================================================

def generate_smt2(prob):
    """Generate a complete SMT-LIB2 file."""
    parts = []
    parts.append(f"; {prob['id']}.smt2 — {prob['desc']}")
    parts.append(f"; Expected: {prob['expected_smt']} (SZS: {prob['expected_szs']})")
    parts.append("")
    parts.append(PREAMBLE)

    # Layer 0
    for kb in prob["kbs"]:
        parts.append(kb)

    # Layer 1 (only if we need constraint structure)
    if prob["grounding"]:
        parts.append(LAYER1)

    # Layer 2
    for g in prob["grounding"]:
        parts.append(g)

    # Declarations
    if prob["declarations"]:
        parts.append(f"\n; === Problem: {prob['id']} ===")
        parts.append(prob["declarations"])

    # Constraints
    if prob["constraints"]:
        parts.append(prob["constraints"])

    # Conjecture
    parts.append("")
    parts.append(prob["conjecture"])
    parts.append("")
    parts.append("(check-sat)")

    return "\n".join(parts)


def run_prover(cmd, filepath, timeout=30):
    """Run a prover and return (result, time_s)."""
    try:
        start = time.time()
        result = subprocess.run(
            cmd + [filepath],
            capture_output=True, text=True, timeout=timeout
        )
        elapsed = time.time() - start
        output = result.stdout.strip().split("\n")[0].strip()
        return output, elapsed
    except subprocess.TimeoutExpired:
        return "timeout", timeout
    except FileNotFoundError:
        return "not_found", 0


def main():
    run = "--run" in sys.argv
    use_cvc5 = "--cvc5" in sys.argv

    # Generate all files
    for prob in PROBLEMS:
        subdir = os.path.join(SMT_DIR, prob["subdir"])
        os.makedirs(subdir, exist_ok=True)
        filepath = os.path.join(subdir, f"{prob['id']}.smt2")
        content = generate_smt2(prob)
        with open(filepath, "w") as f:
            f.write(content)
    print(f"Generated {len(PROBLEMS)} SMT-LIB2 files in {SMT_DIR}/")

    if not run:
        print("Use --run to execute Z3 on all files.")
        return

    # Run Z3
    print()
    print(f"{'Problem':<14} {'Expected':>10} {'Z3':>10} {'Z3 time':>10}", end="")
    if use_cvc5:
        print(f" {'CVC5':>10} {'CVC5 time':>10}", end="")
    print(f"  {'SZS':>16}  {'Match':>5}")
    print("-" * (80 if not use_cvc5 else 105))

    all_match = True
    for prob in PROBLEMS:
        filepath = os.path.join(SMT_DIR, prob["subdir"], f"{prob['id']}.smt2")
        z3_result, z3_time = run_prover(["z3"], filepath)

        match = "✓" if z3_result == prob["expected_smt"] else "✗"
        if z3_result != prob["expected_smt"]:
            all_match = False

        print(f"{prob['id']:<14} {prob['expected_smt']:>10} {z3_result:>10} {z3_time:>9.3f}s", end="")

        if use_cvc5:
            cvc5_result, cvc5_time = run_prover(["cvc5", "--lang=smt2"], filepath)
            print(f" {cvc5_result:>10} {cvc5_time:>9.3f}s", end="")

        print(f"  {prob['expected_szs']:>16}  {match:>5}")

    print()
    if all_match:
        print("All results match expected verdicts. ✓")
    else:
        print("WARNING: Some results did not match! ✗")


if __name__ == "__main__":
    main()