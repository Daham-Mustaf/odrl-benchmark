%--------------------------------------------------------------------------
% File     : ODRL044-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Self-conflict: single rule with isPartOf(wE) ∧ isPartOf(eE)
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 5 (self-conflict within single rule)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ; odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ; odrl:operator odrl:isPartOf ; odrl:rightOperand geo:easternEurope ] ] .
%
% Formal:
%   Same rule, same operand, two spatial constraints:
%   isPartOf(wE) ∧ isPartOf(eE) → must satisfy BOTH
%   disj(wE,eE) → no X satisfies both → rule vacuously empty
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl044, conjecture,
    ![X]: ~( in_denotation(X, westernEurope, isPartOf)
           & in_denotation(X, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
