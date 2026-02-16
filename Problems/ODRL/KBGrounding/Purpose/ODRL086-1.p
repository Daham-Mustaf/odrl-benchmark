%--------------------------------------------------------------------------
% File     : ODRL086-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: isNoneOf({marketing, enforceSecurity}) ∩ isA(serviceProvision) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isNoneOf), Definition 5
% Category : set
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isNoneOf ;
%         odrl:rightOperand ( dpv:Marketing dpv:EnforceSecurity ) ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:ServiceProvision ] ] .
%
% Denotation analysis:
%   Witness: paymentManagement ≤ serviceProvision,
%   disjoint(serviceProvision, marketing) [d_0185],
%   disjoint(serviceProvision, enforceSecurity) [d_0120] → paymentMgmt ∉ excluded
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_086_1, axiom, in_value_list(marketing, none086)).
fof(list_086_2, axiom, in_value_list(enforceSecurity, none086)).

fof(odrl086, conjecture,
    ?[X]: ( in_denotation_set(X, none086, isNoneOf)
          & in_denotation(X, serviceProvision, isA) )).
%--------------------------------------------------------------------------
