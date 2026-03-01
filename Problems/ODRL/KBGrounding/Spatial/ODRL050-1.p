%--------------------------------------------------------------------------
% File     : ODRL050-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Identity: isPartOf(europe) ∩ isPartOf(europe) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 5 (identity)
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ; odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ; odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] ] .
%
% Formal:
%   ⟦isPartOf(europe)⟧ ∩ ⟦isPartOf(europe)⟧ = ⟦isPartOf(europe)⟧ ≠ ∅
%   Witness: europe itself  [leq(europe,europe) — reflexivity]
%
% Notes    : Base case: any constraint is compatible with itself.
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl050, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
