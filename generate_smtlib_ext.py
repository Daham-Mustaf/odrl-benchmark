#!/usr/bin/env python3
"""
enchmarks for VLDB: ~90 new problems (090–207).
Append these to generate_smtlib.py's P list, or run standalone.

Categories:
  Neq          090–096   7   Complement denotation
  HasPart      100–106   7   Upward closure
  IsAnyOf      110–118   9   Union of closures
  IsAllOf      120–128   9   Intersection, nominal collapse, diamond
  IsNoneOf     130–139  10   Negated union, double negation
  Nominal      140–147   8   Identity domain, isA=eq degeneration
  OperatorPairs 150–161 12   Cross-operator interactions
  AdvDeep      170–181  12   Chains, diamonds, single-concept, near-miss
  AlignAdv     190–199  10   Unmapped witness, partial edge cases
  CompDeep     200–207   8   3+ operand, mixed Unknown propagation

Usage:
    python3 generate_smtlib_ext.py              # generate all new .smt2 files
    python3 generate_smtlib_ext.py --run        # generate + run z3
"""
import os, subprocess, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
SMT_DIR = os.path.join(BASE, "SMT/ODRL/KBGrounding")

PREAMBLE = "(set-logic UF)\n(declare-sort Entity 0)\n"

# ============================================================
# Existing KBs (copied from main generator for standalone use)
# ============================================================

GEO_KB = """\
; === GeoNames Spatial KB ===
(declare-fun partOf (Entity Entity) Bool)
(declare-const europe Entity) (declare-const france Entity)
(declare-const germany Entity) (declare-const bavaria Entity)
(assert (forall ((x Entity)) (partOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (partOf x y) (partOf y z)) (partOf x z))))
(assert (partOf france europe)) (assert (partOf germany europe))
(assert (partOf bavaria germany))
(assert (not (partOf germany france))) (assert (not (partOf france germany)))
"""

DPV_CROSS_LEVEL = """\
; Cross-level UNA: leaves ≠ parents
(assert (not (= academicResearch purpose_top)))
(assert (not (= academicResearch commercialPurpose)))
(assert (not (= academicResearch nonCommercialPurpose)))
(assert (not (= academicResearch researchAndDevelopment)))
(assert (not (= academicResearch marketing)))
(assert (not (= scientificResearch purpose_top)))
(assert (not (= scientificResearch commercialPurpose)))
(assert (not (= scientificResearch nonCommercialPurpose)))
(assert (not (= scientificResearch researchAndDevelopment)))
(assert (not (= scientificResearch marketing)))
(assert (not (= commercialResearch purpose_top)))
(assert (not (= commercialResearch commercialPurpose)))
(assert (not (= commercialResearch nonCommercialPurpose)))
(assert (not (= commercialResearch researchAndDevelopment)))
(assert (not (= commercialResearch marketing)))
(assert (not (= nonCommercialResearch purpose_top)))
(assert (not (= nonCommercialResearch commercialPurpose)))
(assert (not (= nonCommercialResearch nonCommercialPurpose)))
(assert (not (= nonCommercialResearch researchAndDevelopment)))
(assert (not (= nonCommercialResearch marketing)))
(assert (not (= advertising purpose_top)))
(assert (not (= advertising commercialPurpose)))
(assert (not (= advertising nonCommercialPurpose)))
(assert (not (= advertising researchAndDevelopment)))
(assert (not (= advertising marketing)))
(assert (not (= directMarketing purpose_top)))
(assert (not (= directMarketing commercialPurpose)))
(assert (not (= directMarketing nonCommercialPurpose)))
(assert (not (= directMarketing researchAndDevelopment)))
(assert (not (= directMarketing marketing)))
"""

DPV_KB = """\
; === DPV Purpose Taxonomy ===
(declare-fun subClassOf (Entity Entity) Bool)
(declare-const purpose_top Entity)
(declare-const commercialPurpose Entity) (declare-const nonCommercialPurpose Entity)
(declare-const researchAndDevelopment Entity) (declare-const marketing Entity)
(declare-const academicResearch Entity) (declare-const scientificResearch Entity)
(declare-const commercialResearch Entity) (declare-const nonCommercialResearch Entity)
(declare-const advertising Entity) (declare-const directMarketing Entity)
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
; === BCP 47 Language Tags ===
(declare-fun subClassOf (Entity Entity) Bool)
(declare-const de Entity) (declare-const de_AT Entity) (declare-const de_CH Entity)
(declare-const en Entity) (declare-const en_US Entity) (declare-const en_GB Entity)
(declare-const fr Entity) (declare-const ar Entity) (declare-const arb Entity) (declare-const arz Entity)
(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))
(assert (subClassOf de_AT de)) (assert (subClassOf de_CH de))
(assert (subClassOf en_US en)) (assert (subClassOf en_GB en))
(assert (subClassOf arb ar)) (assert (subClassOf arz ar))
(assert (not (subClassOf de en))) (assert (not (subClassOf en de)))
(assert (not (subClassOf de fr))) (assert (not (subClassOf fr de)))
(assert (not (subClassOf en fr))) (assert (not (subClassOf fr en)))
(assert (not (subClassOf de ar))) (assert (not (subClassOf ar de)))
(assert (not (subClassOf en ar))) (assert (not (subClassOf ar en)))
(assert (not (subClassOf fr ar))) (assert (not (subClassOf ar fr)))
"""

LNG_KB_FACTS = """\
; === BCP 47 (facts only, no subClassOf decl) ===
(declare-const de Entity) (declare-const de_AT Entity) (declare-const de_CH Entity)
(declare-const en Entity) (declare-const en_US Entity) (declare-const en_GB Entity)
(declare-const fr Entity) (declare-const ar Entity) (declare-const arb Entity) (declare-const arz Entity)
(assert (subClassOf de_AT de)) (assert (subClassOf de_CH de))
(assert (subClassOf en_US en)) (assert (subClassOf en_GB en))
(assert (subClassOf arb ar)) (assert (subClassOf arz ar))
(assert (not (subClassOf de en))) (assert (not (subClassOf en de)))
(assert (not (subClassOf de fr))) (assert (not (subClassOf fr de)))
(assert (not (subClassOf en fr))) (assert (not (subClassOf fr en)))
(assert (not (subClassOf de ar))) (assert (not (subClassOf ar de)))
(assert (not (subClassOf en ar))) (assert (not (subClassOf ar en)))
(assert (not (subClassOf fr ar))) (assert (not (subClassOf ar fr)))
"""

# Alternative KBs for alignment
GEO1_KB = """\
; === ISO 3166 Spatial KB (countries only) ===
(declare-fun partOf (Entity Entity) Bool)
(declare-const eur Entity) (declare-const deu Entity) (declare-const fra Entity)
(assert (forall ((x Entity)) (partOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (partOf x y) (partOf y z)) (partOf x z))))
(assert (partOf deu eur)) (assert (partOf fra eur))
(assert (not (partOf deu fra))) (assert (not (partOf fra deu)))
"""

