%--------------------------------------------------------------------------
% File     : ODRL091-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Runtime witness: Compatible verdict → satisfying context exists
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 10 — Runtime Witness for Compatible Verdict
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   assigns(ω, germany)
%   → leq(germany, europe) [GEO KB] → in_den(germany, europe, isPartOf)
%   → satisfies(ω, europe, isPartOf)  [denotation_to_satisfaction]
%   → germany = germany → in_den(germany, germany, eq)
%   → satisfies(ω, germany, eq)  [denotation_to_satisfaction]
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(runtime_context_091, axiom, assigns(omega091, germany)).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl091, conjecture,
    ( satisfies(omega091, europe, isPartOf)
    & satisfies(omega091, germany, eq) )).
%--------------------------------------------------------------------------
