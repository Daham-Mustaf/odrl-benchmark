%--------------------------------------------------------------------------
% File     : ODRL094-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Multi-operand AND: runtime witness for 2-operand Compatible verdict
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Theorem 2 + 3 — Multi-Operand Runtime Soundness
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   omega094s ↦ germany:  germany ≤ europe → satisfies(s, europe, isPartOf)
%                       germany = germany → satisfies(s, germany, eq)
%   omega094p ↦ academicResearch:
%                       academicResearch ≤ R&D → satisfies(p, R&D, isA)
%                       academicResearch ≤ academicResearch → satisfies(p, aR, isA)
%
% Notes    : Operand independence (Assumption 2): separate Ctx constants per operand. Spatial and purpose constraints are evaluated independently. Static verdict is AND-Compatible on both dimensions.
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
% Per-operand contexts (Assumption 2: operand independence)
fof(ctx_spatial, axiom, assigns(omega094s, germany)).
fof(ctx_purpose, axiom, assigns(omega094p, academicResearch)).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl094, conjecture,
    ( satisfies(omega094s, europe, isPartOf)
    & satisfies(omega094s, germany, eq)
    & satisfies(omega094p, researchAndDevelopment, isA)
    & satisfies(omega094p, academicResearch, isA) )).
%--------------------------------------------------------------------------