LNG1_KB = """\
; === ISO 639-3 Language KB ===
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

# ============================================================
# NEW KBs for extension benchmarks
# ============================================================

# Nominal KB: flat identity domain (deliveryChannel)
NOMINAL_KB = """\
; === Nominal KB: Delivery Channels (flat, no hierarchy) ===
(declare-const email Entity) (declare-const api Entity)
(declare-const ftp Entity) (declare-const streaming Entity)
; No subClassOf or partOf — identity only
; All distinct:
(assert (not (= email api))) (assert (not (= email ftp)))
(assert (not (= email streaming))) (assert (not (= api ftp)))
(assert (not (= api streaming))) (assert (not (= ftp streaming)))
"""

# Chain KB: A ≤ B ≤ C ≤ D ≤ E (depth-5 taxonomy)
CHAIN_KB = """\
; === Chain KB: depth-5 taxonomy ===
(declare-fun subClassOf (Entity Entity) Bool)
(declare-const chainA Entity) (declare-const chainB Entity)
(declare-const chainC Entity) (declare-const chainD Entity)
(declare-const chainE Entity)
(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))
(assert (subClassOf chainA chainB))
(assert (subClassOf chainB chainC))
(assert (subClassOf chainC chainD))
(assert (subClassOf chainD chainE))
; Negative axioms for non-ancestors:
(assert (not (subClassOf chainE chainD)))
(assert (not (subClassOf chainD chainC)))
(assert (not (subClassOf chainC chainB)))
(assert (not (subClassOf chainB chainA)))
"""

# Diamond KB: X ≤ A, X ≤ B, A ≤ C, B ≤ C (diamond inheritance)
DIAMOND_KB = """\
; === Diamond KB: X ≤ A, X ≤ B, A ≤ C, B ≤ C ===
(declare-fun subClassOf (Entity Entity) Bool)
(declare-const diaX Entity) (declare-const diaA Entity)
(declare-const diaB Entity) (declare-const diaC Entity)
(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))
(assert (subClassOf diaX diaA))
(assert (subClassOf diaX diaB))
(assert (subClassOf diaA diaC))
(assert (subClassOf diaB diaC))
; A and B are not comparable:
(assert (not (subClassOf diaA diaB)))
(assert (not (subClassOf diaB diaA)))
"""

# Single-concept KB: |C| = 1
SINGLE_KB = """\
; === Single-concept KB: |C| = 1 ===
(declare-fun subClassOf (Entity Entity) Bool)
(declare-const singleton Entity)
(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))
; Domain closure: only singleton exists
(assert (forall ((x Entity)) (= x singleton)))
"""

# Near-miss KB: two barely-overlapping taxonomies
NEARMISS_KB = """\
; === Near-miss KB: overlap on exactly one concept ===
(declare-fun subClassOf (Entity Entity) Bool)
(declare-const nmRoot Entity) (declare-const nmLeft Entity)
(declare-const nmRight Entity) (declare-const nmShared Entity)
(declare-const nmOnlyLeft Entity) (declare-const nmOnlyRight Entity)
(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))
(assert (subClassOf nmLeft nmRoot)) (assert (subClassOf nmRight nmRoot))
(assert (subClassOf nmShared nmLeft)) (assert (subClassOf nmShared nmRight))
(assert (subClassOf nmOnlyLeft nmLeft)) (assert (subClassOf nmOnlyRight nmRight))
; Disjointness:
(assert (not (subClassOf nmOnlyLeft nmRight)))
(assert (not (subClassOf nmOnlyRight nmLeft)))
"""

# ============================================================
# Distinctness axioms (UNA) — needed for neq, hasPart+eq
# ============================================================

DPV_DISTINCT = """\
; UNA for DPV concepts
(assert (not (= purpose_top commercialPurpose))) (assert (not (= purpose_top nonCommercialPurpose)))
(assert (not (= purpose_top researchAndDevelopment))) (assert (not (= purpose_top marketing)))
(assert (not (= commercialPurpose nonCommercialPurpose)))
(assert (not (= commercialPurpose researchAndDevelopment))) (assert (not (= commercialPurpose marketing)))
(assert (not (= nonCommercialPurpose researchAndDevelopment))) (assert (not (= nonCommercialPurpose marketing)))
(assert (not (= researchAndDevelopment marketing)))
(assert (not (= academicResearch scientificResearch))) (assert (not (= academicResearch commercialResearch)))
(assert (not (= academicResearch nonCommercialResearch))) (assert (not (= academicResearch advertising)))
(assert (not (= academicResearch directMarketing)))
(assert (not (= scientificResearch commercialResearch))) (assert (not (= scientificResearch nonCommercialResearch)))
(assert (not (= scientificResearch advertising))) (assert (not (= scientificResearch directMarketing)))
(assert (not (= commercialResearch nonCommercialResearch)))
(assert (not (= commercialResearch advertising))) (assert (not (= commercialResearch directMarketing)))
(assert (not (= nonCommercialResearch advertising))) (assert (not (= nonCommercialResearch directMarketing)))
(assert (not (= advertising directMarketing)))
"""

GEO_DISTINCT = """\
; UNA for GeoNames concepts
(assert (not (= europe france))) (assert (not (= europe germany))) (assert (not (= europe bavaria)))
(assert (not (= france germany))) (assert (not (= france bavaria))) (assert (not (= germany bavaria)))
"""

GEO_HASP = GEO_KB + GEO_DISTINCT + """\
; Negative hasPart axioms (upward closure needs these)
(assert (not (partOf germany bavaria)))
(assert (not (partOf europe france))) (assert (not (partOf europe germany)))
(assert (not (partOf europe bavaria)))
(assert (not (partOf france bavaria))) (assert (not (partOf bavaria france)))
"""

LNG_DISTINCT = """\
; UNA for BCP47 concepts
(assert (not (= de de_AT))) (assert (not (= de de_CH))) (assert (not (= de en)))
(assert (not (= de en_US))) (assert (not (= de en_GB))) (assert (not (= de fr)))
(assert (not (= de ar))) (assert (not (= de arb))) (assert (not (= de arz)))
(assert (not (= de_AT de_CH))) (assert (not (= de_AT en))) (assert (not (= de_AT en_US)))
(assert (not (= de_AT en_GB))) (assert (not (= de_AT fr))) (assert (not (= de_AT ar)))
(assert (not (= de_AT arb))) (assert (not (= de_AT arz)))
(assert (not (= de_CH en))) (assert (not (= de_CH en_US))) (assert (not (= de_CH en_GB)))
(assert (not (= de_CH fr))) (assert (not (= de_CH ar))) (assert (not (= de_CH arb))) (assert (not (= de_CH arz)))
(assert (not (= en en_US))) (assert (not (= en en_GB))) (assert (not (= en fr)))
(assert (not (= en ar))) (assert (not (= en arb))) (assert (not (= en arz)))
(assert (not (= en_US en_GB))) (assert (not (= en_US fr))) (assert (not (= en_US ar)))
(assert (not (= en_US arb))) (assert (not (= en_US arz)))
(assert (not (= en_GB fr))) (assert (not (= en_GB ar))) (assert (not (= en_GB arb))) (assert (not (= en_GB arz)))
(assert (not (= fr ar))) (assert (not (= fr arb))) (assert (not (= fr arz)))
(assert (not (= ar arb))) (assert (not (= ar arz))) (assert (not (= arb arz)))
"""

CHAIN_DISTINCT = """\
; UNA for chain concepts
(assert (not (= chainA chainB))) (assert (not (= chainA chainC)))
(assert (not (= chainA chainD))) (assert (not (= chainA chainE)))
(assert (not (= chainB chainC))) (assert (not (= chainB chainD))) (assert (not (= chainB chainE)))
(assert (not (= chainC chainD))) (assert (not (= chainC chainE)))
(assert (not (= chainD chainE)))
"""

# LNG1_KB without subClassOf declaration (for multi-KB problems)
LNG1_KB_NODUP = """\
; === ISO 639-3 Language KB (prefixed, no subClassOf decl, for multi-KB) ===
(declare-const lang_deu Entity) (declare-const lang_eng Entity) (declare-const lang_fra Entity)
(declare-const lang_ara Entity) (declare-const lang_arb Entity) (declare-const lang_arz Entity)
(assert (subClassOf lang_arb lang_ara)) (assert (subClassOf lang_arz lang_ara))
(assert (not (subClassOf lang_deu lang_eng))) (assert (not (subClassOf lang_eng lang_deu)))
(assert (not (subClassOf lang_deu lang_fra))) (assert (not (subClassOf lang_fra lang_deu)))
(assert (not (subClassOf lang_deu lang_ara))) (assert (not (subClassOf lang_ara lang_deu)))
(assert (not (subClassOf lang_eng lang_fra))) (assert (not (subClassOf lang_fra lang_eng)))
(assert (not (subClassOf lang_eng lang_ara))) (assert (not (subClassOf lang_ara lang_eng)))
(assert (not (subClassOf lang_fra lang_ara))) (assert (not (subClassOf lang_ara lang_fra)))
"""

# ============================================================
# Layer 1 + Grounding Rules
# ============================================================

LAYER1 = """\
; === Layer 1: ODRL Core ===
(declare-fun has_operand (Entity Entity) Bool)
(declare-fun has_operator (Entity Entity) Bool)
(declare-fun has_value (Entity Entity) Bool)
(declare-fun in_denotation (Entity Entity) Bool)
(declare-const op_eq Entity) (declare-const op_neq Entity)
(declare-const op_isPartOf Entity) (declare-const op_hasPart Entity)
(declare-const op_isA Entity) (declare-const op_isAnyOf Entity)
(declare-const op_isAllOf Entity) (declare-const op_isNoneOf Entity)
; Operator UNA (critical for multi-operator problems)
(assert (not (= op_eq op_neq))) (assert (not (= op_eq op_isPartOf)))
(assert (not (= op_eq op_hasPart))) (assert (not (= op_eq op_isA)))
(assert (not (= op_eq op_isAnyOf))) (assert (not (= op_eq op_isAllOf)))
(assert (not (= op_eq op_isNoneOf)))
(assert (not (= op_neq op_isPartOf))) (assert (not (= op_neq op_hasPart)))
(assert (not (= op_neq op_isA))) (assert (not (= op_neq op_isAnyOf)))
(assert (not (= op_neq op_isAllOf))) (assert (not (= op_neq op_isNoneOf)))
(assert (not (= op_isPartOf op_hasPart))) (assert (not (= op_isPartOf op_isA)))
(assert (not (= op_isPartOf op_isAnyOf))) (assert (not (= op_isPartOf op_isAllOf)))
(assert (not (= op_isPartOf op_isNoneOf)))
(assert (not (= op_hasPart op_isA))) (assert (not (= op_hasPart op_isAnyOf)))
(assert (not (= op_hasPart op_isAllOf))) (assert (not (= op_hasPart op_isNoneOf)))
(assert (not (= op_isA op_isAnyOf))) (assert (not (= op_isA op_isAllOf)))
(assert (not (= op_isA op_isNoneOf)))
(assert (not (= op_isAnyOf op_isAllOf))) (assert (not (= op_isAnyOf op_isNoneOf)))
(assert (not (= op_isAllOf op_isNoneOf)))
(declare-fun mereological (Entity) Bool)
(declare-fun taxonomic (Entity) Bool)
(declare-fun nominal (Entity) Bool)
(declare-const spatial Entity) (declare-const purpose Entity)
(declare-const language Entity) (declare-const channel Entity)
; Operand UNA
(assert (not (= spatial purpose))) (assert (not (= spatial language)))
(assert (not (= spatial channel))) (assert (not (= purpose language)))
(assert (not (= purpose channel))) (assert (not (= language channel)))
(assert (mereological spatial))
(assert (taxonomic purpose)) (assert (taxonomic language))
(assert (nominal channel))
"""

GROUND_EQ = """\
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_eq) (has_value c v) (= x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_eq) (has_value c v))
        (= x v))))
"""

GROUND_NEQ = """\
; neq: C \\ {g} — bidirectional
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_neq) (has_value c v) (not (= x v)))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_neq) (has_value c v))
        (not (= x v)))))
"""

GROUND_ISPARTOF = """\
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isPartOf) (has_value c v) (mereological l) (partOf x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_isPartOf) (has_value c v) (mereological l))
        (partOf x v))))
"""

GROUND_HASPART = """\
; hasPart: {x | g ≤ x} — upward closure, bidirectional
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_hasPart) (has_value c v) (mereological l) (partOf v x))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_hasPart) (has_value c v) (mereological l))
        (partOf v x))))
"""

GROUND_ISA = """\
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isA) (has_value c v) (taxonomic l) (subClassOf x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_isA) (has_value c v) (taxonomic l))
        (subClassOf x v))))
"""

# Nominal isA: degenerates to eq (≤ = identity)
GROUND_ISA_NOM = """\
; isA under nominal domain: degenerates to identity (= eq)
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isA) (has_value c v) (nominal l) (= x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_isA) (has_value c v) (nominal l))
        (= x v))))
