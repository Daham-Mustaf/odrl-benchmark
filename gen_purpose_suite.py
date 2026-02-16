#!/usr/bin/env python3
"""
Generate & run TPTP problem files for ODRL benchmark suite (DPV Purpose domain).
Usage:
  uv run python gen_purpose_suite.py -o Problems/ODRL/KBGrounding/Purpose
  uv run python gen_purpose_suite.py -o Problems/ODRL/KBGrounding/Purpose --run
  uv run python gen_purpose_suite.py --encoding original
  uv run python gen_purpose_suite.py --run --timeout 30 --prover eprover
  uv run python gen_purpose_suite.py --dry-run
  uv run python gen_purpose_suite.py --stats  # Print coverage matrix only

KB Stats (DPV000-0.ax):
  95 concepts | 100 edges | 285 disjoint | Depth 4 | 63 leaves | 31 internal
  Multi-parent: commercialResearch, communicationForCustomerCare,
    improveInternalCRMProcesses, nonCommercialResearch,
    personalisedAdvertising, servicePersonalisation
  Root: purpose (17 direct children)
"""
import os, sys, argparse, subprocess, re, csv, time
from datetime import datetime
from collections import defaultdict

PROBLEMS = []

def P(fn, exp, vrd, paper, diff, ttl, den, conj, flip_conj=None,
      extra="", inc=("DPV", "ODRL"), pl=None, cat=None):
    PROBLEMS.append(dict(fn=fn, exp=exp, vrd=vrd, paper=paper, diff=diff,
        ttl=ttl, den=den, conj=conj, flip_conj=flip_conj,
        extra=extra, inc=inc, pl=pl, cat=cat or "uncategorized"))

def tc(op, oper, val, ind="    "):
    return (f"{ind}odrl:constraint [\n%   {ind}  odrl:leftOperand odrl:{op} ;\n"
            f"%   {ind}  odrl:operator odrl:{oper} ;\n%   {ind}  odrl:rightOperand {val} ]")

def tp(name, rt, act, cs):
    lines = [f"ex:{name} a odrl:Set ;", f"  odrl:{rt} [", f"    odrl:action odrl:{act} ;"]
    for i, c in enumerate(cs):
        lines.append(tc(*c) + (" ;" if i < len(cs) - 1 else " ] ."))
    return "\n%   ".join(lines)

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 1: BASIC CONFLICT DETECTION (ODRL060-079)
#   Single-valued operator pairs × value relationships
# ═══════════════════════════════════════════════════════════════════════════

# --- eq × eq ---
P("ODRL060-1.p", "Theorem", "Compatible", "Definition 3, Definition 5", "Trivial",
  tp("p1", "permission", "use", [("purpose", "eq", "dpv:Marketing")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "eq", "dpv:Marketing")]),
  "⟦eq(marketing)⟧={marketing} ∩ ⟦eq(marketing)⟧={marketing} = {marketing} ≠ ∅",
  "fof(odrl060, conjecture,\n    ?[X]: ( in_denotation(X, marketing, eq)\n          & in_denotation(X, marketing, eq) )).",
  cat="basic", pl="Compatible: eq(marketing) ∩ eq(marketing) — identity")

P("ODRL061-1.p", "CounterSatisfiable", "Conflict", "Definition 3, Definition 5", "Trivial",
  tp("p1", "permission", "use", [("purpose", "eq", "dpv:Marketing")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "eq", "dpv:CustomerManagement")]),
  "⟦eq(mkt)⟧={marketing}, ⟦eq(cm)⟧={customerManagement}\n%   disjoint(marketing, customerManagement) [d_0083] → ∅",
  "fof(odrl061, conjecture,\n    ?[X]: ( in_denotation(X, marketing, eq)\n          & in_denotation(X, customerManagement, eq) )).",
  flip_conj="fof(odrl061, conjecture,\n    ![X]: ~( in_denotation(X, marketing, eq)\n           & in_denotation(X, customerManagement, eq) )).",
  cat="basic", pl="Conflict: eq(marketing) ∩ eq(customerManagement) = ∅")

# --- eq × neq ---
P("ODRL062-1.p", "Theorem", "Compatible", "Definition 3, Definition 5", "Easy",
  tp("p1", "permission", "use", [("purpose", "eq", "dpv:Marketing")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "neq", "dpv:CustomerManagement")]),
  "marketing ∈ C\\{customerManagement} → Witness: marketing",
  "fof(odrl062, conjecture,\n    ?[X]: ( in_denotation(X, marketing, eq)\n          & in_denotation(X, customerManagement, neq) )).",
  cat="basic", pl="Compatible: eq(marketing) ∩ neq(customerManagement) ≠ ∅")

P("ODRL063-1.p", "CounterSatisfiable", "Conflict", "Definition 3, Definition 5", "Easy",
  tp("p1", "permission", "use", [("purpose", "eq", "dpv:Marketing")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "neq", "dpv:Marketing")]),
  "X=marketing ∧ X≠marketing → contradiction",
  "fof(odrl063, conjecture,\n    ?[X]: ( in_denotation(X, marketing, eq)\n          & in_denotation(X, marketing, neq) )).",
  flip_conj="fof(odrl063, conjecture,\n    ![X]: ~( in_denotation(X, marketing, eq)\n           & in_denotation(X, marketing, neq) )).",
  cat="basic", pl="Conflict: eq(marketing) ∩ neq(marketing) = ∅")

# --- neq × neq ---
P("ODRL064-1.p", "Theorem", "Compatible", "Definition 3, Definition 5", "Easy",
  tp("p1", "permission", "use", [("purpose", "neq", "dpv:Marketing")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "neq", "dpv:CustomerManagement")]),
  "C\\{mkt} ∩ C\\{cm} = C\\{mkt,cm} ≠ ∅ (|C|=95)",
  "fof(odrl064, conjecture,\n    ?[X]: ( in_denotation(X, marketing, neq)\n          & in_denotation(X, customerManagement, neq) )).",
  cat="basic", pl="Compatible: neq(marketing) ∩ neq(customerManagement) ≠ ∅")

# --- eq × isA ---
P("ODRL065-1.p", "Theorem", "Compatible", "Definition 3, Definition 5", "Easy",
  tp("p1", "permission", "use", [("purpose", "eq", "dpv:Advertising")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "isA", "dpv:Marketing")]),
  "advertising ∈ ⟦isA(marketing)⟧ since advertising ≤ marketing [h_0002]",
  "fof(odrl065, conjecture,\n    ?[X]: ( in_denotation(X, advertising, eq)\n          & in_denotation(X, marketing, isA) )).",
  cat="basic", pl="Compatible: eq(advertising) ∩ isA(marketing) — child in subtree")

P("ODRL066-1.p", "CounterSatisfiable", "Conflict", "Definition 3, Definition 5", "Medium",
  tp("p1", "permission", "use", [("purpose", "eq", "dpv:Advertising")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "isA", "dpv:CustomerManagement")]),
  "advertising ≤ marketing, disjoint(marketing, customerManagement) [d_0083]\n"
  "%   → advertising ∉ ↓customerManagement (disj_downward) → ∅",
  "fof(odrl066, conjecture,\n    ?[X]: ( in_denotation(X, advertising, eq)\n          & in_denotation(X, customerManagement, isA) )).",
  flip_conj="fof(odrl066, conjecture,\n    ![X]: ~( in_denotation(X, advertising, eq)\n           & in_denotation(X, customerManagement, isA) )).",
  cat="basic", pl="Conflict: eq(advertising) ∩ isA(customerManagement) = ∅")

# --- isA × isA ---
P("ODRL067-1.p", "Theorem", "Compatible", "Definition 3, Definition 5", "Easy",
  tp("p1", "permission", "use", [("purpose", "isA", "dpv:Marketing")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "isA", "dpv:Advertising")]),
  "⟦isA(advertising)⟧ ⊆ ⟦isA(marketing)⟧ since advertising ≤ marketing\n%   Witness: advertising",
  "fof(odrl067, conjecture,\n    ?[X]: ( in_denotation(X, marketing, isA)\n          & in_denotation(X, advertising, isA) )).",
  cat="basic", pl="Compatible: isA(marketing) ∩ isA(advertising) — subtree overlap")

P("ODRL068-1.p", "CounterSatisfiable", "Conflict", "Definition 3, Definition 5", "Medium",
  tp("p1", "permission", "use", [("purpose", "isA", "dpv:Marketing")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "isA", "dpv:EnforceSecurity")]),
  "disjoint(marketing, enforceSecurity) [d_0113] → disj_downward → ∅",
  "fof(odrl068, conjecture,\n    ?[X]: ( in_denotation(X, marketing, isA)\n          & in_denotation(X, enforceSecurity, isA) )).",
  flip_conj="fof(odrl068, conjecture,\n    ![X]: ~( in_denotation(X, marketing, isA)\n           & in_denotation(X, enforceSecurity, isA) )).",
  cat="basic", pl="Conflict: isA(marketing) ∩ isA(enforceSecurity) = ∅")

