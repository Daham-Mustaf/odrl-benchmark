%--------------------------------------------------------------------------
% File     : ODRL084-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: isAllOf({marketing, advertising}) — ancestor+descendant
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAllOf), Definition 5
% Category : set
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isAllOf ;
%         odrl:rightOperand ( dpv:Marketing dpv:Advertising ) ] ] .
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
%   advertising ≤ marketing → advertising ∈ ↓mkt ∩ ↓adv
%   → ⟦isAllOf⟧ = ↓advertising. Witness: advertising
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_084_1, axiom, in_value_list(marketing, set084)).
fof(list_084_2, axiom, in_value_list(advertising, set084)).

fof(odrl084, conjecture,
    ?[X]: ( in_denotation_set(X, set084, isAllOf)
          & in_denotation(X, advertising, eq) )).
%--------------------------------------------------------------------------