"""

GROUND_ISANYOF_TAX = """\
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isAnyOf) (has_value c v) (taxonomic l) (subClassOf x v))
        (in_denotation x c))))
"""

GROUND_ISANYOF_MEREO = """\
; isAnyOf over mereological domain
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isAnyOf) (has_value c v) (mereological l) (partOf x v))
        (in_denotation x c))))
"""

GROUND_ISANYOF_NOM = """\
; isAnyOf under nominal: union of singletons = membership
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isAnyOf) (has_value c v) (nominal l) (= x v))
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

GROUND_ISNONEOF_MEREO = """\
; isNoneOf over mereological: not partOf any listed value
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_isNoneOf) (has_value c v) (mereological l))
        (not (partOf x v)))))
"""

GROUND_ISNONEOF_NOM = """\
; isNoneOf under nominal: x ≠ any listed value
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_isNoneOf) (has_value c v) (nominal l))
        (not (= x v)))))
"""

# ============================================================
# Grounding rule sets
# ============================================================

SG = [GROUND_EQ, GROUND_ISPARTOF]                    # spatial grounding
PG = [GROUND_EQ, GROUND_ISA]                          # purpose/language grounding
HG = [GROUND_EQ, GROUND_ISPARTOF, GROUND_HASPART]     # hasPart + isPartOf
NQ = [GROUND_EQ, GROUND_NEQ]                           # neq
NG = [GROUND_EQ, GROUND_ISNONEOF_TAX_ONLY]             # isNoneOf taxonomic
AG = [GROUND_EQ, GROUND_ISANYOF_TAX]                   # isAnyOf taxonomic
LG = [GROUND_EQ, GROUND_ISALLOF_TAX_ONLY]              # isAllOf taxonomic
TG = [GROUND_EQ, GROUND_ISPARTOF, GROUND_ISA]          # cross-dataspace
NOM_G = [GROUND_EQ, GROUND_ISA_NOM]                    # nominal grounding
NOM_ANY = [GROUND_EQ, GROUND_ISANYOF_NOM]              # nominal isAnyOf
NOM_NONE = [GROUND_EQ, GROUND_ISNONEOF_NOM]            # nominal isNoneOf

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

def allof_if(c, vals, op="purpose"):
    cj = " ".join(f"(subClassOf x {v})" for v in vals)
    return f"(assert (forall ((x Entity)) (=> (and {cj} (taxonomic {op})) (in_denotation x {c}))))"

def noneof_if(c, vals, op="purpose"):
    cj = " ".join(f"(not (subClassOf x {v}))" for v in vals)
    return f"(assert (forall ((x Entity)) (=> (and {cj} (taxonomic {op})) (in_denotation x {c}))))"

def noneof_if_mereo(c, vals):
    cj = " ".join(f"(not (partOf x {v}))" for v in vals)
    return f"(assert (forall ((x Entity)) (=> (and {cj} (mereological spatial)) (in_denotation x {c}))))"

def anyof_only(c, vals):
    dj = " ".join(f"(subClassOf x {v})" for v in vals)
    return f"(assert (forall ((x Entity)) (=> (in_denotation x {c}) (or {dj}))))"

def anyof_only_mereo(c, vals):
    dj = " ".join(f"(partOf x {v})" for v in vals)
    return f"(assert (forall ((x Entity)) (=> (in_denotation x {c}) (or {dj}))))"

def or_compat(c1, c2, c3):
    return f"""(assert (not (or
  (exists ((x Entity)) (and (in_denotation x {c1}) (in_denotation x {c3})))
  (exists ((y Entity)) (and (in_denotation y {c2}) (in_denotation y {c3}))))))"""

def or_conflict(c1, c2, c3):
    return f"""(assert (or
  (exists ((x Entity)) (and (in_denotation x {c1}) (in_denotation x {c3})))
  (exists ((y Entity)) (and (in_denotation y {c2}) (in_denotation y {c3})))))"""

def xone_compat(c1, c2, c3):
    return f"""(assert (not (or
  (exists ((x Entity)) (and (in_denotation x {c1}) (not (in_denotation x {c2})) (in_denotation x {c3})))
  (exists ((y Entity)) (and (in_denotation y {c2}) (not (in_denotation y {c1})) (in_denotation y {c3}))))))"""

def xone_conflict(c1, c2, c3):
    return f"""(assert (or
  (exists ((x Entity)) (and (in_denotation x {c1}) (not (in_denotation x {c2})) (in_denotation x {c3})))
  (exists ((y Entity)) (and (in_denotation y {c2}) (not (in_denotation y {c1})) (in_denotation y {c3})))))"""

def d(*names):
    return "\n".join(f"(declare-const {n} Entity)" for n in names)

# ============================================================
# Problem catalog
# ============================================================
P = []
def add(pid, sub, desc, kbs, gr, decls, cons, conj, esmt, eszs):
    P.append(dict(id=pid, sub=sub, desc=desc, kbs=kbs, gr=gr,
                  decls=decls, cons=cons, conj=conj, esmt=esmt, eszs=eszs))


# ============================================================
# NEQ (090–096): Complement denotation C \ {g}
# ============================================================

# 090: neq acadRes vs eq sciRes → different values → Compatible
add("ODRL090-1","Neq","neq acadRes vs eq sciRes: different values",
    [DPV_KB + DPV_DISTINCT], NQ, d("c1","c2"),
    con("c1","purpose","op_neq","academicResearch")+"\n"+con("c2","purpose","op_eq","scientificResearch"),
    compat("c1","c2"), "unsat","Theorem")

# 091: neq acadRes vs eq acadRes → same value → Conflict
add("ODRL091-1","Neq","neq acadRes vs eq acadRes: same value → Conflict",
    [DPV_KB], NQ, d("c1","c2"),
    con("c1","purpose","op_neq","academicResearch")+"\n"+con("c2","purpose","op_eq","academicResearch"),
    conflict("c1","c2"), "unsat","Theorem")

# 092: neq france vs eq germany → different → Compatible (spatial)
add("ODRL092-1","Neq","neq france vs eq germany: Compatible (spatial)",
    [GEO_KB], [GROUND_EQ, GROUND_NEQ, GROUND_ISPARTOF], d("c1","c2"),
    con("c1","spatial","op_neq","france")+"\n"+con("c2","spatial","op_eq","germany"),
    compat("c1","c2"), "unsat","Theorem")

# 093: neq fr vs isA de → Compatible (fr excluded, de subtree excluded anyway)
add("ODRL093-1","Neq","neq fr vs isA de: Compatible",
    [LNG_KB], [GROUND_EQ, GROUND_NEQ, GROUND_ISA], d("c1","c2"),
    con("c1","language","op_neq","fr")+"\n"+con("c2","language","op_isA","de"),
    compat("c1","c2"), "unsat","Theorem")

# 094: neq de vs isA de → partial overlap (de_AT, de_CH ∈ isA de ∩ neq de)
add("ODRL094-1","Neq","neq de vs isA de: overlap on de_AT, de_CH",
    [LNG_KB + LNG_DISTINCT], [GROUND_EQ, GROUND_NEQ, GROUND_ISA], d("c1","c2"),
    con("c1","language","op_neq","de")+"\n"+con("c2","language","op_isA","de"),
    compat("c1","c2"), "unsat","Theorem")

# 095: neq on single-concept KB → C\{singleton} = ∅ → neq vs eq same → Conflict
add("ODRL095-1","Neq","neq singleton: C\\{g}=∅ on |C|=1",
    [SINGLE_KB], NQ, d("c1","c2"),
    con("c1","purpose","op_neq","singleton")+"\n"+con("c2","purpose","op_eq","singleton"),
    conflict("c1","c2"), "unsat","Theorem")

# 096: neq vs neq on small KB (neq de vs neq fr on BCP47)
# C\{de} ∩ C\{fr} = C\{de,fr} — nonempty since |C|=10 → Compatible
add("ODRL096-1","Neq","neq de vs neq fr: double complement, Compatible",
    [LNG_KB], NQ, d("c1","c2"),
    con("c1","language","op_neq","de")+"\n"+con("c2","language","op_neq","fr"),
    compat("c1","c2"), "unsat","Theorem")


# ============================================================
# HASPART (100–106): Upward closure {x | g ≤ x}
# ============================================================

# hasPart(bavaria) = {x | bavaria ≤ x} = {bavaria, germany, europe}
# hasPart(france)  = {x | france ≤ x}  = {france, europe}
# hasPart(europe)  = {x | europe ≤ x}  = {europe}

# 100: hasPart bavaria vs eq europe → europe ∈ hasPart(bavaria) → Compatible
add("ODRL100-1","HasPart","hasPart bavaria vs eq europe: Compatible",
    [GEO_KB], HG, d("c1","c2"),
    con("c1","spatial","op_hasPart","bavaria")+"\n"+con("c2","spatial","op_eq","europe"),
    compat("c1","c2"), "unsat","Theorem")

# 101: hasPart europe vs eq france → france ∉ {europe} → Conflict
add("ODRL101-1","HasPart","hasPart europe vs eq france: Conflict",
    [GEO_KB], HG, d("c1","c2"),
    con("c1","spatial","op_hasPart","europe")+"\n"+con("c2","spatial","op_eq","france"),
    conflict("c1","c2"), "unsat","Theorem")

# 102: hasPart france vs isPartOf europe → overlap: {france, europe} ∩ {france,germany,bavaria,europe} → Compatible
add("ODRL102-1","HasPart","hasPart france vs isPartOf europe: overlap",
    [GEO_KB], HG, d("c1","c2"),
    con("c1","spatial","op_hasPart","france")+"\n"+con("c2","spatial","op_isPartOf","europe"),
    compat("c1","c2"), "unsat","Theorem")

# 103: hasPart bavaria vs hasPart france → overlap on {europe} → Compatible
add("ODRL103-1","HasPart","hasPart bavaria vs hasPart france: meet at europe",
    [GEO_KB], HG, d("c1","c2"),
    con("c1","spatial","op_hasPart","bavaria")+"\n"+con("c2","spatial","op_hasPart","france"),
    compat("c1","c2"), "unsat","Theorem")

