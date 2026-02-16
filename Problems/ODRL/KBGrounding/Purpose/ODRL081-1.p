%--------------------------------------------------------------------------
% File     : ODRL081-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict: isAnyOf({marketing, enforceSecurity}) ∩ eq(legalCompliance) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3 (isAnyOf), Definition 5
% Category : set
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isAnyOf ;
%         odrl:rightOperand ( dpv:Marketing dpv:EnforceSecurity ) ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand dpv:LegalCompliance ] ] .
%
% Denotation analysis:
%   legalCompliance ≤ fulfilmentOfObligation.
%   disjoint(marketing, fulfilmentOfObligation) [d_0136]
%   disjoint(enforceSecurity, fulfilmentOfObligation) [d_0111]
%   → legalCompliance ∉ ↓mkt ∪ ↓sec → ∅
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_081_1, axiom, in_value_list(marketing, set081)).
fof(list_081_2, axiom, in_value_list(enforceSecurity, set081)).

fof(odrl081, conjecture,
    ![X]: ~( in_denotation_set(X, set081, isAnyOf)
           & in_denotation(X, legalCompliance, eq) )).
%--------------------------------------------------------------------------
