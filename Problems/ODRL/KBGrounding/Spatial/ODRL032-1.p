%--------------------------------------------------------------------------
% File     : ODRL032-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-operator subsumption: eq(germany) ⊆ isPartOf(europe)
% Expected : Theorem
% Verdict  : Subsumption
% Paper    : Definition 7
%
% ODRL Policy (Turtle):
%   c1: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:eq ;
%     odrl:rightOperand geo:germany ] .
%
%   c2: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isPartOf ;
%     odrl:rightOperand geo:europe ] .
%
% Formal:
%   ⟦eq(germany)⟧ = {germany}
%   leq(germany, westernEurope) ∧ leq(westernEurope, europe)  [leq_trans]
%   → germany ∈ ⟦isPartOf(europe)⟧
%   → ⟦eq(germany)⟧ ⊆ ⟦isPartOf(europe)⟧
%
% Notes    : 'Exactly germany' is a refinement of 'anywhere in europe'.
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl032, conjecture,
    ![X]: ( in_denotation(X, germany, eq)
          => in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
