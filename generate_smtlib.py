#!/usr/bin/env python3
"""
Generate SMT-LIB2 encodings for all TPTP-ODRL benchmarks and run Z3.
49 problems across 7 categories: Spatial, Purpose, CrossKB, Adversarial,
Language, Alignment, Runtime.

Usage:
    python3 generate_smtlib.py              # generate all .smt2 files
    python3 generate_smtlib.py --run        # generate + run z3 on all
    python3 generate_smtlib.py --run --cvc5 # also run cvc5 if available
"""
import os, subprocess, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
SMT_DIR = os.path.join(BASE, "SMT/ODRL/KBGrounding")

PREAMBLE = "(set-logic UF)\n(declare-sort Entity 0)\n"

# ============================================================
# Layer 0: Original KBs
# ============================================================

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
; === Layer 0: DPV Purpose Taxonomy ===
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
(assert (subClassOf commercialPurpose purpose_top))
(assert (subClassOf nonCommercialPurpose purpose_top))
(assert (subClassOf researchAndDevelopment purpose_top))
(assert (subClassOf marketing purpose_top))
(assert (subClassOf academicResearch researchAndDevelopment))
(assert (subClassOf scientificResearch researchAndDevelopment))
(assert (subClassOf commercialResearch researchAndDevelopment))
(assert (subClassOf nonCommercialResearch researchAndDevelopment))
(assert (subClassOf commercialResearch commercialPurpose))
(assert (subClassOf nonCommercialResearch nonCommercialPurpose))
(assert (subClassOf advertising marketing))
(assert (subClassOf directMarketing marketing))
(assert (not (subClassOf commercialPurpose nonCommercialPurpose)))
(assert (not (subClassOf nonCommercialPurpose commercialPurpose)))
(assert (not (subClassOf marketing nonCommercialPurpose)))
(assert (not (subClassOf advertising nonCommercialPurpose)))
(assert (not (subClassOf nonCommercialResearch commercialPurpose)))
"""

DPV_KB_ENRICHED = DPV_KB + "(assert (not (subClassOf scientificResearch commercialPurpose)))\n"

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
(assert (not (subClassOf de en)))  (assert (not (subClassOf en de)))
(assert (not (subClassOf de fr)))  (assert (not (subClassOf fr de)))
(assert (not (subClassOf en fr)))  (assert (not (subClassOf fr en)))
(assert (not (subClassOf de ar)))  (assert (not (subClassOf ar de)))
(assert (not (subClassOf en ar)))  (assert (not (subClassOf ar en)))
(assert (not (subClassOf fr ar)))  (assert (not (subClassOf ar fr)))
"""

LNG_KB_FACTS = """\
; === Layer 0: BCP 47 (facts only, no subClassOf decl) ===
(declare-const de Entity) (declare-const de_AT Entity) (declare-const de_CH Entity)
(declare-const en Entity) (declare-const en_US Entity) (declare-const en_GB Entity)
(declare-const fr Entity) (declare-const ar Entity) (declare-const arb Entity) (declare-const arz Entity)
(assert (subClassOf de_AT de)) (assert (subClassOf de_CH de))
(assert (subClassOf en_US en)) (assert (subClassOf en_GB en))
(assert (subClassOf arb ar))   (assert (subClassOf arz ar))
(assert (not (subClassOf de en)))  (assert (not (subClassOf en de)))
(assert (not (subClassOf de fr)))  (assert (not (subClassOf fr de)))
(assert (not (subClassOf en fr)))  (assert (not (subClassOf fr en)))
(assert (not (subClassOf de ar)))  (assert (not (subClassOf ar de)))
(assert (not (subClassOf en ar)))  (assert (not (subClassOf ar en)))
(assert (not (subClassOf fr ar)))  (assert (not (subClassOf ar fr)))
"""

# ============================================================
# Layer 0: Alternative KBs (alignment benchmarks)
# ============================================================

GEO1_KB = """\
; === Layer 0: ISO 3166 Spatial KB (countries only) ===
(declare-fun partOf (Entity Entity) Bool)
(declare-const eur Entity) (declare-const deu Entity) (declare-const fra Entity)
(assert (forall ((x Entity)) (partOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (partOf x y) (partOf y z)) (partOf x z))))
(assert (partOf deu eur)) (assert (partOf fra eur))
(assert (not (partOf deu fra))) (assert (not (partOf fra deu)))
"""

DPV1_KB = """\
; === Layer 0: GDPR-based Purpose Taxonomy ===
(declare-fun subClassOf (Entity Entity) Bool)
(declare-const zweck Entity) (declare-const kommerziellerZweck Entity)
(declare-const nichtKommerziellerZweck Entity) (declare-const forschungUndEntwicklung Entity)
(declare-const kommerzielleForschung Entity) (declare-const nichtKommerzielleForschung Entity)
(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))
(assert (subClassOf kommerziellerZweck zweck))
(assert (subClassOf nichtKommerziellerZweck zweck))
(assert (subClassOf forschungUndEntwicklung zweck))
(assert (subClassOf kommerzielleForschung kommerziellerZweck))
(assert (subClassOf kommerzielleForschung forschungUndEntwicklung))
(assert (subClassOf nichtKommerzielleForschung nichtKommerziellerZweck))
(assert (subClassOf nichtKommerzielleForschung forschungUndEntwicklung))
(assert (not (subClassOf kommerziellerZweck nichtKommerziellerZweck)))
(assert (not (subClassOf nichtKommerziellerZweck kommerziellerZweck)))
(assert (not (subClassOf kommerzielleForschung nichtKommerziellerZweck)))
(assert (not (subClassOf nichtKommerzielleForschung kommerziellerZweck)))
"""

