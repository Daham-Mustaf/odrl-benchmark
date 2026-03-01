%--------------------------------------------------------------------------
% File     : ODRL088-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Downward asymmetry: flat ISO alone cannot detect dE ⊥ pL
% Expected : CounterSatisfiable
% Verdict  : Unknown
% Paper    : Proposition 2(2) — Downward Asymmetry: Flat KB Alone
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   ISO 3166 has $distinct(dE, pL) for UNA — dE ≠ pL
%   BUT $distinct ≠ disjoint/2 (no leq/2 structure forbidding overlap)
%   disjoint(dE, pL) is NOT derivable from ISO alone
%   Compare ODRL081: adds GEO+alignment → Conflict in 0.1s
%
% Notes    : Demonstrates: structural disjointness from richer KB is necessary.
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl088, conjecture,
    ?[X]: ( in_denotation(X, dE, isPartOf)
          & in_denotation(X, pL, isPartOf) )).
%--------------------------------------------------------------------------