# --- isA × isPartOf equivalence ---
P("ODRL069-1.p", "Theorem", "Confirmed", "Definition 3 (isA≡isPartOf)", "Trivial",
  "c1: [ odrl:operator odrl:isA ; odrl:rightOperand dpv:Marketing ] .\n"
  "%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand dpv:Marketing ] .",
  "TAUTOLOGY: isA and isPartOf have identical denotation (Def 3).",
  "fof(odrl069, conjecture,\n    ![X]: ( in_denotation(X, marketing, isA)\n        <=> in_denotation(X, marketing, isPartOf) )).",
  cat="basic", pl="Tautological equivalence: isA(marketing) ≡ isPartOf(marketing)")

# --- hasPart × eq ---
P("ODRL070-1.p", "Theorem", "Compatible", "Definition 3, Definition 5", "Medium",
  tp("p1", "permission", "use", [("purpose", "hasPart", "dpv:Advertising")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "eq", "dpv:Marketing")]),
  "⟦hasPart(advertising)⟧ = {x | advertising ≤ x} = {advertising, marketing, purpose}\n%   marketing ∈ ⟦eq(marketing)⟧ → Witness: marketing",
  "fof(odrl070, conjecture,\n    ?[X]: ( in_denotation(X, advertising, hasPart)\n          & in_denotation(X, marketing, eq) )).",
  cat="basic", pl="Compatible: hasPart(advertising) ∩ eq(marketing) ≠ ∅")

P("ODRL071-1.p", "CounterSatisfiable", "Conflict", "Definition 3, Definition 5, Lemma 1", "Hard",
  tp("p1", "permission", "use", [("purpose", "hasPart", "dpv:Advertising")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "eq", "dpv:FraudPreventionAndDetection")]),
  "⟦hasPart(adv)⟧={adv,marketing,purpose}\n%   fraudPrevention ≤ enforceSecurity, disjoint(enforceSecurity, marketing)\n%   fraudPrevention ∉ {adv, marketing, purpose}… but purpose is root!\n%   Actually: purpose IS in hasPart(adv), and eq(fraud)={fraud}.\n%   fraud ∉ {adv, mkt, purpose} → ∅ (needs UNA for distinct from purpose)",
  "fof(odrl071, conjecture,\n    ?[X]: ( in_denotation(X, advertising, hasPart)\n          & in_denotation(X, fraudPreventionAndDetection, eq) )).",
  flip_conj="fof(odrl071, conjecture,\n    ![X]: ~( in_denotation(X, advertising, hasPart)\n           & in_denotation(X, fraudPreventionAndDetection, eq) )).",
  cat="basic", pl="Conflict: hasPart(advertising) ∩ eq(fraudPrevention) = ∅")

# --- hasPart × isA ---
P("ODRL072-1.p", "Theorem", "Compatible", "Definition 3, Definition 5", "Medium",
  tp("p1", "permission", "use", [("purpose", "hasPart", "dpv:DirectMarketing")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "isA", "dpv:Purpose")]),
  "⟦hasPart(directMkt)⟧ = {directMkt, marketing, purpose}\n%   ⟦isA(purpose)⟧ = C (everything). Witness: anything",
  "fof(odrl072, conjecture,\n    ?[X]: ( in_denotation(X, directMarketing, hasPart)\n          & in_denotation(X, purpose, isA) )).",
  cat="basic", pl="Compatible: hasPart(directMarketing) ∩ isA(purpose) — root covers all")

# --- hasPart × hasPart ---
P("ODRL073-1.p", "Theorem", "Compatible", "Definition 3, Definition 5", "Medium",
  tp("p1", "permission", "use", [("purpose", "hasPart", "dpv:Advertising")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "hasPart", "dpv:DirectMarketing")]),
  "Common ancestor: marketing, purpose. Witness: marketing",
  "fof(odrl073, conjecture,\n    ?[X]: ( in_denotation(X, advertising, hasPart)\n          & in_denotation(X, directMarketing, hasPart) )).",
  cat="basic", pl="Compatible: hasPart(advertising) ∩ hasPart(directMarketing) — common ancestor")

# --- neq × isA ---
P("ODRL074-1.p", "Theorem", "Compatible", "Definition 3, Definition 5", "Medium",
  tp("p1", "permission", "use", [("purpose", "neq", "dpv:Marketing")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "isA", "dpv:ServiceProvision")]),
  "⟦neq(mkt)⟧=C\\{mkt}, ⟦isA(sp)⟧=↓sp. Witness: paymentManagement",
  "fof(odrl074, conjecture,\n    ?[X]: ( in_denotation(X, marketing, neq)\n          & in_denotation(X, serviceProvision, isA) )).",
  cat="basic", pl="Compatible: neq(marketing) ∩ isA(serviceProvision) ≠ ∅")

# --- neq × hasPart ---
P("ODRL075-1.p", "Theorem", "Compatible", "Definition 3, Definition 5", "Medium",
  tp("p1", "permission", "use", [("purpose", "neq", "dpv:Marketing")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "hasPart", "dpv:Advertising")]),
  "⟦hasPart(adv)⟧={adv, marketing, purpose}\n%   ⟦neq(mkt)⟧=C\\{mkt}. Witness: advertising (adv≠mkt)",
  "fof(odrl075, conjecture,\n    ?[X]: ( in_denotation(X, marketing, neq)\n          & in_denotation(X, advertising, hasPart) )).",
  cat="basic", pl="Compatible: neq(marketing) ∩ hasPart(advertising) ≠ ∅")

# --- Deep hierarchy: 4-level chain ---
P("ODRL076-1.p", "Theorem", "Compatible", "Definition 2, Definition 3", "Medium-Hard",
  tp("p1", "permission", "use", [("purpose", "isA", "dpv:Purpose")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "eq", "dpv:TargetedAdvertising")]),
  "Depth-4 chain: targetedAdv→personalisedAdv→advertising→marketing→purpose\n%   targetedAdvertising ∈ ⟦isA(purpose)⟧ via 4 transitivity steps",
  "fof(odrl076, conjecture,\n    ?[X]: ( in_denotation(X, purpose, isA)\n          & in_denotation(X, targetedAdvertising, eq) )).",
  cat="basic", pl="Compatible: 4-level transitivity chain to root")

P("ODRL077-1.p", "Theorem", "Confirmed", "Definition 7 (Subsumption)", "Medium-Hard",
  "c1: isA(targetedAdvertising), c2: isA(marketing)",
  "targetedAdv ≤ personalisedAdv ≤ advertising ≤ marketing\n%   ⟦isA(targetedAdv)⟧ ⊆ ⟦isA(marketing)⟧ via depth-4 chain",
  "fof(odrl077, conjecture,\n    ![X]: ( in_denotation(X, targetedAdvertising, isA)\n          => in_denotation(X, marketing, isA) )).",
  cat="basic", pl="Subsumption across 4-level chain: isA(targetedAdv) ⊆ isA(marketing)")

# --- Large fan-out: root's 17 children ---
P("ODRL078-1.p", "CounterSatisfiable", "Conflict", "Definition 2, Definition 5", "Medium",
  "17 children of purpose are pairwise disjoint.\n"
  "%   Test: isA(marketing) ∩ isA(publicBenefit) = ∅",
  "disjoint(marketing, publicBenefit) [d_0182] → disj_downward → ∅",
  "fof(odrl078, conjecture,\n    ?[X]: ( in_denotation(X, marketing, isA)\n          & in_denotation(X, publicBenefit, isA) )).",
  flip_conj="fof(odrl078, conjecture,\n    ![X]: ~( in_denotation(X, marketing, isA)\n           & in_denotation(X, publicBenefit, isA) )).",
  cat="basic", pl="Conflict: isA(marketing) ∩ isA(publicBenefit) — root siblings")

P("ODRL079-1.p", "CounterSatisfiable", "Conflict", "Definition 2, Definition 5", "Hard",
  "Deep leaves from different root-level subtrees.\n"
  "%   targetedAdvertising (under marketing) vs maintainFraudDatabase (under enforceSecurity)",
  "marketing ⊥⊥ enforceSecurity [d_0113] → disj_downward to leaves → ∅\n"
  "%   Prover must chain: targetedAdv→…→marketing ⊥⊥ enforceSecurity←…←maintainFraud",
  "fof(odrl079, conjecture,\n    ?[X]: ( in_denotation(X, targetedAdvertising, isA)\n          & in_denotation(X, maintainFraudDatabase, isA) )).",
  flip_conj="fof(odrl079, conjecture,\n    ![X]: ~( in_denotation(X, targetedAdvertising, isA)\n           & in_denotation(X, maintainFraudDatabase, isA) )).",
  cat="basic", pl="Conflict: deep leaves across disjoint subtrees (depth 4 × depth 4)")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 2: SET-VALUED OPERATORS (ODRL080-092)