# 104: hasPart germany vs eq bavaria → bavaria ∉ {germany, europe} → Conflict
add("ODRL104-1","HasPart","hasPart germany vs eq bavaria: upward excludes downward",
    [GEO_HASP], HG, d("c1","c2"),
    con("c1","spatial","op_hasPart","germany")+"\n"+con("c2","spatial","op_eq","bavaria"),
    conflict("c1","c2"), "unsat","Theorem")

# 105: hasPart bavaria vs isPartOf germany → {bav,ger,eu} ∩ {bav,ger} → {bav,ger} → Compatible
add("ODRL105-1","HasPart","hasPart bavaria vs isPartOf germany: Compatible",
    [GEO_KB], HG, d("c1","c2"),
    con("c1","spatial","op_hasPart","bavaria")+"\n"+con("c2","spatial","op_isPartOf","germany"),
    compat("c1","c2"), "unsat","Theorem")

# 106: hasPart europe vs isPartOf france → {europe} ∩ {france} → ∅ → Conflict
add("ODRL106-1","HasPart","hasPart europe vs isPartOf france: disjoint",
    [GEO_KB], HG, d("c1","c2"),
    con("c1","spatial","op_hasPart","europe")+"\n"+con("c2","spatial","op_isPartOf","france"),
    conflict("c1","c2"), "unsat","Theorem")


# ============================================================
# ISANYOF extended (110–118): Union of closures
# ============================================================

# 110: isAnyOf {de, en} vs eq de_AT → de_AT ⊑ de → Compatible
add("ODRL110-1","IsAnyOf","isAnyOf {de,en} vs eq de_AT: branch 1 hit",
    [LNG_KB], AG, d("c1","c2"),
    con_multi("c1","language","op_isAnyOf",["de","en"])+"\n"+con("c2","language","op_eq","de_AT"),
    compat("c1","c2"), "unsat","Theorem")

# 111: isAnyOf {de, en} vs eq fr → fr ⊄ de, fr ⊄ en → Conflict
add("ODRL111-1","IsAnyOf","isAnyOf {de,en} vs eq fr: both branches fail",
    [LNG_KB], AG, d("c1","c2"),
    con_multi("c1","language","op_isAnyOf",["de","en"])+"\n"+
    anyof_only("c1",["de","en"])+"\n"+
    con("c2","language","op_eq","fr"),
    conflict("c1","c2"), "unsat","Theorem")

# 112: isAnyOf {comm, nonComm} vs eq sciRes → Unknown (sciRes ⊑? either)
add("ODRL112-1","IsAnyOf","isAnyOf {comm,nonComm} vs eq sciRes: Unknown",
    [DPV_KB], AG, d("c1","c2"),
    con_multi("c1","purpose","op_isAnyOf",["commercialPurpose","nonCommercialPurpose"])+"\n"+
    con("c2","purpose","op_eq","scientificResearch"),
    compat("c1","c2"), "sat","CounterSatisfiable")

# 113: isAnyOf {comm, mkt} vs eq commRes → commRes ⊑ comm → Compatible
add("ODRL113-1","IsAnyOf","isAnyOf {comm,mkt} vs eq commRes: Compatible",
    [DPV_KB], AG, d("c1","c2"),
    con_multi("c1","purpose","op_isAnyOf",["commercialPurpose","marketing"])+"\n"+
    con("c2","purpose","op_eq","commercialResearch"),
    compat("c1","c2"), "unsat","Theorem")

# 114: isAnyOf {france, germany} vs eq bavaria (spatial, mereological)
# bavaria ⊑ germany → Compatible
add("ODRL114-1","IsAnyOf","isAnyOf {france,germany} spatial: bavaria ⊑ germany",
    [GEO_KB], [GROUND_EQ, GROUND_ISANYOF_MEREO], d("c1","c2"),
    con_multi("c1","spatial","op_isAnyOf",["france","germany"])+"\n"+
    con("c2","spatial","op_eq","bavaria"),
    compat("c1","c2"), "unsat","Theorem")

# 115: isAnyOf {france, germany} vs eq europe (spatial)
# europe ⊄ france, europe ⊄ germany → Unknown (no bidirectional needed)
add("ODRL115-1","IsAnyOf","isAnyOf {france,germany} vs eq europe: Unknown",
    [GEO_KB], [GROUND_EQ, GROUND_ISANYOF_MEREO], d("c1","c2"),
    con_multi("c1","spatial","op_isAnyOf",["france","germany"])+"\n"+
    con("c2","spatial","op_eq","europe"),
    compat("c1","c2"), "sat","CounterSatisfiable")

# 116: isAnyOf vs isA cross-operator: isAnyOf {comm,mkt} vs isA R&D
# R&D subtree includes commRes ⊑ comm → overlap → Compatible
add("ODRL116-1","IsAnyOf","isAnyOf {comm,mkt} vs isA R&D: cross-op overlap",
    [DPV_KB], [GROUND_EQ, GROUND_ISA, GROUND_ISANYOF_TAX], d("c1","c2"),
    con_multi("c1","purpose","op_isAnyOf",["commercialPurpose","marketing"])+"\n"+
    con("c2","purpose","op_isA","researchAndDevelopment"),
    compat("c1","c2"), "unsat","Theorem")

# 117: isAnyOf vs isAnyOf: {de,en} vs {fr,ar} → disjoint families → Conflict
add("ODRL117-1","IsAnyOf","isAnyOf {de,en} vs isAnyOf {fr,ar}: open-world Unknown",
    [LNG_KB], [GROUND_EQ, GROUND_ISANYOF_TAX], d("c1","c2"),
    con_multi("c1","language","op_isAnyOf",["de","en"])+"\n"+
    anyof_only("c1",["de","en"])+"\n"+
    con_multi("c2","language","op_isAnyOf",["fr","ar"])+"\n"+
    anyof_only("c2",["fr","ar"]),
    conflict("c1","c2"), "sat","CounterSatisfiable")

# 118: isAnyOf vs isAnyOf: {de,ar} vs {en,ar} → overlap on ar family → Compatible
add("ODRL118-1","IsAnyOf","isAnyOf {de,ar} vs isAnyOf {en,ar}: overlap on ar",
    [LNG_KB], [GROUND_EQ, GROUND_ISANYOF_TAX], d("c1","c2"),
    con_multi("c1","language","op_isAnyOf",["de","ar"])+"\n"+
    con_multi("c2","language","op_isAnyOf",["en","ar"]),
    compat("c1","c2"), "unsat","Theorem")


# ============================================================
# ISALLOF extended (120–128): Intersection of closures
# ============================================================

# 120: isAllOf {R&D, comm} vs eq commRes → commRes ⊑ both → Compatible
add("ODRL120-1","IsAllOf","isAllOf {R&D,comm} vs eq commRes: Compatible",
    [DPV_KB], LG, d("c1","c2"),
    con_multi("c1","purpose","op_isAllOf",["researchAndDevelopment","commercialPurpose"])+"\n"+
    allof_if("c1",["researchAndDevelopment","commercialPurpose"])+"\n"+
    con("c2","purpose","op_eq","commercialResearch"),
    compat("c1","c2"), "unsat","Theorem")

# 121: isAllOf {comm, nonComm} → disjoint → empty intersection → Conflict with anything
add("ODRL121-1","IsAllOf","isAllOf {comm,nonComm}: impossible intersection",
    [DPV_KB], LG, d("c1","c2"),
    con_multi("c1","purpose","op_isAllOf",["commercialPurpose","nonCommercialPurpose"])+"\n"+
    allof_if("c1",["commercialPurpose","nonCommercialPurpose"])+"\n"+
    con("c2","purpose","op_eq","commercialResearch"),
    compat("c1","c2"), "sat","CounterSatisfiable")

# 122: isAllOf {R&D, nonComm} vs eq nonCommRes → nonCommRes ⊑ both → Compatible
add("ODRL122-1","IsAllOf","isAllOf {R&D,nonComm} vs eq nonCommRes: Compatible",
    [DPV_KB], LG, d("c1","c2"),
    con_multi("c1","purpose","op_isAllOf",["researchAndDevelopment","nonCommercialPurpose"])+"\n"+
    allof_if("c1",["researchAndDevelopment","nonCommercialPurpose"])+"\n"+
    con("c2","purpose","op_eq","nonCommercialResearch"),
    compat("c1","c2"), "unsat","Theorem")

# 123: isAllOf {R&D, nonComm} vs eq sciRes → Unknown (sciRes ⊑? nonComm)
add("ODRL123-1","IsAllOf","isAllOf {R&D,nonComm} vs eq sciRes: Unknown",
    [DPV_KB], LG, d("c1","c2"),
    con_multi("c1","purpose","op_isAllOf",["researchAndDevelopment","nonCommercialPurpose"])+"\n"+
    allof_if("c1",["researchAndDevelopment","nonCommercialPurpose"])+"\n"+
    con("c2","purpose","op_eq","scientificResearch"),
    compat("c1","c2"), "sat","CounterSatisfiable")

# 124: isAllOf on diamond KB: isAllOf {diaA, diaB} should find diaX
add("ODRL124-1","IsAllOf","Diamond: isAllOf {A,B} finds X",
    [DIAMOND_KB], [GROUND_EQ, GROUND_ISALLOF_TAX_ONLY], d("c1","c2"),
    con_multi("c1","purpose","op_isAllOf",["diaA","diaB"])+"\n"+
    allof_if("c1",["diaA","diaB"])+"\n"+
    con("c2","purpose","op_eq","diaX"),
    compat("c1","c2"), "unsat","Theorem")

