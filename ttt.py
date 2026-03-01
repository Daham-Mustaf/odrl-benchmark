#!/usr/bin/env python3
"""
gen_extreme_suite.py — EXTREME ATP Challenge Suite (Categories 17–19).

Produces 18 .p files rated "Very Hard" to "Extreme" — pushing ATP limits
using ONLY the existing axiom infrastructure (no new predicates).

Key insight: extreme difficulty comes from COMBINATORIAL DEPTH, not syntax:
  - isNoneOf chains (complement reasoning)
  - Set operator interactions (isAllOf ∩ isNoneOf ∩ isAnyOf)
  - Combined: multi-hop + n-way + set ops + DAG multi-parent
  - Deep universal-existential alternation with set operators

Categories:
  17 — Set Operator Stress (ODRL200–205)       isNoneOf/isAllOf/isAnyOf extremes
  18 — Combined Complexity (ODRL210–215)        Multi-hop + n-way + set ops + DAG
  19 — Adversarial Operator Patterns (ODRL220–225) Boundary/degenerate set ops

Usage:
    python gen_extreme_suite.py --outdir Problems/ODRL

Authors: Mustafa, D. & Sutcliffe, G.
"""
import argparse
import os
from datetime import date


# ═══════════════════════════════════════════════════════════════════════════
# Infrastructure (shared with gen_advanced_suite.py)
# ═══════════════════════════════════════════════════════════════════════════

PROBLEMS = []

INC = {
    "GEO":          "include('Axioms/Layer0-DomainKB/GEO000-0.ax').",
    "DPV":          "include('Axioms/Layer0-DomainKB/DPV000-0.ax').",
    "LANG":         "include('Axioms/Layer0-DomainKB/LANG000-0.ax').",
    "ODRL":         "include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').",
    "RUNTIME":      "include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').",
    "ISO":          "include('Axioms/Layer0-DomainKB/ISO3166-0.ax').",
    "ALIGN_DATA":   "include('Axioms/Alignment/ALIGN-GEO-ISO.ax').",
    "ALIGN_THEORY": "include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').",
}


def tc(op, oper, val, ind="    "):
    return (f"{ind}odrl:constraint [\n%   {ind}  odrl:leftOperand odrl:{op} ;\n"
            f"%   {ind}  odrl:operator odrl:{oper} ;\n"
            f"%   {ind}  odrl:rightOperand {val} ]")


def tp(name, rt, act, cs):
    lines = [f"ex:{name} a odrl:Set ;",
             f"  odrl:{rt} [",
             f"    odrl:action odrl:{act} ;"]
    for i, c in enumerate(cs):
        lines.append(tc(*c) + (" ;" if i < len(cs) - 1 else " ] ."))
    return "\n%   ".join(lines)


def generate_list_closure(list_id, elements):
    disjuncts = " | ".join(f"G = {e}" for e in elements)
    return (f"fof(list_{list_id}_closed, axiom,\n"
            f"    ![G]: (in_value_list(G, {list_id}) => ({disjuncts}))).")


def P(fn, exp, vrd, paper, diff, ttl, den, conj,
      flip_conj=None, extra="", inc=("GEO", "ODRL"), pl=None):
    PROBLEMS.append(dict(
        fn=fn, exp=exp, vrd=vrd, paper=paper, diff=diff,
        ttl=ttl, den=den, conj=conj, flip_conj=flip_conj,
        extra=extra, inc=inc, pl=pl))


CAT_DIR = {
    17: "KBGrounding/SetOperatorStress",
    18: "KBGrounding/CombinedComplexity",
    19: "KBGrounding/AdversarialOperators",
}


def problem_category(fn):
    num = int(fn.replace("ODRL", "").replace("-1.p", ""))
    if num < 210: return 17
    if num < 220: return 18
    return 19


# ═══════════════════════════════════════════════════════════════════════════
# Inline KB Fragments
# ═══════════════════════════════════════════════════════════════════════════

DPV_SAFE_FRAGMENT = """\
% --- DPV Fragment (DAG-SAFE sibling disjointness) ---
fof(dpv_s_root, axiom, concept(purpose)).
fof(dpv_s_c1, axiom, concept(commercialPurpose)).
fof(dpv_s_c2, axiom, concept(researchAndDevelopment)).
fof(dpv_s_c3, axiom, concept(commercialResearch)).
fof(dpv_s_c4, axiom, concept(academicResearch)).
fof(dpv_s_c5, axiom, concept(serviceProvision)).

fof(dpv_s_leq1, axiom, leq(commercialPurpose, purpose)).
fof(dpv_s_leq2, axiom, leq(researchAndDevelopment, purpose)).
fof(dpv_s_leq3, axiom, leq(serviceProvision, purpose)).
fof(dpv_s_leq4, axiom, leq(commercialResearch, commercialPurpose)).
fof(dpv_s_leq5, axiom, leq(commercialResearch, researchAndDevelopment)).
fof(dpv_s_leq6, axiom, leq(academicResearch, researchAndDevelopment)).

fof(dpv_s_refl1, axiom, leq(purpose, purpose)).
fof(dpv_s_refl2, axiom, leq(commercialPurpose, commercialPurpose)).
fof(dpv_s_refl3, axiom, leq(researchAndDevelopment, researchAndDevelopment)).
fof(dpv_s_refl4, axiom, leq(commercialResearch, commercialResearch)).
fof(dpv_s_refl5, axiom, leq(academicResearch, academicResearch)).
fof(dpv_s_refl6, axiom, leq(serviceProvision, serviceProvision)).

fof(dpv_s_disj_safe1, axiom, disjoint(commercialPurpose, serviceProvision)).
fof(dpv_s_disj_safe2, axiom, disjoint(researchAndDevelopment, serviceProvision)).

fof(dpv_s_una, axiom,
    $distinct(purpose, commercialPurpose, researchAndDevelopment,
              commercialResearch, academicResearch, serviceProvision))."""

SYNTH_KB_NO_DISJ = """\
% --- Synthetic KB (SYNTH) — NO native disjointness ---
fof(synth_root, axiom, concept(euZone)).
fof(synth_c1, axiom, concept(zoneWest)).
fof(synth_c2, axiom, concept(zoneEast)).
fof(synth_leq1, axiom, leq(zoneWest, euZone)).
fof(synth_leq2, axiom, leq(zoneEast, euZone)).
fof(synth_refl1, axiom, leq(euZone, euZone)).
fof(synth_refl2, axiom, leq(zoneWest, zoneWest)).
fof(synth_refl3, axiom, leq(zoneEast, zoneEast)).
fof(synth_una, axiom, $distinct(euZone, zoneWest, zoneEast))."""

ALIGN_ISO_SYNTH = """\
% Alignment: ISO 3166 → SYNTH
fof(align_iso_synth_1, axiom, align(europe, euZone)).
fof(align_iso_synth_2, axiom, align(dE, zoneWest)).
fof(align_iso_synth_3, axiom, align(pL, zoneEast))."""

COMP_KB_NO_DISJ = """\
% --- Compliance KB (COMP) — NO native disjointness ---
fof(comp_root, axiom, concept(complianceScope)).
fof(comp_c1, axiom, concept(gdprFull)).
fof(comp_c2, axiom, concept(gdprPartial)).
fof(comp_leq1, axiom, leq(gdprFull, complianceScope)).
fof(comp_leq2, axiom, leq(gdprPartial, complianceScope)).
fof(comp_refl1, axiom, leq(complianceScope, complianceScope)).
fof(comp_refl2, axiom, leq(gdprFull, gdprFull)).
fof(comp_refl3, axiom, leq(gdprPartial, gdprPartial)).
fof(comp_una, axiom, $distinct(complianceScope, gdprFull, gdprPartial))."""

ALIGN_SYNTH_COMP = """\
% Alignment: SYNTH → COMP
fof(align_synth_comp_1, axiom, align(euZone, complianceScope)).
fof(align_synth_comp_2, axiom, align(zoneWest, gdprFull)).
fof(align_synth_comp_3, axiom, align(zoneEast, gdprPartial))."""

_4KB_EXTRA = (SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH + "\n" +
              COMP_KB_NO_DISJ + "\n" + ALIGN_SYNTH_COMP)


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 17: SET OPERATOR STRESS (ODRL200–205)
#
# Tests deep interactions between isNoneOf (complement), isAllOf (∩),
# and isAnyOf (∪). These force the prover into complex set-theoretic
# reasoning over finite KB concepts with CWA closure axioms.
# ═══════════════════════════════════════════════════════════════════════════

# 200: isNoneOf vs isNoneOf — double complement interaction
#   policyA: permission spatial isNoneOf({westernEurope})  → C \ ↓wE
#   policyB: prohibition spatial isNoneOf({easternEurope}) → C \ ↓eE
#
#   Overlap: (C \ ↓wE) ∩ (C \ ↓eE) = C \ (↓wE ∪ ↓eE)
#   If ↓wE ∪ ↓eE = C (i.e., wE and eE partition europe) then overlap = ∅
#   But europe itself: ¬leq(europe, wE) ∧ ¬leq(europe, eE)
#   → europe ∈ isNoneOf({wE}) ∧ europe ∈ isNoneOf({eE})
#   Witness: europe → Compatible
#
#   This is HARD because the prover must reason about what is NOT below wE or eE.
#   The isNoneOf semantics requires ∀-elimination over the CWA closure,
#   then showing ¬leq(europe, wE) (which requires checking all leq axioms).
P("ODRL200-1.p", "Theorem", "Compatible",
  "isNoneOf × isNoneOf — Double Complement Overlap", "Very Hard",
  tp("policyA", "permission", "use", [("spatial", "isNoneOf", "( geo:westernEurope )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isNoneOf", "( geo:easternEurope )")]),
  "Double complement: (C \\ ↓wE) ∩ (C \\ ↓eE)\n"
  "%   europe: ¬leq(europe, wE) ∧ ¬leq(europe, eE)\n"
  "%   Witness: europe ∈ isNoneOf({wE}) ∩ isNoneOf({eE})\n"
  "%   Hard: prover must show ¬leq(europe, wE) — requires CWA over leq.",
  "fof(odrl200, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, noneListA200, isNoneOf)\n"
  "          & in_denotation_set(X, noneListB200, isNoneOf) )).",
  extra=(
      "fof(list_200a, axiom, in_value_list(westernEurope, noneListA200)).\n" +
      generate_list_closure("noneListA200", ["westernEurope"]) + "\n"
      "fof(list_200b, axiom, in_value_list(easternEurope, noneListB200)).\n" +
      generate_list_closure("noneListB200", ["easternEurope"])
  ),
  inc=("GEO", "ODRL"),
  pl="Double complement: isNoneOf({wE}) ∩ isNoneOf({eE}) ≠ ∅ (witness: europe)")

# 201: isNoneOf vs isAllOf — complement meets intersection
#   policyA: permission spatial isNoneOf({easternEurope})  → C \ ↓eE
#   policyB: prohibition spatial isAllOf({europe, westernEurope})
#            → ↓europe ∩ ↓wE = ↓wE (since wE ≤ europe)
#
#   Overlap: (C \ ↓eE) ∩ ↓wE
#   wE⊥eE → ↓wE ∩ ↓eE = ∅ → every X ∈ ↓wE has ¬leq(X, eE)
#   → ↓wE ⊆ isNoneOf({eE})
#   → Overlap = ↓wE ≠ ∅ → Compatible
#   Witness: germany
P("ODRL201-1.p", "Theorem", "Compatible",
  "isNoneOf × isAllOf — Complement Meets Intersection", "Very Hard",
  tp("policyA", "permission", "use", [("spatial", "isNoneOf", "( geo:easternEurope )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isAllOf", "( geo:europe geo:westernEurope )")]),
  "Complement ∩ intersection:\n"
  "%   isNoneOf({eE}) = C \\ ↓eE, isAllOf({europe, wE}) = ↓wE\n"
  "%   wE⊥eE → ↓wE ⊆ (C \\ ↓eE) → overlap = ↓wE ≠ ∅\n"
  "%   Hard: prover must chain disjointness → non-membership → complement inclusion.",
  "fof(odrl201, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, noneList201, isNoneOf)\n"
  "          & in_denotation_set(X, allList201, isAllOf) )).",
  extra=(
      "fof(list_201a, axiom, in_value_list(easternEurope, noneList201)).\n" +
      generate_list_closure("noneList201", ["easternEurope"]) + "\n"
      "fof(list_201b_1, axiom, in_value_list(europe, allList201)).\n"
      "fof(list_201b_2, axiom, in_value_list(westernEurope, allList201)).\n" +
      generate_list_closure("allList201", ["europe", "westernEurope"])
  ),
  inc=("GEO", "ODRL"),
  pl="Complement ∩ intersection: isNoneOf({eE}) ∩ isAllOf({europe,wE}) = ↓wE")

# 202: isNoneOf with large exclusion list → nearly empty complement
#   isNoneOf({westernEurope, easternEurope}) = C \ (↓wE ∪ ↓eE)
#   ↓wE ∪ ↓eE covers almost all of C (all under europe)
#   What's left? europe itself (¬leq(europe, wE) ∧ ¬leq(europe, eE))
#   Prove: europe is the ONLY witness in the complement
#   Specifically: in_denotation_set(X, list, isNoneOf) → X = europe
#   (given GEO KB where wE and eE are the only children of europe)
P("ODRL202-1.p", "Theorem", "NearEmpty",
  "isNoneOf — Large Exclusion, Nearly Empty Complement", "Extreme",
  tp("policyA", "permission", "use",
     [("spatial", "isNoneOf", "( geo:westernEurope geo:easternEurope )")]),
  "isNoneOf({wE, eE}) = C \\ (↓wE ∪ ↓eE)\n"
  "%   In GEO KB: wE and eE are children of europe, which covers all countries.\n"
  "%   Only europe itself is NOT below wE or eE.\n"
  "%   Prove: the complement is exactly {europe}.\n"
  "%   Extreme: requires exhaustive checking of all 24 GEO concepts.",
  "fof(odrl202, conjecture,\n"
  "    ![X]: ( in_denotation_set(X, noneList202, isNoneOf)\n"
  "        => X = europe )).",
  extra=(
      "fof(list_202_1, axiom, in_value_list(westernEurope, noneList202)).\n"
      "fof(list_202_2, axiom, in_value_list(easternEurope, noneList202)).\n" +
      generate_list_closure("noneList202", ["westernEurope", "easternEurope"])
  ),
  inc=("GEO", "ODRL"),
  pl="Near-empty complement: isNoneOf({wE,eE}) = {europe} only")

# 203: 3-way set operator interaction
#   policyA: permission spatial isAnyOf({germany, france})     → ↓de ∪ ↓fr
#   policyB: prohibition spatial isNoneOf({westernEurope})     → C \ ↓wE
#   policyC: prohibition spatial isAllOf({europe, germany})    → ↓europe ∩ ↓de = ↓de
#
#   A∩B: (↓de ∪ ↓fr) ∩ (C \ ↓wE)
#        de ≤ wE → de ∈ ↓wE → de ∉ (C\↓wE)
#        fr ≤ wE → fr ∈ ↓wE → fr ∉ (C\↓wE)
#        All elements of ↓de and ↓fr are ≤ wE → intersection = ∅ → Conflict(A,B)!
#   A∩C: (↓de ∪ ↓fr) ∩ ↓de = ↓de ≠ ∅ → Compatible(A,C)
#   B∩C: (C \ ↓wE) ∩ ↓de = ∅ (de ≤ wE) → Conflict(B,C)
#
#   Non-transitive again, but through set operators!
P("ODRL203-1.p", "Theorem", "MixedNWay",
  "3-Way Set Operators — isAnyOf × isNoneOf × isAllOf", "Extreme",
  tp("policyA", "permission", "use", [("spatial", "isAnyOf", "( geo:germany geo:france )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isNoneOf", "( geo:westernEurope )")]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [("spatial", "isAllOf", "( geo:europe geo:germany )")]),
  "3-way set operator non-transitivity:\n"
  "%   Conflict(A,B): isAnyOf({de,fr}) ∩ isNoneOf({wE}) = ∅\n"
  "%     (de,fr both ≤ wE → excluded from complement)\n"
  "%   Compatible(A,C): isAnyOf({de,fr}) ∩ isAllOf({europe,de}) = ↓de ≠ ∅\n"
  "%   Conflict(B,C): isNoneOf({wE}) ∩ isAllOf({europe,de}) = (C\\↓wE) ∩ ↓de = ∅\n"
  "%   Extreme: 3 different set operators, non-transitive via complement.",
  "fof(odrl203, conjecture,\n"
  "    ( ![X]: ~( in_denotation_set(X, anyList203, isAnyOf)\n"
  "             & in_denotation_set(X, noneList203, isNoneOf) )\n"
  "    & ?[Y]: ( in_denotation_set(Y, anyList203, isAnyOf)\n"
  "            & in_denotation_set(Y, allList203, isAllOf) )\n"
  "    & ![Z]: ~( in_denotation_set(Z, noneList203, isNoneOf)\n"
  "             & in_denotation_set(Z, allList203, isAllOf) ) )).",
  extra=(
      "fof(list_203a_1, axiom, in_value_list(germany, anyList203)).\n"
      "fof(list_203a_2, axiom, in_value_list(france, anyList203)).\n" +
      generate_list_closure("anyList203", ["germany", "france"]) + "\n"
      "fof(list_203b, axiom, in_value_list(westernEurope, noneList203)).\n" +
      generate_list_closure("noneList203", ["westernEurope"]) + "\n"
      "fof(list_203c_1, axiom, in_value_list(europe, allList203)).\n"
      "fof(list_203c_2, axiom, in_value_list(germany, allList203)).\n" +
      generate_list_closure("allList203", ["europe", "germany"])
  ),
  inc=("GEO", "ODRL"),
  pl="3-way set ops: isAnyOf × isNoneOf × isAllOf, non-transitive")

# 204: isNoneOf conflict with isPartOf — universal proof over complement
#   isNoneOf({europe}) = C \ ↓europe
#   isPartOf(germany) = ↓de ⊆ ↓europe (since de ≤ wE ≤ europe)
#   Prove: ∀X: ¬(X ∈ isNoneOf({europe}) ∧ X ∈ isPartOf(germany))
#   Requires: for every X, either X ∈ ↓europe (so ¬isNoneOf) or X ∉ ↓de
P("ODRL204-1.p", "Theorem", "Conflict",
  "isNoneOf × isPartOf — Universal Complement Conflict", "Very Hard",
  tp("policyA", "permission", "use", [("spatial", "isNoneOf", "( geo:europe )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:germany")]),
  "isNoneOf({europe}) ∩ isPartOf(germany) = ∅\n"
  "%   ↓de ⊆ ↓europe → every X ∈ isPartOf(de) has leq(X, europe)\n"
  "%   → X ∉ isNoneOf({europe})\n"
  "%   Universal proof: ∀X: ¬(complement ∧ descendant)",
  "fof(odrl204, conjecture,\n"
  "    ![X]: ~( in_denotation_set(X, noneList204, isNoneOf)\n"
  "           & in_denotation(X, germany, isPartOf) )).",
  extra=(
      "fof(list_204, axiom, in_value_list(europe, noneList204)).\n" +
      generate_list_closure("noneList204", ["europe"])
  ),
  inc=("GEO", "ODRL"),
  pl="Complement conflict: isNoneOf({europe}) ∩ isPartOf(de) = ∅")

