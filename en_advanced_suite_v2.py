#!/usr/bin/env python3
"""
gen_advanced_suite.py — Generate (and optionally run) TPTP Problems: Categories 9–16, 20–21.
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
    uv run python gen_advanced_suite.py --outdir Problems/ODRL
    uv run python gen_advanced_suite.py --run                   # generate + run Vampire
    uv run python gen_advanced_suite.py --run --timeout 60
    uv run python gen_advanced_suite.py --run-only              # run existing files
    uv run python gen_advanced_suite.py --run --category DAGMultiParent
    uv run python gen_advanced_suite.py --dry-run
    uv run python gen_advanced_suite.py --summary

Authors: Mustafa, D. & Sutcliffe, G.
"""
import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
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
# Name → number lookup (for --category filtering)
_CAT_NAME_MAP = {v.split("/")[-1].lower(): k for k, v in CAT_DIR.items()}

def problem_category(fn):
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
# Inline KB Fragments
# ═══════════════════════════════════════════════════════════════════════════
DPV_NAIVE_FRAGMENT = """\
% --- DPV Fragment (NAIVE sibling disjointness) ---
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
fof(dpv_n_refl1, axiom, leq(purpose, purpose)).
fof(dpv_n_refl2, axiom, leq(commercialPurpose, commercialPurpose)).
fof(dpv_n_refl3, axiom, leq(researchAndDevelopment, researchAndDevelopment)).
fof(dpv_n_refl4, axiom, leq(commercialResearch, commercialResearch)).
fof(dpv_n_refl5, axiom, leq(academicResearch, academicResearch)).
fof(dpv_n_refl6, axiom, leq(serviceProvision, serviceProvision)).
fof(dpv_n_disj_PROBLEM, axiom, disjoint(commercialPurpose, researchAndDevelopment)).
fof(dpv_n_disj_safe1, axiom, disjoint(commercialPurpose, serviceProvision)).
fof(dpv_n_disj_safe2, axiom, disjoint(researchAndDevelopment, serviceProvision)).
fof(dpv_n_una, axiom,
    $distinct(purpose, commercialPurpose, researchAndDevelopment,
              commercialResearch, academicResearch, serviceProvision))."""

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
% --- Synthetic KB (SYNTH) --- NO native disjointness ---
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
% Alignment: ISO 3166 → SYNTH (regulatory zones)
fof(align_iso_synth_1, axiom, align(europe, euZone)).
fof(align_iso_synth_2, axiom, align(dE, zoneWest)).
fof(align_iso_synth_3, axiom, align(pL, zoneEast))."""

COMP_KB_NO_DISJ = """\
% --- Compliance KB (COMP) --- NO native disjointness ---
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

MINIMAL_KB_FRAGMENT = """\
% --- Minimal KB: single concept "universe" ---
fof(min_root, axiom, concept(universe)).
fof(min_refl, axiom, leq(universe, universe))."""

KB_WITNESS_SOURCE = """\
% --- Witness-Loss Source KB ---
fof(wit_src_c1, axiom, concept(witA)).
fof(wit_src_c2, axiom, concept(witB)).
fof(wit_src_c3, axiom, concept(witC)).
fof(wit_src_leq1, axiom, leq(witA, witB)).
fof(wit_src_leq2, axiom, leq(witA, witC)).
fof(wit_src_refl1, axiom, leq(witA, witA)).
fof(wit_src_refl2, axiom, leq(witB, witB)).
fof(wit_src_refl3, axiom, leq(witC, witC)).
fof(wit_src_una, axiom, $distinct(witA, witB, witC))."""

KB_WITNESS_TARGET = """\
% --- Witness-Loss Target KB (partial alignment) ---
fof(wit_tgt_c1, axiom, concept(tgtB)).
fof(wit_tgt_c2, axiom, concept(tgtC)).
fof(wit_tgt_refl1, axiom, leq(tgtB, tgtB)).
fof(wit_tgt_refl2, axiom, leq(tgtC, tgtC)).
fof(wit_tgt_una, axiom, $distinct(tgtB, tgtC))."""

KB_WITNESS_TARGET_FULL = """\
% --- Witness-Loss Target KB (downward-closed alignment) ---
fof(wit_full_c1, axiom, concept(tgtA)).
fof(wit_full_c2, axiom, concept(tgtB)).
fof(wit_full_c3, axiom, concept(tgtC)).
fof(wit_full_leq1, axiom, leq(tgtA, tgtB)).
fof(wit_full_leq2, axiom, leq(tgtA, tgtC)).
fof(wit_full_refl1, axiom, leq(tgtA, tgtA)).
fof(wit_full_refl2, axiom, leq(tgtB, tgtB)).
fof(wit_full_refl3, axiom, leq(tgtC, tgtC)).
fof(wit_full_una, axiom, $distinct(tgtA, tgtB, tgtC))."""

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 9: DAG MULTI-PARENT (ODRL100–105)
# ═══════════════════════════════════════════════════════════════════════════
P("ODRL100-1.p", "ContradictoryAxioms", "ContradictoryAxioms",
  "Note 1 — DAG Multi-Parent Contradiction (Naive)", "Medium",
  "(No ODRL policy — KB consistency test)",
  "disjoint(cP,R&D)[naive]+leq(cR,cP)∧leq(cR,R&D)→disj(cR,cR)→⊥",
  "fof(odrl100, conjecture, $false).",
  extra=DPV_NAIVE_FRAGMENT, inc=("ODRL",),
  pl="DAG inconsistency: naive sibling disj on multi-parent → ⊥")

P("ODRL101-1.p", "Theorem", "Compatible",
  "Note 1 — DAG-Safe Multi-Parent Reachability", "Easy",
  tp("policyA","permission","use",[("hasPurpose","isA","dpv:CommercialPurpose")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("hasPurpose","isA","dpv:ResearchAndDevelopment")]),
  "DAG-safe: disj(cP,R&D) suppressed; commercialResearch ≤ both → Compatible",
  "fof(odrl101, conjecture,\n"
  "    ?[X]: ( in_denotation(X, commercialPurpose, isA)\n"
  "          & in_denotation(X, researchAndDevelopment, isA) )).",
  extra=DPV_SAFE_FRAGMENT, inc=("ODRL",),
  pl="DAG-safe: multi-parent reachability preserved")

P("ODRL102-1.p", "CounterSatisfiable", "Conflict",
  "Note 1 — DAG-Safe True Conflict Detection", "Medium",
  tp("policyA","permission","use",[("hasPurpose","isA","dpv:CommercialPurpose")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("hasPurpose","isA","dpv:ServiceProvision")]),
  "disj(cP,sP) IS asserted → Conflict",
  "fof(odrl102, conjecture,\n"
  "    ?[X]: ( in_denotation(X, commercialPurpose, isA)\n"
  "          & in_denotation(X, serviceProvision, isA) )).",
  flip_conj=
  "fof(odrl102, conjecture,\n"
  "    ![X]: ~( in_denotation(X, commercialPurpose, isA)\n"
  "           & in_denotation(X, serviceProvision, isA) )).",
  extra=DPV_SAFE_FRAGMENT, inc=("ODRL",),
  pl="DAG-safe: true conflict cP ⊥ serviceProvision still detected")

P("ODRL103-1.p", "CounterSatisfiable", "Conflict",
  "Note 1 + Lemma 2 — DAG-Safe Conflict Propagation", "Hard",
  tp("policyA","permission","use",[("hasPurpose","isA","dpv:AcademicResearch")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("hasPurpose","isA","dpv:ServiceProvision")]),
  "acR ≤ R&D, R&D ⊥ sP → disj_downward → acR ⊥ sP → Conflict",
  "fof(odrl103, conjecture,\n"
  "    ?[X]: ( in_denotation(X, academicResearch, isA)\n"
  "          & in_denotation(X, serviceProvision, isA) )).",
  flip_conj=
  "fof(odrl103, conjecture,\n"
  "    ![X]: ~( in_denotation(X, academicResearch, isA)\n"
  "           & in_denotation(X, serviceProvision, isA) )).",
  extra=DPV_SAFE_FRAGMENT, inc=("ODRL",),
  pl="DAG-safe: conflict propagation acR ⊥ sP via R&D")