# 125: isAllOf on diamond: isAllOf {A,B} vs eq diaC → diaC ⊑ A? No. → Unknown
# diaC is ancestor of A and B, not descendant
add("ODRL125-1","IsAllOf","Diamond: isAllOf {A,B} vs eq C → C not below both",
    [DIAMOND_KB], [GROUND_EQ, GROUND_ISALLOF_TAX_ONLY], d("c1","c2"),
    con_multi("c1","purpose","op_isAllOf",["diaA","diaB"])+"\n"+
    allof_if("c1",["diaA","diaB"])+"\n"+
    con("c2","purpose","op_eq","diaC"),
    compat("c1","c2"), "sat","CounterSatisfiable")

# 126: isAllOf on chain: isAllOf {chainC, chainD} vs eq chainA
# chainA ⊑ chainB ⊑ chainC ⊑ chainD → chainA ⊑ both → Compatible
add("ODRL126-1","IsAllOf","Chain: isAllOf {C,D} vs eq A: transitive hit",
    [CHAIN_KB], [GROUND_EQ, GROUND_ISALLOF_TAX_ONLY], d("c1","c2"),
    con_multi("c1","purpose","op_isAllOf",["chainC","chainD"])+"\n"+
    allof_if("c1",["chainC","chainD"])+"\n"+
    con("c2","purpose","op_eq","chainA"),
    compat("c1","c2"), "unsat","Theorem")

# 127: isAllOf vs isA: isAllOf {R&D, comm} vs isA comm → overlap on commRes
add("ODRL127-1","IsAllOf","isAllOf {R&D,comm} vs isA comm: overlap",
    [DPV_KB], [GROUND_EQ, GROUND_ISA, GROUND_ISALLOF_TAX_ONLY], d("c1","c2"),
    con_multi("c1","purpose","op_isAllOf",["researchAndDevelopment","commercialPurpose"])+"\n"+
    allof_if("c1",["researchAndDevelopment","commercialPurpose"])+"\n"+
    con("c2","purpose","op_isA","commercialPurpose"),
    compat("c1","c2"), "unsat","Theorem")

# 128: isAllOf vs isAnyOf: isAllOf {R&D,comm} vs isAnyOf {nonComm, mkt}
# isAllOf gives ↓R&D ∩ ↓comm = {commRes}. isAnyOf gives ↓nonComm ∪ ↓mkt.
# commRes ⊑ comm but commRes ⊄ nonComm or mkt → Unknown
add("ODRL128-1","IsAllOf","isAllOf vs isAnyOf: cross-operator Unknown",
    [DPV_KB], [GROUND_EQ, GROUND_ISALLOF_TAX_ONLY, GROUND_ISANYOF_TAX], d("c1","c2"),
    con_multi("c1","purpose","op_isAllOf",["researchAndDevelopment","commercialPurpose"])+"\n"+
    allof_if("c1",["researchAndDevelopment","commercialPurpose"])+"\n"+
    con_multi("c2","purpose","op_isAnyOf",["nonCommercialPurpose","marketing"])+"\n"+
    anyof_only("c2",["nonCommercialPurpose","marketing"]),
    conflict("c1","c2"), "sat","CounterSatisfiable")


# ============================================================
# ISNONEOF extended (130–139): Negated union
# ============================================================

# 130: isNoneOf {comm} vs eq nonCommRes → nonCommRes ⊄ comm → Compatible
add("ODRL130-1","IsNoneOf","isNoneOf {comm} vs eq nonCommRes: Compatible",
    [DPV_KB], NG, d("c1","c2"),
    con("c1","purpose","op_isNoneOf","commercialPurpose")+"\n"+
    noneof_if("c1",["commercialPurpose"])+"\n"+
    con("c2","purpose","op_eq","nonCommercialResearch"),
    compat("c1","c2"), "unsat","Theorem")

# 131: isNoneOf {comm} vs eq commRes → commRes ⊑ comm → Conflict
add("ODRL131-1","IsNoneOf","isNoneOf {comm} vs eq commRes: Conflict",
    [DPV_KB], NG, d("c1","c2"),
    con("c1","purpose","op_isNoneOf","commercialPurpose")+"\n"+
    con("c2","purpose","op_eq","commercialResearch"),
    conflict("c1","c2"), "unsat","Theorem")

# 132: isNoneOf {comm} vs eq sciRes → Unknown (sciRes ⊑? comm)
add("ODRL132-1","IsNoneOf","isNoneOf {comm} vs eq sciRes: Unknown",
    [DPV_KB], NG, d("c1","c2"),
    con("c1","purpose","op_isNoneOf","commercialPurpose")+"\n"+
    noneof_if("c1",["commercialPurpose"])+"\n"+
    con("c2","purpose","op_eq","scientificResearch"),
    compat("c1","c2"), "sat","CounterSatisfiable")

# 133: isNoneOf {comm, nonComm} vs eq R&D → R&D ⊄ either → Compatible
add("ODRL133-1","IsNoneOf","isNoneOf {comm,nonComm} vs eq R&D: Unknown (R&D ⊑? either)",
    [DPV_KB], NG, d("c1","c2"),
    con_multi("c1","purpose","op_isNoneOf",["commercialPurpose","nonCommercialPurpose"])+"\n"+
    noneof_if("c1",["commercialPurpose","nonCommercialPurpose"])+"\n"+
    con("c2","purpose","op_eq","researchAndDevelopment"),
    compat("c1","c2"), "sat","CounterSatisfiable")

# 134: isNoneOf {R&D} vs isA R&D → direct contradiction → Conflict
add("ODRL134-1","IsNoneOf","isNoneOf {R&D} vs isA R&D: contradiction",
    [DPV_KB], [GROUND_EQ, GROUND_ISA, GROUND_ISNONEOF_TAX_ONLY], d("c1","c2"),
    con("c1","purpose","op_isNoneOf","researchAndDevelopment")+"\n"+
    con("c2","purpose","op_isA","researchAndDevelopment"),
    conflict("c1","c2"), "unsat","Theorem")

# 135: isNoneOf {de} vs isA de → contradiction (language)
add("ODRL135-1","IsNoneOf","isNoneOf {de} vs isA de: lang contradiction",
    [LNG_KB], [GROUND_EQ, GROUND_ISA, GROUND_ISNONEOF_TAX_ONLY], d("c1","c2"),
    con("c1","language","op_isNoneOf","de")+"\n"+
    con("c2","language","op_isA","de"),
    conflict("c1","c2"), "unsat","Theorem")

# 136: isNoneOf {france} vs isPartOf europe (spatial, mereological)
# isNoneOf(france) = {x | x ⊄ france}. isPartOf(europe) = {x | x ⊑ europe} = all.
# Overlap: germany, bavaria ∈ both → Compatible
add("ODRL136-1","IsNoneOf","isNoneOf {france} spatial vs isPartOf europe",
    [GEO_KB], [GROUND_EQ, GROUND_ISPARTOF, GROUND_ISNONEOF_MEREO], d("c1","c2"),
    con("c1","spatial","op_isNoneOf","france")+"\n"+
    noneof_if_mereo("c1",["france"])+"\n"+
    con("c2","spatial","op_isPartOf","europe"),
    compat("c1","c2"), "unsat","Theorem")

# 137: isNoneOf {de, en} vs isAnyOf {de, en} → direct contradiction → Conflict
add("ODRL137-1","IsNoneOf","isNoneOf {de,en} vs isAnyOf {de,en}: contradiction",
    [LNG_KB], [GROUND_EQ, GROUND_ISANYOF_TAX, GROUND_ISNONEOF_TAX_ONLY], d("c1","c2"),
    con_multi("c1","language","op_isNoneOf",["de","en"])+"\n"+
    con_multi("c2","language","op_isAnyOf",["de","en"])+"\n"+
    anyof_only("c2",["de","en"]),
    conflict("c1","c2"), "unsat","Theorem")

# 138: double negation: isNoneOf {comm} vs isNoneOf {nonComm}
# C\↓comm ∩ C\↓nonComm → R&D, sciRes, acadRes (neither comm nor nonComm) → Compatible
add("ODRL138-1","IsNoneOf","Double negation: isNoneOf {comm} vs isNoneOf {nonComm}",
    [DPV_KB], NG, d("c1","c2"),
    con("c1","purpose","op_isNoneOf","commercialPurpose")+"\n"+
    noneof_if("c1",["commercialPurpose"])+"\n"+
    con("c2","purpose","op_isNoneOf","nonCommercialPurpose")+"\n"+
    noneof_if("c2",["nonCommercialPurpose"]),
    compat("c1","c2"), "unsat","Theorem")

# 139: isNoneOf on single-concept KB → isNoneOf {singleton} = ∅ → Conflict with eq singleton
add("ODRL139-1","IsNoneOf","isNoneOf singleton on |C|=1: empty set",
    [SINGLE_KB], [GROUND_EQ, GROUND_ISNONEOF_TAX_ONLY], d("c1","c2"),
    con("c1","purpose","op_isNoneOf","singleton")+"\n"+
    con("c2","purpose","op_eq","singleton"),
    conflict("c1","c2"), "unsat","Theorem")


# ============================================================
# NOMINAL (140–147): Identity domain, isA=eq degeneration
# ============================================================

# 140: eq email vs eq email → Compatible (identity)
add("ODRL140-1","Nominal","Nominal eq email vs eq email: Compatible",
    [NOMINAL_KB], [GROUND_EQ], d("c1","c2"),
    con("c1","channel","op_eq","email")+"\n"+con("c2","channel","op_eq","email"),
    compat("c1","c2"), "unsat","Theorem")

# 141: eq email vs eq api → Conflict (different)
add("ODRL141-1","Nominal","Nominal eq email vs eq api: Conflict",
    [NOMINAL_KB], [GROUND_EQ], d("c1","c2"),
    con("c1","channel","op_eq","email")+"\n"+con("c2","channel","op_eq","api"),
    conflict("c1","c2"), "unsat","Theorem")

# 142: isA email under nominal → degenerates to eq → same as eq email
add("ODRL142-1","Nominal","Nominal isA email = eq email: Compatible with eq email",
    [NOMINAL_KB], NOM_G, d("c1","c2"),
    con("c1","channel","op_isA","email")+"\n"+con("c2","channel","op_eq","email"),
    compat("c1","c2"), "unsat","Theorem")