# 205: isAnyOf large union vs isNoneOf large exclusion
#   isAnyOf({germany, france, italy, spain, netherlands})
#   isNoneOf({westernEurope, easternEurope})
#   Union: ↓de ∪ ↓fr ∪ ↓it ∪ ↓es ∪ ↓nl — all ≤ wE
#   Complement: C \ (↓wE ∪ ↓eE) = {europe} (from ODRL202)
#   → Union ∩ Complement = ∅ (all union members ≤ wE → excluded)
#   → Conflict
P("ODRL205-1.p", "CounterSatisfiable", "Conflict",
  "isAnyOf(5) × isNoneOf(2) — Large Union vs Large Exclusion", "Extreme",
  tp("policyA", "permission", "use",
     [("spatial", "isAnyOf", "( geo:germany geo:france geo:italy geo:spain geo:netherlands )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use",
     [("spatial", "isNoneOf", "( geo:westernEurope geo:easternEurope )")]),
  "Large union ∩ large complement:\n"
  "%   isAnyOf({de,fr,it,es,nl}): all ≤ wE → all ∈ ↓wE\n"
  "%   isNoneOf({wE,eE}): C \\ (↓wE ∪ ↓eE) ≈ {europe}\n"
  "%   → Union ∩ Complement = ∅ (all union members excluded)\n"
  "%   Extreme: 5-element list + 2-element exclusion + CWA reasoning.",
  "fof(odrl205, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, anyList205, isAnyOf)\n"
  "          & in_denotation_set(X, noneList205, isNoneOf) )).",
  flip_conj=
  "fof(odrl205, conjecture,\n"
  "    ![X]: ~( in_denotation_set(X, anyList205, isAnyOf)\n"
  "           & in_denotation_set(X, noneList205, isNoneOf) )).",
  extra=(
      "fof(list_205a_1, axiom, in_value_list(germany, anyList205)).\n"
      "fof(list_205a_2, axiom, in_value_list(france, anyList205)).\n"
      "fof(list_205a_3, axiom, in_value_list(italy, anyList205)).\n"
      "fof(list_205a_4, axiom, in_value_list(spain, anyList205)).\n"
      "fof(list_205a_5, axiom, in_value_list(netherlands, anyList205)).\n" +
      generate_list_closure("anyList205",
          ["germany", "france", "italy", "spain", "netherlands"]) + "\n"
      "fof(list_205b_1, axiom, in_value_list(westernEurope, noneList205)).\n"
      "fof(list_205b_2, axiom, in_value_list(easternEurope, noneList205)).\n" +
      generate_list_closure("noneList205", ["westernEurope", "easternEurope"])
  ),
  inc=("GEO", "ODRL"),
  pl="Large union vs large complement: isAnyOf(5) ∩ isNoneOf(2) = ∅")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 18: COMBINED COMPLEXITY (ODRL210–215)
#
# The "boss fights": combine MULTIPLE hard features in one problem.
# Multi-hop alignment + n-way + set operators + DAG multi-parent + runtime.
# ═══════════════════════════════════════════════════════════════════════════

# 210: Multi-hop + set operators
#   isAnyOf({zoneWest, zoneEast}) in SYNTH KB
#   isPartOf(euZone) in SYNTH KB
#   Needs 2-hop alignment to derive disjointness in SYNTH,
#   then tests isAnyOf union against isPartOf.
#   Overlap: (↓zoneWest ∪ ↓zoneEast) ∩ ↓euZone
#   Both ≤ euZone → union ⊆ ↓euZone → overlap = ↓zoneWest ∪ ↓zoneEast ≠ ∅
P("ODRL210-1.p", "Theorem", "Compatible",
  "Multi-Hop + Set Operators — isAnyOf in Aligned KB", "Extreme",
  tp("policyA", "permission", "use",
     [("spatial", "isAnyOf", "( synth:zoneWest synth:zoneEast )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use",
     [("spatial", "isPartOf", "synth:euZone")]),
  "Set operator in aligned KB: isAnyOf({zoneWest,zoneEast}) ∩ isPartOf(euZone)\n"
  "%   Both ≤ euZone → union ⊆ ↓euZone → overlap ≠ ∅\n"
  "%   With 3 loaded KBs (GEO+ISO+SYNTH) and 2 alignment bridges.\n"
  "%   Extreme: set operators + 3-KB context + alignment infrastructure.",
  "fof(odrl210, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, anyList210, isAnyOf)\n"
  "          & in_denotation(X, euZone, isPartOf) )).",
  extra=(
      SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH + "\n"
      "fof(list_210_1, axiom, in_value_list(zoneWest, anyList210)).\n"
      "fof(list_210_2, axiom, in_value_list(zoneEast, anyList210)).\n" +
      generate_list_closure("anyList210", ["zoneWest", "zoneEast"])
  ),
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY"),
  pl="Multi-hop + set ops: isAnyOf in aligned KB")

# 211: 3-hop alignment + isNoneOf — complement in 4th dataspace
#   isNoneOf({gdprFull}) in COMP KB = C_comp \ ↓gdprFull
#   isPartOf(gdprPartial) in COMP KB = ↓gdprPartial
#   3-hop derives disj(gdprFull, gdprPartial) → ↓gdprPartial ∩ ↓gdprFull = ∅
#   → every X ∈ ↓gdprPartial has ¬leq(X, gdprFull) → X ∈ isNoneOf({gdprFull})
#   → overlap ≠ ∅ → Compatible
P("ODRL211-1.p", "Theorem", "Compatible",
  "3-Hop + isNoneOf — Complement in 4th Dataspace", "Extreme",
  tp("policyA", "permission", "use",
     [("spatial", "isNoneOf", "( comp:gdprFull )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use",
     [("spatial", "isPartOf", "comp:gdprPartial")]),
  "isNoneOf({gdprFull}) ∩ isPartOf(gdprPartial) in 4th dataspace.\n"
  "%   3-hop: GEO→ISO→SYNTH→COMP derives disj(gdprFull, gdprPartial)\n"
  "%   → ↓gdprPartial ⊆ (C_comp \\ ↓gdprFull) = isNoneOf({gdprFull})\n"
  "%   → overlap = ↓gdprPartial ≠ ∅\n"
  "%   Extreme: isNoneOf + 3-hop alignment + disjointness → complement inclusion.",
  "fof(odrl211, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, noneList211, isNoneOf)\n"
  "          & in_denotation(X, gdprPartial, isPartOf) )).",
  extra=(
      _4KB_EXTRA + "\n"
      "fof(list_211, axiom, in_value_list(gdprFull, noneList211)).\n" +
      generate_list_closure("noneList211", ["gdprFull"])
  ),
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY"),
  pl="3-hop + isNoneOf: complement in 4th dataspace via alignment")

# 212: N-way + DAG multi-parent + set operators + multi-dim
#   3 policies, each with 2 operands:
#   A: permission, spatial isAnyOf({de, fr}), purpose isA(commercialPurpose)
#   B: prohibition, spatial isNoneOf({easternEurope}), purpose isA(R&D)
#   C: prohibition, spatial isPartOf(westernEurope), purpose isA(commercialResearch)
#
#   A∩B: spatial: isAnyOf({de,fr}) ∩ isNoneOf({eE})
#         de ∈ ↓wE, ¬leq(de,eE) → de ∈ isNoneOf({eE}) ✓
#         purpose: cP ∩ R&D = {cR} (DAG multi-parent!) ✓
#         → Compatible
#   A∩C: spatial: isAnyOf({de,fr}) ∩ isPartOf(wE) = {de,fr,...} ✓
#         purpose: cP ∩ cR: cR ≤ cP → cR ✓
#         → Compatible
#   B∩C: spatial: isNoneOf({eE}) ∩ isPartOf(wE) = ↓wE (disjoint → subset complement) ✓
#         purpose: R&D ∩ cR: cR ≤ R&D → cR ✓
#         → Compatible
#   All 3 pairs Compatible!
P("ODRL212-1.p", "Theorem", "Compatible",
  "N-Way + DAG + Set Ops + Multi-Dim — The Full Monty", "Extreme",
  tp("policyA", "permission", "use", [
      ("spatial", "isAnyOf", "( geo:germany geo:france )"),
      ("hasPurpose", "isA", "dpv:CommercialPurpose")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("spatial", "isNoneOf", "( geo:easternEurope )"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment")
  ]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:westernEurope"),
      ("hasPurpose", "isA", "dpv:CommercialResearch")
  ]),
  "The Full Monty: n-way + DAG multi-parent + set operators + multi-dim.\n"
  "%   A∩B: isAnyOf({de,fr}) ∩ isNoneOf({eE}) ∧ cP∩R&D=cR (DAG!) → Compatible\n"
  "%   A∩C: isAnyOf({de,fr}) ∩ isPartOf(wE) ∧ cP∩cR → Compatible\n"
  "%   B∩C: isNoneOf({eE}) ∩ isPartOf(wE) ∧ R&D∩cR → Compatible\n"
  "%   Extreme: every hard feature combined — prover must unify all patterns.",
  "fof(odrl212, conjecture,\n"
  "    ( ?[Xs,Xp]: ( in_denotation_set(Xs, anyList212, isAnyOf)\n"
  "                & in_denotation_set(Xs, noneList212, isNoneOf)\n"
  "                & in_denotation(Xp, commercialPurpose, isA)\n"
  "                & in_denotation(Xp, researchAndDevelopment, isA) )\n"
  "    & ?[Ys,Yp]: ( in_denotation_set(Ys, anyList212, isAnyOf)\n"
  "                & in_denotation(Ys, westernEurope, isPartOf)\n"
  "                & in_denotation(Yp, commercialPurpose, isA)\n"
  "                & in_denotation(Yp, commercialResearch, isA) )\n"
  "    & ?[Zs,Zp]: ( in_denotation_set(Zs, noneList212, isNoneOf)\n"
  "                & in_denotation(Zs, westernEurope, isPartOf)\n"
  "                & in_denotation(Zp, researchAndDevelopment, isA)\n"
  "                & in_denotation(Zp, commercialResearch, isA) ) )).",
  extra=(
      DPV_SAFE_FRAGMENT + "\n"
      "fof(list_212a_1, axiom, in_value_list(germany, anyList212)).\n"
      "fof(list_212a_2, axiom, in_value_list(france, anyList212)).\n" +
      generate_list_closure("anyList212", ["germany", "france"]) + "\n"
      "fof(list_212b, axiom, in_value_list(easternEurope, noneList212)).\n" +
      generate_list_closure("noneList212", ["easternEurope"])
  ),
  inc=("GEO", "ODRL"),
  pl="The Full Monty: n-way + DAG + isAnyOf + isNoneOf + isPartOf + multi-dim")

# 213: Multi-hop + n-way + DAG — 3 policies across 4 dataspaces
#   A: permission, purpose isA(commercialPurpose), spatial isPartOf(comp:complianceScope)
#   B: prohibition, purpose isA(R&D), spatial isPartOf(comp:gdprFull)
#   C: prohibition, purpose isA(commercialResearch), spatial eq(comp:gdprFull)
#
#   A∩B: purpose(cP∩R&D=cR DAG!) ∧ spatial(compScope∩gdprFull=gdprFull) → Compatible
#   A∩C: purpose(cP∩cR leq!) ∧ spatial(compScope∩gdprFull=gdprFull) → Compatible
#   B∩C: purpose(R&D∩cR leq!) ∧ spatial(gdprFull∩gdprFull=gdprFull) → Compatible
P("ODRL213-1.p", "Theorem", "Compatible",
  "3-Hop + N-Way + DAG — Cross-Dataspace Triple Policy", "Extreme",
  tp("policyA", "permission", "use", [
      ("hasPurpose", "isA", "dpv:CommercialPurpose"),
      ("spatial", "isPartOf", "comp:complianceScope")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment"),
      ("spatial", "isPartOf", "comp:gdprFull")
  ]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [
      ("hasPurpose", "isA", "dpv:CommercialResearch"),
      ("spatial", "eq", "comp:gdprFull")
  ]),
  "3-hop + n-way + DAG: 3 policies, 4 dataspaces, DAG purpose.\n"
  "%   A∩B: purpose(cP∩R&D=cR via DAG) ∧ spatial(compScope∩gdprFull) → Compatible\n"
  "%   A∩C: purpose(cP∩cR via leq) ∧ spatial(compScope∩gdprFull) → Compatible\n"
  "%   B∩C: purpose(R&D∩cR via leq) ∧ spatial(gdprFull=gdprFull) → Compatible\n"
  "%   Extreme: 4 KBs loaded, 3 alignment bridges, DAG purpose, n-way.",
  "fof(odrl213, conjecture,\n"
  "    ( ?[Xp,Xs]: ( in_denotation(Xp, commercialPurpose, isA)\n"
  "                & in_denotation(Xp, researchAndDevelopment, isA)\n"
  "                & in_denotation(Xs, complianceScope, isPartOf)\n"
  "                & in_denotation(Xs, gdprFull, isPartOf) )\n"
  "    & ?[Yp,Ys]: ( in_denotation(Yp, commercialPurpose, isA)\n"
  "                & in_denotation(Yp, commercialResearch, isA)\n"
  "                & in_denotation(Ys, complianceScope, isPartOf)\n"
  "                & in_denotation(Ys, gdprFull, eq) )\n"
  "    & ?[Zp,Zs]: ( in_denotation(Zp, researchAndDevelopment, isA)\n"
  "                & in_denotation(Zp, commercialResearch, isA)\n"
  "                & in_denotation(Zs, gdprFull, isPartOf)\n"
  "                & in_denotation(Zs, gdprFull, eq) ) )).",
  extra=DPV_SAFE_FRAGMENT + "\n" + _4KB_EXTRA,
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY"),
  pl="3-hop + n-way + DAG: 3 policies across 4 dataspaces")

# 214: Runtime + alignment + set operators — full-stack test
#   Uses RUNTIME000-0.ax to check: does a runtime context that assigns
#   a value in zoneWest satisfy a policy with isPartOf(euZone)?
#
#   assigns(omega, zoneWest) + satisfies bridge + leq(zoneWest, euZone)
#   → satisfies(omega, euZone, isPartOf) → runtime witness exists
#   With 3-KB alignment loaded but only SYNTH concepts queried.
P("ODRL214-1.p", "Theorem", "Compatible",
  "Runtime + Alignment + Set Ops — Full Stack", "Extreme",
  tp("policyA", "permission", "use",
     [("spatial", "isPartOf", "synth:euZone")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use",
     [("spatial", "eq", "synth:zoneWest")]),
  "Full-stack: runtime context + alignment infrastructure + denotation.\n"
  "%   Runtime: assigns(omega214, zoneWest) → satisfies(omega214, euZone, isPartOf)\n"
  "%   Denotation: isPartOf(euZone) ∩ eq(zoneWest) → witness: zoneWest\n"
  "%   With RUNTIME + ALIGN + 3 KBs loaded simultaneously.\n"
  "%   Extreme: tests interaction between runtime and denotation semantics.",
  "fof(odrl214_ctx, axiom, assigns(omega214, zoneWest)).\n"
  "\n"
  "fof(odrl214, conjecture,\n"
  "    ( ?[X]: ( in_denotation(X, euZone, isPartOf)\n"
  "            & in_denotation(X, zoneWest, eq) )\n"
  "    & satisfies(omega214, euZone, isPartOf) )).",
  extra=SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH,
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY", "RUNTIME"),
  pl="Full stack: runtime + alignment + denotation in 3-KB context")

# 215: The Ultimate — 4 dataspaces + 3 policies + 3 operands + set ops + DAG
#   A: permission, spatial isAnyOf({gdprFull}) in COMP, purpose isA(cP), language isPartOf(en)
#   B: prohibition, spatial isPartOf(comp:complianceScope), purpose isA(R&D), language eq(enGB)
#   C: prohibition, spatial eq(comp:gdprFull), purpose isA(cR), language isPartOf(en)
#
#   All Compatible: witnesses (gdprFull, commercialResearch, enGB) for all pairs.
P("ODRL215-1.p", "Theorem", "Compatible",
  "Ultimate — 4 KBs × 3 Policies × 3 Operands × Set Ops × DAG", "Extreme",
  tp("policyA", "permission", "use", [
      ("spatial", "isAnyOf", "( comp:gdprFull )"),
      ("hasPurpose", "isA", "dpv:CommercialPurpose"),
      ("language", "isPartOf", "lang:en")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("spatial", "isPartOf", "comp:complianceScope"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment"),
      ("language", "eq", "lang:enGB")
  ]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [
      ("spatial", "eq", "comp:gdprFull"),
      ("hasPurpose", "isA", "dpv:CommercialResearch"),
      ("language", "isPartOf", "lang:en")
  ]),
  "Ultimate: 4 KBs + 3 policies + 3 operands + set ops + DAG.\n"
  "%   All pairs Compatible: witness (gdprFull, cR, enGB) for all.\n"
  "%   Extreme: maximum axiom load — GEO+ISO+SYNTH+COMP+DPV+LANG+ODRL+ALIGN.\n"
  "%   Tests: prover scalability with all infrastructure loaded.",
  "fof(odrl215, conjecture,\n"
  "    ( ?[Xs,Xp,Xl]: ( in_denotation_set(Xs, anyList215, isAnyOf)\n"
  "                   & in_denotation(Xs, complianceScope, isPartOf)\n"
  "                   & in_denotation(Xp, commercialPurpose, isA)\n"
  "                   & in_denotation(Xp, researchAndDevelopment, isA)\n"
  "                   & in_denotation(Xl, en, isPartOf)\n"
  "                   & in_denotation(Xl, enGB, eq) )\n"
  "    & ?[Ys,Yp,Yl]: ( in_denotation_set(Ys, anyList215, isAnyOf)\n"
  "                   & in_denotation(Ys, gdprFull, eq)\n"
  "                   & in_denotation(Yp, commercialPurpose, isA)\n"
  "                   & in_denotation(Yp, commercialResearch, isA)\n"
  "                   & in_denotation(Yl, en, isPartOf)\n"
  "                   & in_denotation(Yl, en, isPartOf) )\n"
  "    & ?[Zs,Zp,Zl]: ( in_denotation(Zs, complianceScope, isPartOf)\n"
  "                   & in_denotation(Zs, gdprFull, eq)\n"
  "                   & in_denotation(Zp, researchAndDevelopment, isA)\n"
  "                   & in_denotation(Zp, commercialResearch, isA)\n"
  "                   & in_denotation(Zl, enGB, eq)\n"
  "                   & in_denotation(Zl, en, isPartOf) ) )).",
  extra=(
      DPV_SAFE_FRAGMENT + "\n" + _4KB_EXTRA + "\n"
      "fof(list_215, axiom, in_value_list(gdprFull, anyList215)).\n" +
      generate_list_closure("anyList215", ["gdprFull"])
  ),
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY", "LANG"),
  pl="Ultimate: 4 KBs × 3 policies × 3 operands × set ops × DAG")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 19: ADVERSARIAL OPERATOR PATTERNS (ODRL220–225)
#
# Tests degenerate, paradoxical, and boundary-case set operator
# combinations that break naive implementations.
# ═══════════════════════════════════════════════════════════════════════════

# 220: isAllOf with single member = isPartOf
#   isAllOf({germany}) = ↓de ∩ ... = ↓de = isPartOf(germany)
#   Prove equivalence: ∀X: isAllOf({de}) ↔ isPartOf(de)
P("ODRL220-1.p", "Theorem", "Equivalence",
  "isAllOf Singleton = isPartOf — Operator Equivalence", "Very Hard",
  "(Meta-property: isAllOf({G}) ≡ isPartOf(G))",
  "isAllOf({G}) = ↓G (single-element intersection) = isPartOf(G).\n"
  "%   Prove: ∀X: in_denotation_set(X, {de}, isAllOf) ↔ in_denotation(X, de, isPartOf)\n"
  "%   Very Hard: biconditional requires proving BOTH directions.",
  "fof(odrl220, conjecture,\n"
  "    ![X]: ( in_denotation_set(X, allList220, isAllOf)\n"
  "        <=> in_denotation(X, germany, isPartOf) )).",
  extra=(
      "fof(list_220, axiom, in_value_list(germany, allList220)).\n" +
      generate_list_closure("allList220", ["germany"])
  ),
  inc=("GEO", "ODRL"),
  pl="Operator equivalence: isAllOf({de}) ≡ isPartOf(de)")

# 221: isAnyOf with single member = isPartOf
#   isAnyOf({germany}) = ↓de ∪ ... = ↓de = isPartOf(germany)
P("ODRL221-1.p", "Theorem", "Equivalence",
  "isAnyOf Singleton = isPartOf — Operator Equivalence", "Very Hard",
  "(Meta-property: isAnyOf({G}) ≡ isPartOf(G))",
  "isAnyOf({G}) = ↓G (single-element union) = isPartOf(G).\n"
  "%   Prove: ∀X: in_denotation_set(X, {de}, isAnyOf) ↔ in_denotation(X, de, isPartOf)",
  "fof(odrl221, conjecture,\n"
  "    ![X]: ( in_denotation_set(X, anyList221, isAnyOf)\n"
  "        <=> in_denotation(X, germany, isPartOf) )).",
  extra=(
      "fof(list_221, axiom, in_value_list(germany, anyList221)).\n" +
      generate_list_closure("anyList221", ["germany"])
  ),
  inc=("GEO", "ODRL"),
  pl="Operator equivalence: isAnyOf({de}) ≡ isPartOf(de)")

# 222: isNoneOf({root}) = ∅ — complement of root is empty
#   isNoneOf({europe}) in GEO KB: C \ ↓europe
#   ALL concepts in GEO KB are ≤ europe (it's the root)
#   → isNoneOf({europe}) = ∅
#   Prove: ∀X: concept(X) → ¬in_denotation_set(X, {europe}, isNoneOf)
P("ODRL222-1.p", "Theorem", "EmptyComplement",
  "isNoneOf({root}) = ∅ — Root Complement Is Empty", "Very Hard",
  "(Meta-property: complement of root concept is empty)",
  "isNoneOf({europe}) = C_geo \\ ↓europe.\n"
  "%   europe is the root → all concepts ≤ europe → complement = ∅.\n"
  "%   Very Hard: requires ∀X: concept(X) → leq(X, europe) (root reachability).",
  "fof(odrl222, conjecture,\n"
  "    ![X]: ( concept(X)\n"
  "        => ~in_denotation_set(X, noneList222, isNoneOf) )).",
  extra=(
      "fof(list_222, axiom, in_value_list(europe, noneList222)).\n" +
      generate_list_closure("noneList222", ["europe"])
  ),
  inc=("GEO", "ODRL"),
  pl="Root complement empty: isNoneOf({europe}) = ∅")

# 223: isAllOf ⊆ isAnyOf — intersection always subset of union
#   For any list L: isAllOf(L) ⊆ isAnyOf(L)
#   (∩ᵢ ↓gᵢ) ⊆ (∪ᵢ ↓gᵢ) trivially.
#   Prove for L = {westernEurope, europe}
P("ODRL223-1.p", "Theorem", "Subsumption",
  "isAllOf ⊆ isAnyOf — Intersection Subsumes Union", "Very Hard",
  "(Meta-property: ∀L: isAllOf(L) ⊆ isAnyOf(L))",
  "isAllOf(L) = ∩ᵢ ↓gᵢ ⊆ ∪ᵢ ↓gᵢ = isAnyOf(L).\n"
  "%   For L = {wE, europe}: ↓wE ∩ ↓europe ⊆ ↓wE ∪ ↓europe\n"
  "%   Very Hard: biconditional over set operator semantics.",
  "fof(odrl223, conjecture,\n"
  "    ![X]: ( in_denotation_set(X, sharedList223, isAllOf)\n"
  "        => in_denotation_set(X, sharedList223, isAnyOf) )).",
  extra=(
      "fof(list_223_1, axiom, in_value_list(westernEurope, sharedList223)).\n"
      "fof(list_223_2, axiom, in_value_list(europe, sharedList223)).\n" +
      generate_list_closure("sharedList223", ["westernEurope", "europe"])
  ),
  inc=("GEO", "ODRL"),
  pl="Set containment: isAllOf({wE,europe}) ⊆ isAnyOf({wE,europe})")

# 224: isAnyOf ∩ isNoneOf with SAME list = ∅ — self-annihilation
#   isAnyOf({de}) ∩ isNoneOf({de}) = ↓de ∩ (C \ ↓de) = ∅
#   Prove: emptiness of contradictory set operators on same value.
P("ODRL224-1.p", "Theorem", "Conflict",
  "isAnyOf ∩ isNoneOf Same List — Self-Annihilation", "Very Hard",
  tp("policyA", "permission", "use",
     [("spatial", "isAnyOf", "( geo:germany )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use",
     [("spatial", "isNoneOf", "( geo:germany )")]),
  "Self-annihilation: isAnyOf({de}) ∩ isNoneOf({de}) = ↓de ∩ (C\\↓de) = ∅.\n"
  "%   Very Hard: prover must show ∀X: leq(X,de) → ¬(¬leq(X,de))\n"
  "%   i.e., set membership and complement are contradictory.",
  "fof(odrl224, conjecture,\n"
  "    ![X]: ~( in_denotation_set(X, anyList224, isAnyOf)\n"
  "           & in_denotation_set(X, noneList224, isNoneOf) )).",
  extra=(
      "fof(list_224a, axiom, in_value_list(germany, anyList224)).\n" +
      generate_list_closure("anyList224", ["germany"]) + "\n"
      "fof(list_224b, axiom, in_value_list(germany, noneList224)).\n" +
      generate_list_closure("noneList224", ["germany"])
  ),
  inc=("GEO", "ODRL"),
  pl="Self-annihilation: isAnyOf({de}) ∩ isNoneOf({de}) = ∅")

# 225: De Morgan-like — isNoneOf({A,B}) vs isAllOf({A,B})
#   isNoneOf({wE, eE}) = C \ (↓wE ∪ ↓eE)  [complement of union]
#   isAllOf({wE, eE}) = ↓wE ∩ ↓eE = ∅      [empty, from ODRL110]
#   Prove: isNoneOf({wE,eE}) ∩ isAllOf({wE,eE}) = ∅ trivially
#   (isAllOf is already empty → intersection with anything = ∅)
#   But MORE interesting: prove they DON'T partition C.
#   ∃X: ¬in_denotation_set(X, L, isNoneOf) ∧ ¬in_denotation_set(X, L, isAllOf)
#   Witness: germany (in ↓wE but NOT in ↓wE∩↓eE and NOT in C\(↓wE∪↓eE))
P("ODRL225-1.p", "Theorem", "NonPartition",
  "De Morgan-like — isNoneOf and isAllOf Don't Partition C", "Extreme",
  "(Meta-property: complement-of-union and intersection don't cover C)",
  "isNoneOf({wE,eE}) = C \\ (↓wE∪↓eE), isAllOf({wE,eE}) = ↓wE∩↓eE = ∅.\n"
  "%   These DON'T partition C: ∃X neither in complement nor in intersection.\n"
  "%   Witness: germany ∈ ↓wE (so not in complement) but ¬∈ ↓eE (so not in isAllOf).\n"
  "%   Extreme: prover must reason about 3 regions: complement, intersection, remainder.",
  "fof(odrl225, conjecture,\n"
  "    ?[X]: ( concept(X)\n"
  "          & ~in_denotation_set(X, sharedList225, isNoneOf)\n"
  "          & ~in_denotation_set(X, sharedList225, isAllOf) )).",
  extra=(
      "fof(list_225_1, axiom, in_value_list(westernEurope, sharedList225)).\n"
      "fof(list_225_2, axiom, in_value_list(easternEurope, sharedList225)).\n" +
      generate_list_closure("sharedList225", ["westernEurope", "easternEurope"])
  ),
  inc=("GEO", "ODRL"),
  pl="Non-partition: ∃X: X ∉ isNoneOf({wE,eE}) ∧ X ∉ isAllOf({wE,eE})")


# ═══════════════════════════════════════════════════════════════════════════
# File generation engine (same as gen_advanced_suite.py)
# ═══════════════════════════════════════════════════════════════════════════

def generate_tptp_header(p, use_flip):
    exp = p["exp"]
    conj_str = p["flip_conj"] if (use_flip and p["flip_conj"]) else p["conj"]
    lines = []
    lines.append("%--------------------------------------------------------------------------")
    lines.append(f"% File     : {p['fn']} : TPTP v0.1.0.")
    lines.append(f"% Domain   : ODRL Policy Conflict Detection")
    lines.append(f"% Problem  : {p['paper']}")
    lines.append(f"% Expected : {exp}")
    lines.append(f"% Verdict  : {p['vrd']}")
    lines.append(f"% Paper    : {p['paper']}")
    lines.append(f"%")
    lines.append(f"% ODRL Policy (Conceptual):")
    for ttl_line in p["ttl"].split("\n"):
        lines.append(f"%   {ttl_line}")
    lines.append(f"%")
    lines.append(f"% Formal test:")
    for den_line in p["den"].split("\n"):
        lines.append(f"%   {den_line}")
    lines.append(f"%")
    if p["pl"]:
        lines.append(f"% One-liner : {p['pl']}")
    lines.append(f"% Difficulty: {p['diff']}")
    lines.append(f"% Authors  : Mustafa, D. & Sutcliffe, G.")
    lines.append(f"% Date     : {date.today().isoformat()}")
    lines.append(f"% Gen      : gen_extreme_suite.py")
    lines.append("%--------------------------------------------------------------------------")
    lines.append("")
    return "\n".join(lines), conj_str


def generate_problem_file(p, use_flip=False):
    header, conj_str = generate_tptp_header(p, use_flip)
    parts = [header]
    for inc_key in p["inc"]:
        if inc_key in INC:
            parts.append(INC[inc_key])
    parts.append("")
    if p["extra"]:
        parts.append("% ─── Problem-specific axioms ─────────────────────────────────────────")
        parts.append(p["extra"])
        parts.append("")
    parts.append("% ─── Conjecture ──────────────────────────────────────────────────────")
    parts.append(conj_str)
    parts.append("")
    parts.append("%--------------------------------------------------------------------------")
    return "\n".join(parts)


def write_problems(outdir, dry_run=False, use_flip=False):
    written = []
    for p in PROBLEMS:
        cat = problem_category(p["fn"])
        subdir = os.path.join(outdir, CAT_DIR[cat])
        if not dry_run:
            os.makedirs(subdir, exist_ok=True)
        filepath = os.path.join(subdir, p["fn"])
        content = generate_problem_file(p, use_flip=use_flip)
        if dry_run:
            print(f"  [DRY] {filepath}  ({len(content)} bytes)")
        else:
            with open(filepath, "w") as f:
                f.write(content)
            written.append(filepath)
    return written


def print_summary():
    print(f"\n{'Cat':<5} {'Problem':<14} {'Expected':<18} {'Verdict':<16} "
          f"{'Diff':<11} {'Includes'}")
    print("=" * 100)
    cats = {}
    for p in PROBLEMS:
        cat = problem_category(p["fn"])
        cats.setdefault(cat, []).append(p)
        incs = "+".join(p["inc"])
        has_extra = " +inline" if p["extra"] else ""
        print(f"  {cat:<3} {p['fn']:<14} {p['exp']:<18} {p['vrd']:<16} "
              f"{p['diff']:<11} {incs}{has_extra}")
    print(f"\n{'─'*50}")
    print(f"Total problems: {len(PROBLEMS)}")
    print(f"\nBy category:")
    for cat, probs in sorted(cats.items()):
        print(f"  Cat {cat} ({CAT_DIR[cat].split('/')[-1]}): {len(probs)} problems")
    statuses = {}
    for p in PROBLEMS:
        statuses[p["exp"]] = statuses.get(p["exp"], 0) + 1
    print(f"\nBy expected status:")
    for s, c in sorted(statuses.items()):
        print(f"  {s}: {c}")
    diffs = {}
    for p in PROBLEMS:
        diffs[p["diff"]] = diffs.get(p["diff"], 0) + 1
    print(f"\nBy difficulty:")
    for d in ["Very Hard", "Extreme"]:
        if d in diffs:
            print(f"  {d}: {diffs[d]}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate TPTP problems: Categories 17–19 (extreme suite).")
    parser.add_argument("--outdir", default="Problems/ODRL",
                        help="Root output directory")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--flip", action="store_true",
                        help="Use flipped conjectures for CounterSatisfiable→Theorem")
    args = parser.parse_args()
    if args.summary:
        print_summary()
        return
    written = write_problems(args.outdir, dry_run=args.dry_run,
                             use_flip=args.flip)
    if not args.dry_run:
        print(f"\nWrote {len(written)} problem files:")
        for f in written:
            print(f"  {f}")
    print_summary()


if __name__ == "__main__":
    main()
    
    
    
    
    
#!/usr/bin/env python3
"""
gen_advanced_suite.py — Generate TPTP Problems: Categories 9–16, 20–21.

Produces 60 .p files testing advanced reasoning patterns for ODRL
policy conflict detection in European data spaces.

Categories:
  9  — DAG Multi-Parent (ODRL100–105)       Note 1 / DAG-safety algorithm
  10 — Nested Set Operators (ODRL110–114)    isAllOf, isAnyOf, isNoneOf interaction
  11 — Quantifier Stress (ODRL120–123)       ∀∃ alternation patterns
  12 — Large-Scale Composition (ODRL130–132) Multi-operand AND / 5-way ∃
  13 — Edge Cases & Adversarial (ODRL140–145) Degenerate / pathological KBs
  14 — Multi-Hop Alignment (ODRL150–159)     2–3 hop + witness-loss bug
  15 — N-Way Policy Conflicts (ODRL160–165)  3–4 policies simultaneously
  16 — N-Way Composed Policies (ODRL170–175) N-way × multi-operand
  20 — XONE / Symmetric Difference (ODRL230–237) Negative denotation reasoning
  21 — Operator Monotonicity (ODRL250–254)   Meta-properties of ODRL operators

Usage:
    python gen_advanced_suite.py --outdir Problems/ODRL

Authors: Mustafa, D. & Sutcliffe, G.
"""
import argparse
import os
import sys
from datetime import date


# ═══════════════════════════════════════════════════════════════════════════
# Infrastructure
# ═══════════════════════════════════════════════════════════════════════════

PROBLEMS = []

INC = {
    "GEO":          "include('Axioms/Layer0-DomainKB/GEO000-0.ax').",
    "DPV":          "include('Axioms/Layer0-DomainKB/DPV000-0.ax').",
    "LANG":         "include('Axioms/Layer0-DomainKB/LANG000-0.ax').",
    "ODRL":         "include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').",
    "RUNTIME":      "include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').",
    "ISO":          "include('Axioms/Layer0-DomainKB/ISO3166-0.ax').",
    "ALIGN_DATA":   "include('Axioms/Alignment/ALIGN-GEO-ISO.ax').",
    "ALIGN_THEORY": "include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').",
}


def tc(op, oper, val, ind="    "):
    """Format a single ODRL constraint triple as a TPTP comment."""
    return (f"{ind}odrl:constraint [\n%   {ind}  odrl:leftOperand odrl:{op} ;\n"
            f"%   {ind}  odrl:operator odrl:{oper} ;\n"
            f"%   {ind}  odrl:rightOperand {val} ]")


def tp(name, rt, act, cs):
    """Format an ODRL policy as a multi-line TPTP comment block."""
    lines = [f"ex:{name} a odrl:Set ;",
             f"  odrl:{rt} [",
             f"    odrl:action odrl:{act} ;"]
    for i, c in enumerate(cs):
        lines.append(tc(*c) + (" ;" if i < len(cs) - 1 else " ] ."))
    return "\n%   ".join(lines)


def generate_list_closure(list_id, elements):
    """Generate a CWA closure axiom for a finite value list."""
    disjuncts = " | ".join(f"G = {e}" for e in elements)
    return (f"fof(list_{list_id}_closed, axiom,\n"
            f"    ![G]: (in_value_list(G, {list_id}) => ({disjuncts}))).")


def P(fn, exp, vrd, paper, diff, ttl, den, conj,
      flip_conj=None, extra="", inc=("GEO", "ODRL"), pl=None):
    """Register a problem specification."""
    PROBLEMS.append(dict(
        fn=fn, exp=exp, vrd=vrd, paper=paper, diff=diff,
        ttl=ttl, den=den, conj=conj, flip_conj=flip_conj,
        extra=extra, inc=inc, pl=pl))


# ─── Category → subdirectory mapping ─────────────────────────────────────
CAT_DIR = {
    9:  "KBGrounding/DAGMultiParent",
    10: "KBGrounding/NestedSetOperators",
    11: "KBGrounding/QuantifierStress",
    12: "KBGrounding/LargeComposition",
    13: "KBGrounding/EdgeCases",
    14: "KBGrounding/MultiHopAlignment",
    15: "KBGrounding/NWayConflict",
    16: "KBGrounding/NWayComposed",
    20: "KBGrounding/XONESymmetricDiff",
    21: "KBGrounding/OperatorMonotonicity",
}


def problem_category(fn):
    """Return category number from filename like ODRL100-1.p or ODRL158-2.p."""
    # Extract number: ODRL158-2.p → 158, ODRL100-1.p → 100
    import re
    m = re.match(r"ODRL(\d+)", fn)
    num = int(m.group(1))
    if num < 110: return 9
    if num < 120: return 10
    if num < 130: return 11
    if num < 140: return 12
    if num < 150: return 13
    if num < 160: return 14
    if num < 170: return 15
    if num < 230: return 16
    if num < 250: return 20
    return 21


# ═══════════════════════════════════════════════════════════════════════════
# Inline KB Fragments (test-specific, not shared axiom files)
# ═══════════════════════════════════════════════════════════════════════════

# ─── DPV NAIVE: with problematic sibling disjointness ────────────────────
DPV_NAIVE_FRAGMENT = """\
% --- DPV Fragment (NAIVE sibling disjointness) ---
% Multi-parent concept: commercialResearch ≤ {commercialPurpose, researchAndDevelopment}
% From Table 1: 6 multi-parent concepts in DPV Purpose taxonomy.
%
% NAIVE sibling disjointness INCLUDES:
%   disjoint(commercialPurpose, researchAndDevelopment)
% which is WRONG because ↓commercialPurpose ∩ ↓researchAndDevelopment ≠ ∅
% (both contain commercialResearch).

% Hierarchy
fof(dpv_n_root, axiom, concept(purpose)).
fof(dpv_n_c1, axiom, concept(commercialPurpose)).
fof(dpv_n_c2, axiom, concept(researchAndDevelopment)).
fof(dpv_n_c3, axiom, concept(commercialResearch)).
fof(dpv_n_c4, axiom, concept(academicResearch)).
fof(dpv_n_c5, axiom, concept(serviceProvision)).

fof(dpv_n_leq1, axiom, leq(commercialPurpose, purpose)).
fof(dpv_n_leq2, axiom, leq(researchAndDevelopment, purpose)).
fof(dpv_n_leq3, axiom, leq(serviceProvision, purpose)).
fof(dpv_n_leq4, axiom, leq(commercialResearch, commercialPurpose)).
fof(dpv_n_leq5, axiom, leq(commercialResearch, researchAndDevelopment)).
fof(dpv_n_leq6, axiom, leq(academicResearch, researchAndDevelopment)).

% Reflexivity for all concepts
fof(dpv_n_refl1, axiom, leq(purpose, purpose)).
fof(dpv_n_refl2, axiom, leq(commercialPurpose, commercialPurpose)).
fof(dpv_n_refl3, axiom, leq(researchAndDevelopment, researchAndDevelopment)).
fof(dpv_n_refl4, axiom, leq(commercialResearch, commercialResearch)).
fof(dpv_n_refl5, axiom, leq(academicResearch, academicResearch)).
fof(dpv_n_refl6, axiom, leq(serviceProvision, serviceProvision)).

% NAIVE sibling disjointness — THE PROBLEMATIC PAIR:
fof(dpv_n_disj_PROBLEM, axiom,
    disjoint(commercialPurpose, researchAndDevelopment)).
% Plus some safe pairs:
fof(dpv_n_disj_safe1, axiom,
    disjoint(commercialPurpose, serviceProvision)).
fof(dpv_n_disj_safe2, axiom,
    disjoint(researchAndDevelopment, serviceProvision)).

% UNA for all concepts
fof(dpv_n_una, axiom,
    $distinct(purpose, commercialPurpose, researchAndDevelopment,
              commercialResearch, academicResearch, serviceProvision))."""

# ─── DPV SAFE: suppresses problematic pair ────────────────────────────────
DPV_SAFE_FRAGMENT = """\
% --- DPV Fragment (DAG-SAFE sibling disjointness) ---
% Same hierarchy as NAIVE, but disjoint(commercialPurpose, researchAndDevelopment)
% is SUPPRESSED because ↓commercialPurpose ∩ ↓researchAndDevelopment ≠ ∅.
% DAG-safety algorithm (Note 1): suppress disj(A,B) when ∃C: C ≤ A ∧ C ≤ B.

% Hierarchy (identical to NAIVE)
fof(dpv_s_root, axiom, concept(purpose)).
fof(dpv_s_c1, axiom, concept(commercialPurpose)).
fof(dpv_s_c2, axiom, concept(researchAndDevelopment)).
fof(dpv_s_c3, axiom, concept(commercialResearch)).
fof(dpv_s_c4, axiom, concept(academicResearch)).
fof(dpv_s_c5, axiom, concept(serviceProvision)).

fof(dpv_s_leq1, axiom, leq(commercialPurpose, purpose)).
fof(dpv_s_leq2, axiom, leq(researchAndDevelopment, purpose)).
fof(dpv_s_leq3, axiom, leq(serviceProvision, purpose)).
fof(dpv_s_leq4, axiom, leq(commercialResearch, commercialPurpose)).
fof(dpv_s_leq5, axiom, leq(commercialResearch, researchAndDevelopment)).
fof(dpv_s_leq6, axiom, leq(academicResearch, researchAndDevelopment)).

% Reflexivity
fof(dpv_s_refl1, axiom, leq(purpose, purpose)).
fof(dpv_s_refl2, axiom, leq(commercialPurpose, commercialPurpose)).
fof(dpv_s_refl3, axiom, leq(researchAndDevelopment, researchAndDevelopment)).
fof(dpv_s_refl4, axiom, leq(commercialResearch, commercialResearch)).
fof(dpv_s_refl5, axiom, leq(academicResearch, academicResearch)).
fof(dpv_s_refl6, axiom, leq(serviceProvision, serviceProvision)).

% DAG-SAFE sibling disjointness — SUPPRESSED: commercialPurpose ⊥ R&D
% Only safe pairs remain:
fof(dpv_s_disj_safe1, axiom,
    disjoint(commercialPurpose, serviceProvision)).
fof(dpv_s_disj_safe2, axiom,
    disjoint(researchAndDevelopment, serviceProvision)).

% UNA
fof(dpv_s_una, axiom,
    $distinct(purpose, commercialPurpose, researchAndDevelopment,
              commercialResearch, academicResearch, serviceProvision))."""

# ─── SYNTH KB: no native disjointness (for multi-hop tests) ──────────────
SYNTH_KB_NO_DISJ = """\
% --- Synthetic KB (SYNTH) — NO native disjointness ---
% Concepts align to ISO 3166 but have no sibling disjointness.
% Disjointness must be derived through 2-hop alignment from GEO.
fof(synth_root, axiom, concept(euZone)).
fof(synth_c1, axiom, concept(zoneWest)).
fof(synth_c2, axiom, concept(zoneEast)).

fof(synth_leq1, axiom, leq(zoneWest, euZone)).
fof(synth_leq2, axiom, leq(zoneEast, euZone)).
fof(synth_refl1, axiom, leq(euZone, euZone)).
fof(synth_refl2, axiom, leq(zoneWest, zoneWest)).
fof(synth_refl3, axiom, leq(zoneEast, zoneEast)).

% NO disjoint axiom — must come from 2-hop alignment
fof(synth_una, axiom, $distinct(euZone, zoneWest, zoneEast))."""

# ─── Alignment: ISO → SYNTH ──────────────────────────────────────────────
ALIGN_ISO_SYNTH = """\
% Alignment: ISO 3166 → SYNTH (regulatory zones)
fof(align_iso_synth_1, axiom, align(europe, euZone)).
fof(align_iso_synth_2, axiom, align(dE, zoneWest)).
fof(align_iso_synth_3, axiom, align(pL, zoneEast))."""

# ─── COMP KB: compliance tiers, no native disjointness (for 3-hop) ────────
COMP_KB_NO_DISJ = """\
% --- Compliance KB (COMP) — NO native disjointness ---
% 4th dataspace: GDPR compliance tier classification.
% Concepts align to SYNTH (regulatory zones) but have no sibling disjointness.
% Disjointness must be derived through 3-hop alignment: GEO → ISO → SYNTH → COMP.
fof(comp_root, axiom, concept(complianceScope)).
fof(comp_c1, axiom, concept(gdprFull)).
fof(comp_c2, axiom, concept(gdprPartial)).

fof(comp_leq1, axiom, leq(gdprFull, complianceScope)).
fof(comp_leq2, axiom, leq(gdprPartial, complianceScope)).
fof(comp_refl1, axiom, leq(complianceScope, complianceScope)).
fof(comp_refl2, axiom, leq(gdprFull, gdprFull)).
fof(comp_refl3, axiom, leq(gdprPartial, gdprPartial)).

% NO disjoint axiom — must come from 3-hop alignment
fof(comp_una, axiom, $distinct(complianceScope, gdprFull, gdprPartial))."""

# ─── Alignment: SYNTH → COMP ─────────────────────────────────────────────
ALIGN_SYNTH_COMP = """\
% Alignment: SYNTH (regulatory zones) → COMP (compliance tiers)
fof(align_synth_comp_1, axiom, align(euZone, complianceScope)).
fof(align_synth_comp_2, axiom, align(zoneWest, gdprFull)).
fof(align_synth_comp_3, axiom, align(zoneEast, gdprPartial))."""

# ─── Minimal KB (single concept) ─────────────────────────────────────────
MINIMAL_KB_FRAGMENT = """\
% --- Minimal KB: single concept "universe" ---
fof(min_root, axiom, concept(universe)).
fof(min_refl, axiom, leq(universe, universe))."""

# ─── Witness-Loss KBs (Proposition 2(2) counterexample) ──────────────────
# Source KB: {witA, witB, witC} where witA ≤ witB, witA ≤ witC,
# witB and witC are incomparable (no disjointness asserted).
# witA is the ONLY witness for isA(witB) ∩ isA(witC).
KB_WITNESS_SOURCE = """\
% --- Witness-Loss Source KB ---
% Counterexample for Proposition 2(2) (Graceful Degradation).
% witA is the shared descendant (witness): witA ≤ witB ∧ witA ≤ witC.
% witB, witC are incomparable — no disjointness asserted.
fof(wit_src_c1, axiom, concept(witA)).
fof(wit_src_c2, axiom, concept(witB)).
fof(wit_src_c3, axiom, concept(witC)).

fof(wit_src_leq1, axiom, leq(witA, witB)).
fof(wit_src_leq2, axiom, leq(witA, witC)).
fof(wit_src_refl1, axiom, leq(witA, witA)).
fof(wit_src_refl2, axiom, leq(witB, witB)).
fof(wit_src_refl3, axiom, leq(witC, witC)).

% NO disjoint(witB, witC) — incomparable, not disjoint.
fof(wit_src_una, axiom, $distinct(witA, witB, witC))."""

# Target KB: only α(witB) and α(witC) — witness witA is UNMAPPED.
# This is what you get after partial alignment with dom(α) = {witB, witC}.
KB_WITNESS_TARGET = """\
% --- Witness-Loss Target KB (after partial alignment) ---
% dom(α) = {witB, witC}. Witness witA is UNMAPPED → lost.
% Target concepts: tgtB = α(witB), tgtC = α(witC).
fof(wit_tgt_c1, axiom, concept(tgtB)).
fof(wit_tgt_c2, axiom, concept(tgtC)).

fof(wit_tgt_refl1, axiom, leq(tgtB, tgtB)).
fof(wit_tgt_refl2, axiom, leq(tgtC, tgtC)).

% NO leq(tgtB, tgtC) or leq(tgtC, tgtB) — incomparable (matching source).
% NO concept corresponding to witA — it was lost in alignment!
fof(wit_tgt_una, axiom, $distinct(tgtB, tgtC))."""

# Target KB (FULL): β maps ALL concepts including witness witA.
# dom(β) = {witA, witB, witC} — downward-closed. Verdict preserved.
KB_WITNESS_TARGET_FULL = """\
% --- Witness-Loss Target KB (downward-closed alignment) ---
% dom(β) = {witA, witB, witC}. Witness witA IS mapped → preserved.
% Target concepts: tgtA = β(witA), tgtB = β(witB), tgtC = β(witC).
fof(wit_full_c1, axiom, concept(tgtA)).
fof(wit_full_c2, axiom, concept(tgtB)).
fof(wit_full_c3, axiom, concept(tgtC)).

fof(wit_full_leq1, axiom, leq(tgtA, tgtB)).
fof(wit_full_leq2, axiom, leq(tgtA, tgtC)).
fof(wit_full_refl1, axiom, leq(tgtA, tgtA)).
fof(wit_full_refl2, axiom, leq(tgtB, tgtB)).
fof(wit_full_refl3, axiom, leq(tgtC, tgtC)).

% Structure preserved: tgtA ≤ tgtB, tgtA ≤ tgtC (mirrors source).
fof(wit_full_una, axiom, $distinct(tgtA, tgtB, tgtC))."""


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 9: DAG MULTI-PARENT (ODRL100–105)
# Paper Note 1 — DAG-safe sibling disjointness generation
# ═══════════════════════════════════════════════════════════════════════════

P("ODRL100-1.p", "Theorem", "ContradictoryAxioms",
  "Note 1 — DAG Multi-Parent Contradiction (Naive)", "Medium",
  "(No ODRL policy — KB consistency test)\n"
  "%   Tests: naive sibling disjointness on DAG taxonomy causes ⊥.",
  "disjoint(commercialPurpose, R&D) [naive sibling]\n"
  "%   + leq(cR, cP) ∧ leq(cR, R&D) [multi-parent]\n"
  "%   → disj_downward → disjoint(cR, cR)\n"
  "%   → contradicts disj_irrefl → ⊥",
  "fof(odrl100, conjecture, $false).",
  extra=DPV_NAIVE_FRAGMENT,
  inc=("ODRL",),
  pl="DAG inconsistency: naive sibling disj on multi-parent → ⊥")

P("ODRL101-1.p", "Theorem", "Compatible",
  "Note 1 — DAG-Safe Multi-Parent Reachability", "Easy",
  tp("policyA", "permission", "use", [("hasPurpose", "isA", "dpv:CommercialPurpose")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("hasPurpose", "isA", "dpv:ResearchAndDevelopment")]),
  "DAG-safe: disjoint(cP, R&D) suppressed because ↓cP ∩ ↓R&D ≠ ∅.\n"
  "%   Witness: commercialResearch ≤ both parents → overlap.\n"
  "%   Verdict: Compatible (not Conflict).",
  "fof(odrl101, conjecture,\n"
  "    ?[X]: ( in_denotation(X, commercialPurpose, isA)\n"
  "          & in_denotation(X, researchAndDevelopment, isA) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("ODRL",),
  pl="DAG-safe: multi-parent reachability preserved")

P("ODRL102-1.p", "CounterSatisfiable", "Conflict",
  "Note 1 — DAG-Safe True Conflict Detection", "Medium",
  tp("policyA", "permission", "use", [("hasPurpose", "isA", "dpv:CommercialPurpose")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("hasPurpose", "isA", "dpv:ServiceProvision")]),
  "DAG-safe: disjoint(cP, serviceProvision) IS asserted (no shared descendant).\n"
  "%   → disj_downward + disj_irrefl → ∅ → Conflict.\n"
  "%   Tests: DAG-safety doesn't suppress genuine conflicts.",
  "fof(odrl102, conjecture,\n"
  "    ?[X]: ( in_denotation(X, commercialPurpose, isA)\n"
  "          & in_denotation(X, serviceProvision, isA) )).",
  flip_conj=
  "fof(odrl102, conjecture,\n"
  "    ![X]: ~( in_denotation(X, commercialPurpose, isA)\n"
  "           & in_denotation(X, serviceProvision, isA) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("ODRL",),
  pl="DAG-safe: true conflict cP ⊥ serviceProvision still detected")

P("ODRL103-1.p", "CounterSatisfiable", "Conflict",
  "Note 1 + Lemma 2 — DAG-Safe Conflict Propagation", "Hard",
  tp("policyA", "permission", "use", [("hasPurpose", "isA", "dpv:AcademicResearch")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("hasPurpose", "isA", "dpv:ServiceProvision")]),
  "academicResearch ≤ R&D, R&D ⊥ serviceProvision [safe]\n"
  "%   → disj_downward → academicResearch ⊥ serviceProvision\n"
  "%   → ⟦isA(acR)⟧ ∩ ⟦isA(sP)⟧ = ∅ → Conflict",
  "fof(odrl103, conjecture,\n"
  "    ?[X]: ( in_denotation(X, academicResearch, isA)\n"
  "          & in_denotation(X, serviceProvision, isA) )).",
  flip_conj=
  "fof(odrl103, conjecture,\n"
  "    ![X]: ~( in_denotation(X, academicResearch, isA)\n"
  "           & in_denotation(X, serviceProvision, isA) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("ODRL",),
  pl="DAG-safe: conflict propagation acR ⊥ sP via R&D")

P("ODRL104-1.p", "Theorem", "Trivial",
  "Note 1 — Ablation: Naive KB Makes Everything Provable", "Easy",
  "(Same query as ODRL101 but with NAIVE sibling disjointness)\n"
  "%   NAIVE KB is inconsistent → any conjecture is a Theorem.",
  "NAIVE KB: ⊥ (from ODRL100) → anything follows.\n"
  "%   Tests: inconsistent KB trivially proves arbitrary conjectures.\n"
  "%   Compare with ODRL101 (same query, DAG-safe → genuine Compatible).",
  "fof(odrl104, conjecture,\n"
  "    ?[X]: ( in_denotation(X, commercialPurpose, isA)\n"
  "          & in_denotation(X, researchAndDevelopment, isA) )).",
  extra=DPV_NAIVE_FRAGMENT,
  inc=("ODRL",),
  pl="Ablation: naive inconsistency makes query trivially provable")

P("ODRL105-1.p", "Theorem", "Subsumption",
  "Note 1 — DAG Subsumption via Multi-Parent Path", "Medium",
  tp("policyA", "permission", "use", [("hasPurpose", "isA", "dpv:CommercialResearch")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("hasPurpose", "isA", "dpv:CommercialPurpose")]),
  "commercialResearch ≤ commercialPurpose [parent A path]\n"
  "%   → den_isA_onlyif: leq(X, cR) → leq(X, cP) [leq_trans]\n"
  "%   → den_isA_if: in_denotation(X, cP, isA)\n"
  "%   Subsumption: ⟦isA(cR)⟧ ⊆ ⟦isA(cP)⟧",
  "fof(odrl105, conjecture,\n"
  "    ![X]: ( in_denotation(X, commercialResearch, isA)\n"
  "        => in_denotation(X, commercialPurpose, isA) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("ODRL",),
  pl="DAG subsumption: cR ⊆ cP via multi-parent path")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 10: NESTED SET OPERATORS (ODRL110–114)
# Paper Definition 3 — isAllOf, isAnyOf, isNoneOf
# ═══════════════════════════════════════════════════════════════════════════

P("ODRL110-1.p", "Theorem", "EmptyDenotation",
  "Definition 3 (isAllOf) — Empty Denotation from Disjoint Members", "Hard",
  tp("policyA", "permission", "use", [("spatial", "isAllOf", "( geo:westernEurope geo:easternEurope )")]),
  "⟦isAllOf({wE, eE})⟧ = ↓wE ∩ ↓eE.\n"
  "%   wE ⊥ eE [sibling disjointness in GEO KB]\n"
  "%   → disj_downward: ∀X: leq(X,wE) ∧ leq(X,eE) → disjoint(X,X)\n"
  "%   → disj_irrefl: ¬disjoint(X,X) → no such X exists.\n"
  "%   ⟦isAllOf({wE,eE})⟧ = ∅ (vacuously true constraint).",
  "fof(odrl110, conjecture,\n"
  "    ![X]: ~in_denotation_set(X, list110, isAllOf)).",
  extra=(
      "fof(list_110_1, axiom, in_value_list(westernEurope, list110)).\n"
      "fof(list_110_2, axiom, in_value_list(easternEurope, list110)).\n" +
      generate_list_closure("list110", ["westernEurope", "easternEurope"])
  ),
  inc=("GEO", "ODRL"),
  pl="isAllOf({wE,eE}) = ∅: disjoint members → empty denotation")

P("ODRL111-1.p", "Theorem", "Compatible",
  "Definition 3 (isAnyOf) — Union Compatible with isPartOf", "Easy",
  tp("policyA", "permission", "use", [("spatial", "isAnyOf", "( geo:germany geo:france )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:westernEurope")]),
  "⟦isAnyOf({de, fr})⟧ = ↓de ∪ ↓fr, both ⊆ ↓wE.\n"
  "%   Witness: germany ∈ ↓de ∩ ↓wE.",
  "fof(odrl111, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, list111, isAnyOf)\n"
  "          & in_denotation(X, westernEurope, isPartOf) )).",
  extra=(
      "fof(list_111_1, axiom, in_value_list(germany, list111)).\n"
      "fof(list_111_2, axiom, in_value_list(france, list111)).\n" +
      generate_list_closure("list111", ["germany", "france"])
  ),
  inc=("GEO", "ODRL"),
  pl="isAnyOf({de,fr}) ∩ isPartOf(wE) ≠ ∅")

P("ODRL112-1.p", "CounterSatisfiable", "Conflict",
  "Definition 3 (isNoneOf) — Conflict with Subsumed isPartOf", "Hard",
  tp("policyA", "permission", "use", [("spatial", "isNoneOf", "( geo:westernEurope )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:germany")]),
  "isNoneOf({wE}) = {X | ¬leq(X, wE)}, isPartOf(de) = {X | leq(X, de)}\n"
  "%   germany ≤ wE → ↓de ⊆ ↓wE → every X ∈ isPartOf(de) is also ≤ wE\n"
  "%   → X ∈ isNoneOf({wE}) requires ¬leq(X, wE) — contradiction.\n"
  "%   ⟦isNoneOf({wE})⟧ ∩ ⟦isPartOf(de)⟧ = ∅ → Conflict",
  "fof(odrl112, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, list112, isNoneOf)\n"
  "          & in_denotation(X, germany, isPartOf) )).",
  flip_conj=
  "fof(odrl112, conjecture,\n"
  "    ![X]: ~( in_denotation_set(X, list112, isNoneOf)\n"
  "           & in_denotation(X, germany, isPartOf) )).",
  extra=(
      "fof(list_112_1, axiom, in_value_list(westernEurope, list112)).\n" +
      generate_list_closure("list112", ["westernEurope"])
  ),
  inc=("GEO", "ODRL"),
  pl="isNoneOf({wE}) ∩ isPartOf(de) = ∅: subsumed → conflict")

P("ODRL113-1.p", "Theorem", "Compatible",
  "Definition 3 — isAnyOf ∩ isNoneOf Partial Overlap", "Medium",
  tp("policyA", "permission", "use", [("spatial", "isAnyOf", "( geo:germany geo:poland )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isNoneOf", "( geo:easternEurope )")]),
  "isAnyOf({de,pl}) ∩ isNoneOf({eE})\n"
  "%   germany ∈ ↓de ∧ ¬leq(de, eE) → germany ∈ isNoneOf({eE})\n"
  "%   Witness: germany → Compatible",
  "fof(odrl113, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, anyList113, isAnyOf)\n"
  "          & in_denotation_set(X, noneList113, isNoneOf) )).",
  extra=(
      "fof(list_113a_1, axiom, in_value_list(germany, anyList113)).\n"
      "fof(list_113a_2, axiom, in_value_list(poland, anyList113)).\n" +
      generate_list_closure("anyList113", ["germany", "poland"]) + "\n"
      "fof(list_113b_1, axiom, in_value_list(easternEurope, noneList113)).\n" +
      generate_list_closure("noneList113", ["easternEurope"])
  ),
  inc=("GEO", "ODRL"),
  pl="isAnyOf({de,pl}) ∩ isNoneOf({eE}): partial overlap → Compatible")

P("ODRL114-1.p", "Theorem", "Compatible",
  "Definition 3 (isAllOf) — Compatible Members Non-Empty", "Easy",
  tp("policyA", "permission", "use", [("spatial", "isAllOf", "( geo:westernEurope geo:europe )")]),
  "⟦isAllOf({wE, europe})⟧ = ↓wE ∩ ↓europe = ↓wE (since wE ≤ europe)\n"
  "%   Witness: germany ∈ ↓wE.",
  "fof(odrl114, conjecture,\n"
  "    ?[X]: in_denotation_set(X, list114, isAllOf)).",
  extra=(
      "fof(list_114_1, axiom, in_value_list(westernEurope, list114)).\n"
      "fof(list_114_2, axiom, in_value_list(europe, list114)).\n" +
      generate_list_closure("list114", ["westernEurope", "europe"])
  ),
  inc=("GEO", "ODRL"),
  pl="isAllOf({wE, europe}) ≠ ∅: compatible members → non-empty")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 11: QUANTIFIER STRESS (ODRL120–123)
# Tests ∀∃ and ∃∀ quantifier patterns that push ATP performance.
# ═══════════════════════════════════════════════════════════════════════════

P("ODRL120-1.p", "Theorem", "Conflict",
  "Definition 5 (universal) — All Descendant Pairs Conflict", "Hard",
  "(Universal variant of ODRL013)\n"
  "%   ∀G1 ∈ ↓wE, ∀G2 ∈ ↓eE: disjoint overlap → Conflict",
  "For any G1 ≤ wE and G2 ≤ eE:\n"
  "%   disj_downward(wE ⊥ eE, G1 ≤ wE, G2 ≤ eE) → disjoint(G1, G2)\n"
  "%   → ⟦isPartOf(G1)⟧ ∩ ⟦isPartOf(G2)⟧ = ∅ → Conflict for ALL pairs.",
  "fof(odrl120, conjecture,\n"
  "    ![G1,G2,X]: (\n"
  "        (leq(G1, westernEurope) & leq(G2, easternEurope))\n"
  "      => ~( in_denotation(X, G1, isPartOf)\n"
  "          & in_denotation(X, G2, isPartOf) ))).",
  inc=("GEO", "ODRL"),
  pl="Universal conflict: ∀G1∈↓wE, ∀G2∈↓eE: overlap = ∅")

P("ODRL121-1.p", "Theorem", "Compatible",
  "∃∀ Pattern — Common Ancestor for Multiple Concepts", "Hard",
  "(∃X common to hasPart denotation of all three countries)",
  "∃X: ∀G ∈ {de, fr, it}: leq(G, X) → in_denotation(X, G, hasPart)\n"
  "%   Witness: europe (all three ≤ europe via regional hierarchy)\n"
  "%   Tests: ∃∀ quantifier alternation with 3 conjuncts.",
  "fof(odrl121, conjecture,\n"
  "    ?[X]: ( in_denotation(X, germany, hasPart)\n"
  "          & in_denotation(X, france, hasPart)\n"
  "          & in_denotation(X, italy, hasPart) )).",
  inc=("GEO", "ODRL"),
  pl="∃∀ pattern: common ancestor europe for {de, fr, it}")

P("ODRL122-1.p", "Theorem", "Subsumption",
  "Lemma 2 (universal) — Denotation Subsumption Chain", "Medium",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:bavaria")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:europe")]),
  "bavaria ≤ germany ≤ westernEurope ≤ europe [3-hop chain]\n"
  "%   → leq_trans: leq(bavaria, europe)\n"
  "%   → ⟦isPartOf(bavaria)⟧ ⊆ ⟦isPartOf(europe)⟧",
  "fof(odrl122, conjecture,\n"
  "    ![X]: ( in_denotation(X, bavaria, isPartOf)\n"
  "        => in_denotation(X, europe, isPartOf) )).",
  inc=("GEO", "ODRL"),
  pl="Subsumption chain: ↓bavaria ⊆ ↓europe via 3-hop leq")

P("ODRL123-1.p", "Theorem", "Sound",
  "∀∃ Pattern — Every Descendant Has an Ancestor", "Hard",
  "(∀G ≤ wE: ∃X such that X ∈ hasPart(G))",
  "For all G ≤ wE: leq(G, westernEurope) → in_denotation(westernEurope, G, hasPart)\n"
  "%   Witness: X = westernEurope (leq(G, wE) → den_hasPart_if → in_den(wE, G, hasPart))\n"
  "%   Tests: universal-existential with quantified KB concepts.",
  "fof(odrl123, conjecture,\n"
  "    ![G]: ( leq(G, westernEurope)\n"
  "        => ?[X]: in_denotation(X, G, hasPart) )).",
  inc=("GEO", "ODRL"),
  pl="∀∃ pattern: every G ≤ wE has ancestor in hasPart(G)")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 12: LARGE-SCALE COMPOSITION (ODRL130–132)
# Tests AND composition over multiple operands simultaneously.
# ═══════════════════════════════════════════════════════════════════════════

P("ODRL130-1.p", "Theorem", "Compatible",
  "Definition 6 — 3-Operand AND Composition", "Medium",
  tp("policyA", "permission", "use", [
      ("spatial", "isPartOf", "geo:europe"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment"),
      ("language", "isPartOf", "lang:en")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("spatial", "eq", "geo:germany"),
      ("hasPurpose", "isA", "dpv:AcademicResearch"),
      ("language", "eq", "lang:enGB")
  ]),
  "3-operand AND: each operand Compatible → composed Compatible.\n"
  "%   Witnesses: germany (spatial), academicResearch (purpose), enGB (language).\n"
  "%   Tests: composition over 3 independent operands.",
  "fof(odrl130, conjecture,\n"
  "    ( ?[X]: ( in_denotation(X, europe, isPartOf)\n"
  "            & in_denotation(X, germany, eq) )\n"
  "    & ?[Y]: ( in_denotation(Y, researchAndDevelopment, isA)\n"
  "            & in_denotation(Y, academicResearch, isA) )\n"
  "    & ?[Z]: ( in_denotation(Z, en, isPartOf)\n"
  "            & in_denotation(Z, enGB, eq) ) )).",
  inc=("GEO", "DPV", "LANG", "ODRL"),
  pl="3-operand AND: spatial + purpose + language all Compatible")

P("ODRL131-1.p", "CounterSatisfiable", "Conflict",
  "Theorem 2 — 3-Operand AND with One Conflict", "Hard",
  tp("policyA", "permission", "use", [
      ("spatial", "isPartOf", "geo:westernEurope"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment"),
      ("language", "isPartOf", "lang:en")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:easternEurope"),
      ("hasPurpose", "isA", "dpv:AcademicResearch"),
      ("language", "eq", "lang:enGB")
  ]),
  "3-operand AND: spatial Conflict → composed Conflict.\n"
  "%   By Theorem 2: AND(Conflict, Compatible, Compatible) = Conflict.\n"
  "%   It suffices to prove the spatial operand conflicts.",
  "fof(odrl131, conjecture,\n"
  "    ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
  "          & in_denotation(X, easternEurope, isPartOf) )).",
  flip_conj=
  "fof(odrl131, conjecture,\n"
  "    ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
  "           & in_denotation(X, easternEurope, isPartOf) )).",
  inc=("GEO", "DPV", "LANG", "ODRL"),
  pl="3-operand AND: spatial Conflict → composed Conflict")

P("ODRL132-1.p", "Theorem", "Compatible",
  "Definition 6 — 5-Way Existential Witness", "Hard",
  "(5 compatible pairs in a single conjecture)\n"
  "%   Tests large-scale existential witness construction.",
  "5 overlap witnesses — each pair from different GEO hierarchy branch.\n"
  "%   Tests: Vampire's ability to find 5 independent witnesses.\n"
  "%   All witnesses are grounded in the GEO KB.",
  "fof(odrl132, conjecture,\n"
  "    ( ?[X1]: ( in_denotation(X1, europe, isPartOf)\n"
  "             & in_denotation(X1, germany, eq) )\n"
  "    & ?[X2]: ( in_denotation(X2, westernEurope, isPartOf)\n"
  "             & in_denotation(X2, france, eq) )\n"
  "    & ?[X3]: ( in_denotation(X3, europe, hasPart)\n"
  "             & in_denotation(X3, germany, hasPart) )\n"
  "    & ?[X4]: ( in_denotation(X4, westernEurope, isPartOf)\n"
  "             & in_denotation(X4, bavaria, isPartOf) )\n"
  "    & ?[X5]: ( in_denotation(X5, europe, isPartOf)\n"
  "             & in_denotation(X5, poland, eq) ) )).",
  inc=("GEO", "ODRL"),
  pl="5-way existential: 5 independent compatible pairs")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 13: EDGE CASES & ADVERSARIAL (ODRL140–145)
# Tests degenerate, pathological, and boundary cases.
# ═══════════════════════════════════════════════════════════════════════════

P("ODRL140-1.p", "CounterSatisfiable", "Conflict",
  "Definition 5 — Tautological Self-Conflict (eq ∩ neq)", "Easy",
  tp("policyA", "permission", "use", [("spatial", "eq", "geo:germany")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "neq", "geo:germany")]),
  "eq(de) = {de}, neq(de) = {X ≠ de} → intersection = ∅.\n"
  "%   Tautological conflict: same concept with contradictory operators.",
  "fof(odrl140, conjecture,\n"
  "    ?[X]: ( in_denotation(X, germany, eq)\n"
  "          & in_denotation(X, germany, neq) )).",
  flip_conj=
  "fof(odrl140, conjecture,\n"
  "    ![X]: ~( in_denotation(X, germany, eq)\n"
  "           & in_denotation(X, germany, neq) )).",
  inc=("GEO", "ODRL"),
  pl="Tautological conflict: eq(de) ∩ neq(de) = ∅")

P("ODRL141-1.p", "Theorem", "Compatible",
  "Edge Case — Single-Concept KB (Degenerate)", "Easy",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "min:universe")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "eq", "min:universe")]),
  "Degenerate KB: only concept is universe, leq(universe, universe).\n"
  "%   isPartOf(universe) = {universe}, eq(universe) = {universe}.\n"
  "%   → trivially Compatible. Tests boundary case.",
  "fof(odrl141, conjecture,\n"
  "    ?[X]: ( in_denotation(X, universe, isPartOf)\n"
  "          & in_denotation(X, universe, eq) )).",
  extra=MINIMAL_KB_FRAGMENT,
  inc=("ODRL",),
  pl="Degenerate: single-concept KB → trivially compatible")

P("ODRL142-1.p", "CounterSatisfiable", "Conflict",
  "Edge Case — Root-Level Conflict (Large KB Loaded)", "Easy",
  tp("policyA", "permission", "use", [("spatial", "eq", "geo:europe")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "neq", "geo:europe")]),
  "eq(europe) ∩ neq(europe) = ∅ — trivial even with 24-concept KB.\n"
  "%   Tests: loading many concepts doesn't disrupt simple reasoning.",
  "fof(odrl142, conjecture,\n"
  "    ?[X]: ( in_denotation(X, europe, eq)\n"
  "          & in_denotation(X, europe, neq) )).",
  flip_conj=
  "fof(odrl142, conjecture,\n"
  "    ![X]: ~( in_denotation(X, europe, eq)\n"
  "           & in_denotation(X, europe, neq) )).",
  inc=("GEO", "ODRL"),
  pl="Root-level eq/neq conflict with full KB loaded")

P("ODRL143-1.p", "Theorem", "Tautology",
  "Reflexivity — Every Concept Is In Its Own isPartOf", "Easy",
  "(Meta-property: ∀G: G ∈ ⟦isPartOf(G)⟧)",
  "leq_refl: leq(G, G) [reflexivity in KB]\n"
  "%   → den_isPartOf_if: in_denotation(G, G, isPartOf)\n"
  "%   Universally quantified over all KB concepts.",
  "fof(odrl143, conjecture,\n"
  "    ![G]: ( concept(G)\n"
  "        => in_denotation(G, G, isPartOf) )).",
  inc=("GEO", "ODRL"),
  pl="Reflexivity: ∀G: concept(G) → G ∈ ⟦isPartOf(G)⟧")

P("ODRL144-1.p", "Theorem", "Conflict",
  "Definition 2 (disj_symm) — Bidirectional Conflict", "Medium",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:westernEurope")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:easternEurope")]),
  "disjoint is symmetric: disj(wE, eE) → disj(eE, wE).\n"
  "%   Proves BOTH directions of the conflict in one conjecture.",
  "fof(odrl144, conjecture,\n"
  "    ( ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
  "             & in_denotation(X, easternEurope, isPartOf) )\n"
  "    & ![Y]: ~( in_denotation(Y, easternEurope, isPartOf)\n"
  "             & in_denotation(Y, westernEurope, isPartOf) ) )).",
  inc=("GEO", "ODRL"),
  pl="Bidirectional conflict: disj(wE,eE) ∧ disj(eE,wE)")

