%--------------------------------------------------------------------------
% File     : ODRL100-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Note 1 — DAG Multi-Parent Contradiction (Naive)
% Expected : Theorem
% Verdict  : ContradictoryAxioms
% Paper    : Note 1 — DAG Multi-Parent Contradiction (Naive)
%
% ODRL Policy (Conceptual):
%   (No ODRL policy — KB consistency test)
%   %   Tests: naive sibling disjointness on DAG taxonomy causes ⊥.
%
% Formal test:
%   disjoint(commercialPurpose, R&D) [naive sibling]
%   %   + leq(cR, cP) ∧ leq(cR, R&D) [multi-parent]
%   %   → disj_downward → disjoint(cR, cR)
%   %   → contradicts disj_irrefl → ⊥
%
% One-liner : DAG inconsistency: naive sibling disj on multi-parent → ⊥
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
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
              commercialResearch, academicResearch, serviceProvision)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl100, conjecture, $false).

%--------------------------------------------------------------------------