DPV1_KB_FACTS = """\
; === Layer 0: GDPR Purpose (with subClassOf for standalone use) ===
(declare-fun subClassOf (Entity Entity) Bool)
(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))
(declare-const zweck Entity) (declare-const kommerziellerZweck Entity)
(declare-const nichtKommerziellerZweck Entity) (declare-const forschungUndEntwicklung Entity)
(declare-const kommerzielleForschung Entity) (declare-const nichtKommerzielleForschung Entity)
(assert (subClassOf kommerziellerZweck zweck))
(assert (subClassOf nichtKommerziellerZweck zweck))
(assert (subClassOf forschungUndEntwicklung zweck))
(assert (subClassOf kommerzielleForschung kommerziellerZweck))
(assert (subClassOf kommerzielleForschung forschungUndEntwicklung))
(assert (subClassOf nichtKommerzielleForschung nichtKommerziellerZweck))
(assert (subClassOf nichtKommerzielleForschung forschungUndEntwicklung))
(assert (not (subClassOf kommerziellerZweck nichtKommerziellerZweck)))
(assert (not (subClassOf nichtKommerziellerZweck kommerziellerZweck)))
(assert (not (subClassOf kommerzielleForschung nichtKommerziellerZweck)))
(assert (not (subClassOf nichtKommerzielleForschung kommerziellerZweck)))
"""

LNG1_KB = """\
; === Layer 0: ISO 639-3 Language KB (no regional variants) ===
(declare-fun subClassOf (Entity Entity) Bool)
(declare-const deu Entity) (declare-const eng Entity) (declare-const fra Entity)
(declare-const ara Entity) (declare-const arb Entity) (declare-const arz Entity)
(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))
(assert (subClassOf arb ara)) (assert (subClassOf arz ara))
(assert (not (subClassOf deu eng))) (assert (not (subClassOf eng deu)))
(assert (not (subClassOf deu fra))) (assert (not (subClassOf fra deu)))
(assert (not (subClassOf deu ara))) (assert (not (subClassOf ara deu)))
(assert (not (subClassOf eng fra))) (assert (not (subClassOf fra eng)))
(assert (not (subClassOf eng ara))) (assert (not (subClassOf ara eng)))
(assert (not (subClassOf fra ara))) (assert (not (subClassOf ara fra)))
"""

LNG1_KB_FACTS = """\
; === Layer 0: ISO 639-3 (facts only, no subClassOf decl) ===
(declare-const deu Entity) (declare-const eng Entity) (declare-const fra Entity)
(declare-const ara Entity) (declare-const arb Entity) (declare-const arz Entity)
(assert (subClassOf arb ara)) (assert (subClassOf arz ara))
(assert (not (subClassOf deu eng))) (assert (not (subClassOf eng deu)))
(assert (not (subClassOf deu fra))) (assert (not (subClassOf fra deu)))
(assert (not (subClassOf deu ara))) (assert (not (subClassOf ara deu)))
(assert (not (subClassOf eng fra))) (assert (not (subClassOf fra eng)))
(assert (not (subClassOf eng ara))) (assert (not (subClassOf ara eng)))
(assert (not (subClassOf fra ara))) (assert (not (subClassOf ara fra)))
"""

# For use with GEO1_KB (which already declares deu, fra)
LNG1_KB_FACTS_NO_DUP = """\
; === Layer 0: ISO 639-3 (facts only, no deu/fra — declared in GEO1) ===
(declare-const eng Entity)
(declare-const ara Entity) (declare-const arb Entity) (declare-const arz Entity)
(assert (subClassOf arb ara)) (assert (subClassOf arz ara))
(assert (not (subClassOf deu eng))) (assert (not (subClassOf eng deu)))
(assert (not (subClassOf deu fra))) (assert (not (subClassOf fra deu)))
(assert (not (subClassOf deu ara))) (assert (not (subClassOf ara deu)))
(assert (not (subClassOf eng fra))) (assert (not (subClassOf fra eng)))
(assert (not (subClassOf eng ara))) (assert (not (subClassOf ara eng)))
(assert (not (subClassOf fra ara))) (assert (not (subClassOf ara fra)))
"""

# ============================================================
# Layer 1 + Layer 2
# ============================================================

LAYER1 = """\
; === Layer 1: ODRL Core ===
(declare-fun has_operand (Entity Entity) Bool)
(declare-fun has_operator (Entity Entity) Bool)
(declare-fun has_value (Entity Entity) Bool)
(declare-fun in_denotation (Entity Entity) Bool)
(declare-const op_eq Entity) (declare-const op_isPartOf Entity)
(declare-const op_isA Entity) (declare-const op_isAnyOf Entity)
(declare-const op_isAllOf Entity) (declare-const op_isNoneOf Entity)
(declare-fun mereological (Entity) Bool)
(declare-fun taxonomic (Entity) Bool)
(declare-const spatial Entity) (declare-const purpose Entity) (declare-const language Entity)
(assert (mereological spatial))
(assert (taxonomic purpose))
(assert (taxonomic language))
"""

GROUND_EQ = """\
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_eq) (has_value c v) (= x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_eq) (has_value c v))
        (= x v))))
"""
GROUND_ISPARTOF = """\
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isPartOf) (has_value c v) (mereological l) (partOf x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_isPartOf) (has_value c v) (mereological l))
        (partOf x v))))
"""
GROUND_ISA = """\
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isA) (has_value c v) (taxonomic l) (subClassOf x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_isA) (has_value c v) (taxonomic l))
        (subClassOf x v))))
"""
GROUND_ISANYOF_TAX = """\
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isAnyOf) (has_value c v) (taxonomic l) (subClassOf x v))
        (in_denotation x c))))
"""
GROUND_ISALLOF_TAX_ONLY = """\
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_isAllOf) (has_value c v) (taxonomic l))
        (subClassOf x v))))
"""
GROUND_ISNONEOF_TAX_ONLY = """\
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_isNoneOf) (has_value c v) (taxonomic l))
        (not (subClassOf x v)))))
"""