P("ODRL145-1.p", "CounterSatisfiable", "Unknown",
  "Edge Case — Query on Non-Existent Concept", "Medium",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:phantomConcept")]),
  "phantomConcept is NOT declared as concept/1 in any KB.\n"
  "%   den_isPartOf_if requires concept(G) — won't fire.\n"
  "%   No axiom produces in_denotation(_, phantomConcept, _).\n"
  "%   Prover cannot prove or refute → Unknown.",
  "fof(odrl145, conjecture,\n"
  "    ?[X]: in_denotation(X, phantomConcept, isPartOf)).",
  inc=("GEO", "ODRL"),
  pl="Non-existent concept: no concept/1 → satisfaction unknown")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 14: MULTI-HOP ALIGNMENT (ODRL150–159)
# Tests alignment composition: GEO → ISO → SYNTH → COMP (up to 4-KB chain)
#   2-hop (ODRL150–153): GEO → ISO → SYNTH
#   3-hop (ODRL154–157): GEO → ISO → SYNTH → COMP
#   Witness-loss (ODRL158–159): Prop 2(2) counterexample
# ═══════════════════════════════════════════════════════════════════════════

P("ODRL150-1.p", "CounterSatisfiable", "Conflict",
  "Proposition 2 (2-hop) — Multi-Hop Alignment Conflict", "Very Hard",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "synth:zoneWest")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "synth:zoneEast")]),
  "2-hop alignment chain: GEO → ISO → SYNTH\n"
  "%   GEO: disj(wE,eE) → disj_downward → disj(de,pl)\n"
  "%   Hop 1: align(de,dE) + align(pl,pL) + align_disj_forward → disj(dE,pL)\n"
  "%   Hop 2: align(dE,zoneWest) + align(pL,zoneEast) + align_disj_forward\n"
  "%          → disj(zoneWest, zoneEast)\n"
  "%   → ⟦isPartOf(zoneWest)⟧ ∩ ⟦isPartOf(zoneEast)⟧ = ∅ → Conflict",
  "fof(odrl150, conjecture,\n"
  "    ?[X]: ( in_denotation(X, zoneWest, isPartOf)\n"
  "          & in_denotation(X, zoneEast, isPartOf) )).",
  flip_conj=
  "fof(odrl150, conjecture,\n"
  "    ![X]: ~( in_denotation(X, zoneWest, isPartOf)\n"
  "           & in_denotation(X, zoneEast, isPartOf) )).",
  extra=SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH,
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY"),
  pl="2-hop alignment: GEO→ISO→SYNTH conflict detection")

