%--------------------------------------------------------------------------
% File     : ODRL061-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Non-tautological: isPartOf(westernEurope) ⊂ C
% Expected : CounterSatisfiable
% Verdict  : Consistent
% Paper    : Tautology Detection
%
% ODRL Policy (Turtle):
%   c: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] .
%
% Formal:
%   ⟦isPartOf(wE)⟧ = ↓wE = {wE, austria, belgium, france, germany,
%   liechtenstein, luxembourg, monaco, netherlands, switzerland}  (10 of 26)
%   Counterexample: poland → leq(poland, easternEurope), ¬leq(poland, wE)
%
% Notes    : Ground witness: poland not in ↓wE. Vampire skipped (CounterSat → Z3 only).
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl061, conjecture,
    ~in_denotation(poland, westernEurope, isPartOf)).
%--------------------------------------------------------------------------