# ═══════════════════════════════════════════════════════════════════════════

# --- isAnyOf ---
P("ODRL080-1.p", "Theorem", "Compatible", "Definition 3 (isAnyOf), Definition 5", "Medium",
  tp("p1", "permission", "use", [("purpose", "isAnyOf", "( dpv:Marketing dpv:EnforceSecurity )")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "eq", "dpv:Advertising")]),
  "⟦isAnyOf({mkt,sec})⟧ = ↓mkt ∪ ↓sec. advertising ∈ ↓mkt → Witness",
  "fof(odrl080, conjecture,\n    ?[X]: ( in_denotation_set(X, set080, isAnyOf)\n          & in_denotation(X, advertising, eq) )).",
  extra="fof(list_080_1, axiom, in_value_list(marketing, set080)).\nfof(list_080_2, axiom, in_value_list(enforceSecurity, set080)).",
  cat="set", pl="Compatible: isAnyOf({marketing, enforceSecurity}) ∩ eq(advertising) ≠ ∅")

P("ODRL081-1.p", "CounterSatisfiable", "Conflict", "Definition 3 (isAnyOf), Definition 5", "Hard",
  tp("p1", "permission", "use", [("purpose", "isAnyOf", "( dpv:Marketing dpv:EnforceSecurity )")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "eq", "dpv:LegalCompliance")]),
  "legalCompliance ≤ fulfilmentOfObligation.\n"
  "%   disjoint(marketing, fulfilmentOfObligation) [d_0136]\n"
  "%   disjoint(enforceSecurity, fulfilmentOfObligation) [d_0111]\n"
  "%   → legalCompliance ∉ ↓mkt ∪ ↓sec → ∅",
  "fof(odrl081, conjecture,\n    ?[X]: ( in_denotation_set(X, set081, isAnyOf)\n          & in_denotation(X, legalCompliance, eq) )).",
  flip_conj="fof(odrl081, conjecture,\n    ![X]: ~( in_denotation_set(X, set081, isAnyOf)\n           & in_denotation(X, legalCompliance, eq) )).",
  extra="fof(list_081_1, axiom, in_value_list(marketing, set081)).\nfof(list_081_2, axiom, in_value_list(enforceSecurity, set081)).",
  cat="set", pl="Conflict: isAnyOf({marketing, enforceSecurity}) ∩ eq(legalCompliance) = ∅")

# --- isAnyOf × isAnyOf ---
P("ODRL082-1.p", "Theorem", "Compatible", "Definition 3 (isAnyOf), Definition 5", "Medium",
  "isAnyOf({marketing, customerManagement}) ∩ isAnyOf({advertising, customerCare})",
  "advertising ≤ marketing → advertising ∈ both → Compatible",
  "fof(odrl082, conjecture,\n    ?[X]: ( in_denotation_set(X, set082a, isAnyOf)\n          & in_denotation_set(X, set082b, isAnyOf) )).",
  extra=("fof(l082a_1, axiom, in_value_list(marketing, set082a)).\n"
         "fof(l082a_2, axiom, in_value_list(customerManagement, set082a)).\n"
         "fof(l082b_1, axiom, in_value_list(advertising, set082b)).\n"
         "fof(l082b_2, axiom, in_value_list(customerCare, set082b))."),
  cat="set", pl="Compatible: isAnyOf × isAnyOf with subtree overlap")

# --- isAllOf ---
P("ODRL083-1.p", "CounterSatisfiable", "Conflict", "Definition 3 (isAllOf), Definition 5", "Hard",
  tp("p1", "permission", "use", [("purpose", "isAllOf", "( dpv:Marketing dpv:EnforceSecurity )")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "eq", "dpv:Advertising")]),
  "disjoint(marketing, enforceSecurity) [d_0113] → ⟦isAllOf⟧ = ∅ → ∅ ∩ anything = ∅",
  "fof(odrl083, conjecture,\n    ?[X]: ( in_denotation_set(X, set083, isAllOf)\n          & in_denotation(X, advertising, eq) )).",
  flip_conj="fof(odrl083, conjecture,\n    ![X]: ~( in_denotation_set(X, set083, isAllOf)\n           & in_denotation(X, advertising, eq) )).",
  extra="fof(list_083_1, axiom, in_value_list(marketing, set083)).\nfof(list_083_2, axiom, in_value_list(enforceSecurity, set083)).",
  cat="set", pl="Conflict: isAllOf({marketing, enforceSecurity}) = ∅ (disjoint parents)")

P("ODRL084-1.p", "Theorem", "Compatible", "Definition 3 (isAllOf), Definition 5", "Medium",
  tp("p1", "permission", "use", [("purpose", "isAllOf", "( dpv:Marketing dpv:Advertising )")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "eq", "dpv:Advertising")]),
  "advertising ≤ marketing → advertising ∈ ↓mkt ∩ ↓adv\n%   → ⟦isAllOf⟧ = ↓advertising. Witness: advertising",
  "fof(odrl084, conjecture,\n    ?[X]: ( in_denotation_set(X, set084, isAllOf)\n          & in_denotation(X, advertising, eq) )).",
  extra="fof(list_084_1, axiom, in_value_list(marketing, set084)).\nfof(list_084_2, axiom, in_value_list(advertising, set084)).",
  cat="set", pl="Compatible: isAllOf({marketing, advertising}) — ancestor+descendant")

# --- isAllOf × isAnyOf ---
P("ODRL085-1.p", "Theorem", "Compatible", "Definition 3 (isAllOf/isAnyOf), Definition 5", "Hard",
  "isAllOf({marketing, advertising}) ∩ isAnyOf({advertising, directMarketing})",
  "⟦isAllOf⟧=↓adv, ⟦isAnyOf⟧=↓adv∪↓directMkt. Witness: advertising",
  "fof(odrl085, conjecture,\n    ?[X]: ( in_denotation_set(X, all085, isAllOf)\n          & in_denotation_set(X, any085, isAnyOf) )).",
  extra=("fof(l085a_1, axiom, in_value_list(marketing, all085)).\n"
         "fof(l085a_2, axiom, in_value_list(advertising, all085)).\n"
         "fof(l085b_1, axiom, in_value_list(advertising, any085)).\n"
         "fof(l085b_2, axiom, in_value_list(directMarketing, any085))."),
  cat="set", pl="Compatible: isAllOf × isAnyOf with overlap")

# --- isNoneOf ---
P("ODRL086-1.p", "Theorem", "Compatible", "Definition 3 (isNoneOf), Definition 5", "Hard",
  tp("p1", "permission", "use", [("purpose", "isNoneOf", "( dpv:Marketing dpv:EnforceSecurity )")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "isA", "dpv:ServiceProvision")]),
  "Witness: paymentManagement ≤ serviceProvision,\n"
  "%   disjoint(serviceProvision, marketing) [d_0185],\n"
  "%   disjoint(serviceProvision, enforceSecurity) [d_0120] → paymentMgmt ∉ excluded",
  "fof(odrl086, conjecture,\n    ?[X]: ( in_denotation_set(X, none086, isNoneOf)\n          & in_denotation(X, serviceProvision, isA) )).",
  extra="fof(list_086_1, axiom, in_value_list(marketing, none086)).\nfof(list_086_2, axiom, in_value_list(enforceSecurity, none086)).",
  cat="set", pl="Compatible: isNoneOf({marketing, enforceSecurity}) ∩ isA(serviceProvision) ≠ ∅")

P("ODRL087-1.p", "CounterSatisfiable", "Conflict", "Definition 3 (isNoneOf), Definition 5", "Very Hard",
  tp("p1", "permission", "use", [("purpose", "isNoneOf", "( dpv:Purpose )")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "isA", "dpv:Marketing")]),
  "isNoneOf({purpose}) = C \\ ↓purpose = C \\ C = ∅ (purpose is root)\n%   ∅ ∩ anything = ∅ → Conflict",
  "fof(odrl087, conjecture,\n    ?[X]: ( in_denotation_set(X, none087, isNoneOf)\n          & in_denotation(X, marketing, isA) )).",
  flip_conj="fof(odrl087, conjecture,\n    ![X]: ~( in_denotation_set(X, none087, isNoneOf)\n           & in_denotation(X, marketing, isA) )).",
  extra="fof(list_087_1, axiom, in_value_list(purpose, none087)).",
  cat="set", pl="Conflict: isNoneOf({purpose}) = ∅ (root exclusion)")

# --- isNoneOf × isNoneOf ---
P("ODRL088-1.p", "Theorem", "Compatible", "Definition 3 (isNoneOf), Definition 5", "Hard",
  "isNoneOf({marketing}) ∩ isNoneOf({enforceSecurity})",
  "C\\↓mkt ∩ C\\↓sec. Witness: legalCompliance (under fulfilmentOfObligation,\n"
  "%   disjoint from both marketing and enforceSecurity)",
  "fof(odrl088, conjecture,\n    ?[X]: ( in_denotation_set(X, none088a, isNoneOf)\n          & in_denotation_set(X, none088b, isNoneOf) )).",
  extra=("fof(l088a_1, axiom, in_value_list(marketing, none088a)).\n"
         "fof(l088b_1, axiom, in_value_list(enforceSecurity, none088b))."),
  cat="set", pl="Compatible: isNoneOf × isNoneOf — large exclusions still overlap")