# ============================================================
# Helpers
# ============================================================

def con(name, operand, operator, value):
    return f"(assert (has_operand {name} {operand}))\n(assert (has_operator {name} {operator}))\n(assert (has_value {name} {value}))"

def con_multi(name, operand, operator, values):
    lines = [f"(assert (has_operand {name} {operand}))", f"(assert (has_operator {name} {operator}))"]
    for v in values: lines.append(f"(assert (has_value {name} {v}))")
    return "\n".join(lines)

def compat(c1, c2):
    return f"(assert (not (exists ((x Entity)) (and (in_denotation x {c1}) (in_denotation x {c2})))))"

def conflict(c1, c2):
    return f"(assert (exists ((x Entity)) (and (in_denotation x {c1}) (in_denotation x {c2}))))"

def cross2(c1, c2, c3, c4):
    return f"(assert (not (and\n  (exists ((x Entity)) (and (in_denotation x {c1}) (in_denotation x {c2})))\n  (exists ((y Entity)) (and (in_denotation y {c3}) (in_denotation y {c4}))))))"

def cross3(c1, c2, c3, c4, c5, c6):
    return f"(assert (not (and\n  (exists ((x Entity)) (and (in_denotation x {c1}) (in_denotation x {c2})))\n  (exists ((y Entity)) (and (in_denotation y {c3}) (in_denotation y {c4})))\n  (exists ((z Entity)) (and (in_denotation z {c5}) (in_denotation z {c6}))))))"

def witness(e, c1, c2):
    return f"(assert (not (and (in_denotation {e} {c1}) (in_denotation {e} {c2}))))"

def rejection(e, c1):
    return f"(assert (in_denotation {e} {c1}))"

def allof_if(c, vals, op="purpose"):
    cj = " ".join(f"(subClassOf x {v})" for v in vals)
    return f"(assert (forall ((x Entity)) (=> (and {cj} (taxonomic {op})) (in_denotation x {c}))))"

def noneof_if(c, vals, op="purpose"):
    cj = " ".join(f"(not (subClassOf x {v}))" for v in vals)
    return f"(assert (forall ((x Entity)) (=> (and {cj} (taxonomic {op})) (in_denotation x {c}))))"

def anyof_only(c, vals):
    dj = " ".join(f"(subClassOf x {v})" for v in vals)
    return f"(assert (forall ((x Entity)) (=> (in_denotation x {c}) (or {dj}))))"

# --- OR: or(c1,c2) compatible/conflict with c3 ---
def or_compat(c1, c2, c3):
    """Negated: ¬(∃x(d(x,c1)∧d(x,c3)) ∨ ∃y(d(y,c2)∧d(y,c3))). unsat=Compatible."""
    return f"""(assert (not (or
  (exists ((x Entity)) (and (in_denotation x {c1}) (in_denotation x {c3})))
  (exists ((y Entity)) (and (in_denotation y {c2}) (in_denotation y {c3}))))))"""

def or_conflict(c1, c2, c3):
    """Asserted: ∃x(d(x,c1)∧d(x,c3)) ∨ ∃y(d(y,c2)∧d(y,c3)). unsat=Conflict."""
    return f"""(assert (or
  (exists ((x Entity)) (and (in_denotation x {c1}) (in_denotation x {c3})))
  (exists ((y Entity)) (and (in_denotation y {c2}) (in_denotation y {c3})))))"""

def or_cross_compat(cs, co, c1, c2, c3):
    """spatial AND or(purpose1, purpose2): ¬(∃x(spatial) ∧ (∃y(p1∧p3) ∨ ∃z(p2∧p3)))."""
    return f"""(assert (not (and
  (exists ((x Entity)) (and (in_denotation x {cs}) (in_denotation x {co})))
  (or
    (exists ((y Entity)) (and (in_denotation y {c1}) (in_denotation y {c3})))
    (exists ((z Entity)) (and (in_denotation z {c2}) (in_denotation z {c3})))))))"""

# --- XONE: xone(c1,c2) compatible/conflict with c3 ---
def xone_compat(c1, c2, c3):
    """Negated: ¬(∃x(d1∧¬d2∧d3) ∨ ∃y(d2∧¬d1∧d3)). unsat=Compatible."""
    return f"""(assert (not (or
  (exists ((x Entity)) (and (in_denotation x {c1}) (not (in_denotation x {c2})) (in_denotation x {c3})))
  (exists ((y Entity)) (and (in_denotation y {c2}) (not (in_denotation y {c1})) (in_denotation y {c3}))))))"""

def xone_conflict(c1, c2, c3):
    """Asserted: ∃x(d1∧¬d2∧d3) ∨ ∃y(d2∧¬d1∧d3). unsat=Conflict."""
    return f"""(assert (or
  (exists ((x Entity)) (and (in_denotation x {c1}) (not (in_denotation x {c2})) (in_denotation x {c3})))
  (exists ((y Entity)) (and (in_denotation y {c2}) (not (in_denotation y {c1})) (in_denotation y {c3})))))"""

def d(*names): return "\n".join(f"(declare-const {n} Entity)" for n in names)

# ============================================================
# Catalog
# ============================================================
P = []
def add(pid, sub, desc, kbs, gr, decls, cons, conj, esmt, eszs):
    P.append(dict(id=pid, sub=sub, desc=desc, kbs=kbs, gr=gr, decls=decls, cons=cons, conj=conj, esmt=esmt, eszs=eszs))

