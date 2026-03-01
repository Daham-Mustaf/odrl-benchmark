%--------------------------------------------------------------------------
% File     : ODRL020-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isAnyOf({wE,nE}) ∩ eq(germany) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isAnyOf ;
%         odrl:rightOperand ( geo:westernEurope geo:northernEurope ) ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:germany ] ] .
%
% Formal:
%   ⟦isAnyOf({wE,nE})⟧ = ↓wE ∪ ↓nE
%   germany ∈ ↓wE  [leq(germany, westernEurope)]
%   Witness: germany
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(list_regions020_1, axiom, in_value_list(westernEurope, regions020)).
fof(list_regions020_2, axiom, in_value_list(northernEurope, regions020)).
fof(list_regions020_closed, axiom,
    ![G]: (in_value_list(G, regions020) => (G = westernEurope | G = northernEurope))).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl020, conjecture,
    ?[X]: ( in_denotation_set(X, regions020, isAnyOf)
          & in_denotation(X, germany, eq) )).
%--------------------------------------------------------------------------