P("ODRL151-1.p", "Theorem", "Compatible",
  "Proposition 2 (2-hop) — Multi-Hop Compatible", "Medium",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "synth:euZone")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "eq", "synth:zoneWest")]),
  "isPartOf(euZone) ∩ eq(zoneWest) → Compatible\n"
  "%   Witness: zoneWest (leq(zoneWest, euZone) ∧ zoneWest = zoneWest)\n"
  "%   Tests: compatibility in 3-KB context.",
  "fof(odrl151, conjecture,\n"
  "    ?[X]: ( in_denotation(X, euZone, isPartOf)\n"
  "          & in_denotation(X, zoneWest, eq) )).",
  extra=SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH,
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY"),
  pl="2-hop compatible: isPartOf(euZone) ∩ eq(zoneWest) ≠ ∅")

P("ODRL152-1.p", "CounterSatisfiable", "Unknown",
  "2-Hop Ablation — SYNTH Alone Cannot Detect Conflict", "Hard",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "synth:zoneWest")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "synth:zoneEast")]),
  "Same query as ODRL150 but WITHOUT GEO/ISO/alignment.\n"
  "%   SYNTH_NO_DISJ has no disjoint axioms → prover cannot derive disjoint(zoneWest, zoneEast).\n"
  "%   → Unknown (CounterSatisfiable timeout).",
  "fof(odrl152, conjecture,\n"
  "    ?[X]: ( in_denotation(X, zoneWest, isPartOf)\n"
  "          & in_denotation(X, zoneEast, isPartOf) )).",
  extra=SYNTH_KB_NO_DISJ,
  inc=("ODRL",),
  pl="Ablation: SYNTH alone → Unknown (no disjointness)")