# 143: isA email vs eq api → Conflict (isA degenerates to eq, different values)
add("ODRL143-1","Nominal","Nominal isA email vs eq api: Conflict",
    [NOMINAL_KB], NOM_G, d("c1","c2"),
    con("c1","channel","op_isA","email")+"\n"+con("c2","channel","op_eq","api"),
    conflict("c1","c2"), "unsat","Theorem")

# 144: isAnyOf {email, api} under nominal → membership test
# vs eq ftp → ftp ∉ {email, api} → Conflict
add("ODRL144-1","Nominal","Nominal isAnyOf {email,api} vs eq ftp: Conflict",
    [NOMINAL_KB], NOM_ANY, d("c1","c2"),
    con_multi("c1","channel","op_isAnyOf",["email","api"])+"\n"+
    "(assert (forall ((x Entity)) (=> (in_denotation x c1) (or (= x email) (= x api)))))\n"+
    con("c2","channel","op_eq","ftp"),
    conflict("c1","c2"), "unsat","Theorem")

# 145: isAnyOf {email, api} vs eq email → Compatible
add("ODRL145-1","Nominal","Nominal isAnyOf {email,api} vs eq email: Compatible",
    [NOMINAL_KB], NOM_ANY, d("c1","c2"),
    con_multi("c1","channel","op_isAnyOf",["email","api"])+"\n"+
    con("c2","channel","op_eq","email"),
    compat("c1","c2"), "unsat","Theorem")

# 146: isNoneOf {email, api} under nominal vs eq ftp → ftp ≠ email,api → Compatible
add("ODRL146-1","Nominal","Nominal isNoneOf {email,api} vs eq ftp: Compatible",
    [NOMINAL_KB], NOM_NONE, d("c1","c2"),
    con_multi("c1","channel","op_isNoneOf",["email","api"])+"\n"+
    "(assert (forall ((x Entity)) (=> (in_denotation x c1) (and (not (= x email)) (not (= x api))))))\n"+
    "(assert (forall ((x Entity)) (=> (and (not (= x email)) (not (= x api))) (in_denotation x c1))))\n"+
    con("c2","channel","op_eq","ftp"),
    compat("c1","c2"), "unsat","Theorem")

# 147: neq email under nominal vs eq email → Conflict
add("ODRL147-1","Nominal","Nominal neq email vs eq email: Conflict",
    [NOMINAL_KB], [GROUND_EQ, GROUND_NEQ], d("c1","c2"),
    con("c1","channel","op_neq","email")+"\n"+con("c2","channel","op_eq","email"),
    conflict("c1","c2"), "unsat","Theorem")


# ============================================================
# OPERATOR PAIRS (150–161): Cross-operator interactions
# ============================================================

# 150: isA vs isNoneOf same concept → direct contradiction
add("ODRL150-1","OperatorPairs","isA nonComm vs isNoneOf nonComm: contradiction",
    [DPV_KB], [GROUND_EQ, GROUND_ISA, GROUND_ISNONEOF_TAX_ONLY], d("c1","c2"),
    con("c1","purpose","op_isA","nonCommercialPurpose")+"\n"+
    con("c2","purpose","op_isNoneOf","nonCommercialPurpose"),
    conflict("c1","c2"), "unsat","Theorem")

# 151: neq vs isA: neq comm vs isA comm → overlap (commRes ⊑ comm, commRes ≠ comm)
add("ODRL151-1","OperatorPairs","neq comm vs isA comm: overlap on children",
    [DPV_KB + DPV_DISTINCT + DPV_CROSS_LEVEL], [GROUND_EQ, GROUND_NEQ, GROUND_ISA], d("c1","c2"),
    con("c1","purpose","op_neq","commercialPurpose")+"\n"+
    con("c2","purpose","op_isA","commercialPurpose"),
    compat("c1","c2"), "unsat","Theorem")

# 152: hasPart vs isPartOf same value → overlap on that value (reflexive)
add("ODRL152-1","OperatorPairs","hasPart france vs isPartOf france: reflexive overlap",
    [GEO_KB], HG, d("c1","c2"),
    con("c1","spatial","op_hasPart","france")+"\n"+
    con("c2","spatial","op_isPartOf","france"),
    compat("c1","c2"), "unsat","Theorem")

# 153: isAllOf vs isAnyOf: {R&D, nonComm} vs {comm, mkt} → commRes vs nonCommRes → ?
add("ODRL153-1","OperatorPairs","isAllOf {R&D,nonComm} vs isAnyOf {comm,mkt}: Unknown",
    [DPV_KB], [GROUND_EQ, GROUND_ISALLOF_TAX_ONLY, GROUND_ISANYOF_TAX], d("c1","c2"),
    con_multi("c1","purpose","op_isAllOf",["researchAndDevelopment","nonCommercialPurpose"])+"\n"+
    allof_if("c1",["researchAndDevelopment","nonCommercialPurpose"])+"\n"+
    con_multi("c2","purpose","op_isAnyOf",["commercialPurpose","marketing"])+"\n"+
    anyof_only("c2",["commercialPurpose","marketing"]),
    conflict("c1","c2"), "sat","CounterSatisfiable")

# 154: isNoneOf vs isNoneOf overlapping: isNoneOf {de} vs isNoneOf {en}
# C\{de↓} ∩ C\{en↓} = {fr, ar, arb, arz} → Compatible
add("ODRL154-1","OperatorPairs","isNoneOf {de} vs isNoneOf {en}: shared exclusion",
    [LNG_KB], [GROUND_EQ, GROUND_ISNONEOF_TAX_ONLY], d("c1","c2"),
    con("c1","language","op_isNoneOf","de")+"\n"+
    noneof_if("c1",["de"],"language")+"\n"+
    con("c2","language","op_isNoneOf","en")+"\n"+
    noneof_if("c2",["en"],"language"),
    compat("c1","c2"), "unsat","Theorem")

# 155: isPartOf vs hasPart inverse test (not same entity)
# isPartOf(germany) = {bavaria, germany}. hasPart(france) = {france, europe}.
# Overlap? germany ∈ isPartOf(germany). germany ∈ hasPart(france)? → germany ≥ france? No.
# → no proven overlap → Unknown
add("ODRL155-1","OperatorPairs","isPartOf germany vs hasPart france: no proven overlap",
    [GEO_KB], HG, d("c1","c2"),
    con("c1","spatial","op_isPartOf","germany")+"\n"+
    con("c2","spatial","op_hasPart","france"),
    compat("c1","c2"), "sat","CounterSatisfiable")

# 156: eq vs isNoneOf: eq acadRes vs isNoneOf {R&D} → acadRes ⊑ R&D → Conflict
add("ODRL156-1","OperatorPairs","eq acadRes vs isNoneOf {R&D}: Conflict",
    [DPV_KB], [GROUND_EQ, GROUND_ISNONEOF_TAX_ONLY], d("c1","c2"),
    con("c1","purpose","op_eq","academicResearch")+"\n"+
    con("c2","purpose","op_isNoneOf","researchAndDevelopment"),
    conflict("c1","c2"), "unsat","Theorem")

# 157: isAnyOf vs isNoneOf same values: isAnyOf {de,en} vs isNoneOf {de,en}
add("ODRL157-1","OperatorPairs","isAnyOf {de,en} vs isNoneOf {de,en}: contradiction",
    [LNG_KB], [GROUND_EQ, GROUND_ISANYOF_TAX, GROUND_ISNONEOF_TAX_ONLY], d("c1","c2"),
    con_multi("c1","language","op_isAnyOf",["de","en"])+"\n"+
    anyof_only("c1",["de","en"])+"\n"+
    con_multi("c2","language","op_isNoneOf",["de","en"])+"\n"+
    noneof_if("c2",["de","en"],"language"),
    conflict("c1","c2"), "unsat","Theorem")

# 158: neq vs neq: neq de vs neq en → large overlap → Compatible
add("ODRL158-1","OperatorPairs","neq de vs neq en: large overlap",
    [LNG_KB], NQ, d("c1","c2"),
    con("c1","language","op_neq","de")+"\n"+con("c2","language","op_neq","en"),
    compat("c1","c2"), "unsat","Theorem")

# 159: isA vs isAnyOf overlap: isA R&D vs isAnyOf {comm, nonComm}
# R&D subtree includes commRes ⊑ comm → overlap → Compatible
add("ODRL159-1","OperatorPairs","isA R&D vs isAnyOf {comm,nonComm}: overlap",
    [DPV_KB], [GROUND_EQ, GROUND_ISA, GROUND_ISANYOF_TAX], d("c1","c2"),
    con("c1","purpose","op_isA","researchAndDevelopment")+"\n"+
    con_multi("c2","purpose","op_isAnyOf",["commercialPurpose","nonCommercialPurpose"]),
    compat("c1","c2"), "unsat","Theorem")

# 160: hasPart vs hasPart disjoint: hasPart(germany)={ger,eu} vs hasPart(france)={fr,eu}
# Overlap on europe → Compatible
add("ODRL160-1","OperatorPairs","hasPart germany vs hasPart france: meet at europe",
    [GEO_KB], HG, d("c1","c2"),
    con("c1","spatial","op_hasPart","germany")+"\n"+
    con("c2","spatial","op_hasPart","france"),
    compat("c1","c2"), "unsat","Theorem")

# 161: isAllOf vs isNoneOf: isAllOf {R&D,comm} vs isNoneOf {comm} → Conflict
# isAllOf requires ⊑ comm, isNoneOf excludes ⊑ comm → disjoint
add("ODRL161-1","OperatorPairs","isAllOf {R&D,comm} vs isNoneOf {comm}: Conflict",
    [DPV_KB], [GROUND_EQ, GROUND_ISALLOF_TAX_ONLY, GROUND_ISNONEOF_TAX_ONLY], d("c1","c2"),
    con_multi("c1","purpose","op_isAllOf",["researchAndDevelopment","commercialPurpose"])+"\n"+
    allof_if("c1",["researchAndDevelopment","commercialPurpose"])+"\n"+
    con("c2","purpose","op_isNoneOf","commercialPurpose"),
    conflict("c1","c2"), "unsat","Theorem")


