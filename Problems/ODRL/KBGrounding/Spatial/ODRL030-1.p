%--------------------------------------------------------------------------
% File     : ODRL030-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption confirmed: isPartOf(germany) ⊆ isPartOf(europe)
% Expected : Theorem
% Verdict  : Subsumption
% Paper    : Definition 7 (Constraint Subsumption)
%
% ODRL Policy (Turtle):
%   c1: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isPartOf ;
%     odrl:rightOperand geo:germany ] .
%
%   c2: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isPartOf ;
%     odrl:rightOperand geo:europe ] .
%
% Formal:
%   ∀X: leq(X,germany) → leq(X,westernEurope) → leq(X,europe)  [leq_trans×2]
%   ⟦isPartOf(germany)⟧ ⊆ ⟦isPartOf(europe)⟧
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl030, conjecture,
    ![X]: ( in_denotation(X, germany, isPartOf)
          => in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
