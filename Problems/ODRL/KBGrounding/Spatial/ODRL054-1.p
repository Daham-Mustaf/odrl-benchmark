%--------------------------------------------------------------------------
% File     : ODRL054-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Counterintuitive: hasPart(europe) ⊆ hasPart(germany)
% Expected : Theorem
% Verdict  : Subsumption
% Paper    : Definition 7
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] .
%   c2: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:germany ] .
%
% Formal:
%   ⟦hasPart(europe)⟧  = {X | leq(europe,X)} = {europe, world}
%   ⟦hasPart(germany)⟧ = {X | leq(germany,X)} = {germany,wE,europe,world}
%   {europe,world} ⊆ {germany,wE,europe,world}  →  Subsumption
%   Proof: leq(europe,X) ∧ leq(germany,europe) → leq(germany,X)  [leq_trans]
%
% Notes    : MORE GENERAL concept → SMALLER hasPart denotation. Reversal of isPartOf.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl054, conjecture,
    ![X]: ( in_denotation(X, europe, hasPart)
          => in_denotation(X, germany, hasPart) )).
%--------------------------------------------------------------------------