# --- isAllOf × isNoneOf ---
P("ODRL089-1.p", "CounterSatisfiable", "Conflict", "Definition 3, Definition 5", "Very Hard",
  "isAllOf({marketing, advertising}) ∩ isNoneOf({marketing})",
  "⟦isAllOf⟧=↓adv ⊆ ↓mkt, isNoneOf excludes ↓mkt → ∅",
  "fof(odrl089, conjecture,\n    ?[X]: ( in_denotation_set(X, all089, isAllOf)\n          & in_denotation_set(X, none089, isNoneOf) )).",
  flip_conj="fof(odrl089, conjecture,\n    ![X]: ~( in_denotation_set(X, all089, isAllOf)\n           & in_denotation_set(X, none089, isNoneOf) )).",
  extra=("fof(l089a_1, axiom, in_value_list(marketing, all089)).\n"
         "fof(l089a_2, axiom, in_value_list(advertising, all089)).\n"
         "fof(l089b_1, axiom, in_value_list(marketing, none089))."),
  cat="set", pl="Conflict: isAllOf({mkt,adv}) ⊆ ↓mkt, isNoneOf({mkt}) excludes ↓mkt")

# --- eq × isAnyOf ---
P("ODRL090-1.p", "Theorem", "Compatible", "Definition 3 (isAnyOf), Definition 5", "Easy",
  "eq(advertising) ∩ isAnyOf({marketing, enforceSecurity})",
  "advertising ∈ ↓marketing → Witness",
  "fof(odrl090, conjecture,\n    ?[X]: ( in_denotation(X, advertising, eq)\n          & in_denotation_set(X, set090, isAnyOf) )).",
  extra="fof(l090_1, axiom, in_value_list(marketing, set090)).\nfof(l090_2, axiom, in_value_list(enforceSecurity, set090)).",
  cat="set", pl="Compatible: eq(advertising) ∩ isAnyOf({marketing, enforceSecurity})")

# --- eq × isNoneOf ---
P("ODRL091-1.p", "Theorem", "Compatible", "Definition 3 (isNoneOf), Definition 5", "Medium",
  "eq(legalCompliance) ∩ isNoneOf({marketing, enforceSecurity})",
  "legalCompliance ≤ fulfilmentOfObligation, disjoint from both → Witness",
  "fof(odrl091, conjecture,\n    ?[X]: ( in_denotation(X, legalCompliance, eq)\n          & in_denotation_set(X, none091, isNoneOf) )).",
  extra="fof(l091_1, axiom, in_value_list(marketing, none091)).\nfof(l091_2, axiom, in_value_list(enforceSecurity, none091)).",
  cat="set", pl="Compatible: eq(legalCompliance) ∩ isNoneOf({marketing, enforceSecurity})")

P("ODRL092-1.p", "CounterSatisfiable", "Conflict", "Definition 3 (isNoneOf), Definition 5", "Medium",
  "eq(advertising) ∩ isNoneOf({marketing})",
  "advertising ≤ marketing → advertising ∈ ↓mkt → excluded → ∅",
  "fof(odrl092, conjecture,\n    ?[X]: ( in_denotation(X, advertising, eq)\n          & in_denotation_set(X, none092, isNoneOf) )).",
  flip_conj="fof(odrl092, conjecture,\n    ![X]: ~( in_denotation(X, advertising, eq)\n           & in_denotation_set(X, none092, isNoneOf) )).",
  extra="fof(l092_1, axiom, in_value_list(marketing, none092)).",
  cat="set", pl="Conflict: eq(advertising) ∩ isNoneOf({marketing}) — child excluded by ancestor")

# --- isAnyOf × isPartOf ---
P("ODRL093-1.p", "Theorem", "Compatible", "Definition 3, Definition 5", "Medium",
  "isAnyOf({advertising, customerCare}) ∩ isPartOf(customerManagement)",
  "customerCare ≤ customerManagement → customerCare ∈ both → Witness",
  "fof(odrl093, conjecture,\n    ?[X]: ( in_denotation_set(X, set093, isAnyOf)\n          & in_denotation(X, customerManagement, isPartOf) )).",
  extra="fof(l093_1, axiom, in_value_list(advertising, set093)).\nfof(l093_2, axiom, in_value_list(customerCare, set093)).",
  cat="set", pl="Compatible: isAnyOf({advertising, customerCare}) ∩ isPartOf(customerMgmt)")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 3: MULTI-PARENT / KB CONSISTENCY (ODRL094-103)
#   The 6 multi-parent concepts that create contradictions under
#   disj_downward + the hierarchy. THE HARDEST AND MOST NOVEL TESTS.
# ═══════════════════════════════════════════════════════════════════════════

P("ODRL094-1.p", "Theorem", "Compatible", "Definition 3, Multi-parent", "Very Hard",
  "commercialResearch ≤ commercialPurpose ∧ commercialResearch ≤ researchAndDevelopment\n"
  "%   disjoint(commercialPurpose, researchAndDevelopment) [d_0044]\n"
  "%   Under disj_downward: commercialResearch ⊥⊥ researchAndDevelopment AND\n"
  "%   commercialResearch ≤ researchAndDevelopment → Lemma 1 contradiction!\n"
  "%   THIS PROBLEM TESTS WHETHER THE KB IS CONSISTENT.",
  "isA(commercialPurpose) ∩ isA(researchAndDevelopment)\n"
  "%   Expected: Compatible (commercialResearch is witness)\n"
  "%   BUT: with disj_downward, KB becomes inconsistent → Theorem trivially",
  "fof(odrl094, conjecture,\n    ?[X]: ( in_denotation(X, commercialPurpose, isA)\n          & in_denotation(X, researchAndDevelopment, isA) )).",
  cat="multiparent",
  pl="Multi-parent: commercialResearch bridges disjoint subtrees (KB consistency test)")

P("ODRL095-1.p", "Theorem", "Compatible", "Definition 3, Multi-parent", "Very Hard",
  "personalisedAdvertising ≤ advertising(≤marketing) ∧ personalisedAdvertising ≤ personalisation\n"
  "%   disjoint(marketing, personalisation) [d_0181]\n"
  "%   Under disj_downward: contradiction (Lemma 1)",
  "isA(marketing) ∩ isA(personalisation)\n"
  "%   Witness: personalisedAdvertising (if consistent)\n"
  "%   KB inconsistency: ex falso if disj_downward propagates",
  "fof(odrl095, conjecture,\n    ?[X]: ( in_denotation(X, marketing, isA)\n          & in_denotation(X, personalisation, isA) )).",
  cat="multiparent",
  pl="Multi-parent: personalisedAdvertising bridges marketing ⊥⊥ personalisation")

P("ODRL096-1.p", "Theorem", "Compatible", "Definition 3, Multi-parent", "Very Hard",
  "servicePersonalisation ≤ personalisation ∧ servicePersonalisation ≤ serviceProvision\n"
  "%   disjoint(personalisation, serviceProvision) [d_0218]",
  "isA(personalisation) ∩ isA(serviceProvision)\n"
  "%   Witness: servicePersonalisation (if consistent)",
  "fof(odrl096, conjecture,\n    ?[X]: ( in_denotation(X, personalisation, isA)\n          & in_denotation(X, serviceProvision, isA) )).",
  cat="multiparent",
  pl="Multi-parent: servicePersonalisation bridges personalisation ⊥⊥ serviceProvision")

P("ODRL097-1.p", "Theorem", "Compatible", "Definition 3, Multi-parent", "Very Hard",
  "communicationForCustomerCare ≤ communicationManagement ∧\n"
  "%   communicationForCustomerCare ≤ customerCare ≤ customerManagement\n"
  "%   disjoint(communicationManagement, customerManagement) [d_0049]",
  "isA(communicationManagement) ∩ isA(customerManagement)\n"
  "%   Witness: communicationForCustomerCare (if consistent)",
  "fof(odrl097, conjecture,\n    ?[X]: ( in_denotation(X, communicationManagement, isA)\n          & in_denotation(X, customerManagement, isA) )).",
  cat="multiparent",
  pl="Multi-parent: communicationForCustomerCare bridges commMgmt ⊥⊥ custMgmt")

P("ODRL098-1.p", "Theorem", "Compatible", "Definition 3, Multi-parent", "Very Hard",
  "nonCommercialResearch ≤ nonCommercialPurpose ∧ nonCommercialResearch ≤ researchAndDevelopment\n"
  "%   disjoint(nonCommercialPurpose, researchAndDevelopment) [d_0194]",
  "isA(nonCommercialPurpose) ∩ isA(researchAndDevelopment)",
  "fof(odrl098, conjecture,\n    ?[X]: ( in_denotation(X, nonCommercialPurpose, isA)\n          & in_denotation(X, researchAndDevelopment, isA) )).",
  cat="multiparent",
  pl="Multi-parent: nonCommercialResearch bridges nonCommPurpose ⊥⊥ R&D")

