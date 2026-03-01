%--------------------------------------------------------------------------
% File     : ODRL036-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-operator subsumption: isPartOf(germany) ⊆ neq(france)
% Expected : Theorem
% Verdict  : Subsumption
% Paper    : Definition 7
%
% ODRL Policy (Turtle):
%   c1: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isPartOf ;
%     odrl:rightOperand geo:germany ] .
%
%   c2: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:neq ;
%     odrl:rightOperand geo:france ] .
%
% Formal:
%   ∀X: leq(X,germany) → X ≠ france
%   Proof: leq(X,germany) ∧ X=france → leq(france,germany)
%   But disj(wE,wE_other) → disj(france,germany)  [siblings]
%   disj_order_consistency: leq(france,germany) → ¬disj(france,germany)
%   Contradiction → X ≠ france
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl036, conjecture,
    ![X]: ( in_denotation(X, germany, isPartOf)
          => in_denotation(X, france, neq) )).
%--------------------------------------------------------------------------