P("ODRL153-1.p", "Theorem", "Conflict",
  "2-Hop Intermediate — 1-Hop Result as Prerequisite", "Medium",
  "(Proves intermediate result needed for ODRL150 hop 2)",
  "1-hop alignment: GEO → ISO\n"
  "%   disj(wE,eE) → disj_downward → disj(de,pl)\n"
  "%   align(de,dE) + align(pl,pL) + align_disj_forward → disj(dE,pL)\n"
  "%   Tests: hop 1 result that feeds into ODRL150.",
  "fof(odrl153, conjecture, disjoint(dE, pL)).",
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY"),
  pl="Intermediate: hop 1 derives disjoint(dE, pL)")

# ─── 3-Hop: GEO → ISO → SYNTH → COMP (4 dataspaces) ─────────────────────

# Combined inline axioms for the full 4-KB chain
_4KB_EXTRA = (SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH + "\n" +
              COMP_KB_NO_DISJ + "\n" + ALIGN_SYNTH_COMP)

P("ODRL154-1.p", "CounterSatisfiable", "Conflict",
  "Proposition 2 (3-hop) — 4-Dataspace Alignment Conflict", "Very Hard",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "comp:gdprFull")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "comp:gdprPartial")]),
  "3-hop alignment chain: GEO → ISO → SYNTH → COMP\n"
  "%   GEO: disj(wE,eE) → disj_downward → disj(de,pl)\n"
  "%   Hop 1: align(de,dE) + align(pl,pL) → disj(dE,pL)\n"
  "%   Hop 2: align(dE,zoneWest) + align(pL,zoneEast) → disj(zoneWest,zoneEast)\n"
  "%   Hop 3: align(zoneWest,gdprFull) + align(zoneEast,gdprPartial)\n"
  "%          → disj(gdprFull, gdprPartial)\n"
  "%   → ⟦isPartOf(gdprFull)⟧ ∩ ⟦isPartOf(gdprPartial)⟧ = ∅ → Conflict",
  "fof(odrl154, conjecture,\n"
  "    ?[X]: ( in_denotation(X, gdprFull, isPartOf)\n"
  "          & in_denotation(X, gdprPartial, isPartOf) )).",
  flip_conj=
  "fof(odrl154, conjecture,\n"
  "    ![X]: ~( in_denotation(X, gdprFull, isPartOf)\n"
  "           & in_denotation(X, gdprPartial, isPartOf) )).",
  extra=_4KB_EXTRA,
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY"),
  pl="3-hop alignment: GEO→ISO→SYNTH→COMP conflict detection")

P("ODRL155-1.p", "Theorem", "Compatible",
  "Proposition 2 (3-hop) — 4-Dataspace Compatible", "Medium",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "comp:complianceScope")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "eq", "comp:gdprFull")]),
  "isPartOf(complianceScope) ∩ eq(gdprFull) → Compatible\n"
  "%   Witness: gdprFull (leq(gdprFull, complianceScope) ∧ gdprFull = gdprFull)\n"
  "%   Tests: compatibility query in 4-KB context with 3 alignment bridges.",
  "fof(odrl155, conjecture,\n"
  "    ?[X]: ( in_denotation(X, complianceScope, isPartOf)\n"
  "          & in_denotation(X, gdprFull, eq) )).",
  extra=_4KB_EXTRA,
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY"),
  pl="3-hop compatible: isPartOf(complianceScope) ∩ eq(gdprFull) ≠ ∅")

P("ODRL156-1.p", "CounterSatisfiable", "Unknown",
  "3-Hop Ablation — COMP Alone Cannot Detect Conflict", "Hard",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "comp:gdprFull")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "comp:gdprPartial")]),
  "Same query as ODRL154 but WITHOUT GEO/ISO/SYNTH/alignment.\n"
  "%   COMP has no disjoint axioms → prover cannot derive disj(gdprFull, gdprPartial).\n"
  "%   → Unknown (expected timeout).",
  "fof(odrl156, conjecture,\n"
  "    ?[X]: ( in_denotation(X, gdprFull, isPartOf)\n"
  "          & in_denotation(X, gdprPartial, isPartOf) )).",
  extra=COMP_KB_NO_DISJ,
  inc=("ODRL",),
  pl="Ablation: COMP alone → Unknown (no disjointness)")

P("ODRL157-1.p", "Theorem", "Conflict",
  "3-Hop Intermediate — Hop 2 Result as Prerequisite", "Hard",
  "(Proves hop 2 intermediate: disj(zoneWest, zoneEast) for ODRL154 hop 3)",
  "2-hop alignment: GEO → ISO → SYNTH\n"
  "%   disj(wE,eE) → disj(de,pl) → disj(dE,pL) → disj(zoneWest,zoneEast)\n"
  "%   Tests: hop 2 result that feeds into ODRL154.",
  "fof(odrl157, conjecture, disjoint(zoneWest, zoneEast)).",
  extra=SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH,
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY"),
  pl="Intermediate: hop 2 derives disjoint(zoneWest, zoneEast)")

# ─── Proposition 2(2) Counterexample: Witness Loss under Partial Alignment ──

P("ODRL158-1.p", "Theorem", "Compatible",
  "Proposition 2(2) Baseline — Compatible in Source KB", "Easy",
  tp("policyA", "permission", "use", [("hasPurpose", "isA", "wit:witB")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("hasPurpose", "isA", "wit:witC")]),
  "Baseline for Prop 2(2) counterexample.\n"
  "%   Source KB: witA ≤ witB, witA ≤ witC, no disjoint(witB, witC).\n"
  "%   ⟦isA(witB)⟧ = {witA, witB}, ⟦isA(witC)⟧ = {witA, witC}\n"
  "%   Intersection = {witA} ≠ ∅ → Compatible.\n"
  "%   Witness: witA (shared descendant of both witB and witC).",
  "fof(odrl158, conjecture,\n"
  "    ?[X]: ( in_denotation(X, witB, isA)\n"
  "          & in_denotation(X, witC, isA) )).",
  extra=KB_WITNESS_SOURCE,
  inc=("ODRL",),
  pl="Prop 2(2) baseline: witA witnesses isA(witB) ∩ isA(witC) ≠ ∅")

P("ODRL159-1.p", "CounterSatisfiable", "FabricatedConflict",
  "Proposition 2(2) Bug — Fabricated Conflict from Partial Alignment", "Very Hard",
  tp("policyA", "permission", "use", [("hasPurpose", "isA", "tgt:tgtB")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("hasPurpose", "isA", "tgt:tgtC")]),
  "Proposition 2(2) COUNTEREXAMPLE: partial alignment creates false Conflict.\n"
  "%   Partial alignment α: dom(α) = {witB, witC}. Witness witA is UNMAPPED.\n"
  "%   Target KB: {tgtB, tgtC} only (no concept for witA).\n"
  "%   ⟦isA(tgtB)⟧ = {tgtB}, ⟦isA(tgtC)⟧ = {tgtC}\n"
  "%   Intersection = ∅ (tgtB ≠ tgtC by UNA) → FABRICATED Conflict!\n"
  "%   Source was Compatible (ODRL158), target is Conflict → verdict NOT preserved.\n"
  "%   Disproves: 'partial alignment can only weaken toward Unknown, never fabricate'.",
  "fof(odrl159, conjecture,\n"
  "    ?[X]: ( in_denotation(X, tgtB, isA)\n"
  "          & in_denotation(X, tgtC, isA) )).",
  flip_conj=
  "fof(odrl159, conjecture,\n"
  "    ![X]: ~( in_denotation(X, tgtB, isA)\n"
  "           & in_denotation(X, tgtC, isA) )).",
  extra=KB_WITNESS_TARGET,
  inc=("ODRL",),
  pl="Prop 2(2) BUG: partial alignment loses witness → fabricated Conflict")

