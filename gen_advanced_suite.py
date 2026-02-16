#!/usr/bin/env python3
"""
gen_advanced_suite.py — Generate TPTP Problems: Categories 9–14.

Produces 32 .p files testing advanced reasoning patterns for ODRL
policy conflict detection in European data spaces.

Categories:
  9  — DAG Multi-Parent (ODRL100–105)       Note 1 / DAG-safety algorithm
  10 — Nested Set Operators (ODRL110–114)    isAllOf, isAnyOf, isNoneOf interaction
  11 — Quantifier Stress (ODRL120–123)       ∀∃ alternation patterns
  12 — Large-Scale Composition (ODRL130–132) Multi-operand AND / 5-way ∃
  13 — Edge Cases & Adversarial (ODRL140–145) Degenerate / pathological KBs
  14 — Multi-Hop Alignment (ODRL150–157)     2–3 hop, up to 4 dataspaces

Usage:
  
    uv run python gen_advanced_suite.py --outdir Problems/ODRL          # normal
    uv run python gen_advanced_suite.py --outdir Problems/ODRL --flip   # CounterSat→Theorem
    uv run python gen_advanced_suite.py --summary                       # table only
    uv run python gen_advanced_suite.py --dry-run                       # preview


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
}


def problem_category(fn):
    """Return category number from filename like ODRL100-1.p."""
    num = int(fn.replace("ODRL", "").replace("-1.p", ""))
    if num < 110: return 9
    if num < 120: return 10
    if num < 130: return 11
    if num < 140: return 12
    if num < 150: return 13
    return 14


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

P("ODRL100-1.p", "ContradictoryAxioms", "Inconsistent",
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