P("ODRL104-1.p", "Theorem", "Trivial",
  "Note 1 — Ablation: Naive KB Makes Everything Provable", "Easy",
  "(Same query as ODRL101 with NAIVE sibling disjointness)",
  "NAIVE KB: ⊥ → anything follows",
  "fof(odrl104, conjecture,\n"
  "    ?[X]: ( in_denotation(X, commercialPurpose, isA)\n"
  "          & in_denotation(X, researchAndDevelopment, isA) )).",
  extra=DPV_NAIVE_FRAGMENT, inc=("ODRL",),
  pl="Ablation: naive inconsistency → trivially provable")

P("ODRL105-1.p", "Theorem", "Subsumption",
  "Note 1 — DAG Subsumption via Multi-Parent Path", "Medium",
  tp("policyA","permission","use",[("hasPurpose","isA","dpv:CommercialResearch")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("hasPurpose","isA","dpv:CommercialPurpose")]),
  "cR ≤ cP → ⟦isA(cR)⟧ ⊆ ⟦isA(cP)⟧",
  "fof(odrl105, conjecture,\n"
  "    ![X]: ( in_denotation(X, commercialResearch, isA)\n"
  "        => in_denotation(X, commercialPurpose, isA) )).",
  extra=DPV_SAFE_FRAGMENT, inc=("ODRL",),
  pl="DAG subsumption: cR ⊆ cP via multi-parent path")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 10: NESTED SET OPERATORS (ODRL110–114)
# ═══════════════════════════════════════════════════════════════════════════
P("ODRL110-1.p", "Theorem", "EmptyDenotation",
  "Definition 3 (isAllOf) — Empty Denotation from Disjoint Members", "Hard",
  tp("policyA","permission","use",[("spatial","isAllOf","( geo:westernEurope geo:easternEurope )")]),
  "isAllOf({wE,eE}) = ↓wE ∩ ↓eE = ∅ (wE ⊥ eE)",
  "fof(odrl110, conjecture,\n"
  "    ![X]: ~in_denotation_set(X, list110, isAllOf)).",
  extra=(
      "fof(list_110_1, axiom, in_value_list(westernEurope, list110)).\n"
      "fof(list_110_2, axiom, in_value_list(easternEurope, list110)).\n" +
      generate_list_closure("list110", ["westernEurope","easternEurope"])),
  inc=("GEO","ODRL"),
  pl="isAllOf({wE,eE}) = ∅: disjoint members → empty denotation")