P("ODRL158-2.p", "Theorem", "Compatible",
  "Proposition 2(2) Fix — Downward-Closed Alignment Preserves Verdict", "Hard",
  tp("policyA", "permission", "use", [("hasPurpose", "isA", "tgt:tgtB")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("hasPurpose", "isA", "tgt:tgtC")]),
  "Proposition 2(2) FIX: downward-closed alignment preserves Compatible.\n"
  "%   Total alignment β: dom(β) = {witA, witB, witC}. ALL concepts mapped.\n"
  "%   Target KB: {tgtA, tgtB, tgtC} with tgtA ≤ tgtB, tgtA ≤ tgtC.\n"
  "%   ⟦isA(tgtB)⟧ = {tgtA, tgtB}, ⟦isA(tgtC)⟧ = {tgtA, tgtC}\n"
  "%   Intersection = {tgtA} ≠ ∅ → Compatible PRESERVED.\n"
  "%   Compare: ODRL158 (source), ODRL159 (partial → fabricated Conflict).\n"
  "%   Fix: require dom(α) ⊇ ↓g for each grounding value g.",
  "fof(odrl158b, conjecture,\n"
  "    ?[X]: ( in_denotation(X, tgtB, isA)\n"
  "          & in_denotation(X, tgtC, isA) )).",
  extra=KB_WITNESS_TARGET_FULL,
  inc=("ODRL",),
  pl="Prop 2(2) FIX: downward-closed alignment → Compatible preserved")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 15: N-WAY POLICY CONFLICTS (ODRL160–165)
# Tests 3+ policies simultaneously — not just pairwise.
#
# Key insight: pairwise conflict analysis is NECESSARY but not SUFFICIENT.
# Compatibility is NOT transitive: Compatible(A,B) ∧ Compatible(B,C) ⊬ Compatible(A,C).
# N-way analysis reveals patterns invisible to pairwise checking.
#
# Patterns tested:
#   160 — 3-policy mutual exclusion (all C(3,2) = 3 pairs conflict)
#   161 — 3-policy common witness (3-way ∃)
#   162 — Non-transitive compatibility (A~B, B~C, A⊥C)
#   163 — Multi-dimensional 3-way (spatial + purpose, mixed verdicts)
#   164 — 4-policy subsumption chain (4-way ∃)
#   165 — 4-policy one spoiler (D conflicts with B,C but not A)
# ═══════════════════════════════════════════════════════════════════════════

# 160: 3-policy mutual exclusion — all 3 pairs conflict
#   policyA: permission spatial isPartOf(germany)
#   policyB: prohibition spatial isPartOf(france)
#   policyC: prohibition spatial isPartOf(poland)
#
#   de ⊥ fr (siblings under wE)
#   de ⊥ pl (disj_downward from wE ⊥ eE)
#   fr ⊥ pl (disj_downward from wE ⊥ eE)
#   Prove: all 3 pairwise intersections are empty.
P("ODRL160-1.p", "Theorem", "Conflict",
  "N-Way — 3-Policy Mutual Exclusion", "Hard",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:germany")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:france")]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [("spatial", "isPartOf", "geo:poland")]),
  "3-policy mutual exclusion: all C(3,2) = 3 pairs conflict.\n"
  "%   de ⊥ fr [siblings under wE]\n"
  "%   de ⊥ pl [disj_downward from wE ⊥ eE + leq(de,wE) + leq(pl,eE)]\n"
  "%   fr ⊥ pl [disj_downward from wE ⊥ eE + leq(fr,wE) + leq(pl,eE)]\n"
  "%   Proves: pairwise analysis scales — all 3 pairs are independently empty.",
  "fof(odrl160, conjecture,\n"
  "    ( ![X]: ~( in_denotation(X, germany, isPartOf)\n"
  "             & in_denotation(X, france, isPartOf) )\n"
  "    & ![Y]: ~( in_denotation(Y, germany, isPartOf)\n"
  "             & in_denotation(Y, poland, isPartOf) )\n"
  "    & ![Z]: ~( in_denotation(Z, france, isPartOf)\n"
  "             & in_denotation(Z, poland, isPartOf) ) )).",
  inc=("GEO", "ODRL"),
  pl="3-policy mutual exclusion: all 3 pairs conflict (de⊥fr, de⊥pl, fr⊥pl)")

# 161: 3-policy common witness — 3-way existential
#   policyA: permission spatial isPartOf(europe)
#   policyB: prohibition spatial isPartOf(westernEurope)
#   policyC: prohibition spatial eq(germany)
#
#   ∃X: X ∈ ↓europe ∧ X ∈ ↓wE ∧ X = de
#   Witness: germany (leq(de,wE), leq(wE,europe), de=de)
#   Tests: prover finds a single witness satisfying 3 constraints simultaneously.
P("ODRL161-1.p", "Theorem", "Compatible",
  "N-Way — 3-Policy Common Witness", "Medium",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:europe")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:westernEurope")]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [("spatial", "eq", "geo:germany")]),
  "3-way existential: ∃X in all three denotations simultaneously.\n"
  "%   Witness: germany (leq(de,wE), leq(wE,europe) → leq(de,europe), de=de)\n"
  "%   Tests: 3-way intersection ≠ ∅ → all 3 policies overlap at germany.",
  "fof(odrl161, conjecture,\n"
  "    ?[X]: ( in_denotation(X, europe, isPartOf)\n"
  "          & in_denotation(X, westernEurope, isPartOf)\n"
  "          & in_denotation(X, germany, eq) )).",
  inc=("GEO", "ODRL"),
  pl="3-policy common witness: ∃X ∈ ↓europe ∩ ↓wE ∩ {de}")

# 162: Non-transitive compatibility — the key N-way insight
#   policyA: permission spatial isPartOf(westernEurope)
#   policyB: prohibition spatial isPartOf(europe)
#   policyC: prohibition spatial isPartOf(easternEurope)
#
#   A∩B = ↓wE ∩ ↓europe = ↓wE ≠ ∅        → Compatible(A,B)
#   B∩C = ↓europe ∩ ↓eE = ↓eE ≠ ∅         → Compatible(B,C)
#   A∩C = ↓wE ∩ ↓eE = ∅                    → Conflict(A,C) !!
#
#   This is THE motivating example for N-way analysis:
#   Compatible(A,B) ∧ Compatible(B,C) ⊬ Compatible(A,C)
#   Pairwise checking of adjacent policies misses this.
P("ODRL162-1.p", "Theorem", "NonTransitive",
  "N-Way — Non-Transitive Compatibility", "Hard",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:westernEurope")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:europe")]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [("spatial", "isPartOf", "geo:easternEurope")]),
  "Non-transitive compatibility — the key N-way insight.\n"
  "%   Compatible(A,B): ↓wE ∩ ↓europe = ↓wE ≠ ∅  [witness: germany]\n"
  "%   Compatible(B,C): ↓europe ∩ ↓eE = ↓eE ≠ ∅   [witness: poland]\n"
  "%   Conflict(A,C):   ↓wE ∩ ↓eE = ∅              [wE ⊥ eE]\n"
  "%   Proves: Compatible(A,B) ∧ Compatible(B,C) ⊬ Compatible(A,C)",
  "fof(odrl162, conjecture,\n"
  "    ( ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
  "            & in_denotation(X, europe, isPartOf) )\n"
  "    & ?[Y]: ( in_denotation(Y, europe, isPartOf)\n"
  "            & in_denotation(Y, easternEurope, isPartOf) )\n"
  "    & ![Z]: ~( in_denotation(Z, westernEurope, isPartOf)\n"
  "             & in_denotation(Z, easternEurope, isPartOf) ) )).",
  inc=("GEO", "ODRL"),
  pl="Non-transitive: Compatible(A,B) ∧ Compatible(B,C) but Conflict(A,C)")

# 163: Multi-dimensional 3-way (spatial + purpose)
#   policyA: permission, spatial isPartOf(europe), purpose isA(R&D)
#   policyB: prohibition, spatial isPartOf(germany), purpose isA(academicResearch)
#   policyC: prohibition, spatial isPartOf(france), purpose isA(commercialPurpose)
#
#   A vs B — spatial: de ≤ europe → Compatible
#            purpose: acR ≤ R&D → Compatible
#            AND: Compatible ∧ Compatible → Compatible
#   A vs C — spatial: fr ≤ europe → Compatible
#            purpose: isA(R&D) ∩ isA(cP) → witness cR (DAG-safe!) → Compatible
#            AND: Compatible ∧ Compatible → Compatible
#   B vs C — spatial: ↓de ∩ ↓fr = ∅ [de ⊥ fr] → Conflict
#            AND: Conflict ∧ anything → Conflict (Theorem 2)
#
#   Pattern: "hub" policy A is compatible with both B and C,
#   but B and C conflict on the spatial dimension.
P("ODRL163-1.p", "Theorem", "MixedNWay",
  "N-Way — Multi-Dimensional 3-Way (Spatial + Purpose)", "Very Hard",
  tp("policyA", "permission", "use", [
      ("spatial", "isPartOf", "geo:europe"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:germany"),
      ("hasPurpose", "isA", "dpv:AcademicResearch")
  ]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:france"),
      ("hasPurpose", "isA", "dpv:CommercialPurpose")
  ]),
  "Multi-dimensional 3-way with mixed verdicts:\n"
  "%   A vs B: spatial Compatible (de ≤ europe) ∧ purpose Compatible (acR ≤ R&D) → Compatible\n"
  "%   A vs C: spatial Compatible (fr ≤ europe) ∧ purpose Compatible (cR ≤ R&D ∧ cR ≤ cP) → Compatible\n"
  "%   B vs C: spatial Conflict (de ⊥ fr) → Conflict (Thm 2: one Conflict operand suffices)\n"
  "%   Tests: multi-dimensional n-way with DAG-safe purpose KB.",
  "fof(odrl163, conjecture,\n"
  "    ( ?[Xs,Xp]: ( in_denotation(Xs, europe, isPartOf)\n"
  "               & in_denotation(Xs, germany, isPartOf)\n"
  "               & in_denotation(Xp, researchAndDevelopment, isA)\n"
  "               & in_denotation(Xp, academicResearch, isA) )\n"
  "    & ?[Ys,Yp]: ( in_denotation(Ys, europe, isPartOf)\n"
  "               & in_denotation(Ys, france, isPartOf)\n"
  "               & in_denotation(Yp, researchAndDevelopment, isA)\n"
  "               & in_denotation(Yp, commercialPurpose, isA) )\n"
  "    & ![Z]: ~( in_denotation(Z, germany, isPartOf)\n"
  "             & in_denotation(Z, france, isPartOf) ) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("GEO", "ODRL"),
  pl="Multi-dim 3-way: A~B, A~C (spatial+purpose), but B⊥C (spatial)")

# 164: 4-policy subsumption chain — 4-way existential
#   policyA: permission spatial isPartOf(europe)
#   policyB: prohibition spatial isPartOf(westernEurope)
#   policyC: prohibition spatial isPartOf(germany)
#   policyD: prohibition spatial eq(bavaria)
#
#   All 4 overlap at bavaria: leq(bav,de), leq(de,wE), leq(wE,europe)
#   ∃X: X ∈ ↓europe ∩ ↓wE ∩ ↓de ∩ {bavaria}
#   Witness: bavaria
P("ODRL164-1.p", "Theorem", "Compatible",
  "N-Way — 4-Policy Subsumption Chain", "Medium",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:europe")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:westernEurope")]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [("spatial", "isPartOf", "geo:germany")]) + "\n%\n%   " +
  tp("policyD", "prohibition", "use", [("spatial", "eq", "geo:bavaria")]),
  "4-way existential: all 4 policies overlap at single witness.\n"
  "%   Witness: bavaria (leq(bav,de), leq(de,wE), leq(wE,europe), bav=bav)\n"
  "%   Tests: prover must find a witness satisfying 4 constraints simultaneously.",
  "fof(odrl164, conjecture,\n"
  "    ?[X]: ( in_denotation(X, europe, isPartOf)\n"
  "          & in_denotation(X, westernEurope, isPartOf)\n"
  "          & in_denotation(X, germany, isPartOf)\n"
  "          & in_denotation(X, bavaria, eq) )).",
  inc=("GEO", "ODRL"),
  pl="4-policy chain: ∃X ∈ ↓europe ∩ ↓wE ∩ ↓de ∩ {bav}")

# 165: 4-policy one spoiler — D conflicts with B,C but not A
#   policyA: permission spatial isPartOf(europe)          [broad]
#   policyB: permission spatial isPartOf(westernEurope)   [west]
#   policyC: permission spatial eq(germany)               [specific]
#   policyD: prohibition spatial isPartOf(easternEurope)  [east — the spoiler]
#
#   A∩D = ↓europe ∩ ↓eE = ↓eE ≠ ∅                  → Compatible [witness: poland]
#   B∩D = ↓wE ∩ ↓eE = ∅                             → Conflict [wE ⊥ eE]
#   C∩D = {de} ∩ ↓eE = ∅                            → Conflict [de ≤ wE, wE ⊥ eE]
#
#   Pattern: "spoiler" policy D selectively conflicts with some but not all.
#   Shows why every pair must be checked — ignoring D-vs-A would miss the safe pair.
P("ODRL165-1.p", "Theorem", "MixedNWay",
  "N-Way — 4-Policy One Spoiler", "Hard",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:europe")]) + "\n%\n%   " +
  tp("policyB", "permission", "use", [("spatial", "isPartOf", "geo:westernEurope")]) + "\n%\n%   " +
  tp("policyC", "permission", "use", [("spatial", "eq", "geo:germany")]) + "\n%\n%   " +
  tp("policyD", "prohibition", "use", [("spatial", "isPartOf", "geo:easternEurope")]),
  "4-policy one spoiler: D conflicts with B,C but NOT with A.\n"
  "%   Compatible(A,D): ↓europe ∩ ↓eE = ↓eE ≠ ∅    [witness: poland]\n"
  "%   Conflict(B,D):   ↓wE ∩ ↓eE = ∅                [wE ⊥ eE]\n"
  "%   Conflict(C,D):   {de} ∩ ↓eE = ∅                [de ≤ wE, wE ⊥ eE → de ⊥ eE]\n"
  "%   Shows: spoiler analysis — every pair must be checked independently.",
  "fof(odrl165, conjecture,\n"
  "    ( ?[X]: ( in_denotation(X, europe, isPartOf)\n"
  "            & in_denotation(X, easternEurope, isPartOf) )\n"
  "    & ![Y]: ~( in_denotation(Y, westernEurope, isPartOf)\n"
  "             & in_denotation(Y, easternEurope, isPartOf) )\n"
  "    & ![Z]: ~( in_denotation(Z, germany, eq)\n"
  "             & in_denotation(Z, easternEurope, isPartOf) ) )).",
  inc=("GEO", "ODRL"),
  pl="4-policy spoiler: Compatible(A,D) ∧ Conflict(B,D) ∧ Conflict(C,D)")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 16: N-WAY COMPOSED POLICIES (ODRL170–175)
# Combines Categories 12 (large composition) + 15 (n-way): 3–4 policies,
# each with 2–3 operands (spatial + purpose + language).
#
# Tests: Does Theorem 2 (operand composition) scale to N-way interactions?
# Key: one Conflict operand suffices for composed Conflict (Theorem 2),
# so multi-dim N-way can short-circuit on a single dimension.
# ═══════════════════════════════════════════════════════════════════════════

# 170: 3-Policy Multi-Dim All Compatible
#   A: permission, spatial isPartOf(europe), purpose isA(R&D)
#   B: prohibition, spatial eq(germany), purpose isA(academicResearch)
#   C: prohibition, spatial isPartOf(westernEurope), purpose isA(R&D)
#
#   A∩B: spatial(europe∩de=de) ∧ purpose(R&D∩acR=acR) → Compatible
#   A∩C: spatial(europe∩wE=wE) ∧ purpose(R&D∩R&D=R&D) → Compatible
#   B∩C: spatial(de∩wE=de) ∧ purpose(acR∩R&D=acR) → Compatible
P("ODRL170-1.p", "Theorem", "Compatible",
  "N-Way Composed — 3 Policies All Compatible (Spatial + Purpose)", "Very Hard",
  tp("policyA", "permission", "use", [
      ("spatial", "isPartOf", "geo:europe"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("spatial", "eq", "geo:germany"),
      ("hasPurpose", "isA", "dpv:AcademicResearch")
  ]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:westernEurope"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment")
  ]),
  "3-way multi-dim: all 3 pairs compatible on BOTH dimensions.\n"
  "%   A∩B: spatial(europe∩germany=germany) ∧ purpose(R&D∩academic=academic) → Compatible\n"
  "%   A∩C: spatial(europe∩wE=wE) ∧ purpose(R&D∩R&D=R&D) → Compatible\n"
  "%   B∩C: spatial(germany∩wE=germany) ∧ purpose(academic∩R&D=academic) → Compatible\n"
  "%   Witness sets: (germany, academicResearch) for all pairs",
  "fof(odrl170, conjecture,\n"
  "    ( ?[Xs,Xp]: ( in_denotation(Xs, europe, isPartOf)\n"
  "                & in_denotation(Xs, germany, eq)\n"
  "                & in_denotation(Xp, researchAndDevelopment, isA)\n"
  "                & in_denotation(Xp, academicResearch, isA) )\n"
  "    & ?[Ys,Yp]: ( in_denotation(Ys, europe, isPartOf)\n"
  "                & in_denotation(Ys, westernEurope, isPartOf)\n"
  "                & in_denotation(Yp, researchAndDevelopment, isA)\n"
  "                & in_denotation(Yp, researchAndDevelopment, isA) )\n"
  "    & ?[Zs,Zp]: ( in_denotation(Zs, germany, eq)\n"
  "                & in_denotation(Zs, westernEurope, isPartOf)\n"
  "                & in_denotation(Zp, academicResearch, isA)\n"
  "                & in_denotation(Zp, researchAndDevelopment, isA) ) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("GEO", "ODRL"),
  pl="3-policy multi-dim: all pairs Compatible on spatial+purpose")

# 171: Non-Transitive Multi-Dim
#   A: permission, spatial isPartOf(westernEurope), purpose isA(R&D)
#   B: prohibition, spatial isPartOf(europe), purpose isA(academicResearch)
#   C: prohibition, spatial isPartOf(easternEurope), purpose isA(commercialResearch)
#
#   A∩B: spatial(wE∩europe=wE ✓) ∧ purpose(R&D∩acR=acR ✓) → Compatible
#   B∩C: spatial(europe∩eE=eE ✓) ∧ purpose(acR∩cR: both ≤ R&D, witness cR ✓) → Compatible
#   A∩C: spatial(wE⊥eE = ∅) → Conflict (Thm 2: one dimension suffices)
#
#   Key: non-transitivity persists even with multi-operand composition.
P("ODRL171-1.p", "Theorem", "NonTransitive",
  "N-Way Composed — Non-Transitive on ONE Dimension", "Very Hard",
  tp("policyA", "permission", "use", [
      ("spatial", "isPartOf", "geo:westernEurope"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:europe"),
      ("hasPurpose", "isA", "dpv:AcademicResearch")
  ]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:easternEurope"),
      ("hasPurpose", "isA", "dpv:CommercialResearch")
  ]),
  "Non-transitivity in multi-dimensional space:\n"
  "%   A∩B: spatial(wE∩europe=wE) ∧ purpose(R&D∩acR=acR) → Compatible\n"
  "%   B∩C: spatial(europe∩eE=eE) ∧ purpose(acR∩cR: both ≤ R&D) → Compatible\n"
  "%   A∩C: spatial(wE⊥eE=∅) → Conflict (Thm 2: one conflict dimension suffices)\n"
  "%   Shows: Compatible(A,B) ∧ Compatible(B,C) ⊬ Compatible(A,C) even with multi-operand",
  "fof(odrl171, conjecture,\n"
  "    ( ?[Xs,Xp]: ( in_denotation(Xs, westernEurope, isPartOf)\n"
  "                & in_denotation(Xs, europe, isPartOf)\n"
  "                & in_denotation(Xp, researchAndDevelopment, isA)\n"
  "                & in_denotation(Xp, academicResearch, isA) )\n"
  "    & ?[Ys,Yp]: ( in_denotation(Ys, europe, isPartOf)\n"
  "                & in_denotation(Ys, easternEurope, isPartOf)\n"
  "                & in_denotation(Yp, academicResearch, isA)\n"
  "                & in_denotation(Yp, commercialResearch, isA) )\n"
  "    & ![Zs]: ~( in_denotation(Zs, westernEurope, isPartOf)\n"
  "              & in_denotation(Zs, easternEurope, isPartOf) ) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("GEO", "ODRL"),
  pl="Non-transitive multi-dim: spatial conflict breaks transitivity")