# ============================================================
# ADVERSARIAL DEEP (170–181): Chains, diamonds, edge cases
# ============================================================

# 170: Chain depth-5: isA chainE vs eq chainA → chainA ⊑ chainE → Compatible
add("ODRL170-1","AdvDeep","Chain-5: isA E vs eq A → transitive Compatible",
    [CHAIN_KB], [GROUND_EQ, GROUND_ISA], d("c1","c2"),
    con("c1","purpose","op_isA","chainE")+"\n"+con("c2","purpose","op_eq","chainA"),
    compat("c1","c2"), "unsat","Theorem")

# 171: Chain: isA chainC vs eq chainD → chainD ⊄ chainC → Conflict
add("ODRL171-1","AdvDeep","Chain-5: isA C vs eq D → D not below C → Conflict",
    [CHAIN_KB], [GROUND_EQ, GROUND_ISA], d("c1","c2"),
    con("c1","purpose","op_isA","chainC")+"\n"+con("c2","purpose","op_eq","chainD"),
    conflict("c1","c2"), "unsat","Theorem")

# 172: Diamond: isA C vs eq X → X ⊑ A ⊑ C → Compatible
add("ODRL172-1","AdvDeep","Diamond: isA C vs eq X → X ⊑ C via A",
    [DIAMOND_KB], [GROUND_EQ, GROUND_ISA], d("c1","c2"),
    con("c1","purpose","op_isA","diaC")+"\n"+con("c2","purpose","op_eq","diaX"),
    compat("c1","c2"), "unsat","Theorem")

# 173: Diamond: isA A vs isA B → overlap on X → Compatible
add("ODRL173-1","AdvDeep","Diamond: isA A vs isA B → overlap on X",
    [DIAMOND_KB], [GROUND_EQ, GROUND_ISA], d("c1","c2"),
    con("c1","purpose","op_isA","diaA")+"\n"+con("c2","purpose","op_isA","diaB"),
    compat("c1","c2"), "unsat","Theorem")

# 174: Diamond: isA A vs eq B → B ⊄ A → Conflict
add("ODRL174-1","AdvDeep","Diamond: isA A vs eq B → incomparable → Conflict",
    [DIAMOND_KB], [GROUND_EQ, GROUND_ISA], d("c1","c2"),
    con("c1","purpose","op_isA","diaA")+"\n"+con("c2","purpose","op_eq","diaB"),
    conflict("c1","c2"), "unsat","Theorem")

# 175: Single-concept KB: eq singleton vs eq singleton → Compatible (trivially)
add("ODRL175-1","AdvDeep","Single |C|=1: eq vs eq → Compatible",
    [SINGLE_KB], [GROUND_EQ], d("c1","c2"),
    con("c1","purpose","op_eq","singleton")+"\n"+con("c2","purpose","op_eq","singleton"),
    compat("c1","c2"), "unsat","Theorem")

# 176: Single-concept: isA singleton vs neq singleton → Conflict (isA={singleton}, neq=∅)
add("ODRL176-1","AdvDeep","Single |C|=1: isA vs neq → Conflict",
    [SINGLE_KB], [GROUND_EQ, GROUND_ISA, GROUND_NEQ], d("c1","c2"),
    con("c1","purpose","op_isA","singleton")+"\n"+con("c2","purpose","op_neq","singleton"),
    conflict("c1","c2"), "unsat","Theorem")

# 177: Near-miss: isA nmLeft vs isA nmRight → overlap on nmShared → Compatible
add("ODRL177-1","AdvDeep","Near-miss: isA Left vs isA Right → overlap on Shared",
    [NEARMISS_KB], [GROUND_EQ, GROUND_ISA], d("c1","c2"),
    con("c1","purpose","op_isA","nmLeft")+"\n"+con("c2","purpose","op_isA","nmRight"),
    compat("c1","c2"), "unsat","Theorem")

# 178: Near-miss: eq nmOnlyLeft vs isA nmRight → nmOnlyLeft ⊄ nmRight → Conflict
add("ODRL178-1","AdvDeep","Near-miss: eq OnlyLeft vs isA Right → Conflict",
    [NEARMISS_KB], [GROUND_EQ, GROUND_ISA], d("c1","c2"),
    con("c1","purpose","op_eq","nmOnlyLeft")+"\n"+con("c2","purpose","op_isA","nmRight"),
    conflict("c1","c2"), "unsat","Theorem")

# 179: All-⊤ composition: spatial Unknown AND purpose Unknown → conjunction Unknown
# Use KBs where both operands have missing negative axioms
add("ODRL179-1","AdvDeep","All-Unknown conjunction: both operands Unknown",
    [GEO_KB, DPV_KB], TG, d("c1","c2","c3","c4"),
    con("c1","spatial","op_isPartOf","france")+"\n"+
    con("c2","spatial","op_eq","bavaria")+"\n"+
    con("c3","purpose","op_isA","nonCommercialPurpose")+"\n"+
    con("c4","purpose","op_eq","scientificResearch"),
    cross2("c1","c2","c3","c4"), "sat","CounterSatisfiable")

# 180: Chain: isAnyOf {chainA, chainE} vs eq chainC → both branches: A⊑C ✓ → Compatible
add("ODRL180-1","AdvDeep","Chain: isAnyOf {A,E} vs eq C → A ⊑ C",
    [CHAIN_KB], [GROUND_EQ, GROUND_ISANYOF_TAX], d("c1","c2"),
    con_multi("c1","purpose","op_isAnyOf",["chainA","chainE"])+"\n"+
    con("c2","purpose","op_eq","chainC"),
    compat("c1","c2"), "unsat","Theorem")

# 181: Chain: isNoneOf {chainE} vs eq chainD → chainD ⊄ chainE → Compatible
add("ODRL181-1","AdvDeep","Chain: isNoneOf {E} vs eq D → D ⊑ E → Conflict",
    [CHAIN_KB + CHAIN_DISTINCT], [GROUND_EQ, GROUND_ISNONEOF_TAX_ONLY], d("c1","c2"),
    con("c1","purpose","op_isNoneOf","chainE")+"\n"+
    noneof_if("c1",["chainE"])+"\n"+
    con("c2","purpose","op_eq","chainD"),
    conflict("c1","c2"), "unsat","Theorem")


# ============================================================
# ALIGNMENT ADVERSARIAL (190–199): Edge cases
# ============================================================

# 190: Alignment where witness is unmapped → must degrade
# BCP47 de_AT compatible with isA de, but ISO639-3 lacks de_AT → Unknown
add("ODRL190-1","AlignAdv","Unmapped witness: de_AT compatible in KB_A, unmapped in KB_B",
    [LNG1_KB], PG, d("c1","c2","de_AT"),
    con("c1","language","op_isA","deu")+"\n"+con("c2","language","op_eq","de_AT"),
    compat("c1","c2"), "sat","CounterSatisfiable")

# 191: Same as 190 but testing conflict direction → also Unknown
add("ODRL191-1","AlignAdv","Unmapped witness: no false conflict either",
    [LNG1_KB], PG, d("c1","c2","de_AT"),
    con("c1","language","op_isA","deu")+"\n"+con("c2","language","op_eq","de_AT"),
    conflict("c1","c2"), "sat","CounterSatisfiable")

# 192: Partial spatial alignment: GEO1 has no bavaria
# isPartOf deu vs eq bavaria → Unknown in GEO1
add("ODRL192-1","AlignAdv","Spatial: bavaria unmapped in ISO3166",
    [GEO1_KB], SG, d("c1","c2","bavaria"),
    con("c1","spatial","op_isPartOf","deu")+"\n"+con("c2","spatial","op_eq","bavaria"),
    compat("c1","c2"), "sat","CounterSatisfiable")

# 193: Aligned conflict preserved with isAnyOf: isAnyOf {deu,eng} vs eq fra
add("ODRL193-1","AlignAdv","Aligned isAnyOf conflict: {deu,eng} vs fra",
    [LNG1_KB], [GROUND_EQ, GROUND_ISANYOF_TAX], d("c1","c2"),
    con_multi("c1","language","op_isAnyOf",["deu","eng"])+"\n"+
    anyof_only("c1",["deu","eng"])+"\n"+
    con("c2","language","op_eq","fra"),
    conflict("c1","c2"), "unsat","Theorem")

# 194: Aligned isNoneOf: isNoneOf {deu} vs eq fra → Compatible in ISO639-3
add("ODRL194-1","AlignAdv","Aligned isNoneOf: {deu} vs eq fra → Compatible",
    [LNG1_KB], [GROUND_EQ, GROUND_ISNONEOF_TAX_ONLY], d("c1","c2"),
    con("c1","language","op_isNoneOf","deu")+"\n"+
    noneof_if("c1",["deu"],"language")+"\n"+
    con("c2","language","op_eq","fra"),
    compat("c1","c2"), "unsat","Theorem")

# 195: Cross-KB hasPart: hasPart fra vs eq eur in ISO3166 → Compatible
add("ODRL195-1","AlignAdv","Aligned hasPart: fra hasPart vs eq eur",
    [GEO1_KB], HG, d("c1","c2"),
    con("c1","spatial","op_hasPart","fra")+"\n"+con("c2","spatial","op_eq","eur"),
    compat("c1","c2"), "unsat","Theorem")

# 196: Alignment with neq: neq deu vs eq fra → Compatible in ISO639-3
add("ODRL196-1","AlignAdv","Aligned neq: neq deu vs eq fra → Compatible",
    [LNG1_KB], [GROUND_EQ, GROUND_NEQ], d("c1","c2"),
    con("c1","language","op_neq","deu")+"\n"+con("c2","language","op_eq","fra"),
    compat("c1","c2"), "unsat","Theorem")

