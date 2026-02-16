%--------------------------------------------------------------------------
% File     : ODRL044-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Self-conflict: single rule with contradictory constraints
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 5 (self-conflict within single rule)
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:westernEurope ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:easternEurope ] ] .
%
% Denotation analysis:
%   Same rule, same operand, two constraints: isPartOf(wE) ∧ isPartOf(eE)
%   disjoint(wE, eE) → no X satisfies both → rule is vacuous
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl044, conjecture,
    ![X]: ~( in_denotation(X, westernEurope, isPartOf)
           & in_denotation(X, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