# 172: 3-Policy Mutual Exclusion Multi-Dim
#   A: permission, spatial isPartOf(germany), purpose isA(commercialPurpose)
#   B: prohibition, spatial isPartOf(france), purpose isA(serviceProvision)
#   C: prohibition, spatial isPartOf(poland), purpose isA(serviceProvision)
#
#   Spatial: de⊥fr, de⊥pl, fr⊥pl — all 3 pairs disjoint.
#   By Theorem 2, spatial Conflict alone suffices → composed Conflict for all pairs.
#
#   NOTE: Purpose is NOT mutually exclusive for all 3 pairs in DAG-safe:
#   cP⊥sP ✓, but cP is NOT disjoint from sP for the B∩C pair (both have sP).
#   B∩C purpose: sP∩sP = sP (trivially compatible).
#   However spatial kills ALL pairs regardless of purpose.
P("ODRL172-1.p", "Theorem", "Conflict",
  "N-Way Composed — 3-Policy Mutual Exclusion (Spatial Suffices)", "Very Hard",
  tp("policyA", "permission", "use", [
      ("spatial", "isPartOf", "geo:germany"),
      ("hasPurpose", "isA", "dpv:CommercialPurpose")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:france"),
      ("hasPurpose", "isA", "dpv:ServiceProvision")
  ]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:poland"),
      ("hasPurpose", "isA", "dpv:ServiceProvision")
  ]),
  "3-way mutual exclusion via spatial (Theorem 2 short-circuit):\n"
  "%   Spatial: de⊥fr, de⊥pl, fr⊥pl → all 3 pairs Conflict\n"
  "%   By Theorem 2: AND(spatial=Conflict, purpose=any) = Conflict\n"
  "%   Purpose operand irrelevant — spatial suffices for all pairs.\n"
  "%   Tests: Theorem 2 short-circuit in N-way composed context.",
  "fof(odrl172, conjecture,\n"
  "    ( ![X]: ~( in_denotation(X, germany, isPartOf)\n"
  "             & in_denotation(X, france, isPartOf) )\n"
  "    & ![Y]: ~( in_denotation(Y, germany, isPartOf)\n"
  "             & in_denotation(Y, poland, isPartOf) )\n"
  "    & ![Z]: ~( in_denotation(Z, france, isPartOf)\n"
  "             & in_denotation(Z, poland, isPartOf) ) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("GEO", "ODRL"),
  pl="3-policy mutual exclusion: spatial conflict suffices (Thm 2)")

# 173: 3-Operand × 3-Policy — maximum pairwise complexity
#   A: permission, spatial isPartOf(europe), purpose isA(R&D), language isPartOf(en)
#   B: prohibition, spatial eq(germany), purpose isA(acR), language eq(enGB)
#   C: prohibition, spatial isPartOf(wE), purpose isA(R&D), language isPartOf(en)
#
#   9 pairwise operand checks (3 pairs × 3 operands), all Compatible.
P("ODRL173-1.p", "Theorem", "Compatible",
  "N-Way Composed — 3 Operands × 3 Policies", "Very Hard",
  tp("policyA", "permission", "use", [
      ("spatial", "isPartOf", "geo:europe"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment"),
      ("language", "isPartOf", "lang:en")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("spatial", "eq", "geo:germany"),
      ("hasPurpose", "isA", "dpv:AcademicResearch"),
      ("language", "eq", "lang:enGB")
  ]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:westernEurope"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment"),
      ("language", "isPartOf", "lang:en")
  ]),
  "Maximum complexity: 3 operands × 3 policies = 9 pairwise operand checks.\n"
  "%   Tests: Vampire's ability to find witnesses across 3 dimensions and 3 policies.\n"
  "%   All 3 pairs compatible on all 3 dimensions.",
  "fof(odrl173, conjecture,\n"
  "    ( ?[Xs,Xp,Xl]: ( in_denotation(Xs, europe, isPartOf)\n"
  "                   & in_denotation(Xs, germany, eq)\n"
  "                   & in_denotation(Xp, researchAndDevelopment, isA)\n"
  "                   & in_denotation(Xp, academicResearch, isA)\n"
  "                   & in_denotation(Xl, en, isPartOf)\n"
  "                   & in_denotation(Xl, enGB, eq) )\n"
  "    & ?[Ys,Yp,Yl]: ( in_denotation(Ys, europe, isPartOf)\n"
  "                   & in_denotation(Ys, westernEurope, isPartOf)\n"
  "                   & in_denotation(Yp, researchAndDevelopment, isA)\n"
  "                   & in_denotation(Yp, researchAndDevelopment, isA)\n"
  "                   & in_denotation(Yl, en, isPartOf)\n"
  "                   & in_denotation(Yl, en, isPartOf) )\n"
  "    & ?[Zs,Zp,Zl]: ( in_denotation(Zs, germany, eq)\n"
  "                   & in_denotation(Zs, westernEurope, isPartOf)\n"
  "                   & in_denotation(Zp, academicResearch, isA)\n"
  "                   & in_denotation(Zp, researchAndDevelopment, isA)\n"
  "                   & in_denotation(Zl, enGB, eq)\n"
  "                   & in_denotation(Zl, en, isPartOf) ) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("GEO", "DPV", "LANG", "ODRL"),
  pl="3-operand × 3-policy: maximum complexity, all pairs Compatible")

# 174: 4-Policy One Spoiler Multi-Dim
#   A: permission, spatial isPartOf(europe), purpose isA(R&D)
#   B: permission, spatial isPartOf(westernEurope), purpose isA(academicResearch)
#   C: permission, spatial eq(germany), purpose isA(commercialResearch)
#   D: prohibition, spatial isPartOf(easternEurope), purpose isA(R&D)
#
#   A∩D: spatial(europe∩eE=eE ✓) ∧ purpose(R&D∩R&D=R&D ✓) → Compatible
#   B∩D: spatial(wE⊥eE=∅) → Conflict (Thm 2: spatial suffices)
#   C∩D: spatial(de⊥eE=∅, de ≤ wE, wE⊥eE) → Conflict
#
#   NOTE: Purpose(A)=R&D=Purpose(D), so purpose is trivially compatible for A∩D.
#   D's spatial (eE) is the spoiler — only breaks policies in western Europe.
P("ODRL174-1.p", "Theorem", "MixedNWay",
  "N-Way Composed — 4-Policy Spoiler on Spatial Dimension", "Very Hard",
  tp("policyA", "permission", "use", [
      ("spatial", "isPartOf", "geo:europe"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment")
  ]) + "\n%\n%   " +
  tp("policyB", "permission", "use", [
      ("spatial", "isPartOf", "geo:westernEurope"),
      ("hasPurpose", "isA", "dpv:AcademicResearch")
  ]) + "\n%\n%   " +
  tp("policyC", "permission", "use", [
      ("spatial", "eq", "geo:germany"),
      ("hasPurpose", "isA", "dpv:CommercialResearch")
  ]) + "\n%\n%   " +
  tp("policyD", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:easternEurope"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment")
  ]),
  "4-policy spoiler: D conflicts with B,C on spatial but compatible with A.\n"
  "%   Compatible(A,D): spatial(europe∩eE=eE ✓) ∧ purpose(R&D∩R&D=R&D ✓) → Compatible\n"
  "%   Conflict(B,D): spatial(wE⊥eE) → Conflict (Thm 2 short-circuit)\n"
  "%   Conflict(C,D): spatial(de⊥eE, via de≤wE, wE⊥eE) → Conflict\n"
  "%   Purpose dimension compatible everywhere — spatial spoils B,C only.",
  "fof(odrl174, conjecture,\n"
  "    ( ?[Xs,Xp]: ( in_denotation(Xs, europe, isPartOf)\n"
  "                & in_denotation(Xs, easternEurope, isPartOf)\n"
  "                & in_denotation(Xp, researchAndDevelopment, isA)\n"
  "                & in_denotation(Xp, researchAndDevelopment, isA) )\n"
  "    & ![Ys]: ~( in_denotation(Ys, westernEurope, isPartOf)\n"
  "              & in_denotation(Ys, easternEurope, isPartOf) )\n"
  "    & ![Zs]: ~( in_denotation(Zs, germany, eq)\n"
  "              & in_denotation(Zs, easternEurope, isPartOf) ) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("GEO", "ODRL"),
  pl="4-policy spoiler: spatial conflict on B,C; purpose compatible with A")

# 175: DAG Multi-Parent in N-Way Composed
#   A: permission, purpose isA(commercialPurpose), spatial isPartOf(germany)
#   B: prohibition, purpose isA(researchAndDevelopment), spatial isPartOf(europe)
#   C: prohibition, purpose isA(commercialResearch), spatial eq(germany)
#
#   commercialResearch ≤ cP [parent A] ∧ commercialResearch ≤ R&D [parent B]
#   A∩B: purpose(cP∩R&D: witness=cR, DAG-safe!) ∧ spatial(de∩europe=de) → Compatible
#   A∩C: purpose(cP∩cR: cR≤cP → cR) ∧ spatial(de∩de) → Compatible
#   B∩C: purpose(R&D∩cR: cR≤R&D → cR) ∧ spatial(europe∩de=de) → Compatible
#   Witness: (commercialResearch, germany) for all 3 pairs!
P("ODRL175-1.p", "Theorem", "Compatible",
  "N-Way Composed — DAG Multi-Parent Across 3 Policies", "Very Hard",
  tp("policyA", "permission", "use", [
      ("hasPurpose", "isA", "dpv:CommercialPurpose"),
      ("spatial", "isPartOf", "geo:germany")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment"),
      ("spatial", "isPartOf", "geo:europe")
  ]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [
      ("hasPurpose", "isA", "dpv:CommercialResearch"),
      ("spatial", "eq", "geo:germany")
  ]),
  "3-way with DAG multi-parent: commercialResearch ≤ {cP, R&D}.\n"
  "%   A∩B: purpose(cP∩R&D via cR) ∧ spatial(germany∩europe=germany) → Compatible\n"
  "%   A∩C: purpose(cP∩cR via leq) ∧ spatial(germany∩germany) → Compatible\n"
  "%   B∩C: purpose(R&D∩cR via leq) ∧ spatial(europe∩germany) → Compatible\n"
  "%   Witness: (commercialResearch, germany) for all pairs\n"
  "%   Tests: DAG-safe multi-parent in N-way composed context",
  "fof(odrl175, conjecture,\n"
  "    ( ?[Xp,Xs]: ( in_denotation(Xp, commercialPurpose, isA)\n"
  "                & in_denotation(Xp, researchAndDevelopment, isA)\n"
  "                & in_denotation(Xs, germany, isPartOf)\n"
  "                & in_denotation(Xs, europe, isPartOf) )\n"
  "    & ?[Yp,Ys]: ( in_denotation(Yp, commercialPurpose, isA)\n"
  "                & in_denotation(Yp, commercialResearch, isA)\n"
  "                & in_denotation(Ys, germany, isPartOf)\n"
  "                & in_denotation(Ys, germany, eq) )\n"
  "    & ?[Zp,Zs]: ( in_denotation(Zp, researchAndDevelopment, isA)\n"
  "                & in_denotation(Zp, commercialResearch, isA)\n"
  "                & in_denotation(Zs, europe, isPartOf)\n"
  "                & in_denotation(Zs, germany, eq) ) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("GEO", "ODRL"),
  pl="DAG multi-parent in 3-way: cR witnesses all pairs")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 20: XONE & SYMMETRIC DIFFERENCE (ODRL230–237)
#
# XONE at denotation level = symmetric difference: D₁ △ D₂ ≠ ∅
# ∃X: (X ∈ D₁ ∧ X ∉ D₂) ∨ (X ∉ D₁ ∧ X ∈ D₂)
#
# KEY CHALLENGE: proving ~in_denotation (negative reasoning)
# Negative proof path for ~in_denotation(X, G, isPartOf):
#   1. Assume in_denotation(X, G, isPartOf) → leq(X, G)  [den_onlyif]
#   2. From disjointness: disjoint(A, B) ∧ leq(X, A) ∧ leq(X, G) → ...
#   3. disj_downward → disjoint(X, X)
#   4. disj_irrefl → ⊥  → therefore ~in_denotation(X, G, isPartOf)
#
# This is genuinely hard for ATPs: proof by contradiction with chain reasoning.
# ═══════════════════════════════════════════════════════════════════════════

# 230: Basic 2-way XONE — disjoint siblings
#   isPartOf(de) △ isPartOf(fr)
#   de ⊥ fr [siblings under wE, directly asserted]
#   Witness: germany (∈ ↓de, ∉ ↓fr)
#   Negative proof: in_den(de,fr,isPO) → leq(de,fr) → disj_downward(de,fr,de,de) → disj(de,de) → ⊥
P("ODRL230-1.p", "Theorem", "XONESuccess",
  "XONE — Basic Symmetric Difference (Disjoint Siblings)", "Very Hard",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:germany")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:france")]),
  "XONE: ∃X in exactly one of ↓de, ↓fr (symmetric difference).\n"
  "%   Witness: germany ∈ ↓de ∧ germany ∉ ↓fr.\n"
  "%   Negative proof: leq(de,fr) → disj_downward(de,fr,de,de) → disj(de,de) → ⊥\n"
  "%   Tests: ATP proof by contradiction for negative denotation membership.",
  "fof(odrl230, conjecture,\n"
  "    ?[X]: ( ( in_denotation(X, germany, isPartOf)\n"
  "            & ~in_denotation(X, france, isPartOf) )\n"
  "          | ( ~in_denotation(X, germany, isPartOf)\n"
  "            & in_denotation(X, france, isPartOf) ) )).",
  inc=("GEO", "ODRL"),
  pl="XONE: ↓de △ ↓fr ≠ ∅ via sibling disjointness")

# 231: XONE via derived disjointness — cross-region
#   isPartOf(de) △ isPartOf(pl)
#   de ≤ wE, pl ≤ eE, wE ⊥ eE → disj_downward → de ⊥ pl [DERIVED, not direct]
#   Witness: germany (∈ ↓de, ∉ ↓pl)
#   Harder than 230: negative proof requires derived disjointness chain.
P("ODRL231-1.p", "Theorem", "XONESuccess",
  "XONE — Symmetric Difference (Derived Disjointness)", "Very Hard",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:germany")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:poland")]),
  "XONE via derived disjointness:\n"
  "%   de ≤ wE, pl ≤ eE, disjoint(wE,eE)\n"
  "%   → disj_downward → disjoint(de, pl) [derived, not asserted]\n"
  "%   Witness: germany ∈ ↓de ∧ germany ∉ ↓pl.\n"
  "%   Harder: negative proof requires multi-step derivation chain.",
  "fof(odrl231, conjecture,\n"
  "    ?[X]: ( ( in_denotation(X, germany, isPartOf)\n"
  "            & ~in_denotation(X, poland, isPartOf) )\n"
  "          | ( ~in_denotation(X, germany, isPartOf)\n"
  "            & in_denotation(X, poland, isPartOf) ) )).",
  inc=("GEO", "ODRL"),
  pl="XONE: ↓de △ ↓pl ≠ ∅ via derived disjointness (wE⊥eE)")

# 232: 3-way XONE — exactly one of three mutually disjoint
#   de, fr, pl: pairwise disjoint
#   ∃X: exactly one of {↓de, ↓fr, ↓pl} contains X
#   Witness: germany (∈ ↓de, ∉ ↓fr, ∉ ↓pl)
#   Requires 2 negative proofs per disjunct. With 3 disjuncts → 6 potential negative proofs.
P("ODRL232-1.p", "Theorem", "XONEThreeWay",
  "XONE — 3-Way Exactly-One (Mutual Exclusion)", "Extreme",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:germany")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:france")]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [("spatial", "isPartOf", "geo:poland")]),
  "3-way XONE: ∃X in exactly one of {↓de, ↓fr, ↓pl}.\n"
  "%   de ⊥ fr [sibling], de ⊥ pl [derived wE⊥eE], fr ⊥ pl [derived wE⊥eE]\n"
  "%   Witness: germany (∈ ↓de, ∉ ↓fr, ∉ ↓pl)\n"
  "%   Requires: 1 positive proof + 2 negative proofs (contradiction chains).\n"
  "%   Tests: 3-way symmetric difference with mixed direct/derived disjointness.",
  "fof(odrl232, conjecture,\n"
  "    ?[X]: ( ( in_denotation(X, germany, isPartOf)\n"
  "            & ~in_denotation(X, france, isPartOf)\n"
  "            & ~in_denotation(X, poland, isPartOf) )\n"
  "          | ( ~in_denotation(X, germany, isPartOf)\n"
  "            & in_denotation(X, france, isPartOf)\n"
  "            & ~in_denotation(X, poland, isPartOf) )\n"
  "          | ( ~in_denotation(X, germany, isPartOf)\n"
  "            & ~in_denotation(X, france, isPartOf)\n"
  "            & in_denotation(X, poland, isPartOf) ) )).",
  inc=("GEO", "ODRL"),
  pl="3-way XONE: exactly one of {↓de, ↓fr, ↓pl}")

# 233: XONE failure — DAG-safe suppression prevents proof
#   isA(cP) △ isA(R&D) with DAG-safe KB
#   DAG-safe suppresses disjoint(cP, R&D) → ~leq(cP, R&D) is UNPROVABLE
#   Model A: leq(cP, R&D) = false → acR is XONE witness → conjecture TRUE
#   Model B: leq(cP, R&D) = true  → cP ∈ ↓R&D, ↓cP ⊆ ↓R&D → no XONE → conjecture FALSE
#   Both models consistent with axioms → CounterSatisfiable
#
#   This is THE motivating example for XONE + DAG:
#   suppressed disjointness creates logical ambiguity the prover cannot resolve.
P("ODRL233-1.p", "CounterSatisfiable", "XONEFailure",
  "XONE Failure — DAG-Safe Suppression Blocks Proof", "Very Hard",
  tp("policyA", "permission", "use", [("hasPurpose", "isA", "dpv:CommercialPurpose")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("hasPurpose", "isA", "dpv:ResearchAndDevelopment")]),
  "XONE fails: DAG-safe suppresses disjoint(cP, R&D).\n"
  "%   Without disjointness, ~leq(cP, R&D) is unprovable.\n"
  "%   Model A: leq(cP,R&D)=false → acR is XONE witness → conjecture TRUE\n"
  "%   Model B: leq(cP,R&D)=true  → ↓cP ⊆ ↓R&D → no XONE → conjecture FALSE\n"
  "%   Both consistent → CounterSatisfiable (prover cannot decide).\n"
  "%   Tests: DAG-safe suppression creates irreducible ambiguity for XONE.",
  "fof(odrl233, conjecture,\n"
  "    ?[X]: ( ( in_denotation(X, commercialPurpose, isA)\n"
  "            & ~in_denotation(X, researchAndDevelopment, isA) )\n"
  "          | ( ~in_denotation(X, commercialPurpose, isA)\n"
  "            & in_denotation(X, researchAndDevelopment, isA) ) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("ODRL",),
  pl="XONE failure: DAG-safe suppresses cP⊥R&D → proof blocked")

# 234: XONE + isNoneOf — set negation interacts with XONE
#   isNoneOf({wE}) △ isPartOf(eE)
#   isNoneOf({wE}) = {X : concept(X) ∧ ¬leq(X, wE)}
#   isPartOf(eE) = {X : leq(X, eE)}
#
#   Second disjunct (X ∈ ↓wE ∧ X ∈ ↓eE): impossible (wE ⊥ eE)
#   First disjunct (X ∉ ↓wE ∧ X ∉ ↓eE):
#     Witness: europe (not ≤ wE, not ≤ eE)
#     ~leq(europe, wE): assume leq → leq(eE, europe) → leq(eE, wE) → disj(eE,eE) → ⊥
#     ~leq(europe, eE): assume leq → leq(wE, europe) → leq(wE, eE) → disj(wE,wE) → ⊥
P("ODRL234-1.p", "Theorem", "XONESetOp",
  "XONE + isNoneOf — Set Negation × Symmetric Difference", "Extreme",
  tp("policyA", "permission", "use", [("spatial", "isNoneOf", "( geo:westernEurope )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:easternEurope")]),
  "XONE: isNoneOf({wE}) △ isPartOf(eE)\n"
  "%   Second disjunct (X ≤ wE ∧ X ≤ eE): impossible (wE ⊥ eE)\n"
  "%   First disjunct: ∃X: X ∉ ↓wE ∧ X ∉ ↓eE\n"
  "%   Witness: europe (~leq(europe,wE) via eE-collapse, ~leq(europe,eE) via wE-collapse)\n"
  "%   Tests: XONE with set-theoretic complement (isNoneOf) + negative root reasoning.",
  "fof(odrl234, conjecture,\n"
  "    ?[X]: ( ( in_denotation_set(X, noneList234, isNoneOf)\n"
  "            & ~in_denotation(X, easternEurope, isPartOf) )\n"
  "          | ( ~in_denotation_set(X, noneList234, isNoneOf)\n"
  "            & in_denotation(X, easternEurope, isPartOf) ) )).",
  extra=(
      "fof(list_234_1, axiom, in_value_list(westernEurope, noneList234)).\n" +
      generate_list_closure("noneList234", ["westernEurope"])
  ),
  inc=("GEO", "ODRL"),
  pl="XONE: isNoneOf({wE}) △ isPartOf(eE), witness = europe (root)")

