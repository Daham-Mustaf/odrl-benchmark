#!/usr/bin/env python3
"""
gen_advanced_suite.py — Generate TPTP Problems: Categories 9–15.

Produces 38 .p files testing advanced reasoning patterns for ODRL
policy conflict detection in European data spaces.

Categories:
  9  — DAG Multi-Parent (ODRL100–105)       Note 1 / DAG-safety algorithm
  10 — Nested Set Operators (ODRL110–114)    isAllOf, isAnyOf, isNoneOf interaction
  11 — Quantifier Stress (ODRL120–123)       ∀∃ alternation patterns
  12 — Large-Scale Composition (ODRL130–132) Multi-operand AND / 5-way ∃
  13 — Edge Cases & Adversarial (ODRL140–145) Degenerate / pathological KBs
  14 — Multi-Hop Alignment (ODRL150–157)     2–3 hop, up to 4 dataspaces
  15 — N-Way Policy Conflicts (ODRL160–165)  3–4 policies simultaneously

Usage:
    uv run python gen_advanced_suite.py --outdir Problems/ODRL

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
}


def problem_category(fn):
    """Return category number from filename like ODRL100-1.p."""
    num = int(fn.replace("ODRL", "").replace("-1.p", ""))
    if num < 110: return 9
    if num < 120: return 10
    if num < 130: return 11
    if num < 140: return 12
    if num < 150: return 13
    if num < 160: return 14
    return 15


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
# CATEGORY 14: MULTI-HOP ALIGNMENT (ODRL150–157)
# Tests alignment composition: GEO → ISO → SYNTH → COMP (up to 4-KB chain)
#   2-hop (ODRL150–153): GEO → ISO → SYNTH
#   3-hop (ODRL154–157): GEO → ISO → SYNTH → COMP
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
  "%   B∩C: spatial(europe∩eE=eE) ∧ purpose(acR∩cR via R&D) → Compatible\n"
  "%   A∩C: spatial(wE∩eE=∅) → Conflict (Thm 2: one conflict dimension suffices)\n"
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

P("ODRL172-1.p", "Theorem", "Conflict",
  "N-Way Composed — 3-Policy Mutual Exclusion (Multi-Dim)", "Very Hard",
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
      ("hasPurpose", "isA", "dpv:ResearchAndDevelopment")
  ]),
  "3-way mutual exclusion on BOTH dimensions:\n"
  "%   Spatial: de⊥fr (siblings), de⊥pl (wE⊥eE), fr⊥pl (wE⊥eE)\n"
  "%   Purpose: cP⊥sP, cP⊥R&D (via DAG-safe), sP⊥R&D (DAG-safe)\n"
  "%   All 3 pairs conflict on BOTH dimensions → mutual exclusion",
  "fof(odrl172, conjecture,\n"
  "    ( ![X]: ~( in_denotation(X, germany, isPartOf)\n"
  "             & in_denotation(X, france, isPartOf) )\n"
  "    & ![Y]: ~( in_denotation(Y, germany, isPartOf)\n"
  "             & in_denotation(Y, poland, isPartOf) )\n"
  "    & ![Z]: ~( in_denotation(Z, france, isPartOf)\n"
  "             & in_denotation(Z, poland, isPartOf) )\n"
  "    & ![Xp]: ~( in_denotation(Xp, commercialPurpose, isA)\n"
  "               & in_denotation(Xp, serviceProvision, isA) )\n"
  "    & ![Yp]: ~( in_denotation(Yp, commercialPurpose, isA)\n"
  "               & in_denotation(Yp, researchAndDevelopment, isA) )\n"
  "    & ![Zp]: ~( in_denotation(Zp, serviceProvision, isA)\n"
  "               & in_denotation(Zp, researchAndDevelopment, isA) ) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("GEO", "ODRL"),
  pl="3-policy mutual exclusion: all pairs conflict on BOTH dimensions")

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
  pl="3-operand × 3-policy: maximum complexity test")

P("ODRL174-1.p", "Theorem", "MixedNWay",
  "N-Way Composed — 4-Policy Spoiler on One Dimension", "Very Hard",
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
      ("hasPurpose", "isA", "dpv:ServiceProvision")
  ]),
  "4-policy spoiler: D conflicts with B,C on spatial but compatible with A.\n"
  "%   Compatible(A,D): spatial(europe∩eE=eE) ∧ purpose(R&D vs sP compatible)\n"
  "%   Conflict(B,D): spatial(wE⊥eE) → conflict\n"
  "%   Conflict(C,D): spatial(germany⊥eE) → conflict\n"
  "%   Purpose dimension compatible everywhere → spatial spoils B,C only",
  "fof(odrl174, conjecture,\n"
  "    ( ?[Xs,Xp]: ( in_denotation(Xs, europe, isPartOf)\n"
  "                & in_denotation(Xs, easternEurope, isPartOf)\n"
  "                & in_denotation(Xp, researchAndDevelopment, isA)\n"
  "                & in_denotation(Xp, serviceProvision, isA) )\n"
  "    & ![Ys]: ~( in_denotation(Ys, westernEurope, isPartOf)\n"
  "              & in_denotation(Ys, easternEurope, isPartOf) )\n"
  "    & ![Zs]: ~( in_denotation(Zs, germany, eq)\n"
  "              & in_denotation(Zs, easternEurope, isPartOf) ) )).",
  extra=DPV_SAFE_FRAGMENT,
  inc=("GEO", "ODRL"),
  pl="4-policy spoiler: spatial conflict on B,C only, purpose compatible")
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
    for d in ["Easy", "Medium", "Hard", "Very Hard"]:
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