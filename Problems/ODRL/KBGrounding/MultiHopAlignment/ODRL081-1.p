%--------------------------------------------------------------------------
% File     : ODRL081-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Aligned conflict: disjoint(dE, pL) via alignment transfer
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Def. 8(ii), Proposition 2(1) — Disjointness Transfer
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   disj_downward(wE⊥eE, de≤wE, pl≤eE) → disj(germany, poland)
%   align_disj_forward(germany→dE, poland→pL, disj(de,pl))
%   → disj(dE, pL) in ISO 3166
%   → ⟦isPartOf(dE)⟧ ∩ ⟦isPartOf(pL)⟧ = ∅ → Conflict
%
% Notes    : Compare ODRL088 (ISO alone) and ODRL089 (data without theory).
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl081, conjecture,
    ![X]: ~( in_denotation(X, dE, isPartOf)
           & in_denotation(X, pL, isPartOf) )).
%--------------------------------------------------------------------------
