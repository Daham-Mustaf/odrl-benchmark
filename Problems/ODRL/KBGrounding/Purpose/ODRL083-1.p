%--------------------------------------------------------------------------
% File     : ODRL083-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict: isAllOf({marketing, enforceSecurity}) = ∅ (disjoint parents)
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3 (isAllOf), Definition 5
% Category : set
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isAllOf ;
%         odrl:rightOperand ( dpv:Marketing dpv:EnforceSecurity ) ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand dpv:Advertising ] ] .
%
% Denotation analysis:
%   disjoint(marketing, enforceSecurity) [d_0113] → ⟦isAllOf⟧ = ∅ → ∅ ∩ anything = ∅
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_083_1, axiom, in_value_list(marketing, set083)).
fof(list_083_2, axiom, in_value_list(enforceSecurity, set083)).

fof(odrl083, conjecture,
    ![X]: ~( in_denotation_set(X, set083, isAllOf)
           & in_denotation(X, advertising, eq) )).
%--------------------------------------------------------------------------