SG = [GROUND_EQ, GROUND_ISPARTOF]
PG = [GROUND_EQ, GROUND_ISA]
AG = [GROUND_EQ, GROUND_ISANYOF_TAX]
LG = [GROUND_EQ, GROUND_ISALLOF_TAX_ONLY]
NG = [GROUND_EQ, GROUND_ISNONEOF_TAX_ONLY]
TG = [GROUND_EQ, GROUND_ISPARTOF, GROUND_ISA]

# --- Spatial 010-015 ---
add("ODRL010-1","Spatial","L0: partOf(bavaria,europe)",
    [GEO_KB],[],  "","", "(assert (not (partOf bavaria europe)))","unsat","Theorem")
add("ODRL011-1","Spatial","L0: ~partOf(germany,france)",
    [GEO_KB],[],  "","", "(assert (partOf germany france))","unsat","Theorem")
add("ODRL012-1","Spatial","Compatible: france ⊑ europe",
    [GEO_KB],SG, d("c1","c2"), con("c1","spatial","op_isPartOf","europe")+"\n"+con("c2","spatial","op_eq","france"), compat("c1","c2"),"unsat","Theorem")
add("ODRL013-1","Spatial","Conflict: germany ⊄ france",
    [GEO_KB],SG, d("c1","c2"), con("c1","spatial","op_isPartOf","france")+"\n"+con("c2","spatial","op_eq","germany"), conflict("c1","c2"),"unsat","Theorem")
add("ODRL014-1","Spatial","Compatible: bavaria→germany→europe",
    [GEO_KB],SG, d("c1","c2"), con("c1","spatial","op_isPartOf","europe")+"\n"+con("c2","spatial","op_eq","bavaria"), compat("c1","c2"),"unsat","Theorem")
add("ODRL015-1","Spatial","Unknown: ~partOf(bavaria,france) missing",
    [GEO_KB],SG, d("c1","c2"), con("c1","spatial","op_isPartOf","france")+"\n"+con("c2","spatial","op_eq","bavaria"), conflict("c1","c2"),"sat","CounterSatisfiable")

# --- Purpose 020-029 ---
add("ODRL020-1","Purpose","Compatible: nonCommRes ⊑ nonComm",    [DPV_KB],PG,d("c1","c2"),con("c1","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c2","purpose","op_eq","nonCommercialResearch"),compat("c1","c2"),"unsat","Theorem")
add("ODRL021-1","Purpose","Unknown: sciRes ⊑? nonComm",         [DPV_KB],PG,d("c1","c2"),con("c1","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c2","purpose","op_eq","scientificResearch"),compat("c1","c2"),"sat","CounterSatisfiable")
add("ODRL022-1","Purpose","Compatible: commRes ⊑ commPurp (DAG)",[DPV_KB],PG,d("c1","c2"),con("c1","purpose","op_isA","commercialPurpose")+"\n"+con("c2","purpose","op_eq","commercialResearch"),compat("c1","c2"),"unsat","Theorem")
add("ODRL023-1","Purpose","Conflict: advertising ⊄ nonComm",    [DPV_KB],PG,d("c1","c2"),con("c1","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c2","purpose","op_eq","advertising"),conflict("c1","c2"),"unsat","Theorem")
add("ODRL024-1","Purpose","isAnyOf compat: advert ⊑ marketing", [DPV_KB],AG,d("c1","c2"),con_multi("c1","purpose","op_isAnyOf",["nonCommercialPurpose","marketing"])+"\n"+con("c2","purpose","op_eq","advertising"),compat("c1","c2"),"unsat","Theorem")
add("ODRL025-1","Purpose","isAnyOf Unknown: commRes unreachable",[DPV_KB],AG,d("c1","c2"),con_multi("c1","purpose","op_isAnyOf",["nonCommercialPurpose","marketing"])+"\n"+con("c2","purpose","op_eq","commercialResearch"),compat("c1","c2"),"sat","CounterSatisfiable")
add("ODRL026-1","Purpose","isAllOf compat: commRes ⊑ R&D∩comm", [DPV_KB],LG,d("c1","c2"),con_multi("c1","purpose","op_isAllOf",["researchAndDevelopment","commercialPurpose"])+"\n"+allof_if("c1",["researchAndDevelopment","commercialPurpose"])+"\n"+con("c2","purpose","op_eq","commercialResearch"),compat("c1","c2"),"unsat","Theorem")
add("ODRL027-1","Purpose","isAllOf Unknown: sciRes ⊄ R&D∩nonC", [DPV_KB],LG,d("c1","c2"),con_multi("c1","purpose","op_isAllOf",["researchAndDevelopment","nonCommercialPurpose"])+"\n"+allof_if("c1",["researchAndDevelopment","nonCommercialPurpose"])+"\n"+con("c2","purpose","op_eq","scientificResearch"),compat("c1","c2"),"sat","CounterSatisfiable")
add("ODRL028-1","Purpose","isNoneOf compat: nonCommRes ∉ {comm}",[DPV_KB],NG,d("c1","c2"),con("c1","purpose","op_isNoneOf","commercialPurpose")+"\n"+noneof_if("c1",["commercialPurpose"])+"\n"+con("c2","purpose","op_eq","nonCommercialResearch"),compat("c1","c2"),"unsat","Theorem")
add("ODRL029-1","Purpose","isNoneOf conflict: commRes ∈ {comm}",[DPV_KB],NG,d("c1","c2"),con("c1","purpose","op_isNoneOf","commercialPurpose")+"\n"+con("c2","purpose","op_eq","commercialResearch"),conflict("c1","c2"),"unsat","Theorem")

