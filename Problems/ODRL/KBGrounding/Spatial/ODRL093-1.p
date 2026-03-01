%--------------------------------------------------------------------------
% File     : ODRL093-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Permissive ⊤: ungrounded constraint → satisfy by default
% Expected : Theorem
% Verdict  : Consistent
% Paper    : Definition 10 (⊤ case) — Permissive Satisfaction
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   assigns(ω, germany) ∧ ungrounded(unknownConcept)
%   → permissive_satisfaction → satisfies(ω, unknownConcept, isPartOf)
%   Backward bridge blocked: ungrounded_not_concept prevents concept(unknownConcept)
%   → satisfaction_to_denotation guard fails → no in_denotation contradiction
%
% Notes    : Tests the ⊤ branch of Def. 10. The guard concept(G) on the backward bridge is essential: without it, permissive_sat + backward → in_den(X,unkG,Op) → leq(X,unkG) → concept(unkG) contradicts ungrounded(unkG).
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(runtime_context_093, axiom, assigns(omega093, germany)).
fof(unknown_ungrounded, axiom, ungrounded(unknownConcept)).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl093, conjecture,
    satisfies(omega093, unknownConcept, isPartOf)).
%--------------------------------------------------------------------------
