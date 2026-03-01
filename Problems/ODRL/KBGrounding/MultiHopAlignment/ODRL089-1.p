%--------------------------------------------------------------------------
% File     : ODRL089-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Upward asymmetry: alignment data without theory is inert
% Expected : CounterSatisfiable
% Verdict  : Unknown
% Paper    : Proposition 2(2) — Upward Asymmetry: Data Without Theory
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   GEO: disj(germany, poland) derivable [disj_downward(wE⊥eE)]
%   ALIGN-GEO-ISO: align(germany,dE), align(poland,pL) present
%   MISSING: ALIGN000-0.ax (align_disj_forward rule)
%   Without the theory, align/2 facts cannot bridge GEO→ISO
%   Compare ODRL081: adds ALIGN_THEORY → Conflict in 0.1s
%
% Notes    : Paired with ODRL081/ODRL088: both alone fail, both together succeed.
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl089, conjecture,
    ?[X]: ( in_denotation(X, dE, isPartOf)
          & in_denotation(X, pL, isPartOf) )).
%--------------------------------------------------------------------------