# --- CrossKB 030-033 ---
add("ODRL030-1","CrossKB","Cross-DS compat: spatial+purpose",   [GEO_KB,DPV_KB],TG,d("c1","c2","c3","c4"),con("c1","spatial","op_isPartOf","europe")+"\n"+con("c3","purpose","op_isA","researchAndDevelopment")+"\n"+con("c2","spatial","op_eq","france")+"\n"+con("c4","purpose","op_eq","academicResearch"),cross2("c1","c2","c3","c4"),"unsat","Theorem")
add("ODRL031-1","CrossKB","Cross-DS blocked: purpose conflicts", [GEO_KB,DPV_KB],TG,d("c1","c2","c3","c4"),con("c1","spatial","op_isPartOf","europe")+"\n"+con("c3","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c2","spatial","op_eq","bavaria")+"\n"+con("c4","purpose","op_eq","advertising"),cross2("c1","c2","c3","c4"),"sat","CounterSatisfiable")
add("ODRL032-1","CrossKB","Diagnosis: purpose blocks",          [GEO_KB,DPV_KB],TG,d("c3","c4"),con("c3","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c4","purpose","op_eq","advertising"),conflict("c3","c4"),"unsat","Theorem")
add("ODRL033-1","CrossKB","Cross-DS double Unknown",             [GEO_KB,DPV_KB],TG,d("c1","c2","c3","c4"),con("c1","spatial","op_isPartOf","france")+"\n"+con("c3","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c2","spatial","op_eq","bavaria")+"\n"+con("c4","purpose","op_eq","scientificResearch"),cross2("c1","c2","c3","c4"),"sat","CounterSatisfiable")

# --- Adversarial 040-045 ---
add("ODRL040-1","Adversarial","ATK-1: Reflexive self-overlap",              [DPV_KB],[GROUND_EQ],d("c1","c2"),con("c1","purpose","op_eq","academicResearch")+"\n"+con("c2","purpose","op_eq","academicResearch"),compat("c1","c2"),"unsat","Theorem")
add("ODRL041-1","Adversarial","ATK-2: Cross-operator (isA×isAnyOf)",        [DPV_KB],[GROUND_EQ,GROUND_ISA,GROUND_ISANYOF_TAX],d("c1","c2"),con("c1","purpose","op_isA","researchAndDevelopment")+"\n"+con_multi("c2","purpose","op_isAnyOf",["commercialPurpose","marketing"]),compat("c1","c2"),"unsat","Theorem")
add("ODRL042-1","Adversarial","ATK-3: isNoneOf vs isA contradiction",       [DPV_KB],[GROUND_EQ,GROUND_ISA,GROUND_ISNONEOF_TAX_ONLY],d("c1","c2"),con("c1","purpose","op_isA","researchAndDevelopment")+"\n"+con("c2","purpose","op_isNoneOf","researchAndDevelopment"),conflict("c1","c2"),"unsat","Theorem")
add("ODRL043-1","Adversarial","ATK-4: Phantom entity (impossible isAllOf)", [DPV_KB],[GROUND_EQ,GROUND_ISALLOF_TAX_ONLY],d("c1","c2"),con_multi("c1","purpose","op_isAllOf",["commercialPurpose","nonCommercialPurpose"])+"\n"+allof_if("c1",["commercialPurpose","nonCommercialPurpose"])+"\n"+con("c2","purpose","op_eq","commercialResearch"),compat("c1","c2"),"sat","CounterSatisfiable")
add("ODRL044-1","Adversarial","ATK-5: Type guard (isPartOf on taxonomic)",  [GEO_KB,DPV_KB],[GROUND_EQ,GROUND_ISPARTOF],d("c1","c2"),con("c1","purpose","op_isPartOf","researchAndDevelopment")+"\n"+con("c2","purpose","op_eq","academicResearch"),compat("c1","c2"),"sat","CounterSatisfiable")
add("ODRL045-1","Adversarial","ATK-6a: KB gap (missing negative)",          [DPV_KB],NG,d("c1","c2"),con("c1","purpose","op_isNoneOf","commercialPurpose")+"\n"+noneof_if("c1",["commercialPurpose"])+"\n"+con("c2","purpose","op_eq","scientificResearch"),compat("c1","c2"),"sat","CounterSatisfiable")
add("ODRL045-2","Adversarial","ATK-6b: KB enrichment resolves gap",         [DPV_KB_ENRICHED],NG,d("c1","c2"),con("c1","purpose","op_isNoneOf","commercialPurpose")+"\n"+noneof_if("c1",["commercialPurpose"])+"\n"+con("c2","purpose","op_eq","scientificResearch"),compat("c1","c2"),"unsat","Theorem")