# 197: Alignment with neq: neq deu vs eq deu → Conflict
add("ODRL197-1","AlignAdv","Aligned neq: neq deu vs eq deu → Conflict",
    [LNG1_KB], [GROUND_EQ, GROUND_NEQ], d("c1","c2"),
    con("c1","language","op_neq","deu")+"\n"+con("c2","language","op_eq","deu"),
    conflict("c1","c2"), "unsat","Theorem")

# 198: 3-KB aligned cross-DS with hasPart
add("ODRL198-1","AlignAdv","3-KB aligned: hasPart spatial + isA purpose + isA lang",
    [GEO1_KB, DPV_KB, LNG1_KB_NODUP], [GROUND_EQ, GROUND_HASPART, GROUND_ISPARTOF, GROUND_ISA],
    d("c1","c2","c3","c4","c5","c6"),
    con("c1","spatial","op_hasPart","fra")+"\n"+
    con("c2","spatial","op_eq","eur")+"\n"+
    con("c3","purpose","op_isA","researchAndDevelopment")+"\n"+
    con("c4","purpose","op_eq","academicResearch")+"\n"+
    con("c5","language","op_isA","lang_deu")+"\n"+
    con("c6","language","op_eq","lang_fra"),
    cross3("c1","c2","c3","c4","c5","c6"), "sat","CounterSatisfiable")

# 199: Alignment degradation on all 3 operands → all Unknown → conjunction Unknown
add("ODRL199-1","AlignAdv","Triple degradation: all 3 operands unmapped",
    [GEO1_KB, DPV_KB, LNG1_KB_NODUP], TG,
    d("c1","c2","c3","c4","c5","c6","bavaria","lang_de_AT"),
    con("c1","spatial","op_isPartOf","deu")+"\n"+
    con("c2","spatial","op_eq","bavaria")+"\n"+
    con("c3","purpose","op_isA","researchAndDevelopment")+"\n"+
    con("c4","purpose","op_eq","scientificResearch")+"\n"+
    con("c5","language","op_isA","lang_deu")+"\n"+
    con("c6","language","op_eq","lang_de_AT"),
    cross3("c1","c2","c3","c4","c5","c6"), "sat","CounterSatisfiable")


# ============================================================
# COMPOSITION DEEP (200–207): Complex composition patterns
# ============================================================

# 200: 3-operand AND: spatial+purpose+language all Compatible → Theorem
add("ODRL200-1","CompDeep","3-op AND all Compatible",
    [GEO_KB, DPV_KB, LNG_KB_FACTS], TG, d("c1","c2","c3","c4","c5","c6"),
    con("c1","spatial","op_isPartOf","europe")+"\n"+
    con("c2","spatial","op_eq","france")+"\n"+
    con("c3","purpose","op_isA","researchAndDevelopment")+"\n"+
    con("c4","purpose","op_eq","academicResearch")+"\n"+
    con("c5","language","op_isA","de")+"\n"+
    con("c6","language","op_eq","de_AT"),
    cross3("c1","c2","c3","c4","c5","c6"), "unsat","Theorem")

# 201: 3-op AND: last operand conflicts → blocks → CounterSat
add("ODRL201-1","CompDeep","3-op AND: language conflicts → blocks",
    [GEO_KB, DPV_KB, LNG_KB_FACTS], TG, d("c1","c2","c3","c4","c5","c6"),
    con("c1","spatial","op_isPartOf","europe")+"\n"+
    con("c2","spatial","op_eq","france")+"\n"+
    con("c3","purpose","op_isA","researchAndDevelopment")+"\n"+
    con("c4","purpose","op_eq","academicResearch")+"\n"+
    con("c5","language","op_isA","de")+"\n"+
    con("c6","language","op_eq","fr"),
    cross3("c1","c2","c3","c4","c5","c6"), "sat","CounterSatisfiable")

# 202: OR where all branches Unknown except one Compatible
# or(isA nonComm, isA de) vs eq de_AT: first branch indeterminate, second Compatible
add("ODRL202-1","CompDeep","OR: one Compatible branch resolves",
    [DPV_KB, LNG_KB_FACTS], [GROUND_EQ, GROUND_ISA], d("c1","c2","c3"),
    con("c1","purpose","op_isA","nonCommercialPurpose")+"\n"+
    con("c2","language","op_isA","de")+"\n"+
    con("c3","language","op_eq","de_AT"),
    or_compat("c1","c2","c3"), "unsat","Theorem")

# 203: OR where all branches are Conflict
add("ODRL203-1","CompDeep","OR: all branches Conflict",
    [LNG_KB], PG, d("c1","c2","c3"),
    con("c1","language","op_isA","de")+"\n"+
    con("c2","language","op_isA","en")+"\n"+
    con("c3","language","op_eq","fr"),
    or_conflict("c1","c2","c3"), "unsat","Theorem")

# 204: XONE where two branches are both Compatible → should be Unknown
# xone(isA R&D, isA nonComm) vs eq nonCommRes: nonCommRes in both → violates exclusivity
add("ODRL204-1","CompDeep","XONE: two branches Compatible → Unknown",
    [DPV_KB], PG, d("c1","c2","c3"),
    con("c1","purpose","op_isA","researchAndDevelopment")+"\n"+
    con("c2","purpose","op_isA","nonCommercialPurpose")+"\n"+
    con("c3","purpose","op_eq","nonCommercialResearch"),
    xone_compat("c1","c2","c3"), "sat","CounterSatisfiable")

# 205: XONE with one Compatible, one Unknown → must return Unknown
# xone(isA comm, isA nonComm) vs eq sciRes: sciRes ⊑? either → both Unknown → XONE Unknown
add("ODRL205-1","CompDeep","XONE: one Unknown branch → Unknown",
    [DPV_KB], PG, d("c1","c2","c3"),
    con("c1","purpose","op_isA","commercialPurpose")+"\n"+
    con("c2","purpose","op_isA","nonCommercialPurpose")+"\n"+
    con("c3","purpose","op_eq","scientificResearch"),
    xone_compat("c1","c2","c3"), "sat","CounterSatisfiable")

# 206: AND of OR: (spatial compat) AND or(purpose1, purpose2) both branches
add("ODRL206-1","CompDeep","AND-of-OR: spatial AND or(purpose)",
    [GEO_KB, DPV_KB], TG, d("cs","co","c1","c2","c3"),
    con("cs","spatial","op_isPartOf","europe")+"\n"+
    con("co","spatial","op_eq","france")+"\n"+
    con("c1","purpose","op_isA","commercialPurpose")+"\n"+
    con("c2","purpose","op_isA","nonCommercialPurpose")+"\n"+
    con("c3","purpose","op_eq","nonCommercialResearch"),
    f"""(assert (not (and
  (exists ((x Entity)) (and (in_denotation x cs) (in_denotation x co)))
  (or
    (exists ((y Entity)) (and (in_denotation y c1) (in_denotation y c3)))
    (exists ((z Entity)) (and (in_denotation z c2) (in_denotation z c3)))))))""",
    "unsat","Theorem")

# 207: AND of XONE: spatial AND xone(purpose1, purpose2) 
# Spatial Compatible, XONE Unknown → conjunction Unknown
add("ODRL207-1","CompDeep","AND-of-XONE: spatial compat AND xone purpose → Unknown",
    [GEO_KB, DPV_KB], TG, d("cs","co","c1","c2","c3"),
    con("cs","spatial","op_isPartOf","europe")+"\n"+
    con("co","spatial","op_eq","france")+"\n"+
    con("c1","purpose","op_isA","commercialPurpose")+"\n"+
    con("c2","purpose","op_isA","nonCommercialPurpose")+"\n"+
    con("c3","purpose","op_eq","scientificResearch"),
    f"""(assert (not (and
  (exists ((x Entity)) (and (in_denotation x cs) (in_denotation x co)))
  (or
    (exists ((y Entity)) (and (in_denotation y c1) (not (in_denotation y c2)) (in_denotation y c3)))
    (exists ((z Entity)) (and (in_denotation z c2) (not (in_denotation z c1)) (in_denotation z c3)))))))""",
    "sat","CounterSatisfiable")


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

    # Count by category
    cats = {}
    for p in P:
        c = p["sub"]
        cats[c] = cats.get(c, 0) + 1

    for p in P:
        sd = os.path.join(SMT_DIR, p["sub"])
        os.makedirs(sd, exist_ok=True)
        with open(os.path.join(sd, f"{p['id']}.smt2"), "w") as f:
            f.write(gen(p))

    print(f"Generated {len(P)} extension SMT-LIB2 files in {SMT_DIR}/")
    print("\nBreakdown:")
    for c, n in sorted(cats.items()): print(f"  {c:<16} {n}")

    if not do_run: print("\nUse --run to execute Z3."); return

    hdr = f"{'Problem':<14} {'Expected':>8} {'Z3':>8} {'Time':>8}  {'SZS':>16}  {'OK':>3}"
    print(); print(hdr); print("-"*len(hdr))

    ok = True; rcats = {}
    for p in P:
        fp = os.path.join(SMT_DIR, p["sub"], f"{p['id']}.smt2")
        z3r, z3t = run(["z3"], fp)
        m = "✓" if z3r == p["esmt"] else "✗"
        if z3r != p["esmt"]: ok = False
        print(f"{p['id']:<14} {p['esmt']:>8} {z3r:>8} {z3t:>7.3f}s  {p['eszs']:>16}  {m:>3}")
        c = p["sub"]
        if c not in rcats: rcats[c] = [0,0]
        rcats[c][0] += 1; rcats[c][1] += 1 if z3r == p["esmt"] else 0

    print()
    for c, (t, p_) in sorted(rcats.items()): print(f"  {c:<16} {p_}/{t} {'✓' if p_==t else '✗'}")
    total_ok = sum(v[1] for v in rcats.values()); total = sum(v[0] for v in rcats.values())
    print(f"  {'TOTAL':<16} {total_ok}/{total}")
    print("\nAll match ✓" if ok else "\nWARNING: mismatches ✗")

if __name__ == "__main__":
    main()