P("ODRL111-1.p", "Theorem", "Compatible",
  "Definition 3 (isAnyOf) — Union Compatible with isPartOf", "Easy",
  tp("policyA","permission","use",[("spatial","isAnyOf","( geo:germany geo:france )")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:westernEurope")]),
  "isAnyOf({de,fr}) ∩ ↓wE ≠ ∅; witness: germany",
  "fof(odrl111, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, list111, isAnyOf)\n"
  "          & in_denotation(X, westernEurope, isPartOf) )).",
  extra=(
      "fof(list_111_1, axiom, in_value_list(germany, list111)).\n"
      "fof(list_111_2, axiom, in_value_list(france, list111)).\n" +
      generate_list_closure("list111",["germany","france"])),
  inc=("GEO","ODRL"),
  pl="isAnyOf({de,fr}) ∩ isPartOf(wE) ≠ ∅")

P("ODRL112-1.p", "CounterSatisfiable", "Conflict",
  "Definition 3 (isNoneOf) — Conflict with Subsumed isPartOf", "Hard",
  tp("policyA","permission","use",[("spatial","isNoneOf","( geo:westernEurope )")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:germany")]),
  "de ≤ wE → ↓de ⊆ ↓wE → isNoneOf({wE}) ∩ isPartOf(de) = ∅",
  "fof(odrl112, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, list112, isNoneOf)\n"
  "          & in_denotation(X, germany, isPartOf) )).",
  flip_conj=
  "fof(odrl112, conjecture,\n"
  "    ![X]: ~( in_denotation_set(X, list112, isNoneOf)\n"
  "           & in_denotation(X, germany, isPartOf) )).",
  extra=(
      "fof(list_112_1, axiom, in_value_list(westernEurope, list112)).\n" +
      generate_list_closure("list112",["westernEurope"])),
  inc=("GEO","ODRL"),
  pl="isNoneOf({wE}) ∩ isPartOf(de) = ∅: subsumed → conflict")

P("ODRL113-1.p", "Theorem", "Compatible",
  "Definition 3 — isAnyOf ∩ isNoneOf Partial Overlap", "Medium",
  tp("policyA","permission","use",[("spatial","isAnyOf","( geo:germany geo:poland )")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isNoneOf","( geo:easternEurope )")]),
  "germany ∈ isAnyOf({de,pl}) ∧ ¬leq(de,eE) → Compatible",
  "fof(odrl113, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, anyList113, isAnyOf)\n"
  "          & in_denotation_set(X, noneList113, isNoneOf) )).",
  extra=(
      "fof(list_113a_1, axiom, in_value_list(germany, anyList113)).\n"
      "fof(list_113a_2, axiom, in_value_list(poland, anyList113)).\n" +
      generate_list_closure("anyList113",["germany","poland"]) + "\n"
      "fof(list_113b_1, axiom, in_value_list(easternEurope, noneList113)).\n" +
      generate_list_closure("noneList113",["easternEurope"])),
  inc=("GEO","ODRL"),
  pl="isAnyOf({de,pl}) ∩ isNoneOf({eE}): partial overlap → Compatible")

P("ODRL114-1.p", "Theorem", "Compatible",
  "Definition 3 (isAllOf) — Compatible Members Non-Empty", "Easy",
  tp("policyA","permission","use",[("spatial","isAllOf","( geo:westernEurope geo:europe )")]),
  "isAllOf({wE,europe}) = ↓wE ≠ ∅; witness: germany",
  "fof(odrl114, conjecture,\n"
  "    ?[X]: in_denotation_set(X, list114, isAllOf)).",
  extra=(
      "fof(list_114_1, axiom, in_value_list(westernEurope, list114)).\n"
      "fof(list_114_2, axiom, in_value_list(europe, list114)).\n" +
      generate_list_closure("list114",["westernEurope","europe"])),
  inc=("GEO","ODRL"),
  pl="isAllOf({wE,europe}) ≠ ∅: compatible members → non-empty")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 11: QUANTIFIER STRESS (ODRL120–123)
# ═══════════════════════════════════════════════════════════════════════════
P("ODRL120-1.p", "Theorem", "Conflict",
  "Definition 5 (universal) — All Descendant Pairs Conflict", "Hard",
  "(Universal variant)",
  "∀G1≤wE, ∀G2≤eE: isPartOf(G1) ∩ isPartOf(G2) = ∅",
  "fof(odrl120, conjecture,\n"
  "    ![G1,G2,X]: (\n"
  "        (leq(G1, westernEurope) & leq(G2, easternEurope))\n"
  "      => ~( in_denotation(X, G1, isPartOf)\n"
  "          & in_denotation(X, G2, isPartOf) ))).",
  inc=("GEO","ODRL"),
  pl="Universal conflict: ∀G1∈↓wE, ∀G2∈↓eE: overlap = ∅")

P("ODRL121-1.p", "Theorem", "Compatible",
  "∃∀ Pattern — Common Ancestor for Multiple Concepts", "Hard",
  "(∃X in hasPart of all three)",
  "∃X: leq(de,X) ∧ leq(fr,X) ∧ leq(it,X); witness: europe",
  "fof(odrl121, conjecture,\n"
  "    ?[X]: ( in_denotation(X, germany, hasPart)\n"
  "          & in_denotation(X, france, hasPart)\n"
  "          & in_denotation(X, italy, hasPart) )).",
  inc=("GEO","ODRL"),
  pl="∃∀ pattern: common ancestor europe for {de, fr, it}")

P("ODRL122-1.p", "Theorem", "Subsumption",
  "Lemma 2 (universal) — Denotation Subsumption Chain", "Medium",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:bavaria")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:europe")]),
  "bav ≤ de ≤ wE ≤ europe → ↓bav ⊆ ↓europe",
  "fof(odrl122, conjecture,\n"
  "    ![X]: ( in_denotation(X, bavaria, isPartOf)\n"
  "        => in_denotation(X, europe, isPartOf) )).",
  inc=("GEO","ODRL"),
  pl="Subsumption chain: ↓bavaria ⊆ ↓europe via 3-hop leq")

P("ODRL123-1.p", "Theorem", "Sound",
  "∀∃ Pattern — Every Descendant Has an Ancestor", "Hard",
  "(∀G ≤ wE: ∃X in hasPart(G))",
  "Witness: X = westernEurope",
  "fof(odrl123, conjecture,\n"
  "    ![G]: ( leq(G, westernEurope)\n"
  "        => ?[X]: in_denotation(X, G, hasPart) )).",
  inc=("GEO","ODRL"),
  pl="∀∃ pattern: every G ≤ wE has ancestor in hasPart(G)")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 12: LARGE-SCALE COMPOSITION (ODRL130–132)
# ═══════════════════════════════════════════════════════════════════════════
P("ODRL130-1.p", "Theorem", "Compatible",
  "Definition 6 — 3-Operand AND Composition", "Medium",
  tp("policyA","permission","use",[
      ("spatial","isPartOf","geo:europe"),
      ("hasPurpose","isA","dpv:ResearchAndDevelopment"),
      ("language","isPartOf","lang:en")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[
      ("spatial","eq","geo:germany"),
      ("hasPurpose","isA","dpv:AcademicResearch"),
      ("language","eq","lang:enGB")]),
  "3-operand AND Compatible; witnesses: germany, academicResearch, enGB",
  "fof(odrl130, conjecture,\n"
  "    ( ?[X]: ( in_denotation(X, europe, isPartOf)\n"
  "            & in_denotation(X, germany, eq) )\n"
  "    & ?[Y]: ( in_denotation(Y, researchAndDevelopment, isA)\n"
  "            & in_denotation(Y, academicResearch, isA) )\n"
  "    & ?[Z]: ( in_denotation(Z, en, isPartOf)\n"
  "            & in_denotation(Z, enGB, eq) ) )).",
  inc=("GEO","DPV","LANG","ODRL"),
  pl="3-operand AND: spatial + purpose + language all Compatible")

P("ODRL131-1.p", "CounterSatisfiable", "Conflict",
  "Theorem 2 — 3-Operand AND with One Conflict", "Hard",
  tp("policyA","permission","use",[
      ("spatial","isPartOf","geo:westernEurope"),
      ("hasPurpose","isA","dpv:ResearchAndDevelopment"),
      ("language","isPartOf","lang:en")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[
      ("spatial","isPartOf","geo:easternEurope"),
      ("hasPurpose","isA","dpv:AcademicResearch"),
      ("language","eq","lang:enGB")]),
  "spatial Conflict (wE ⊥ eE) → composed Conflict (Thm 2)",
  "fof(odrl131, conjecture,\n"
  "    ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
  "          & in_denotation(X, easternEurope, isPartOf) )).",
  flip_conj=
  "fof(odrl131, conjecture,\n"
  "    ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
  "           & in_denotation(X, easternEurope, isPartOf) )).",
  inc=("GEO","DPV","LANG","ODRL"),
  pl="3-operand AND: spatial Conflict → composed Conflict")

P("ODRL132-1.p", "Theorem", "Compatible",
  "Definition 6 — 5-Way Existential Witness", "Hard",
  "(5 compatible pairs in one conjecture)",
  "5 independent witnesses from different GEO branches",
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
  inc=("GEO","ODRL"),
  pl="5-way existential: 5 independent compatible pairs")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 13: EDGE CASES & ADVERSARIAL (ODRL140–145)
# ═══════════════════════════════════════════════════════════════════════════
P("ODRL140-1.p", "CounterSatisfiable", "Conflict",
  "Definition 5 — Tautological Self-Conflict (eq ∩ neq)", "Easy",
  tp("policyA","permission","use",[("spatial","eq","geo:germany")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","neq","geo:germany")]),
  "eq(de) ∩ neq(de) = ∅",
  "fof(odrl140, conjecture,\n"
  "    ?[X]: ( in_denotation(X, germany, eq)\n"
  "          & in_denotation(X, germany, neq) )).",
  flip_conj=
  "fof(odrl140, conjecture,\n"
  "    ![X]: ~( in_denotation(X, germany, eq)\n"
  "           & in_denotation(X, germany, neq) )).",
  inc=("GEO","ODRL"),
  pl="Tautological conflict: eq(de) ∩ neq(de) = ∅")

P("ODRL141-1.p", "Theorem", "Compatible",
  "Edge Case — Single-Concept KB (Degenerate)", "Easy",
  tp("policyA","permission","use",[("spatial","isPartOf","min:universe")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","eq","min:universe")]),
  "Degenerate: single concept; isPartOf(univ) ∩ eq(univ) = {univ}",
  "fof(odrl141, conjecture,\n"
  "    ?[X]: ( in_denotation(X, universe, isPartOf)\n"
  "          & in_denotation(X, universe, eq) )).",
  extra=MINIMAL_KB_FRAGMENT, inc=("ODRL",),
  pl="Degenerate: single-concept KB → trivially compatible")

P("ODRL142-1.p", "CounterSatisfiable", "Conflict",
  "Edge Case — Root-Level Conflict (Large KB Loaded)", "Easy",
  tp("policyA","permission","use",[("spatial","eq","geo:europe")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","neq","geo:europe")]),
  "eq(europe) ∩ neq(europe) = ∅ with full KB",
  "fof(odrl142, conjecture,\n"
  "    ?[X]: ( in_denotation(X, europe, eq)\n"
  "          & in_denotation(X, europe, neq) )).",
  flip_conj=
  "fof(odrl142, conjecture,\n"
  "    ![X]: ~( in_denotation(X, europe, eq)\n"
  "           & in_denotation(X, europe, neq) )).",
  inc=("GEO","ODRL"),
  pl="Root-level eq/neq conflict with full KB loaded")

P("ODRL143-1.p", "Theorem", "Tautology",
  "Reflexivity — Every Concept Is In Its Own isPartOf", "Easy",
  "(Meta-property: ∀G: G ∈ ⟦isPartOf(G)⟧)",
  "leq_refl + den_isPartOf_if",
  "fof(odrl143, conjecture,\n"
  "    ![G]: ( concept(G)\n"
  "        => in_denotation(G, G, isPartOf) )).",
  inc=("GEO","ODRL"),
  pl="Reflexivity: ∀G: concept(G) → G ∈ ⟦isPartOf(G)⟧")

P("ODRL144-1.p", "Theorem", "Conflict",
  "Definition 2 (disj_symm) — Bidirectional Conflict", "Medium",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:westernEurope")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:easternEurope")]),
  "disj(wE,eE) ∧ disj(eE,wE)",
  "fof(odrl144, conjecture,\n"
  "    ( ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
  "             & in_denotation(X, easternEurope, isPartOf) )\n"
  "    & ![Y]: ~( in_denotation(Y, easternEurope, isPartOf)\n"
  "             & in_denotation(Y, westernEurope, isPartOf) ) )).",
  inc=("GEO","ODRL"),
  pl="Bidirectional conflict: disj(wE,eE) ∧ disj(eE,wE)")

P("ODRL145-1.p", "CounterSatisfiable", "Unknown",
  "Edge Case — Query on Non-Existent Concept", "Medium",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:phantomConcept")]),
  "phantomConcept not in concept/1 → Unknown",
  "fof(odrl145, conjecture,\n"
  "    ?[X]: in_denotation(X, phantomConcept, isPartOf)).",
  inc=("GEO","ODRL"),
  pl="Non-existent concept: no concept/1 → satisfaction unknown")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 14: MULTI-HOP ALIGNMENT (ODRL150–159)
# ═══════════════════════════════════════════════════════════════════════════
_4KB_EXTRA = (SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH + "\n" +
              COMP_KB_NO_DISJ + "\n" + ALIGN_SYNTH_COMP)

P("ODRL150-1.p", "CounterSatisfiable", "Conflict",
  "Proposition 2 (2-hop) — Multi-Hop Alignment Conflict", "Very Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","synth:zoneWest")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","synth:zoneEast")]),
  "GEO→ISO→SYNTH 2-hop chain → disj(zW,zE) → Conflict",
  "fof(odrl150, conjecture,\n"
  "    ?[X]: ( in_denotation(X, zoneWest, isPartOf)\n"
  "          & in_denotation(X, zoneEast, isPartOf) )).",
  flip_conj=
  "fof(odrl150, conjecture,\n"
  "    ![X]: ~( in_denotation(X, zoneWest, isPartOf)\n"
  "           & in_denotation(X, zoneEast, isPartOf) )).",
  extra=SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH,
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="2-hop alignment: GEO→ISO→SYNTH conflict detection")

P("ODRL151-1.p", "Theorem", "Compatible",
  "Proposition 2 (2-hop) — Multi-Hop Compatible", "Medium",
  tp("policyA","permission","use",[("spatial","isPartOf","synth:euZone")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","eq","synth:zoneWest")]),
  "isPartOf(euZone) ∩ eq(zW) ≠ ∅; witness: zoneWest",
  "fof(odrl151, conjecture,\n"
  "    ?[X]: ( in_denotation(X, euZone, isPartOf)\n"
  "          & in_denotation(X, zoneWest, eq) )).",
  extra=SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH,
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="2-hop compatible: isPartOf(euZone) ∩ eq(zoneWest) ≠ ∅")

P("ODRL152-1.p", "CounterSatisfiable", "Unknown",
  "2-Hop Ablation — SYNTH Alone Cannot Detect Conflict", "Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","synth:zoneWest")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","synth:zoneEast")]),
  "Without GEO/ISO/align: no disjointness → Unknown",
  "fof(odrl152, conjecture,\n"
  "    ?[X]: ( in_denotation(X, zoneWest, isPartOf)\n"
  "          & in_denotation(X, zoneEast, isPartOf) )).",
  extra=SYNTH_KB_NO_DISJ, inc=("ODRL",),
  pl="Ablation: SYNTH alone → Unknown (no disjointness)")

P("ODRL153-1.p", "Theorem", "Conflict",
  "2-Hop Intermediate — 1-Hop Result as Prerequisite", "Medium",
  "(Proves intermediate: disj(dE,pL))",
  "align + disj(de,pl) → disj(dE,pL)",
  "fof(odrl153, conjecture, disjoint(dE, pL)).",
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="Intermediate: hop 1 derives disjoint(dE, pL)")

P("ODRL154-1.p", "CounterSatisfiable", "Conflict",
  "Proposition 2 (3-hop) — 4-Dataspace Alignment Conflict", "Very Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","comp:gdprFull")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","comp:gdprPartial")]),
  "GEO→ISO→SYNTH→COMP 3-hop → disj(gdprFull,gdprPartial) → Conflict",
  "fof(odrl154, conjecture,\n"
  "    ?[X]: ( in_denotation(X, gdprFull, isPartOf)\n"
  "          & in_denotation(X, gdprPartial, isPartOf) )).",
  flip_conj=
  "fof(odrl154, conjecture,\n"
  "    ![X]: ~( in_denotation(X, gdprFull, isPartOf)\n"
  "           & in_denotation(X, gdprPartial, isPartOf) )).",
  extra=_4KB_EXTRA,
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="3-hop alignment: GEO→ISO→SYNTH→COMP conflict detection")

P("ODRL155-1.p", "Theorem", "Compatible",
  "Proposition 2 (3-hop) — 4-Dataspace Compatible", "Medium",
  tp("policyA","permission","use",[("spatial","isPartOf","comp:complianceScope")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","eq","comp:gdprFull")]),
  "isPartOf(complianceScope) ∩ eq(gdprFull) ≠ ∅; witness: gdprFull",
  "fof(odrl155, conjecture,\n"
  "    ?[X]: ( in_denotation(X, complianceScope, isPartOf)\n"
  "          & in_denotation(X, gdprFull, eq) )).",
  extra=_4KB_EXTRA,
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="3-hop compatible: isPartOf(complianceScope) ∩ eq(gdprFull) ≠ ∅")

P("ODRL156-1.p", "CounterSatisfiable", "Unknown",
  "3-Hop Ablation — COMP Alone Cannot Detect Conflict", "Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","comp:gdprFull")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","comp:gdprPartial")]),
  "Without GEO/ISO/SYNTH/align → Unknown",
  "fof(odrl156, conjecture,\n"
  "    ?[X]: ( in_denotation(X, gdprFull, isPartOf)\n"
  "          & in_denotation(X, gdprPartial, isPartOf) )).",
  extra=COMP_KB_NO_DISJ, inc=("ODRL",),
  pl="Ablation: COMP alone → Unknown (no disjointness)")

P("ODRL157-1.p", "Theorem", "Conflict",
  "3-Hop Intermediate — Hop 2 Result as Prerequisite", "Hard",
  "(Proves hop 2: disj(zoneWest,zoneEast))",
  "2-hop: GEO→ISO→SYNTH → disj(zW,zE)",
  "fof(odrl157, conjecture, disjoint(zoneWest, zoneEast)).",
  extra=SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH,
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="Intermediate: hop 2 derives disjoint(zoneWest, zoneEast)")

P("ODRL158-1.p", "Theorem", "Compatible",
  "Proposition 2(2) Baseline — Compatible in Source KB", "Easy",
  tp("policyA","permission","use",[("hasPurpose","isA","wit:witB")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("hasPurpose","isA","wit:witC")]),
  "witA ≤ witB ∧ witA ≤ witC, no disj → Compatible; witness: witA",
  "fof(odrl158, conjecture,\n"
  "    ?[X]: ( in_denotation(X, witB, isA)\n"
  "          & in_denotation(X, witC, isA) )).",
  extra=KB_WITNESS_SOURCE, inc=("ODRL",),
  pl="Prop 2(2) baseline: witA witnesses isA(witB) ∩ isA(witC) ≠ ∅")

P("ODRL159-1.p", "CounterSatisfiable", "FabricatedConflict",
  "Proposition 2(2) Bug — Fabricated Conflict from Partial Alignment", "Very Hard",
  tp("policyA","permission","use",[("hasPurpose","isA","tgt:tgtB")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("hasPurpose","isA","tgt:tgtC")]),
  "Partial α: witA unmapped → tgtB,tgtC disjoint → fabricated Conflict",
  "fof(odrl159, conjecture,\n"
  "    ?[X]: ( in_denotation(X, tgtB, isA)\n"
  "          & in_denotation(X, tgtC, isA) )).",
  flip_conj=
  "fof(odrl159, conjecture,\n"
  "    ![X]: ~( in_denotation(X, tgtB, isA)\n"
  "           & in_denotation(X, tgtC, isA) )).",
  extra=KB_WITNESS_TARGET, inc=("ODRL",),
  pl="Prop 2(2) BUG: partial alignment loses witness → fabricated Conflict")

P("ODRL158-2.p", "Theorem", "Compatible",
  "Proposition 2(2) Fix — Downward-Closed Alignment Preserves Verdict", "Hard",
  tp("policyA","permission","use",[("hasPurpose","isA","tgt:tgtB")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("hasPurpose","isA","tgt:tgtC")]),
  "Total β: tgtA ≤ tgtB ∧ tgtA ≤ tgtC → Compatible preserved",
  "fof(odrl158b, conjecture,\n"
  "    ?[X]: ( in_denotation(X, tgtB, isA)\n"
  "          & in_denotation(X, tgtC, isA) )).",
  extra=KB_WITNESS_TARGET_FULL, inc=("ODRL",),
  pl="Prop 2(2) FIX: downward-closed alignment → Compatible preserved")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 15: N-WAY POLICY CONFLICTS (ODRL160–165)
# ═══════════════════════════════════════════════════════════════════════════
P("ODRL160-1.p", "Theorem", "Conflict",
  "N-Way — 3-Policy Mutual Exclusion", "Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:germany")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:france")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[("spatial","isPartOf","geo:poland")]),
  "de⊥fr, de⊥pl, fr⊥pl — all 3 pairs conflict",
  "fof(odrl160, conjecture,\n"
  "    ( ![X]: ~( in_denotation(X, germany, isPartOf)\n"
  "             & in_denotation(X, france, isPartOf) )\n"
  "    & ![Y]: ~( in_denotation(Y, germany, isPartOf)\n"
  "             & in_denotation(Y, poland, isPartOf) )\n"
  "    & ![Z]: ~( in_denotation(Z, france, isPartOf)\n"
  "             & in_denotation(Z, poland, isPartOf) ) )).",
  inc=("GEO","ODRL"),
  pl="3-policy mutual exclusion: all 3 pairs conflict (de⊥fr, de⊥pl, fr⊥pl)")

P("ODRL161-1.p", "Theorem", "Compatible",
  "N-Way — 3-Policy Common Witness", "Medium",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:europe")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:westernEurope")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[("spatial","eq","geo:germany")]),
  "∃X ∈ ↓europe ∩ ↓wE ∩ {de}; witness: germany",
  "fof(odrl161, conjecture,\n"
  "    ?[X]: ( in_denotation(X, europe, isPartOf)\n"
  "          & in_denotation(X, westernEurope, isPartOf)\n"
  "          & in_denotation(X, germany, eq) )).",
  inc=("GEO","ODRL"),
  pl="3-policy common witness: ∃X ∈ ↓europe ∩ ↓wE ∩ {de}")

P("ODRL162-1.p", "Theorem", "NonTransitive",
  "N-Way — Non-Transitive Compatibility", "Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:westernEurope")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:europe")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[("spatial","isPartOf","geo:easternEurope")]),
  "A~B ∧ B~C but A⊥C: key N-way insight",
  "fof(odrl162, conjecture,\n"
  "    ( ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
  "            & in_denotation(X, europe, isPartOf) )\n"
  "    & ?[Y]: ( in_denotation(Y, europe, isPartOf)\n"
  "            & in_denotation(Y, easternEurope, isPartOf) )\n"
  "    & ![Z]: ~( in_denotation(Z, westernEurope, isPartOf)\n"
  "             & in_denotation(Z, easternEurope, isPartOf) ) )).",
  inc=("GEO","ODRL"),
  pl="Non-transitive: Compatible(A,B) ∧ Compatible(B,C) but Conflict(A,C)")

P("ODRL163-1.p", "Theorem", "MixedNWay",
  "N-Way — Multi-Dimensional 3-Way (Spatial + Purpose)", "Very Hard",
  tp("policyA","permission","use",[
      ("spatial","isPartOf","geo:europe"),
      ("hasPurpose","isA","dpv:ResearchAndDevelopment")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[
      ("spatial","isPartOf","geo:germany"),
      ("hasPurpose","isA","dpv:AcademicResearch")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[
      ("spatial","isPartOf","geo:france"),
      ("hasPurpose","isA","dpv:CommercialPurpose")]),
  "A~B, A~C (both dims), B⊥C (spatial: de⊥fr)",
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
  extra=DPV_SAFE_FRAGMENT, inc=("GEO","ODRL"),
  pl="Multi-dim 3-way: A~B, A~C (spatial+purpose), but B⊥C (spatial)")

P("ODRL164-1.p", "Theorem", "Compatible",
  "N-Way — 4-Policy Subsumption Chain", "Medium",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:europe")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:westernEurope")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[("spatial","isPartOf","geo:germany")]) + "\n%\n%   " +
  tp("policyD","prohibition","use",[("spatial","eq","geo:bavaria")]),
  "4-way: ∃X ∈ ↓europe ∩ ↓wE ∩ ↓de ∩ {bav}; witness: bavaria",
  "fof(odrl164, conjecture,\n"
  "    ?[X]: ( in_denotation(X, europe, isPartOf)\n"
  "          & in_denotation(X, westernEurope, isPartOf)\n"
  "          & in_denotation(X, germany, isPartOf)\n"
  "          & in_denotation(X, bavaria, eq) )).",
  inc=("GEO","ODRL"),
  pl="4-policy chain: ∃X ∈ ↓europe ∩ ↓wE ∩ ↓de ∩ {bav}")

P("ODRL165-1.p", "Theorem", "MixedNWay",
  "N-Way — 4-Policy One Spoiler", "Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:europe")]) + "\n%\n%   " +
  tp("policyB","permission","use",[("spatial","isPartOf","geo:westernEurope")]) + "\n%\n%   " +
  tp("policyC","permission","use",[("spatial","eq","geo:germany")]) + "\n%\n%   " +
  tp("policyD","prohibition","use",[("spatial","isPartOf","geo:easternEurope")]),
  "Compatible(A,D) ∧ Conflict(B,D) ∧ Conflict(C,D): D spoils B,C only",
  "fof(odrl165, conjecture,\n"
  "    ( ?[X]: ( in_denotation(X, europe, isPartOf)\n"
  "            & in_denotation(X, easternEurope, isPartOf) )\n"
  "    & ![Y]: ~( in_denotation(Y, westernEurope, isPartOf)\n"
  "             & in_denotation(Y, easternEurope, isPartOf) )\n"
  "    & ![Z]: ~( in_denotation(Z, germany, eq)\n"
  "             & in_denotation(Z, easternEurope, isPartOf) ) )).",
  inc=("GEO","ODRL"),
  pl="4-policy spoiler: Compatible(A,D) ∧ Conflict(B,D) ∧ Conflict(C,D)")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 16: N-WAY COMPOSED POLICIES (ODRL170–175)
# ═══════════════════════════════════════════════════════════════════════════
P("ODRL170-1.p", "Theorem", "Compatible",
  "N-Way Composed — 3 Policies All Compatible (Spatial + Purpose)", "Very Hard",
  tp("policyA","permission","use",[
      ("spatial","isPartOf","geo:europe"),
      ("hasPurpose","isA","dpv:ResearchAndDevelopment")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[
      ("spatial","eq","geo:germany"),
      ("hasPurpose","isA","dpv:AcademicResearch")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[
      ("spatial","isPartOf","geo:westernEurope"),
      ("hasPurpose","isA","dpv:ResearchAndDevelopment")]),
  "All 3 pairs Compatible on both dims; witness: (germany, academicResearch)",
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
  extra=DPV_SAFE_FRAGMENT, inc=("GEO","ODRL"),
  pl="3-policy multi-dim: all pairs Compatible on spatial+purpose")

P("ODRL171-1.p", "Theorem", "NonTransitive",
  "N-Way Composed — Non-Transitive on ONE Dimension", "Very Hard",
  tp("policyA","permission","use",[
      ("spatial","isPartOf","geo:westernEurope"),
      ("hasPurpose","isA","dpv:ResearchAndDevelopment")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[
      ("spatial","isPartOf","geo:europe"),
      ("hasPurpose","isA","dpv:AcademicResearch")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[
      ("spatial","isPartOf","geo:easternEurope"),
      ("hasPurpose","isA","dpv:CommercialResearch")]),
  "A~B (both dims), B~C (both dims), A⊥C (spatial: wE⊥eE, Thm 2 short-circuit)",
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
  extra=DPV_SAFE_FRAGMENT, inc=("GEO","ODRL"),
  pl="Non-transitive multi-dim: spatial conflict breaks transitivity")

P("ODRL172-1.p", "Theorem", "Conflict",
  "N-Way Composed — 3-Policy Mutual Exclusion (Spatial Suffices)", "Very Hard",
  tp("policyA","permission","use",[
      ("spatial","isPartOf","geo:germany"),
      ("hasPurpose","isA","dpv:CommercialPurpose")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[
      ("spatial","isPartOf","geo:france"),
      ("hasPurpose","isA","dpv:ServiceProvision")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[
      ("spatial","isPartOf","geo:poland"),
      ("hasPurpose","isA","dpv:ServiceProvision")]),
  "de⊥fr, de⊥pl, fr⊥pl (spatial) → Thm 2 short-circuit: Conflict all pairs",
  "fof(odrl172, conjecture,\n"
  "    ( ![X]: ~( in_denotation(X, germany, isPartOf)\n"
  "             & in_denotation(X, france, isPartOf) )\n"
  "    & ![Y]: ~( in_denotation(Y, germany, isPartOf)\n"
  "             & in_denotation(Y, poland, isPartOf) )\n"
  "    & ![Z]: ~( in_denotation(Z, france, isPartOf)\n"
  "             & in_denotation(Z, poland, isPartOf) ) )).",
  extra=DPV_SAFE_FRAGMENT, inc=("GEO","ODRL"),
  pl="3-policy mutual exclusion: spatial conflict suffices (Thm 2)")

P("ODRL173-1.p", "Theorem", "Compatible",
  "N-Way Composed — 3 Operands × 3 Policies", "Very Hard",
  tp("policyA","permission","use",[
      ("spatial","isPartOf","geo:europe"),
      ("hasPurpose","isA","dpv:ResearchAndDevelopment"),
      ("language","isPartOf","lang:en")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[
      ("spatial","eq","geo:germany"),
      ("hasPurpose","isA","dpv:AcademicResearch"),
      ("language","eq","lang:enGB")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[
      ("spatial","isPartOf","geo:westernEurope"),
      ("hasPurpose","isA","dpv:ResearchAndDevelopment"),
      ("language","isPartOf","lang:en")]),
  "9 pairwise operand checks (3×3), all Compatible",
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
  extra=DPV_SAFE_FRAGMENT, inc=("GEO","DPV","LANG","ODRL"),
  pl="3-operand × 3-policy: maximum complexity, all pairs Compatible")

P("ODRL174-1.p", "Theorem", "MixedNWay",
  "N-Way Composed — 4-Policy Spoiler on Spatial Dimension", "Very Hard",
  tp("policyA","permission","use",[
      ("spatial","isPartOf","geo:europe"),
      ("hasPurpose","isA","dpv:ResearchAndDevelopment")]) + "\n%\n%   " +
  tp("policyB","permission","use",[
      ("spatial","isPartOf","geo:westernEurope"),
      ("hasPurpose","isA","dpv:AcademicResearch")]) + "\n%\n%   " +
  tp("policyC","permission","use",[
      ("spatial","eq","geo:germany"),
      ("hasPurpose","isA","dpv:CommercialResearch")]) + "\n%\n%   " +
  tp("policyD","prohibition","use",[
      ("spatial","isPartOf","geo:easternEurope"),
      ("hasPurpose","isA","dpv:ResearchAndDevelopment")]),
  "Compatible(A,D) ∧ Conflict(B,D) ∧ Conflict(C,D): spatial spoiler",
  "fof(odrl174, conjecture,\n"
  "    ( ?[Xs,Xp]: ( in_denotation(Xs, europe, isPartOf)\n"
  "                & in_denotation(Xs, easternEurope, isPartOf)\n"
  "                & in_denotation(Xp, researchAndDevelopment, isA)\n"
  "                & in_denotation(Xp, researchAndDevelopment, isA) )\n"
  "    & ![Ys]: ~( in_denotation(Ys, westernEurope, isPartOf)\n"
  "              & in_denotation(Ys, easternEurope, isPartOf) )\n"
  "    & ![Zs]: ~( in_denotation(Zs, germany, eq)\n"
  "              & in_denotation(Zs, easternEurope, isPartOf) ) )).",
  extra=DPV_SAFE_FRAGMENT, inc=("GEO","ODRL"),
  pl="4-policy spoiler: spatial conflict on B,C; purpose compatible with A")

P("ODRL175-1.p", "Theorem", "Compatible",
  "N-Way Composed — DAG Multi-Parent Across 3 Policies", "Very Hard",
  tp("policyA","permission","use",[
      ("hasPurpose","isA","dpv:CommercialPurpose"),
      ("spatial","isPartOf","geo:germany")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[
      ("hasPurpose","isA","dpv:ResearchAndDevelopment"),
      ("spatial","isPartOf","geo:europe")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[
      ("hasPurpose","isA","dpv:CommercialResearch"),
      ("spatial","eq","geo:germany")]),
  "cR ≤ {cP,R&D}: (cR,germany) witnesses all 3 pairs",
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
  extra=DPV_SAFE_FRAGMENT, inc=("GEO","ODRL"),
  pl="DAG multi-parent in 3-way: cR witnesses all pairs")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 20: XONE & SYMMETRIC DIFFERENCE (ODRL230–237)
# ═══════════════════════════════════════════════════════════════════════════
P("ODRL230-1.p", "Theorem", "XONESuccess",
  "XONE — Basic Symmetric Difference (Disjoint Siblings)", "Very Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:germany")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:france")]),
  "∃X ∈ ↓de △ ↓fr; witness: germany (de⊥fr direct)",
  "fof(odrl230, conjecture,\n"
  "    ?[X]: ( ( in_denotation(X, germany, isPartOf)\n"
  "            & ~in_denotation(X, france, isPartOf) )\n"
  "          | ( ~in_denotation(X, germany, isPartOf)\n"
  "            & in_denotation(X, france, isPartOf) ) )).",
  inc=("GEO","ODRL"),
  pl="XONE: ↓de △ ↓fr ≠ ∅ via sibling disjointness")

P("ODRL231-1.p", "Theorem", "XONESuccess",
  "XONE — Symmetric Difference (Derived Disjointness)", "Very Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:germany")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:poland")]),
  "∃X ∈ ↓de △ ↓pl; de⊥pl derived via wE⊥eE",
  "fof(odrl231, conjecture,\n"
  "    ?[X]: ( ( in_denotation(X, germany, isPartOf)\n"
  "            & ~in_denotation(X, poland, isPartOf) )\n"
  "          | ( ~in_denotation(X, germany, isPartOf)\n"
  "            & in_denotation(X, poland, isPartOf) ) )).",
  inc=("GEO","ODRL"),
  pl="XONE: ↓de △ ↓pl ≠ ∅ via derived disjointness (wE⊥eE)")

P("ODRL232-1.p", "Theorem", "XONEThreeWay",
  "XONE — 3-Way Exactly-One (Mutual Exclusion)", "Extreme",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:germany")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:france")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[("spatial","isPartOf","geo:poland")]),
  "∃X in exactly one of {↓de,↓fr,↓pl}; witness: germany",
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
  inc=("GEO","ODRL"),
  pl="3-way XONE: exactly one of {↓de, ↓fr, ↓pl}")

P("ODRL233-1.p", "CounterSatisfiable", "XONEFailure",
  "XONE Failure — DAG-Safe Suppression Blocks Proof", "Very Hard",
  tp("policyA","permission","use",[("hasPurpose","isA","dpv:CommercialPurpose")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("hasPurpose","isA","dpv:ResearchAndDevelopment")]),
  "DAG-safe suppresses disj(cP,R&D) → unprovable → CounterSatisfiable",
  "fof(odrl233, conjecture,\n"
  "    ?[X]: ( ( in_denotation(X, commercialPurpose, isA)\n"
  "            & ~in_denotation(X, researchAndDevelopment, isA) )\n"
  "          | ( ~in_denotation(X, commercialPurpose, isA)\n"
  "            & in_denotation(X, researchAndDevelopment, isA) ) )).",
  extra=DPV_SAFE_FRAGMENT, inc=("ODRL",),
  pl="XONE failure: DAG-safe suppresses cP⊥R&D → proof blocked")

P("ODRL234-1.p", "Theorem", "XONESetOp",
  "XONE + isNoneOf — Set Negation × Symmetric Difference", "Extreme",
  tp("policyA","permission","use",[("spatial","isNoneOf","( geo:westernEurope )")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:easternEurope")]),
  "isNoneOf({wE}) △ isPartOf(eE); witness: europe",
  "fof(odrl234, conjecture,\n"
  "    ?[X]: ( ( in_denotation_set(X, noneList234, isNoneOf)\n"
  "            & ~in_denotation(X, easternEurope, isPartOf) )\n"
  "          | ( ~in_denotation_set(X, noneList234, isNoneOf)\n"
  "            & in_denotation(X, easternEurope, isPartOf) ) )).",
  extra=(
      "fof(list_234_1, axiom, in_value_list(westernEurope, noneList234)).\n" +
      generate_list_closure("noneList234",["westernEurope"])),
  inc=("GEO","ODRL"),
  pl="XONE: isNoneOf({wE}) △ isPartOf(eE), witness = europe (root)")

P("ODRL235-1.p", "Theorem", "XONEAligned",
  "XONE + 2-Hop Alignment — Cross-Dataspace Symmetric Difference", "Extreme",
  tp("policyA","permission","use",[("spatial","isPartOf","synth:zoneWest")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","synth:zoneEast")]),
  "XONE via 2-hop chain; witness: zoneWest",
  "fof(odrl235, conjecture,\n"
  "    ?[X]: ( ( in_denotation(X, zoneWest, isPartOf)\n"
  "            & ~in_denotation(X, zoneEast, isPartOf) )\n"
  "          | ( ~in_denotation(X, zoneWest, isPartOf)\n"
  "            & in_denotation(X, zoneEast, isPartOf) ) )).",
  extra=SYNTH_KB_NO_DISJ + "\n" + ALIGN_ISO_SYNTH,
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="XONE: zoneWest △ zoneEast via 2-hop alignment chain")

P("ODRL236-1.p", "Theorem", "XONEMatrix",
  "XONE All-Pairs Matrix — 3 Concepts, All Pairs", "Extreme",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:germany")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:france")]) + "\n%\n%   " +
  tp("policyC","prohibition","use",[("spatial","isPartOf","geo:poland")]),
  "All C(3,2)=3 pairwise symmetric diffs non-empty",
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
  inc=("GEO","ODRL"),
  pl="XONE matrix: all C(3,2)=3 pairwise symmetric diffs non-empty")

P("ODRL237-1.p", "Theorem", "XONEMultiDim",
  "XONE Multi-Dimensional — Spatial XONE × Purpose Compatible", "Extreme",
  tp("policyA","permission","use",[
      ("spatial","isPartOf","geo:germany"),
      ("hasPurpose","isA","dpv:ResearchAndDevelopment")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[
      ("spatial","isPartOf","geo:france"),
      ("hasPurpose","isA","dpv:AcademicResearch")]),
  "spatial(de△fr) × purpose(R&D∩acR≠∅)",
  "fof(odrl237, conjecture,\n"
  "    ( ?[Xs]: ( ( in_denotation(Xs, germany, isPartOf)\n"
  "               & ~in_denotation(Xs, france, isPartOf) )\n"
  "             | ( ~in_denotation(Xs, germany, isPartOf)\n"
  "               & in_denotation(Xs, france, isPartOf) ) )\n"
  "    & ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n"
  "             & in_denotation(Xp, academicResearch, isA) ) )).",
  extra=DPV_SAFE_FRAGMENT, inc=("GEO","ODRL"),
  pl="XONE+multi-dim: spatial(de△fr) × purpose(R&D∩acR)")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 21: OPERATOR MONOTONICITY (ODRL250–254)
# ═══════════════════════════════════════════════════════════════════════════
P("ODRL250-1.p", "Theorem", "Monotone",
  "Lemma 2 (universal) — isPartOf Monotonicity", "Hard",
  "(Meta-property: no ODRL policy)",
  "∀A,B,X: leq(A,B) ∧ in_den(X,A,isPO) → in_den(X,B,isPO)",
  "fof(odrl250, conjecture,\n"
  "    ![A,B,X]: (\n"
  "        (leq(A, B) & in_denotation(X, A, isPartOf))\n"
  "      => in_denotation(X, B, isPartOf) )).",
  inc=("GEO","ODRL"),
  pl="isPartOf monotonicity: leq(A,B) → ↓A ⊆ ↓B (universal)")

P("ODRL251-1.p", "Theorem", "AntiMonotone",
  "Lemma 2 (universal) — hasPart Anti-Monotonicity", "Hard",
  "(Meta-property: no ODRL policy)",
  "∀A,B,X: leq(A,B) ∧ in_den(X,B,hP) → in_den(X,A,hP)",
  "fof(odrl251, conjecture,\n"
  "    ![A,B,X]: (\n"
  "        (leq(A, B) & in_denotation(X, B, hasPart))\n"
  "      => in_denotation(X, A, hasPart) )).",
  inc=("GEO","ODRL"),
  pl="hasPart anti-monotonicity: leq(A,B) → ↑B ⊆ ↑A (universal)")

P("ODRL252-1.p", "Theorem", "AntiMonotone",
  "Corollary — isNoneOf Anti-Monotonicity (Concrete)", "Very Hard",
  tp("policyA","permission","use",[("spatial","isNoneOf","( geo:westernEurope )")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","isNoneOf","( geo:germany )")]),
  "leq(de,wE) → isNoneOf({wE}) ⊆ isNoneOf({de})",
  "fof(odrl252, conjecture,\n"
  "    ![X]: (\n"
  "        in_denotation_set(X, noneListWE252, isNoneOf)\n"
  "      => in_denotation_set(X, noneListDE252, isNoneOf) )).",
  extra=(
      "fof(list_252a, axiom, in_value_list(westernEurope, noneListWE252)).\n" +
      generate_list_closure("noneListWE252",["westernEurope"]) + "\n"
      "fof(list_252b, axiom, in_value_list(germany, noneListDE252)).\n" +
      generate_list_closure("noneListDE252",["germany"])),
  inc=("GEO","ODRL"),
  pl="isNoneOf anti-monotone: de ≤ wE → isNoneOf({wE}) ⊆ isNoneOf({de})")

P("ODRL253-1.p", "Theorem", "NonMonotone",
  "Counterexample — eq Is Non-Monotone", "Medium",
  tp("policyA","permission","use",[("spatial","eq","geo:bavaria")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","eq","geo:germany")]),
  "leq(bav,de): bav ∈ eq(bav) ∧ bav ∉ eq(de) → non-monotone",
  "fof(odrl253, conjecture,\n"
  "    ?[X]: ( in_denotation(X, bavaria, eq)\n"
  "          & ~in_denotation(X, germany, eq) )).",
  inc=("GEO","ODRL"),
  pl="eq non-monotone: bav ∈ eq(bav) ∧ bav ∉ eq(de) despite bav ≤ de")

P("ODRL254-1.p", "Theorem", "NonMonotone",
  "Counterexample — neq Is Non-Monotone", "Medium",
  tp("policyA","permission","use",[("spatial","neq","geo:bavaria")]) + "\n%\n%   " +
  tp("policyB","prohibition","use",[("spatial","neq","geo:germany")]),
  "leq(bav,de): de ∈ neq(bav) ∧ de ∉ neq(de) → non-monotone",
  "fof(odrl254, conjecture,\n"
  "    ?[X]: ( in_denotation(X, bavaria, neq)\n"
  "          & ~in_denotation(X, germany, neq) )).",
  inc=("GEO","ODRL"),
  pl="neq non-monotone: de ∈ neq(bav) ∧ de ∉ neq(de) despite bav ≤ de")

# ═══════════════════════════════════════════════════════════════════════════
# File generation engine
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


def write_problems(outdir, dry_run=False, use_flip=False, problems=None):
    if problems is None:
        problems = PROBLEMS
    written = []
    for p in problems:
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


def print_summary(problems=None):
    if problems is None:
        problems = PROBLEMS
    print(f"\n{'Cat':<5} {'Problem':<14} {'Expected':<22} {'Verdict':<18} "
          f"{'Diff':<11} {'Includes'}")
    print("=" * 105)
    cats = {}
    for p in problems:
        cat = problem_category(p["fn"])
        cats.setdefault(cat, []).append(p)
        incs = "+".join(p["inc"])
        has_extra = " +inline" if p["extra"] else ""
        print(f"  {cat:<3} {p['fn']:<14} {p['exp']:<22} {p['vrd']:<18} "
              f"{p['diff']:<11} {incs}{has_extra}")
    print(f"\n{'─'*50}")
    print(f"Total problems: {len(problems)}")
    print(f"\nBy category:")
    for cat, probs in sorted(cats.items()):
        print(f"  Cat {cat} ({CAT_DIR[cat].split('/')[-1]}): {len(probs)} problems")
    statuses = {}
    for p in problems:
        statuses[p["exp"]] = statuses.get(p["exp"], 0) + 1
    print(f"\nBy expected status:")
    for s, c in sorted(statuses.items()):
        print(f"  {s}: {c}")
    diffs = {}
    for p in problems:
        diffs[p["diff"]] = diffs.get(p["diff"], 0) + 1
    print(f"\nBy difficulty:")
    for d in ["Easy", "Medium", "Hard", "Very Hard", "Extreme"]:
        if d in diffs:
            print(f"  {d}: {diffs[d]}")

# ═══════════════════════════════════════════════════════════════════════════
# Runner infrastructure  (mirrors gen_hierarchy_suite.py)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class RunResult:
    filename: str
    category: int
    prover:   str
    expected: str
    actual:   str
    match:    bool
    time_s:   float
    error:    str = ""


def run_vampire(tptp_path: Path, include_dir: Path,
                timeout: int = 30) -> tuple[str, float, str]:
    """Run Vampire on a .p file. Returns (szs_status, elapsed, error)."""
    try:
        start = time.time()
        proc = subprocess.run(
            ["vampire",
             "--input_syntax", "tptp",
             "--include", str(include_dir),
             "--time_limit", str(timeout),
             str(tptp_path)],
            capture_output=True, text=True, timeout=timeout + 10,
        )
        elapsed = time.time() - start
        for line in proc.stdout.splitlines():
            if "SZS status" in line:
                status = line.split("SZS status")[1].strip().split()[0]
                return status, elapsed, ""
        err = (proc.stderr.strip() or proc.stdout.strip())[:300] or "No SZS status"
        return "Error", elapsed, err
    except FileNotFoundError:
        return "Error", 0.0, "vampire not found in PATH"
    except subprocess.TimeoutExpired:
        return "Timeout", float(timeout), ""


def _expected_status(p: dict) -> str:
    """Map p['exp'] to a Vampire SZS token."""
    exp = p["exp"]
    # Already an SZS token
    if exp in ("Theorem", "CounterSatisfiable", "Satisfiable",
               "ContradictoryAxioms", "Unknown", "GaveUp"):
        return exp
    # Semantic labels used in this suite — all prove as Theorem
    return "Theorem"


def _filter_category(problems: list, cat_arg: str | None) -> list:
    """Filter problems by category name or number string."""
    if cat_arg is None:
        return problems
    if cat_arg.isdigit():
        target = int(cat_arg)
        return [p for p in problems if problem_category(p["fn"]) == target]
    target = _CAT_NAME_MAP.get(cat_arg.lower())
    if target is None:
        available = sorted(_CAT_NAME_MAP.keys())
        print(f"Error: unknown category {cat_arg!r}")
        print(f"Available names: {', '.join(available)}")
        print(f"Available numbers: {sorted(CAT_DIR.keys())}")
        sys.exit(1)
    return [p for p in problems if problem_category(p["fn"]) == target]


def run_advanced_problems(problems: list, base: Path,
                          timeout: int = 30) -> list[RunResult]:
    """Run Vampire on .p files; return RunResult list."""
    results: list[RunResult] = []
    include_dir = base / "Problems" / "ODRL"

    has_vampire = shutil.which("vampire") is not None
    if not has_vampire:
        print("  ⚠  vampire not found — skipping benchmarks")
        return results

    GREEN, RED, RESET = "\033[32m", "\033[31m", "\033[0m"

    for p in problems:
        cat = problem_category(p["fn"])
        tptp_path = base / "Problems" / "ODRL" / CAT_DIR[cat] / p["fn"]
        if not tptp_path.exists():
            print(f"  ⚠  {p['fn']} not found — skipped (run without --run-only first)")
            continue

        exp    = _expected_status(p)
        actual, elapsed, err = run_vampire(tptp_path, include_dir, timeout)
        match  = (actual == exp)
        sym    = f"{GREEN}✓{RESET}" if match else f"{RED}✗{RESET}"
        err_str = f"  ERROR: {err}" if err else ""
        print(f"  {sym} {p['fn']:<16} exp={exp:<22} got={actual:<22} "
              f"[{elapsed:.2f}s]{err_str}")
        results.append(RunResult(
            filename=p["fn"], category=cat,
            prover="vampire", expected=exp, actual=actual,
            match=match, time_s=elapsed, error=err,
        ))

    return results


def write_csv_results(results: list[RunResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["benchmark", "category", "prover",
                    "expected", "actual", "match", "time_s", "error"])
        for r in results:
            w.writerow([r.filename, CAT_DIR.get(r.category, str(r.category)),
                        r.prover, r.expected, r.actual, r.match,
                        f"{r.time_s:.3f}", r.error])
    print(f"\n  Results → {path}")


def print_run_summary(results: list[RunResult]) -> None:
    GREEN, RED, RESET = "\033[32m", "\033[31m", "\033[0m"
    total   = len(results)
    passed  = sum(1 for r in results if r.match)
    failed  = total - passed
    errors  = sum(1 for r in results if r.error)
    timeouts = sum(1 for r in results if "Timeout" in r.actual)

    print(f"\n{'='*66}")
    print(f"  RESULTS SUMMARY")
    print(f"{'='*66}")

    by_cat: dict[int, list[RunResult]] = {}
    for r in results:
        by_cat.setdefault(r.category, []).append(r)
    for cat in sorted(by_cat):
        cat_results = by_cat[cat]
        cat_pass  = sum(1 for r in cat_results if r.match)
        cat_total = len(cat_results)
        sym = f"{GREEN}✓{RESET}" if cat_pass == cat_total else f"{RED}✗{RESET}"
        name = CAT_DIR[cat].split("/")[-1]
        print(f"  {sym}  Cat {cat:2d} {name:<24}  {cat_pass}/{cat_total}")

    c = GREEN if passed == total else RED
    print(f"\n  Total: {total}   Pass: {c}{passed}{RESET}   "
          f"Fail: {RED if failed else ''}{failed}{RESET if failed else ''}")
    if errors:
        print(f"  Errors:   {errors}")
    if timeouts:
        print(f"  Timeouts: {timeouts}")
    if passed == total:
        print(f"\n  {GREEN}✓ All problems pass{RESET}")
    else:
        print(f"\n  {RED}✗ {failed} failure(s) — investigate{RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(
        description="Generate and optionally run ODRL advanced benchmark suite.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                   # generate all .p files
  %(prog)s --run                             # generate + run Vampire
  %(prog)s --run --timeout 60               # longer timeout
  %(prog)s --run-only                        # run on existing files
  %(prog)s --run --category DAGMultiParent  # one category (name)
  %(prog)s --run --category 9               # one category (number)
  %(prog)s --dry-run                         # preview without writing
  %(prog)s --summary                         # print problem table
  %(prog)s --flip                            # use flipped conjectures
""")
    ap.add_argument("--outdir",    default="Problems/ODRL",
                    help="Root output directory (default: Problems/ODRL)")
    ap.add_argument("--base-dir",  default=".",
                    help="Repo root for --include path (default: .)")
    ap.add_argument("--category",  default=None,
                    help="Filter: category name (DAGMultiParent) or number (9)")
    ap.add_argument("--dry-run",   action="store_true",
                    help="Preview files without writing")
    ap.add_argument("--summary",   action="store_true",
                    help="Print summary table only")
    ap.add_argument("--flip",      action="store_true",
                    help="Use flipped conjectures for CounterSatisfiable problems")
    ap.add_argument("--run",       action="store_true",
                    help="Generate + run Vampire on all problems")
    ap.add_argument("--run-only",  action="store_true",
                    help="Run Vampire on existing files (skip generation)")
    ap.add_argument("--timeout",   type=int, default=30,
                    help="Vampire timeout in seconds (default: 30)")
    args = ap.parse_args()

    base = Path(args.base_dir).resolve()

    if args.summary:
        print_summary()
        return

    # ── Filter ────────────────────────────────────────────────────────────
    problems = _filter_category(PROBLEMS, args.category)
    if not problems:
        print(f"No problems matched category {args.category!r}")
        sys.exit(1)

    # ── Generate ──────────────────────────────────────────────────────────
    if not args.run_only:
        if args.dry_run:
            print("DRY RUN — no files will be written\n")
        written = write_problems(args.outdir, dry_run=args.dry_run,
                                 use_flip=args.flip, problems=problems)
        tag = "[DRY RUN] " if args.dry_run else ""
        print(f"\n{tag}Generated {len(problems)} problems → "
              f"{len(written)} files written")
        if not (args.run or args.run_only) or args.dry_run:
            print_summary(problems)
            return

    # ── Run ───────────────────────────────────────────────────────────────
    if (args.run or args.run_only) and not args.dry_run:
        cat_label = f" (category: {args.category})" if args.category else " (all)"
        print(f"\n{'='*60}")
        print(f"  RUNNING VAMPIRE{cat_label}  (timeout={args.timeout}s)")
        print(f"{'='*60}")

        results = run_advanced_problems(problems, base, timeout=args.timeout)

        if results:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            cat_tag = f"_{args.category}" if args.category else "_all"
            csv_path = base / "results" / "advanced" / f"advanced{cat_tag}_{ts}.csv"
            write_csv_results(results, csv_path)
            print_run_summary(results)

            total  = len(results)
            passed = sum(1 for r in results if r.match)
            print(f"\n  Total: {total}  Pass: {passed}  Fail: {total - passed}")


if __name__ == "__main__":
    main()