# --- Language 050-056 ---
add("ODRL050-1","Language","Compatible: de_AT ⊑ de",            [LNG_KB],PG,d("c1","c2"),con("c1","language","op_isA","de")+"\n"+con("c2","language","op_eq","de_AT"),compat("c1","c2"),"unsat","Theorem")
add("ODRL051-1","Language","Conflict: fr ⊄ de",                 [LNG_KB],PG,d("c1","c2"),con("c1","language","op_isA","de")+"\n"+con("c2","language","op_eq","fr"),conflict("c1","c2"),"unsat","Theorem")
add("ODRL052-1","Language","isAnyOf conflict: fr ∉ {de,en}↓",   [LNG_KB],AG,d("c1","c2"),con_multi("c1","language","op_isAnyOf",["de","en"])+"\n"+anyof_only("c1",["de","en"])+"\n"+con("c2","language","op_eq","fr"),conflict("c1","c2"),"unsat","Theorem")
add("ODRL053-1","Language","Compatible: arz ⊑ ar (macrolang)",  [LNG_KB],PG,d("c1","c2"),con("c1","language","op_isA","ar")+"\n"+con("c2","language","op_eq","arz"),compat("c1","c2"),"unsat","Theorem")
add("ODRL054-1","Language","isAnyOf compat: en_GB ⊑ en",        [LNG_KB],AG,d("c1","c2"),con_multi("c1","language","op_isAnyOf",["de","en"])+"\n"+con("c2","language","op_eq","en_GB"),compat("c1","c2"),"unsat","Theorem")
add("ODRL055-1","Language","3-KB cross-DS: lang blocks",        [GEO_KB,DPV_KB,LNG_KB_FACTS],TG,d("c1","c2","c3","c4","c5","c6"),con("c1","spatial","op_isPartOf","europe")+"\n"+con("c3","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c5","language","op_isA","de")+"\n"+con("c2","spatial","op_eq","france")+"\n"+con("c4","purpose","op_eq","scientificResearch")+"\n"+con("c6","language","op_eq","fr"),cross3("c1","c2","c3","c4","c5","c6"),"sat","CounterSatisfiable")
add("ODRL056-1","Language","Diagnostic: language blocks",        [LNG_KB],PG,d("c5","c6"),con("c5","language","op_isA","de")+"\n"+con("c6","language","op_eq","fr"),conflict("c5","c6"),"unsat","Theorem")

# --- Alignment Language 057-059 ---
add("ODRL057-1","Alignment","Align: lang conflict preserved",   [LNG1_KB],PG,d("c1","c2"),con("c1","language","op_isA","deu")+"\n"+con("c2","language","op_eq","fra"),conflict("c1","c2"),"unsat","Theorem")
add("ODRL058-1","Alignment","Align: lang compat preserved",     [LNG1_KB],PG,d("c1","c2"),con("c1","language","op_isA","ara")+"\n"+con("c2","language","op_eq","arz"),compat("c1","c2"),"unsat","Theorem")
add("ODRL059-1","Alignment","Align: lang degradation (de_AT)",  [LNG1_KB],PG,d("c1","c2","de_AT"),con("c1","language","op_isA","deu")+"\n"+con("c2","language","op_eq","de_AT"),compat("c1","c2"),"sat","CounterSatisfiable")
add("ODRL059-2","Alignment","Align: no false conflict (de_AT)", [LNG1_KB],PG,d("c1","c2","de_AT"),con("c1","language","op_isA","deu")+"\n"+con("c2","language","op_eq","de_AT"),conflict("c1","c2"),"sat","CounterSatisfiable")

# --- Alignment Spatial 060-062 ---
add("ODRL060-1","Alignment","Align: spatial conflict preserved", [GEO1_KB],SG,d("c1","c2"),con("c1","spatial","op_isPartOf","deu")+"\n"+con("c2","spatial","op_eq","fra"),conflict("c1","c2"),"unsat","Theorem")
add("ODRL061-1","Alignment","Align: spatial compat preserved",   [GEO1_KB],SG,d("c1","c2"),con("c1","spatial","op_isPartOf","eur")+"\n"+con("c2","spatial","op_eq","fra"),compat("c1","c2"),"unsat","Theorem")
add("ODRL062-1","Alignment","Align: spatial degrad (bavaria)",   [GEO1_KB],SG,d("c1","c2","bavaria"),con("c1","spatial","op_isPartOf","deu")+"\n"+con("c2","spatial","op_eq","bavaria"),compat("c1","c2"),"sat","CounterSatisfiable")
add("ODRL062-2","Alignment","Align: no false spatial conflict",  [GEO1_KB],SG,d("c1","c2","bavaria"),con("c1","spatial","op_isPartOf","deu")+"\n"+con("c2","spatial","op_eq","bavaria"),conflict("c1","c2"),"sat","CounterSatisfiable")

# --- Alignment Purpose 063-065 ---
add("ODRL063-1","Alignment","Align: purpose conflict preserved", [DPV1_KB],PG,d("c1","c2"),con("c1","purpose","op_isA","nichtKommerziellerZweck")+"\n"+con("c2","purpose","op_eq","kommerzielleForschung"),conflict("c1","c2"),"unsat","Theorem")
add("ODRL064-1","Alignment","Align: purpose compat preserved",   [DPV1_KB],PG,d("c1","c2"),con("c1","purpose","op_isA","nichtKommerziellerZweck")+"\n"+con("c2","purpose","op_eq","nichtKommerzielleForschung"),compat("c1","c2"),"unsat","Theorem")
add("ODRL065-1","Alignment","Align: purpose degrad (sciRes)",    [DPV1_KB],PG,d("c1","c2","scientificResearch"),con("c1","purpose","op_isA","forschungUndEntwicklung")+"\n"+con("c2","purpose","op_eq","scientificResearch"),compat("c1","c2"),"sat","CounterSatisfiable")
add("ODRL065-2","Alignment","Align: no false purpose conflict",  [DPV1_KB],PG,d("c1","c2","scientificResearch"),con("c1","purpose","op_isA","forschungUndEntwicklung")+"\n"+con("c2","purpose","op_eq","scientificResearch"),conflict("c1","c2"),"sat","CounterSatisfiable")

# --- Alignment Crown Jewel 066 ---
add("ODRL066-1","Alignment","3-KB cross-KB: all alt standards",
    [GEO1_KB,DPV1_KB_FACTS,LNG1_KB_FACTS_NO_DUP],TG,
    d("c1","c2","c3","c4","c5","c6")+"\n(declare-const scientificResearch Entity)",
    con("c1","spatial","op_isPartOf","eur")+"\n"+con("c3","purpose","op_isA","nichtKommerziellerZweck")+"\n"+con("c5","language","op_isA","deu")+"\n"+con("c2","spatial","op_eq","fra")+"\n"+con("c4","purpose","op_eq","scientificResearch")+"\n"+con("c6","language","op_eq","fra"),
    cross3("c1","c2","c3","c4","c5","c6"),"sat","CounterSatisfiable")