P("ODRL099-1.p", "Theorem", "Compatible", "Definition 3, Multi-parent", "Very Hard",
  "improveInternalCRMProcesses ≤ customerRelationshipManagement(≤customerManagement)\n"
  "%   ∧ improveInternalCRMProcesses ≤ optimisationForController(≤serviceOptimisation≤serviceProvision)\n"
  "%   disjoint(customerManagement, serviceProvision) [d_0090]",
  "isA(customerManagement) ∩ isA(serviceProvision)\n"
  "%   Witness: improveInternalCRMProcesses (longest chain, 2 hops each side)",
  "fof(odrl099, conjecture,\n    ?[X]: ( in_denotation(X, customerManagement, isA)\n          & in_denotation(X, serviceProvision, isA) )).",
  cat="multiparent",
  pl="Multi-parent: improveInternalCRMProcesses bridges custMgmt ⊥⊥ servProv (deepest)")

# --- Explicit consistency check ---
P("ODRL100-1.p", "CounterSatisfiable", "Consistent", "Lemma 1 (disj-order consistency)", "Very Hard",
  "META-TEST: Can we derive ⊥ from the KB?\n"
  "%   If disj_downward is active, multi-parent nodes create contradictions.",
  "Conjecture: ∃ concept that is both ≤ X and ⊥⊥ X → should be impossible\n"
  "%   by Lemma 1. If Theorem: KB is INCONSISTENT.",
  "fof(odrl100, conjecture,\n    ?[X,Y]: ( leq(X, Y) & disjoint(X, Y) )).",
  flip_conj="fof(odrl100, conjecture,\n    ![X,Y]: ~( leq(X, Y) & disjoint(X, Y) )).",
  cat="multiparent",
  pl="KB consistency: ¬∃(X≤Y ∧ X⊥⊥Y) — Lemma 1 meta-test")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 4: SUBSUMPTION (ODRL104-113)
# ═══════════════════════════════════════════════════════════════════════════

P("ODRL104-1.p", "Theorem", "Confirmed", "Definition 7", "Easy",
  "c1: isA(advertising), c2: isA(marketing)",
  "advertising ≤ marketing → ↓adv ⊆ ↓mkt",
  "fof(odrl104, conjecture,\n    ![X]: ( in_denotation(X, advertising, isA)\n          => in_denotation(X, marketing, isA) )).",
  cat="subsumption", pl="Subsumption: isA(advertising) ⊆ isA(marketing)")

P("ODRL105-1.p", "CounterSatisfiable", "Refuted", "Definition 7", "Medium",
  "c1: isA(marketing), c2: isA(advertising)",
  "Counterexample: directMarketing ∈ ↓mkt but directMarketing ∉ ↓adv",
  "fof(odrl105, conjecture,\n    ![X]: ( in_denotation(X, marketing, isA)\n          => in_denotation(X, advertising, isA) )).",
  flip_conj="fof(odrl105, conjecture,\n    ?[X]: ( in_denotation(X, marketing, isA)\n          & ~in_denotation(X, advertising, isA) )).",
  cat="subsumption", pl="Subsumption refuted: isA(marketing) ⊄ isA(advertising)")

P("ODRL106-1.p", "Theorem", "Confirmed", "Definition 7 (cross-operator)", "Easy",
  "c1: eq(directMarketing), c2: isA(marketing)",
  "directMarketing ≤ marketing → {directMarketing} ⊆ ↓mkt",
  "fof(odrl106, conjecture,\n    ![X]: ( in_denotation(X, directMarketing, eq)\n          => in_denotation(X, marketing, isA) )).",
  cat="subsumption", pl="Cross-operator: eq(directMarketing) ⊆ isA(marketing)")

P("ODRL107-1.p", "Theorem", "Confirmed", "Definition 7 (hasPart contravariance)", "Medium",
  "c1: hasPart(marketing), c2: hasPart(advertising)",
  "⟦hasPart(mkt)⟧ = {mkt, purpose}\n"
  "%   ⟦hasPart(adv)⟧ = {adv, mkt, purpose}\n"
  "%   {mkt,purpose} ⊆ {adv,mkt,purpose} → Confirmed (counterintuitive!)",
  "fof(odrl107, conjecture,\n    ![X]: ( in_denotation(X, marketing, hasPart)\n          => in_denotation(X, advertising, hasPart) )).",
  cat="subsumption", pl="Counterintuitive: hasPart(marketing) ⊆ hasPart(advertising)")

P("ODRL108-1.p", "CounterSatisfiable", "Refuted", "Definition 7", "Medium",
  "c1: hasPart(advertising), c2: hasPart(marketing)",
  "Counterexample: advertising ∈ ⟦hasPart(adv)⟧ but advertising ∉ ⟦hasPart(mkt)⟧",
  "fof(odrl108, conjecture,\n    ![X]: ( in_denotation(X, advertising, hasPart)\n          => in_denotation(X, marketing, hasPart) )).",
  flip_conj="fof(odrl108, conjecture,\n    ?[X]: ( in_denotation(X, advertising, hasPart)\n          & ~in_denotation(X, marketing, hasPart) )).",
  cat="subsumption", pl="Subsumption refuted: hasPart(advertising) ⊄ hasPart(marketing)")

# --- Conflict propagation ---
P("ODRL109-1.p", "CounterSatisfiable", "Conflict", "Lemma 2 (Conflict Propagation)", "Medium",
  "c1=isA(advertising), c2=isA(marketing), c3=isA(enforceSecurity)\n"
  "%   c1⊑c2 (ODRL104) ∧ conflict(c2,c3) (ODRL068) → conflict(c1,c3)",
  "advertising ≤ marketing, marketing ⊥⊥ enforceSecurity → advertising ⊥⊥ enforceSecurity",
  "fof(odrl109, conjecture,\n    ?[X]: ( in_denotation(X, advertising, isA)\n          & in_denotation(X, enforceSecurity, isA) )).",
  flip_conj="fof(odrl109, conjecture,\n    ![X]: ~( in_denotation(X, advertising, isA)\n           & in_denotation(X, enforceSecurity, isA) )).",
  cat="subsumption", pl="Conflict propagation: isA(adv)⊑isA(mkt) ∧ conflict(mkt,sec) → conflict(adv,sec)")

P("ODRL110-1.p", "Theorem", "Confirmed", "Definition 7 (cross neq)", "Medium",
  "c1: eq(advertising), c2: neq(customerManagement)",
  "advertising ≤ marketing, disjoint(marketing, customerManagement)\n"
  "%   → advertising ≠ customerManagement → {adv} ⊆ C\\{cm}",
  "fof(odrl110, conjecture,\n    ![X]: ( in_denotation(X, advertising, eq)\n          => in_denotation(X, customerManagement, neq) )).",
  cat="subsumption", pl="Cross-operator: eq(advertising) ⊆ neq(customerManagement)")

# --- Redundancy detection ---
P("ODRL111-1.p", "Theorem", "Confirmed", "Definition 7 (redundancy)", "Easy",
  "Same rule, two constraints:\n"
  "%   c1: isA(advertising), c2: isA(marketing)\n"
  "%   c1 ⊆ c2 → c2 is redundant (subsumed by c1)",
  "Policy simplification: remove redundant broader constraint.",
  "fof(odrl111, conjecture,\n    ![X]: ( in_denotation(X, advertising, isA)\n          => in_denotation(X, marketing, isA) )).",
  cat="subsumption", pl="Redundancy: isA(advertising) ⊆ isA(marketing) — broader is redundant")

# --- 3-level subsumption chain ---
P("ODRL112-1.p", "Theorem", "Confirmed", "Definition 7 (transitivity)", "Medium-Hard",
  "c1: isA(targetedAdvertising) ⊆ c2: isA(advertising) ⊆ c3: isA(marketing)",
  "Subsumption transitivity over 3 constraints.",
  "fof(odrl112, conjecture,\n    ![X]: ( in_denotation(X, targetedAdvertising, isA)\n          => in_denotation(X, marketing, isA) )).",
  cat="subsumption", pl="Transitive subsumption: isA(targetedAdv) ⊆ isA(adv) ⊆ isA(marketing)")

P("ODRL113-1.p", "CounterSatisfiable", "Refuted", "Definition 7", "Medium",
  "c1: neq(marketing), c2: isA(enforceSecurity)",
  "Counterexample: purpose ∈ C\\{marketing} but purpose ∉ ↓enforceSecurity",
  "fof(odrl113, conjecture,\n    ![X]: ( in_denotation(X, marketing, neq)\n          => in_denotation(X, enforceSecurity, isA) )).",
  flip_conj="fof(odrl113, conjecture,\n    ?[X]: ( in_denotation(X, marketing, neq)\n          & ~in_denotation(X, enforceSecurity, isA) )).",
  cat="subsumption", pl="Subsumption refuted: neq(marketing) ⊄ isA(enforceSecurity)")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 5: COMPOSITION (ODRL114-124)
