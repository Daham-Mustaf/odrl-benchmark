%--------------------------------------------------------------------------
% File     : ODRL033-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Tautological equivalence: isA(germany) ≡ isPartOf(germany)
% Expected : Theorem
% Verdict  : Subsumption
% Paper    : Definition 3 (isA = isPartOf), Definition 7
%
% ODRL Policy (Turtle):
%   c1: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isA ;
%     odrl:rightOperand geo:germany ] .
%
%   c2: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isPartOf ;
%     odrl:rightOperand geo:germany ] .
%
% Formal:
%   den_isA_if/onlyif and den_isPartOf_if/onlyif in ODRL000-0.ax
%   both reduce to leq(X, germany)
%   → ⟦isA(germany)⟧ = ⟦isPartOf(germany)⟧  (biconditional)
%
% Notes    : isA is a semantic alias for isPartOf in ODRL000-0.ax.
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl033, conjecture,
    ![X]: ( in_denotation(X, germany, isA)
          => in_denotation(X, germany, isPartOf) )).
%--------------------------------------------------------------------------