# --- Runtime 070-075 ---
add("ODRL070-1","Runtime","Witness: de_AT satisfies both",       [LNG_KB],PG,d("c1","c2"),con("c1","language","op_isA","de")+"\n"+con("c2","language","op_eq","de_AT"),witness("de_AT","c1","c2"),"unsat","Theorem")
add("ODRL071-1","Runtime","Rejection: fr ∉ ⟦isA de⟧",           [LNG_KB],PG,d("c1"),con("c1","language","op_isA","de"),rejection("fr","c1"),"unsat","Theorem")
add("ODRL072-1","Runtime","Witness: france satisfies both",      [GEO_KB],SG,d("c1","c2"),con("c1","spatial","op_isPartOf","europe")+"\n"+con("c2","spatial","op_eq","france"),witness("france","c1","c2"),"unsat","Theorem")

_073 = " ".join(f"(not (and (in_denotation {l} c1) (in_denotation {l} c2)))" for l in ["de","de_AT","de_CH","en","en_US","en_GB","fr","ar","arb","arz"])
add("ODRL073-1","Runtime","Exhaustive: all 10 concepts fail",    [LNG_KB],PG,d("c1","c2"),con("c1","language","op_isA","de")+"\n"+con("c2","language","op_eq","fr"),f"(assert (not (and {_073})))","unsat","Theorem")

add("ODRL074-1","Runtime","Witness: nonCommRes satisfies both",  [DPV_KB],PG,d("c1","c2"),con("c1","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c2","purpose","op_eq","nonCommercialResearch"),witness("nonCommercialResearch","c1","c2"),"unsat","Theorem")
add("ODRL075-1","Runtime","Rejection: advert ∉ ⟦isA nonComm⟧",  [DPV_KB],PG,d("c1"),con("c1","purpose","op_isA","nonCommercialPurpose"),rejection("advertising","c1"),"unsat","Theorem")

# ==========================
# OR composition (080–084)
# ==========================

# ODRL080-1: or(isA de, isA ar) vs eq arz → arz ⊑ ar → second branch works → Compatible
add("ODRL080-1","LogicalOr","OR compatible: or(de,ar) vs arz",
    [LNG_KB],PG,d("c1","c2","c3"),
    con("c1","language","op_isA","de")+"\n"+con("c2","language","op_isA","ar")+"\n"+con("c3","language","op_eq","arz"),
    or_compat("c1","c2","c3"),"unsat","Theorem")

# ODRL081-1: or(isA de, isA en) vs eq fr → fr ⊄ de AND fr ⊄ en → Conflict
add("ODRL081-1","LogicalOr","OR conflict: or(de,en) vs fr",
    [LNG_KB],PG,d("c1","c2","c3"),
    con("c1","language","op_isA","de")+"\n"+con("c2","language","op_isA","en")+"\n"+con("c3","language","op_eq","fr"),
    or_conflict("c1","c2","c3"),"unsat","Theorem")

# ODRL082-1: or(isA nonComm, isA marketing) vs eq sciRes → Unknown (both branches indeterminate)
add("ODRL082-1","LogicalOr","OR Unknown: or(nonComm,mkt) vs sciRes",
    [DPV_KB],PG,d("c1","c2","c3"),
    con("c1","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c2","purpose","op_isA","marketing")+"\n"+con("c3","purpose","op_eq","scientificResearch"),
    or_compat("c1","c2","c3"),"sat","CounterSatisfiable")

# ODRL083-1: spatial AND or(purpose1, purpose2) — both work
# spatial: isPartOf europe vs eq france → Compatible
# or(isA nonComm, isA R&D) vs eq academicResearch → acadRes ⊑ R&D → Compatible
add("ODRL083-1","LogicalOr","Cross-DS AND-OR: spatial ∧ or(purpose)",
    [GEO_KB,DPV_KB],TG,d("c_s1","c_s2","c_p1","c_p2","c_p3"),
    con("c_s1","spatial","op_isPartOf","europe")+"\n"+con("c_s2","spatial","op_eq","france")+"\n"+
    con("c_p1","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c_p2","purpose","op_isA","researchAndDevelopment")+"\n"+
    con("c_p3","purpose","op_eq","academicResearch"),
    or_cross_compat("c_s1","c_s2","c_p1","c_p2","c_p3"),"unsat","Theorem")

# ODRL084-1: spatial AND or(purpose) — spatial ok, or(purpose) unknown
# spatial: isPartOf europe vs eq france → Compatible
# or(isA nonComm, isA marketing) vs eq sciRes → both branches indeterminate → Unknown
add("ODRL084-1","LogicalOr","Cross-DS AND-OR blocked: or(purpose) unknown",
    [GEO_KB,DPV_KB],TG,d("c_s1","c_s2","c_p1","c_p2","c_p3"),
    con("c_s1","spatial","op_isPartOf","europe")+"\n"+con("c_s2","spatial","op_eq","france")+"\n"+
    con("c_p1","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c_p2","purpose","op_isA","marketing")+"\n"+
    con("c_p3","purpose","op_eq","scientificResearch"),
    or_cross_compat("c_s1","c_s2","c_p1","c_p2","c_p3"),"sat","CounterSatisfiable")

# ==========================
# XONE composition (085–088)
# ==========================