#   Multi-operand verdicts using DPV purpose × GEO spatial
# ═══════════════════════════════════════════════════════════════════════════

P("ODRL114-1.p", "Theorem", "Compatible", "Definition 6 (AND)", "Medium",
  tp("p1", "permission", "use", [("purpose", "isA", "dpv:Marketing"), ("spatial", "isPartOf", "geo:Europe")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "eq", "dpv:Advertising"), ("spatial", "eq", "geo:Germany")]),
  "V_purpose=Compatible(adv≤mkt), V_spatial=Compatible(de≤eu) → AND=Compatible",
  "fof(odrl114, conjecture,\n    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)\n             & in_denotation(Xp, advertising, eq) )\n    & ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n             & in_denotation(Xs, germany, eq) ) )).",
  inc=("DPV", "GEO", "ODRL"), cat="composition",
  pl="AND-Compatible: purpose ✓ ∧ spatial ✓ → Compatible")

P("ODRL115-1.p", "CounterSatisfiable", "Conflict", "Definition 6 (AND)", "Hard",
  tp("p1", "permission", "use", [("purpose", "isA", "dpv:Marketing"), ("spatial", "isPartOf", "geo:Europe")]) + "\n%\n%   " +
  tp("p2", "prohibition", "use", [("purpose", "isA", "dpv:EnforceSecurity"), ("spatial", "eq", "geo:Germany")]),
  "V_purpose=Conflict(mkt⊥sec), V_spatial=Compatible → AND=Conflict",
  "fof(odrl115, conjecture,\n    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)\n             & in_denotation(Xp, enforceSecurity, isA) )\n    & ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n             & in_denotation(Xs, germany, eq) ) )).",
  flip_conj="fof(odrl115, conjecture,\n    ![Xp]: ~( in_denotation(Xp, marketing, isA)\n            & in_denotation(Xp, enforceSecurity, isA) )).",
  inc=("DPV", "GEO", "ODRL"), cat="composition",
  pl="AND-Conflict: purpose ✗ ∧ spatial ✓ → Conflict")

P("ODRL116-1.p", "Theorem", "Compatible", "Definition 6 (OR)", "Hard",
  "V_purpose=Conflict(mkt⊥sec), V_spatial=Compatible(de≤eu) → OR=Compatible",
  "Disjunction: ∃k:V_k=Compatible → Compatible",
  "fof(odrl116, conjecture,\n    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)\n             & in_denotation(Xp, enforceSecurity, isA) )\n    | ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n             & in_denotation(Xs, germany, eq) ) )).",
  inc=("DPV", "GEO", "ODRL"), cat="composition",
  pl="OR-Compatible: purpose ✗ ∨ spatial ✓ → Compatible")

P("ODRL117-1.p", "CounterSatisfiable", "Conflict", "Definition 6 (OR)", "Hard",
  "V_purpose=Conflict(mkt⊥sec), V_spatial=Conflict(wE⊥eE) → OR=Conflict",
  "∀k:V_k=Conflict → Conflict",
  "fof(odrl117, conjecture,\n    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)\n             & in_denotation(Xp, enforceSecurity, isA) )\n    | ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)\n             & in_denotation(Xs, easternEurope, isPartOf) ) )).",
  flip_conj="fof(odrl117, conjecture,\n    ( ![Xp]: ~( in_denotation(Xp, marketing, isA)\n              & in_denotation(Xp, enforceSecurity, isA) )\n    & ![Xs]: ~( in_denotation(Xs, westernEurope, isPartOf)\n              & in_denotation(Xs, easternEurope, isPartOf) ) )).",
  inc=("DPV", "GEO", "ODRL"), cat="composition",
  pl="OR-Conflict: purpose ✗ ∨ spatial ✗ → Conflict")

P("ODRL118-1.p", "Theorem", "Compatible", "Definition 6 (XONE)", "Very Hard",
  "V_purpose=Compatible, V_spatial=Conflict (provable via ⊥⊥)\n"
  "%   XONE: ∃!k:Compat ∧ ∀j≠k:Conflict → Compatible",
  "Exactly one branch satisfiable + other provably empty",
  "fof(odrl118, conjecture,\n    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)\n             & in_denotation(Xp, advertising, isA) )\n    & ~( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)\n                & in_denotation(Xs, easternEurope, isPartOf) ) ) )).",
  inc=("DPV", "GEO", "ODRL"), cat="composition",
  pl="XONE-Compatible: purpose ✓ ⊕ spatial ✗ → Compatible")

P("ODRL119-1.p", "CounterSatisfiable", "Unknown", "Definition 6 (XONE)", "Very Hard",
  "V_purpose=Compatible, V_spatial=Compatible → both branches overlap → Unknown",
  "XONE requires exclusive satisfaction — both Compatible fails exclusivity",
  "fof(odrl119, conjecture,\n    ( ( ?[Xp]: ( in_denotation(Xp, marketing, isA)\n              & in_denotation(Xp, advertising, isA) )\n      & ~( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n                   & in_denotation(Xs, germany, eq) ) ) )\n    | ( ?[Xs2]: ( in_denotation(Xs2, europe, isPartOf)\n                & in_denotation(Xs2, germany, eq) )\n      & ~( ?[Xp2]: ( in_denotation(Xp2, marketing, isA)\n                    & in_denotation(Xp2, advertising, isA) ) ) ) )).",
  flip_conj="fof(odrl119, conjecture,\n    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)\n             & in_denotation(Xp, advertising, isA) )\n    & ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n             & in_denotation(Xs, germany, eq) ) )).",
  inc=("DPV", "GEO", "ODRL"), cat="composition",
  pl="XONE-Unknown: purpose ✓ ⊕ spatial ✓ → Unknown (exclusivity fails)")

P("ODRL120-1.p", "CounterSatisfiable", "Conflict", "Definition 6 (XONE)", "Hard",
  "V_purpose=Conflict, V_spatial=Conflict → XONE=Conflict",
  "∀k:V_k=Conflict → Conflict",
  "fof(odrl120, conjecture,\n    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)\n             & in_denotation(Xp, enforceSecurity, isA) )\n    | ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)\n             & in_denotation(Xs, easternEurope, isPartOf) ) )).",
  flip_conj="fof(odrl120, conjecture,\n    ( ![Xp]: ~( in_denotation(Xp, marketing, isA)\n              & in_denotation(Xp, enforceSecurity, isA) )\n    & ![Xs]: ~( in_denotation(Xs, westernEurope, isPartOf)\n              & in_denotation(Xs, easternEurope, isPartOf) ) )).",
  inc=("DPV", "GEO", "ODRL"), cat="composition",
  pl="XONE-Conflict: purpose ✗ ⊕ spatial ✗ → Conflict")

# --- Self-conflict (single rule, contradictory constraints) ---
P("ODRL121-1.p", "CounterSatisfiable", "Conflict", "Definition 5 (intra-rule)", "Medium",
  "ex:policy1 a odrl:Set ;\n"
  "%     odrl:permission [\n"
  "%       odrl:action odrl:use ;\n"
  "%       odrl:constraint [ odrl:operator odrl:isA ; odrl:rightOperand dpv:Marketing ] ;\n"
  "%       odrl:constraint [ odrl:operator odrl:isA ; odrl:rightOperand dpv:EnforceSecurity ] ] .",
  "Same rule, same operand: isA(marketing) ∧ isA(enforceSecurity)\n"
  "%   disjoint → rule is vacuous (never activates)",
  "fof(odrl121, conjecture,\n    ?[X]: ( in_denotation(X, marketing, isA)\n          & in_denotation(X, enforceSecurity, isA) )).",
  flip_conj="fof(odrl121, conjecture,\n    ![X]: ~( in_denotation(X, marketing, isA)\n           & in_denotation(X, enforceSecurity, isA) )).",
  cat="composition", pl="Self-conflict: single rule with isA(marketing) ∧ isA(enforceSecurity)")

# --- 3-operand composition ---
P("ODRL122-1.p", "CounterSatisfiable", "Conflict", "Definition 6 (AND, 3-operand)", "Hard",
  "AND over 3 operands: purpose=Conflict, spatial=Compatible, language=Compatible\n"
  "%   AND: ∃k:Conflict → Conflict (purpose alone kills it)",
  "One conflict among three operands suffices for AND-Conflict",
  "fof(odrl122, conjecture,\n    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)\n             & in_denotation(Xp, enforceSecurity, isA) )\n    & ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n             & in_denotation(Xs, germany, eq) )\n    & ?[Xl]: ( in_denotation(Xl, english, isA)\n             & in_denotation(Xl, english, eq) ) )).",
  flip_conj="fof(odrl122, conjecture,\n    ![Xp]: ~( in_denotation(Xp, marketing, isA)\n            & in_denotation(Xp, enforceSecurity, isA) )).",
  inc=("DPV", "GEO", "LANG", "ODRL"), cat="composition",
  pl="AND-3-operand: purpose ✗ ∧ spatial ✓ ∧ language ✓ → Conflict")

