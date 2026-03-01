%--------------------------------------------------------------------------
% File     : ODRL080-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict preservation: wE ⊥ eE holds with alignment loaded
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Proposition 2(1) — Conflict Preservation (baseline)
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   disjoint(westernEurope, easternEurope) in GEO → ∅ → Conflict
%   Tests: loading ISO3166 + alignment does NOT disrupt source-KB reasoning
%
% Difficulty: Hard
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
fof(odrl080, conjecture,
    ![X]: ~( in_denotation(X, westernEurope, isPartOf)
           & in_denotation(X, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
