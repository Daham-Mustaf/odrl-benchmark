%--------------------------------------------------------------------------
% File     : ODRL121-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Self-conflict: single rule with isA(marketing) ∧ isA(enforceSecurity)
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 5 (intra-rule)
% Category : composition
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [ odrl:operator odrl:isA ; odrl:rightOperand dpv:Marketing ] ;
%       odrl:constraint [ odrl:operator odrl:isA ; odrl:rightOperand dpv:EnforceSecurity ] ] .
%
% Denotation analysis:
%   Same rule, same operand: isA(marketing) ∧ isA(enforceSecurity)
%   disjoint → rule is vacuous (never activates)
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl121, conjecture,
    ![X]: ~( in_denotation(X, marketing, isA)
           & in_denotation(X, enforceSecurity, isA) )).
%--------------------------------------------------------------------------
