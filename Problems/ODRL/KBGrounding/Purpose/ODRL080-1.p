%--------------------------------------------------------------------------
% File     : ODRL080-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: isAnyOf({marketing, enforceSecurity}) ∩ eq(advertising) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf), Definition 5
% Category : set
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
%         odrl:rightOperand dpv:Advertising ] ] .
%
% Denotation analysis:
%   ⟦isAnyOf({mkt,sec})⟧ = ↓mkt ∪ ↓sec. advertising ∈ ↓mkt → Witness
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_080_1, axiom, in_value_list(marketing, set080)).
fof(list_080_2, axiom, in_value_list(enforceSecurity, set080)).

fof(odrl080, conjecture,
    ?[X]: ( in_denotation_set(X, set080, isAnyOf)
          & in_denotation(X, advertising, eq) )).
%--------------------------------------------------------------------------