P("ODRL123-1.p", "Theorem", "Compatible", "Definition 6 (OR, 3-operand)", "Hard",
  "OR over 3 operands: purpose=Conflict, spatial=Conflict, language=Compatible\n"
  "%   OR: ∃k:Compatible → Compatible",
  "One compatible among three operands suffices for OR-Compatible",
  "fof(odrl123, conjecture,\n    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)\n             & in_denotation(Xp, enforceSecurity, isA) )\n    | ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)\n             & in_denotation(Xs, easternEurope, isPartOf) )\n    | ?[Xl]: ( in_denotation(Xl, english, isA)\n             & in_denotation(Xl, english, eq) ) )).",
  inc=("DPV", "GEO", "LANG", "ODRL"), cat="composition",
  pl="OR-3-operand: purpose ✗ ∨ spatial ✗ ∨ language ✓ → Compatible")

P("ODRL124-1.p", "Theorem", "Compatible", "Definition 6 (AND, all compatible)", "Medium",
  "AND: all 3 operands compatible → Compatible",
  "V_purpose=Compatible, V_spatial=Compatible, V_language=Compatible",
  "fof(odrl124, conjecture,\n    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)\n             & in_denotation(Xp, advertising, isA) )\n    & ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n             & in_denotation(Xs, germany, eq) )\n    & ?[Xl]: ( in_denotation(Xl, english, isA)\n             & in_denotation(Xl, english, eq) ) )).",
  inc=("DPV", "GEO", "LANG", "ODRL"), cat="composition",
  pl="AND-3-operand: purpose ✓ ∧ spatial ✓ ∧ language ✓ → Compatible")

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 6: EDGE CASES & BOUNDARY (ODRL125-132)
# ═══════════════════════════════════════════════════════════════════════════

P("ODRL125-1.p", "Theorem", "Compatible", "Definition 5 (identity)", "Trivial",
  "Identical constraints on permission and prohibition.",
  "⟦isA(mkt)⟧ ∩ ⟦isA(mkt)⟧ = ⟦isA(mkt)⟧ ≠ ∅",
  "fof(odrl125, conjecture,\n    ?[X]: ( in_denotation(X, marketing, isA)\n          & in_denotation(X, marketing, isA) )).",
  cat="edge", pl="Self-compatible: isA(marketing) ∩ isA(marketing) ≠ ∅")

P("ODRL126-1.p", "Theorem", "Compatible", "Definition 3 (root)", "Medium",
  "isA(purpose) covers entire concept space → compatible with anything grounded.",
  "⟦isA(purpose)⟧ = C, ⟦eq(advertising)⟧ = {advertising}. Witness: advertising",
  "fof(odrl126, conjecture,\n    ?[X]: ( in_denotation(X, purpose, isA)\n          & in_denotation(X, advertising, eq) )).",
  cat="edge", pl="Root coverage: isA(purpose) = C → always compatible")

P("ODRL127-1.p", "Theorem", "Compatible", "Definition 3 (leaf eq × leaf eq siblings)", "Trivial",
  "Two leaves under same parent — but using hasPart (upward).",
  "⟦hasPart(sellDataToThirdParties)⟧ ∩ ⟦hasPart(sellInsightsFromData)⟧\n"
  "%   Both under sellProducts. Witness: sellProducts",
  "fof(odrl127, conjecture,\n    ?[X]: ( in_denotation(X, sellDataToThirdParties, hasPart)\n          & in_denotation(X, sellInsightsFromData, hasPart) )).",
  cat="edge", pl="Sibling leaves: hasPart upward finds common parent sellProducts")

P("ODRL128-1.p", "CounterSatisfiable", "Conflict", "Definition 3, Definition 5", "Easy",
  "Same parent's children are disjoint — isA goes downward.",
  "sellDataToThirdParties ⊥⊥ sellInsightsFromData [d_0263]\n"
  "%   ↓sellData ∩ ↓sellInsights = ∅ (both are leaves)",
  "fof(odrl128, conjecture,\n    ?[X]: ( in_denotation(X, sellDataToThirdParties, isA)\n          & in_denotation(X, sellInsightsFromData, isA) )).",
  flip_conj="fof(odrl128, conjecture,\n    ![X]: ~( in_denotation(X, sellDataToThirdParties, isA)\n           & in_denotation(X, sellInsightsFromData, isA) )).",
  cat="edge", pl="Conflict: sibling leaves isA — disjoint by axiom")

P("ODRL129-1.p", "Theorem", "Confirmed", "Definition 2 (KB transitivity)", "Trivial",
  "(No ODRL policy — pure KB property test)\n"
  "%   targetedAdvertising ≤ personalisedAdvertising ≤ advertising ≤ marketing ≤ purpose",
  "leq(targetedAdvertising, purpose) via 4 transitivity steps",
  "fof(odrl129, conjecture, leq(targetedAdvertising, purpose)).",
  cat="edge", pl="KB transitivity: targetedAdvertising ≤ purpose (depth 4)")

# --- isAnyOf 3-element ---
P("ODRL130-1.p", "Theorem", "Compatible", "Definition 3 (isAnyOf, 3-element)", "Medium",
  "isAnyOf({advertising, customerCare, legalCompliance}) ∩ eq(directMarketing)",
  "directMarketing ≤ marketing, advertising ≤ marketing, but directMarketing ∉ ↓adv\n"
  "%   directMarketing ∉ ↓customerCare, directMarketing ∉ ↓legalCompliance\n"
  "%   BUT: is directMarketing ≤ advertising? NO (siblings under marketing)\n"
  "%   So: directMarketing NOT in union → Conflict? Wait...\n"
  "%   directMarketing ∉ ↓adv (sibling), ∉ ↓custCare (disjoint subtree), ∉ ↓legal (disjoint)\n"
  "%   → Actually CONFLICT. Let me pick a better witness.\n"
  "%   Use isAnyOf({marketing, customerCare, legalCompliance}) ∩ eq(advertising) instead.",
  "advertising ≤ marketing → advertising ∈ ↓marketing ⊆ union → Witness",
  "fof(odrl130, conjecture,\n    ?[X]: ( in_denotation_set(X, set130, isAnyOf)\n          & in_denotation(X, advertising, eq) )).",
  extra=("fof(l130_1, axiom, in_value_list(marketing, set130)).\n"
         "fof(l130_2, axiom, in_value_list(customerCare, set130)).\n"
         "fof(l130_3, axiom, in_value_list(legalCompliance, set130))."),
  cat="edge", pl="Compatible: isAnyOf 3-element set ∩ eq — one subtree matches")

P("ODRL131-1.p", "Theorem", "Compatible", "Definition 3 (isAllOf, ancestor chain)", "Medium",
  "isAllOf({marketing, purpose}) ∩ eq(advertising)",
  "advertising ≤ marketing ≤ purpose → advertising ∈ ↓mkt ∩ ↓purpose = ↓marketing\n"
  "%   Witness: advertising",
  "fof(odrl131, conjecture,\n    ?[X]: ( in_denotation_set(X, all131, isAllOf)\n          & in_denotation(X, advertising, eq) )).",
  extra="fof(l131_1, axiom, in_value_list(marketing, all131)).\nfof(l131_2, axiom, in_value_list(purpose, all131)).",
  cat="edge", pl="Compatible: isAllOf({marketing, purpose}) — ancestor chain, non-empty")

P("ODRL132-1.p", "CounterSatisfiable", "Conflict", "Definition 3 (neq, same value x2)", "Easy",
  "neq(purpose) ∩ eq(purpose)",
  "purpose ∈ ⟦eq(purpose)⟧, purpose ∉ ⟦neq(purpose)⟧\n"
  "%   All other X: X ∈ ⟦neq(purpose)⟧ but X ∉ ⟦eq(purpose)⟧ → ∅",
  "fof(odrl132, conjecture,\n    ?[X]: ( in_denotation(X, purpose, neq)\n          & in_denotation(X, purpose, eq) )).",
  flip_conj="fof(odrl132, conjecture,\n    ![X]: ~( in_denotation(X, purpose, neq)\n           & in_denotation(X, purpose, eq) )).",
  cat="edge", pl="Conflict: neq(purpose) ∩ eq(purpose) = ∅ — root exclusion")

# ═══════════════════════════════════════════════════════════════════════════
# INCLUDE MAP
# ═══════════════════════════════════════════════════════════════════════════
INC = {
    "GEO":  "include('Axioms/Layer0-DomainKB/GEO000-0.ax').",
    "DPV":  "include('Axioms/Layer0-DomainKB/DPV000-0.ax').",
    "LANG": "include('Axioms/Layer0-DomainKB/LANG000-0.ax').",
    "ODRL": "include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').",
}