# ODRL085-1: xone(isA comm, isA nonComm) vs eq nonCommRes
# nonCommRes ⊑ nonComm ✓, ¬(nonCommRes ⊑ comm) ✓ [explicit] → exactly one → Compatible
add("ODRL085-1","LogicalXone","XONE compatible: exactly one branch holds",
    [DPV_KB],PG,d("c1","c2","c3"),
    con("c1","purpose","op_isA","commercialPurpose")+"\n"+con("c2","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c3","purpose","op_eq","nonCommercialResearch"),
    xone_compat("c1","c2","c3"),"unsat","Theorem")

# ODRL086-1: xone(isA comm, isA nonComm) vs eq commRes
# commRes ⊑ comm ✓. But ¬(commRes ⊑ nonComm)? NOT explicit in DPV KB!
# Open world: commRes COULD be under both → can't confirm exclusivity → Unknown
# Compare ODRL085: nonCommRes HAS explicit ¬(⊑ comm) in KB → works.
# Insight: xone requires explicit disjointness axioms; open-world blocks it otherwise.
add("ODRL086-1","LogicalXone","XONE Unknown: missing explicit disjointness",
    [DPV_KB],PG,d("c1","c2","c3"),
    con("c1","purpose","op_isA","commercialPurpose")+"\n"+con("c2","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c3","purpose","op_eq","commercialResearch"),
    xone_compat("c1","c2","c3"),"sat","CounterSatisfiable")

# ODRL087-1: xone(isA R&D, isA nonComm) vs eq nonCommRes
# nonCommRes ⊑ R&D ✓ AND nonCommRes ⊑ nonComm ✓ → BOTH branches → violates xone
# But open world: maybe other values satisfy exactly one? → Unknown
add("ODRL087-1","LogicalXone","XONE both-in: nonCommRes in both branches",
    [DPV_KB],PG,d("c1","c2","c3"),
    con("c1","purpose","op_isA","researchAndDevelopment")+"\n"+con("c2","purpose","op_isA","nonCommercialPurpose")+"\n"+con("c3","purpose","op_eq","nonCommercialResearch"),
    xone_compat("c1","c2","c3"),"sat","CounterSatisfiable")

# ODRL088-1: xone(isA de, isA en) vs eq fr
# fr ⊄ de ✗ AND fr ⊄ en ✗ → neither branch → Conflict
add("ODRL088-1","LogicalXone","XONE conflict: neither branch holds",
    [LNG_KB],PG,d("c1","c2","c3"),
    con("c1","language","op_isA","de")+"\n"+con("c2","language","op_isA","en")+"\n"+con("c3","language","op_eq","fr"),
    xone_conflict("c1","c2","c3"),"unsat","Theorem")

# ============================================================
# Generator + Runner
# ============================================================

def gen(p):
    parts = [f"; {p['id']}.smt2 — {p['desc']}", f"; Expected: {p['esmt']} (SZS: {p['eszs']})", "", PREAMBLE]
    for kb in p["kbs"]: parts.append(kb)
    if p["gr"]: parts.append(LAYER1)
    for g in p["gr"]: parts.append(g)
    if p["decls"]: parts += [f"\n; === Problem: {p['id']} ===", p["decls"]]
    if p["cons"]: parts.append(p["cons"])
    parts += ["", p["conj"], "", "(check-sat)"]
    return "\n".join(parts)

def run(cmd, fp, timeout=30):
    try:
        t0 = time.time()
        r = subprocess.run(cmd+[fp], capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip().split("\n")[0].strip(), time.time()-t0
    except subprocess.TimeoutExpired: return "timeout", timeout
    except FileNotFoundError: return "not_found", 0

def main():
    do_run = "--run" in sys.argv
    do_cvc5 = "--cvc5" in sys.argv

    for p in P:
        sd = os.path.join(SMT_DIR, p["sub"])
        os.makedirs(sd, exist_ok=True)
        with open(os.path.join(sd, f"{p['id']}.smt2"), "w") as f:
            f.write(gen(p))
    print(f"Generated {len(P)} SMT-LIB2 files in {SMT_DIR}/")

    if not do_run: print("Use --run to execute Z3."); return

    hdr = f"{'Problem':<14} {'Expected':>8} {'Z3':>8} {'Time':>8}"
    if do_cvc5: hdr += f" {'CVC5':>8} {'Time':>8}"
    hdr += f"  {'SZS':>16}  {'OK':>3}"
    print(); print(hdr); print("-"*len(hdr))

    ok = True; cats = {}
    for p in P:
        fp = os.path.join(SMT_DIR, p["sub"], f"{p['id']}.smt2")
        z3r, z3t = run(["z3"], fp)
        m = "✓" if z3r == p["esmt"] else "✗"
        if z3r != p["esmt"]: ok = False
        line = f"{p['id']:<14} {p['esmt']:>8} {z3r:>8} {z3t:>7.3f}s"
        if do_cvc5:
            cr, ct = run(["cvc5","--lang=smt2"], fp)
            line += f" {cr:>8} {ct:>7.3f}s"
        line += f"  {p['eszs']:>16}  {m:>3}"
        print(line)
        c = p["sub"]
        if c not in cats: cats[c] = [0,0]
        cats[c][0] += 1
        cats[c][1] += 1 if z3r == p["esmt"] else 0

    print()
    for c, (t, p_) in cats.items(): print(f"  {c:<16} {p_}/{t} {'✓' if p_==t else '✗'}")
    print(f"  {'TOTAL':<16} {sum(v[1] for v in cats.values())}/{sum(v[0] for v in cats.values())}")
    print("\nAll match ✓" if ok else "\nWARNING: mismatches ✗")

if __name__ == "__main__":
    main()