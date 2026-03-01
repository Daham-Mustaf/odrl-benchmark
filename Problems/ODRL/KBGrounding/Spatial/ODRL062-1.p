%--------------------------------------------------------------------------
% File     : ODRL062-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Non-tautological: hasPart(europe) = {europe} ≠ C
% Expected : CounterSatisfiable
% Verdict  : Consistent
% Paper    : Tautology Detection (hasPart root)
%
% ODRL Policy (Turtle):
%   c: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] .
%
% Formal:
%   ⟦hasPart(europe)⟧ = {X ∈ C | leq(europe, X)} = {europe}  [only via reflexivity]
%   europe is maximal (root) — no leq(europe, X) except X=europe
%   Counterexample: germany — leq(europe, germany) not in KB
%
% Notes    : Contrast with ODRL060: hasPart at root has smallest denotation (1 element). isPartOf at root has largest (all 26). Vampire skipped (CounterSat → Z3 only).
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl062, conjecture,
    ~in_denotation(germany, europe, hasPart)).
%--------------------------------------------------------------------------