# ═══════════════════════════════════════════════════════════════════════════
# GENERATE
# ═══════════════════════════════════════════════════════════════════════════
def generate(args):
    OUT = args.output
    os.makedirs(OUT, exist_ok=True)
    use_flip = (args.encoding == "prover")
    written = []
    for p in PROBLEMS:
        if use_flip and p["flip_conj"]:
            conj = p["flip_conj"]
            expected = "Theorem"
            enc_note = "% Encoding : prover-friendly (flipped for refutation provers)\n"
        else:
            conj = p["conj"]
            expected = p["exp"]
            enc_note = ""
        includes = "\n".join(INC[i] for i in p["inc"])
        extra = "\n" + p["extra"] + "\n" if p["extra"] else ""
        content = (
            f"%--------------------------------------------------------------------------\n"
            f"% File     : {p['fn']} : TPTP v0.1.0\n"
            f"% Domain   : ODRL Policy Conflict Detection (DPV Purpose)\n"
            f"% Problem  : {p.get('pl') or p['vrd']}\n"
            f"% Expected : {expected}\n"
            f"% Verdict  : {p['vrd']}\n"
            f"% Paper    : {p['paper']}\n"
            f"% Category : {p['cat']}\n"
            f"{enc_note}"
            f"%\n"
            f"% ODRL Policy (Turtle):\n"
            f"%   {p['ttl']}\n"
            f"%\n"
            f"% Denotation analysis:\n"
            f"%   {p['den']}\n"
            f"%\n"
            f"% Difficulty: {p['diff']}\n"
            f"% Authors  : Mustafa, D. & Sutcliffe, G.\n"
            f"% Date     : {datetime.now().strftime('%Y-%m-%d')}\n"
            f"%--------------------------------------------------------------------------\n"
            f"{includes}\n"
            f"{extra}\n"
            f"{conj}\n"
            f"%--------------------------------------------------------------------------\n"
        )
        path = os.path.join(OUT, p["fn"])
        if args.dry_run:
            print(f"  [dry-run] {p['fn']}")
        else:
            with open(path, 'w') as f:
                f.write(content)
            written.append(path)
            print(f"  ✓ {p['fn']}")
    n = len(written) if not args.dry_run else len(PROBLEMS)
    enc_label = "prover (all Theorem)" if use_flip else "original (mixed)"
    print(f"\n{'='*60}")
    print(f"Generated {n} problems [{enc_label}] → {os.path.abspath(OUT)}")
    print(f"{'='*60}")
    return written

# ═══════════════════════════════════════════════════════════════════════════
# STATS
# ═══════════════════════════════════════════════════════════════════════════
def print_stats():
    print(f"\n{'='*70}")
    print(f"DPV PURPOSE BENCHMARK SUITE — COVERAGE REPORT")
    print(f"{'='*70}")
    print(f"\nTotal problems: {len(PROBLEMS)}")

    # By category
    cats = defaultdict(list)
    for p in PROBLEMS:
        cats[p["cat"]].append(p)
    print(f"\nBy category:")
    for cat in ["basic", "set", "multiparent", "subsumption", "composition", "edge"]:
        if cat in cats:
            print(f"  {cat:15s}: {len(cats[cat]):3d} problems")

    # By verdict
    vrds = defaultdict(int)
    for p in PROBLEMS:
        vrds[p["vrd"]] += 1
    print(f"\nBy verdict:")
    for v in ["Compatible", "Conflict", "Confirmed", "Refuted", "Unknown", "Consistent", "Valid"]:
        if v in vrds:
            print(f"  {v:15s}: {vrds[v]:3d}")

    # By difficulty
    diffs = defaultdict(int)
    for p in PROBLEMS:
        diffs[p["diff"]] += 1
    print(f"\nBy difficulty:")
    for d in ["Trivial", "Easy", "Medium", "Medium-Hard", "Hard", "Very Hard"]:
        if d in diffs:
            print(f"  {d:15s}: {diffs[d]:3d}")

    # By SZS
    szs = defaultdict(int)
    for p in PROBLEMS:
        szs[p["exp"]] += 1
    print(f"\nBy SZS status (original):")
    for s, c in sorted(szs.items()):
        print(f"  {s:20s}: {c:3d}")

    # Operator coverage
    ops = set()
    for p in PROBLEMS:
        fn = p["fn"]
        conj = p["conj"]
        for op in ["eq", "neq", "isA", "isPartOf", "hasPart", "isAnyOf", "isAllOf", "isNoneOf"]:
            if f", {op})" in conj or f", {op} )" in conj:
                ops.add(op)
    print(f"\nOperators exercised: {sorted(ops)}")

    # Multi-parent coverage
    mp = [p for p in PROBLEMS if p["cat"] == "multiparent"]
    print(f"\nMulti-parent tests: {len(mp)} (covering all 6 multi-parent concepts + consistency)")

    print(f"\n{'='*70}")

# ═══════════════════════════════════════════════════════════════════════════
# RUN PROVER
# ═══════════════════════════════════════════════════════════════════════════
def run_prover(args, paths):
    prover = args.prover
    timeout = args.timeout
    inc_path = args.include
    results = []
    counts = {"pass": 0, "fail": 0, "timeout": 0}
    GREEN, RED, YELLOW, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[0m"
    print(f"\n{'='*60}")
    print(f"Running {prover} (timeout={timeout}s, include={inc_path})")
    print(f"{'='*60}\n")
    for path in sorted(paths):
        fn = os.path.basename(path)
        with open(path) as f:
            text = f.read()
        m = re.search(r'^% Expected\s*:\s*(\w+)', text, re.MULTILINE)
        expected = m.group(1) if m else "?"
        m2 = re.search(r'^% Verdict\s*:\s*(\w+)', text, re.MULTILINE)
        verdict = m2.group(1) if m2 else "?"
        m3 = re.search(r'^% Category\s*:\s*(\w+)', text, re.MULTILINE)
        category = m3.group(1) if m3 else "?"
        if prover == "vampire":
            cmd = ["vampire", "--include", inc_path,
                   "--time_limit", str(timeout), "--mode", "casc", path]
        else:
            cmd = ["eprover", f"--include={inc_path}",
                   f"--cpu-limit={timeout}", "--auto", path]
        t0 = time.time()
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=timeout + 10)
            output = proc.stdout + proc.stderr
        except subprocess.TimeoutExpired:
            output = ""
        elapsed = time.time() - t0
        m = re.search(r'SZS status (\w+)', output)
        actual = m.group(1) if m else "Timeout"
        if actual == expected:
            sym, col = "✓", GREEN; counts["pass"] += 1
        elif actual == "Timeout":
            sym, col = "⏱", YELLOW; counts["timeout"] += 1
        else:
            sym, col = "✗", RED; counts["fail"] += 1
        print(f"  {col}{sym}{RESET} {fn:<18} exp={expected:<20} got={actual:<20} "
              f"vrd={verdict:<12} cat={category:<12} {elapsed:.1f}s")
        results.append(dict(problem=fn, expected_szs=expected, actual_szs=actual,
                            verdict=verdict, category=category,
                            time_s=f"{elapsed:.3f}", passed=(actual == expected)))
    total = len(results)
    print(f"\n{'='*60}")
    print(f"  {GREEN}✓ {counts['pass']}{RESET} pass  "
          f"{RED}✗ {counts['fail']}{RESET} fail  "
          f"{YELLOW}⏱ {counts['timeout']}{RESET} timeout  "
          f"(total: {total})")
    print(f"{'='*60}")
    os.makedirs("results", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = f"results/benchmark_purpose_{args.encoding}_{ts}.csv"
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    print(f"CSV → {csv_path}")
    return results

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser(
        description="Generate & run ODRL TPTP Purpose (DPV) benchmark.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -o Problems/ODRL/KBGrounding/Purpose
  %(prog)s -o Problems/ODRL/KBGrounding/Purpose --encoding prover --run
  %(prog)s --stats
  %(prog)s --dry-run
""")
    ap.add_argument("-o", "--output", default="Problems/ODRL/KBGrounding/Purpose")
    ap.add_argument("--encoding", choices=["original", "prover"], default="prover",
        help="original=mixed Theorem/CSA; prover=all Theorem (default: prover)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--run", action="store_true", help="Run prover after generating")
    ap.add_argument("--timeout", type=int, default=60, help="Prover timeout (s)")
    ap.add_argument("--prover", choices=["vampire", "eprover"], default="vampire")
    ap.add_argument("--include", default="Problems/ODRL", help="TPTP include path")
    ap.add_argument("--stats", action="store_true", help="Print coverage stats only")
    args = ap.parse_args()
    if args.stats:
        print_stats()
        return
    paths = generate(args)
    if args.run and not args.dry_run:
        run_prover(args, paths)

if __name__ == "__main__":
    main()