# 235: XONE + 2-hop alignment — cross-dataspace symmetric difference
#   isPartOf(zoneWest) △ isPartOf(zoneEast)
#   Disjointness derived via 2-hop alignment: GEO → ISO → SYNTH
#   GEO: disj(wE,eE) → disj(de,pl) → Hop 1: disj(dE,pL) → Hop 2: disj(zoneWest,zoneEast)
#   Once disj(zoneWest,zoneEast) is derived, XONE proof follows.
#   Witness: zoneWest (∈ ↓zoneWest, ∉ ↓zoneEast)
P("ODRL235-1.p", "Theorem", "XONEAligned",
  "XONE + 2-Hop Alignment — Cross-Dataspace Symmetric Difference", "Extreme",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "synth:zoneWest")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "synth:zoneEast")]),
  "XONE via 2-hop alignment:\n"
  "%   GEO: disj(wE,eE) → disj_downward → disj(de,pl)\n"
  "%   Hop 1: align(de,dE) + align(pl,pL) → disj(dE,pL)\n"
  "%   Hop 2: align(dE,zoneWest) + align(pL,zoneEast) → disj(zoneWest,zoneEast)\n"
  "%   → ~leq(zoneWest, zoneEast) → ~in_den(zoneWest, zoneEast, isPartOf)\n"
  "%   Witness: zoneWest. Tests: XONE proof requires alignment + disjointness chain.",
  "fof(odrl235, conjecture,\n"
  "    ?[X]: ( ( in_denotation(X, zoneWest, isPartOf)\n"
  "            & ~in_denotation(X, zoneEast, isPartOf) )\n"
  "          | ( ~in_denotation(X, zoneWest, isPartOf)\n"
  "            & in_denotation(X, zoneEast, isPartOf) ) )).",
  extra=SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH,
  inc=("GEO", "ISO", "ALIGN_DATA", "ODRL", "ALIGN_THEORY"),
  pl="XONE: zoneWest △ zoneEast via 2-hop alignment chain")

# 236: XONE all-pairs verdict matrix — 3 concepts, all XONE pairs in one conjecture
#   de, fr, pl: pairwise XONE (symmetric difference non-empty for each pair)
#   Proves: de△fr ≠ ∅ ∧ de△pl ≠ ∅ ∧ fr△pl ≠ ∅
#   Each pair needs a witness + negative proof → 3 × 2 = 6 total sub-goals.
P("ODRL236-1.p", "Theorem", "XONEMatrix",
  "XONE All-Pairs Matrix — 3 Concepts, All Pairs", "Extreme",
  tp("policyA", "permission", "use", [("spatial", "isPartOf", "geo:germany")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isPartOf", "geo:france")]) + "\n%\n%   " +
  tp("policyC", "prohibition", "use", [("spatial", "isPartOf", "geo:poland")]),
  "XONE all-pairs: prove symmetric difference non-empty for ALL C(3,2) = 3 pairs.\n"
  "%   de△fr ≠ ∅ [witness: germany, de ⊥ fr sibling]\n"
  "%   de△pl ≠ ∅ [witness: germany, de ⊥ pl derived]\n"
  "%   fr△pl ≠ ∅ [witness: france, fr ⊥ pl derived]\n"
  "%   3 witnesses, 6 negative proofs → massive proof obligation.",
  "fof(odrl236, conjecture,\n"
  "    ( ?[X1]: ( ( in_denotation(X1, germany, isPartOf)\n"
  "               & ~in_denotation(X1, france, isPartOf) )\n"
  "             | ( ~in_denotation(X1, germany, isPartOf)\n"
  "               & in_denotation(X1, france, isPartOf) ) )\n"
  "    & ?[X2]: ( ( in_denotation(X2, germany, isPartOf)\n"
  "               & ~in_denotation(X2, poland, isPartOf) )\n"
  "             | ( ~in_denotation(X2, germany, isPartOf)\n"
  "               & in_denotation(X2, poland, isPartOf) ) )\n"
  "    & ?[X3]: ( ( in_denotation(X3, france, isPartOf)\n"
  "               & ~in_denotation(X3, poland, isPartOf) )\n"
  "             | ( ~in_denotation(X3, france, isPartOf)\n"
  "               & in_denotation(X3, poland, isPartOf) ) ) )).",
  inc=("GEO", "ODRL"),
  pl="XONE matrix: all C(3,2)=3 pairwise symmetric diffs non-empty")

# 237: XONE + multi-dimensional — spatial XONE with purpose compatibility
#   Two policies, each with 2 operands:
#   A: spatial isPartOf(germany), purpose isA(R&D)
#   B: spatial isPartOf(france), purpose isA(R&D)
#
#   Spatial: de △ fr ≠ ∅ (XONE — disjoint siblings)
#   Purpose: R&D ∩ R&D = R&D (trivially compatible — same denotation)
#
#   Combined: spatial has XONE pattern, purpose has overlap.
#   Proves both simultaneously: spatial XONE + purpose compatible.
#   Tests: interaction of XONE on one dimension with compatibility on another.
P("ODRL237-1.p", "Theorem", "XONEMultiDim",
  "XONE Multi-Dimensional — Spatial XONE × Purpose Compatible", "Extreme",
  tp("policyA", "permission", "use", [
      ("spatial", "isPartOf", "geo:germany"),
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment")
  ]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [
      ("spatial", "isPartOf", "geo:france"),
      ("hasPurpose", "isA", "dpv:AcademicResearch")
  ]),
  "XONE multi-dim: spatial XONE × purpose compatible.\n"
  "%   Spatial: de △ fr ≠ ∅ [XONE — disjoint siblings]\n"
  "%   Purpose: R&D ∩ acR = acR ≠ ∅ [Compatible — acR ≤ R&D]\n"
  "%   Combined conjecture proves both: spatial asymmetry + purpose overlap.\n"
  "%   Tests: XONE on one operand + compatibility on another in single formula.",
  "fof(odrl237, conjecture,\n"
  "    ( ?[Xs]: ( ( in_denotation(Xs, germany, isPartOf)\n"
  "               & ~in_denotation(Xs, france, isPartOf) )\n"
  "             | ( ~in_denotation(Xs, germany, isPartOf)\n"
  "               & in_denotation(Xs, france, isPartOf) ) )\n"
  "    & ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n"
  "             & in_denotation(Xp, academicResearch, isA) ) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("GEO", "ODRL"),
  pl="XONE+multi-dim: spatial(de△fr) × purpose(R&D∩acR)")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 21: OPERATOR MONOTONICITY (ODRL250–254)
#
# Tests meta-properties of ODRL operators w.r.t. the KB hierarchy.
#
#   Monotone:      leq(A,B) → ⟦op(A)⟧ ⊆ ⟦op(B)⟧    (isPartOf, isA)
#   Anti-monotone:  leq(A,B) → ⟦op(B)⟧ ⊆ ⟦op(A)⟧    (hasPart, isNoneOf)
#   Non-monotone:   Neither direction holds            (eq, neq)
#
# These are universally quantified theorems about ALL concept pairs,
# not just specific instances like ODRL122. They push ATPs because
# the prover must reason about arbitrary concepts, not ground terms.
# ═══════════════════════════════════════════════════════════════════════════

# 250: isPartOf is monotone — THE fundamental denotation property
#   ∀A,B,X: leq(A,B) → (in_den(X,A,isPartOf) → in_den(X,B,isPartOf))
#   Proof: in_den(X,A,isPartOf) → leq(X,A) [den_onlyif]
#          leq(X,A) ∧ leq(A,B) → leq(X,B) [leq_trans]
#          leq(X,B) → in_den(X,B,isPartOf) [den_if]
P("ODRL250-1.p", "Theorem", "Monotone",
  "Lemma 2 (universal) — isPartOf Monotonicity", "Hard",
  "(Meta-property: no ODRL policy — operator characterization)",
  "∀A,B,X: leq(A,B) → (in_den(X,A,isPartOf) → in_den(X,B,isPartOf))\n"
  "%   Proof chain: den_isPartOf_onlyif → leq_trans → den_isPartOf_if\n"
  "%   Tests: universally quantified operator property over arbitrary concepts.",
  "fof(odrl250, conjecture,\n"
  "    ![A,B,X]: (\n"
  "        (leq(A, B) & in_denotation(X, A, isPartOf))\n"
  "      => in_denotation(X, B, isPartOf) )).",
  inc=("GEO", "ODRL"),
  pl="isPartOf monotonicity: leq(A,B) → ↓A ⊆ ↓B (universal)")

# 251: hasPart is anti-monotone
#   ∀A,B,X: leq(A,B) → (in_den(X,B,hasPart) → in_den(X,A,hasPart))
#   Proof: in_den(X,B,hasPart) → leq(B,X) [den_onlyif]
#          leq(A,B) ∧ leq(B,X) → leq(A,X) [leq_trans]
#          leq(A,X) → in_den(X,A,hasPart) [den_if]
#   Note: direction REVERSES — smaller concept has LARGER hasPart denotation.
P("ODRL251-1.p", "Theorem", "AntiMonotone",
  "Lemma 2 (universal) — hasPart Anti-Monotonicity", "Hard",
  "(Meta-property: no ODRL policy — operator characterization)",
  "∀A,B,X: leq(A,B) → (in_den(X,B,hasPart) → in_den(X,A,hasPart))\n"
  "%   Proof chain: den_hasPart_onlyif → leq_trans → den_hasPart_if\n"
  "%   Direction reverses: A ≤ B → ↑B ⊆ ↑A (smaller concept, more ancestors).\n"
  "%   Tests: anti-monotone reasoning with universally quantified hasPart.",
  "fof(odrl251, conjecture,\n"
  "    ![A,B,X]: (\n"
  "        (leq(A, B) & in_denotation(X, B, hasPart))\n"
  "      => in_denotation(X, A, hasPart) )).",
  inc=("GEO", "ODRL"),
  pl="hasPart anti-monotonicity: leq(A,B) → ↑B ⊆ ↑A (universal)")

# 252: isNoneOf is anti-monotone (concrete instance with set ops)
#   leq(germany, westernEurope)
#   → isNoneOf({westernEurope}) ⊆ isNoneOf({germany})
#   "If X is outside wE, then X is also outside germany."
#   Proof (contrapositive of isPartOf monotonicity):
#     in_den_set(X, listWE, isNoneOf) → concept(X) ∧ ¬leq(X, wE)
#     Contrapositive of mono: if leq(X, de) → leq(X, wE)
#     So ¬leq(X, wE) → ¬leq(X, de) → in_den_set(X, listDE, isNoneOf)
P("ODRL252-1.p", "Theorem", "AntiMonotone",
  "Corollary — isNoneOf Anti-Monotonicity (Concrete)", "Very Hard",
  tp("policyA", "permission", "use", [("spatial", "isNoneOf", "( geo:westernEurope )")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "isNoneOf", "( geo:germany )")]),
  "isNoneOf anti-monotonicity: leq(de, wE) → isNoneOf({wE}) ⊆ isNoneOf({de})\n"
  "%   Contrapositive of isPartOf monotonicity.\n"
  "%   ∀X: (concept(X) ∧ ¬leq(X,wE)) → (concept(X) ∧ ¬leq(X,de))\n"
  "%   Tests: negation + set operator + hierarchy reasoning combined.",
  "fof(odrl252, conjecture,\n"
  "    ![X]: (\n"
  "        in_denotation_set(X, noneListWE252, isNoneOf)\n"
  "      => in_denotation_set(X, noneListDE252, isNoneOf) )).",
  extra=(
      "fof(list_252a, axiom, in_value_list(westernEurope, noneListWE252)).\n" +
      generate_list_closure("noneListWE252", ["westernEurope"]) + "\n"
      "fof(list_252b, axiom, in_value_list(germany, noneListDE252)).\n" +
      generate_list_closure("noneListDE252", ["germany"])
  ),
  inc=("GEO", "ODRL"),
  pl="isNoneOf anti-monotone: de ≤ wE → isNoneOf({wE}) ⊆ isNoneOf({de})")

# 253: eq is non-monotone — counterexample with negative reasoning
#   leq(bavaria, germany) but eq(bavaria) ⊄ eq(germany)
#   Witness: bavaria ∈ eq(bavaria) but bavaria ∉ eq(germany)
#   eq(bavaria) = {bavaria}, eq(germany) = {germany}
#   Negative proof: in_den(bav, de, eq) → bav = de → $distinct contradiction → ⊥
P("ODRL253-1.p", "Theorem", "NonMonotone",
  "Counterexample — eq Is Non-Monotone", "Medium",
  tp("policyA", "permission", "use", [("spatial", "eq", "geo:bavaria")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "eq", "geo:germany")]),
  "eq is non-monotone: leq(bavaria, germany) but eq(bav) ⊄ eq(de).\n"
  "%   Positive: in_den(bavaria, bavaria, eq) [den_eq_if: bav = bav]\n"
  "%   Negative: ~in_den(bavaria, germany, eq) [den_eq_onlyif: bav = de → ⊥ by UNA]\n"
  "%   Tests: proof by contradiction using UNA ($distinct) for negative membership.",
  "fof(odrl253, conjecture,\n"
  "    ?[X]: ( in_denotation(X, bavaria, eq)\n"
  "          & ~in_denotation(X, germany, eq) )).",
  inc=("GEO", "ODRL"),
  pl="eq non-monotone: bav ∈ eq(bav) ∧ bav ∉ eq(de) despite bav ≤ de")

# 254: neq is non-monotone — counterexample (reverse direction)
#   leq(bavaria, germany) but neq(bavaria) ⊄ neq(germany)
#   Witness: germany ∈ neq(bavaria) but germany ∉ neq(germany)
#   neq(bavaria) = C\{bavaria}, neq(germany) = C\{germany}
#   de ∈ neq(bav) because de ≠ bav, but de ∉ neq(de) because de = de.
P("ODRL254-1.p", "Theorem", "NonMonotone",
  "Counterexample — neq Is Non-Monotone", "Medium",
  tp("policyA", "permission", "use", [("spatial", "neq", "geo:bavaria")]) + "\n%\n%   " +
  tp("policyB", "prohibition", "use", [("spatial", "neq", "geo:germany")]),
  "neq is non-monotone: leq(bav, de) but neq(bav) ⊄ neq(de).\n"
  "%   Positive: in_den(germany, bavaria, neq) [den_neq_if: de ≠ bav by UNA]\n"
  "%   Negative: ~in_den(germany, germany, neq) [den_neq_onlyif: de ≠ de → ⊥]\n"
  "%   Tests: neq non-monotonicity via UNA-based positive + self-equality negative.",
  "fof(odrl254, conjecture,\n"
  "    ?[X]: ( in_denotation(X, bavaria, neq)\n"
  "          & ~in_denotation(X, germany, neq) )).",
  inc=("GEO", "ODRL"),
  pl="neq non-monotone: de ∈ neq(bav) ∧ de ∉ neq(de) despite bav ≤ de")


# ═══════════════════════════════════════════════════════════════════════════
# File generation engine
# ═══════════════════════════════════════════════════════════════════════════

def generate_tptp_header(p, use_flip):
    """Generate standard TPTP problem file header."""
    exp = p["exp"]
    conj_str = p["flip_conj"] if (use_flip and p["flip_conj"]) else p["conj"]

    lines = []
    lines.append("%--------------------------------------------------------------------------")
    lines.append(f"% File     : {p['fn']} : TPTP v0.1.0.")
    lines.append(f"% Domain   : ODRL Policy Conflict Detection")
    lines.append(f"% Problem  : {p['paper']}")
    lines.append(f"% Expected : {exp}")
    lines.append(f"% Verdict  : {p['vrd']}")
    lines.append(f"% Paper    : {p['paper']}")
    lines.append(f"%")
    lines.append(f"% ODRL Policy (Conceptual):")
    for ttl_line in p["ttl"].split("\n"):
        lines.append(f"%   {ttl_line}")
    lines.append(f"%")
    lines.append(f"% Formal test:")
    for den_line in p["den"].split("\n"):
        lines.append(f"%   {den_line}")
    lines.append(f"%")
    if p["pl"]:
        lines.append(f"% One-liner : {p['pl']}")
    lines.append(f"% Difficulty: {p['diff']}")
    lines.append(f"% Authors  : Mustafa, D. & Sutcliffe, G.")
    lines.append(f"% Date     : {date.today().isoformat()}")
    lines.append(f"% Gen      : gen_advanced_suite.py")
    lines.append("%--------------------------------------------------------------------------")
    lines.append("")
    return "\n".join(lines), conj_str


def generate_problem_file(p, use_flip=False):
    """Generate complete .p file content for a problem."""
    header, conj_str = generate_tptp_header(p, use_flip)

    parts = [header]

    # Include directives
    for inc_key in p["inc"]:
        if inc_key in INC:
            parts.append(INC[inc_key])
    parts.append("")

    # Inline extra axioms (test-specific KB fragments)
    if p["extra"]:
        parts.append("% ─── Problem-specific axioms ─────────────────────────────────────────")
        parts.append(p["extra"])
        parts.append("")

    # Conjecture
    parts.append("% ─── Conjecture ──────────────────────────────────────────────────────")
    parts.append(conj_str)
    parts.append("")
    parts.append("%--------------------------------------------------------------------------")

    return "\n".join(parts)


def write_problems(outdir, dry_run=False, use_flip=False):
    """Write all problem files to the output directory."""
    written = []
    for p in PROBLEMS:
        cat = problem_category(p["fn"])
        subdir = os.path.join(outdir, CAT_DIR[cat])

        if not dry_run:
            os.makedirs(subdir, exist_ok=True)

        filepath = os.path.join(subdir, p["fn"])
        content = generate_problem_file(p, use_flip=use_flip)

        if dry_run:
            print(f"  [DRY] {filepath}  ({len(content)} bytes)")
        else:
            with open(filepath, "w") as f:
                f.write(content)
            written.append(filepath)

    return written


def print_summary():
    """Print summary table of all problems."""
    print(f"\n{'Cat':<5} {'Problem':<14} {'Expected':<18} {'Verdict':<16} "
          f"{'Diff':<11} {'Includes'}")
    print("=" * 100)

    cats = {}
    for p in PROBLEMS:
        cat = problem_category(p["fn"])
        cats.setdefault(cat, []).append(p)

        incs = "+".join(p["inc"])
        has_extra = " +inline" if p["extra"] else ""
        print(f"  {cat:<3} {p['fn']:<14} {p['exp']:<18} {p['vrd']:<16} "
              f"{p['diff']:<11} {incs}{has_extra}")

    print(f"\n{'─'*50}")
    print(f"Total problems: {len(PROBLEMS)}")
    print(f"\nBy category:")
    for cat, probs in sorted(cats.items()):
        print(f"  Cat {cat} ({CAT_DIR[cat].split('/')[-1]}): {len(probs)} problems")

    # Status distribution
    statuses = {}
    for p in PROBLEMS:
        statuses[p["exp"]] = statuses.get(p["exp"], 0) + 1
    print(f"\nBy expected status:")
    for s, c in sorted(statuses.items()):
        print(f"  {s}: {c}")

    # Difficulty distribution
    diffs = {}
    for p in PROBLEMS:
        diffs[p["diff"]] = diffs.get(p["diff"], 0) + 1
    print(f"\nBy difficulty:")
    for d in ["Easy", "Medium", "Hard", "Very Hard", "Extreme"]:
        if d in diffs:
            print(f"  {d}: {diffs[d]}")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Generate TPTP problems: Categories 9–14 (advanced suite).")
    parser.add_argument("--outdir", default="Problems/ODRL",
                        help="Root output directory (default: Problems/ODRL)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be generated without writing files")
    parser.add_argument("--summary", action="store_true",
                        help="Print summary table only")
    parser.add_argument("--flip", action="store_true",
                        help="Use flipped conjectures for CounterSatisfiable→Theorem")
    args = parser.parse_args()

    if args.summary:
        print_summary()
        return

    if args.dry_run:
        print("DRY RUN — no files will be written\n")

    written = write_problems(args.outdir, dry_run=args.dry_run,
                             use_flip=args.flip)

    if not args.dry_run:
        print(f"\nWrote {len(written)} problem files:")
        for f in written:
            print(f"  {f}")

    print_summary()


if __name__ == "__main__":
    main()