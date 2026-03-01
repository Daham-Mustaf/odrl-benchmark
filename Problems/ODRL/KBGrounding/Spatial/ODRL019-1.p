%--------------------------------------------------------------------------
% File     : ODRL019-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isPartOf(northernEurope) ∩ isPartOf(southernEurope) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 2 (disj_downward), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:northernEurope ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:southernEurope ] ] .
%
% Formal:
%   disjoint(northernEurope, southernEurope)  [siblings under europe]
%   disj_downward: ∀X. leq(X,nE) ∧ leq(X,sE) → disjoint(X,X)
%   disj_irrefl → contradiction → ∅
%
% Notes    : Same proof pattern as ODRL013 but different sibling pair.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl019, conjecture,
    ![X]: ~( in_denotation(X, northernEurope, isPartOf)
           & in_denotation(X, southernEurope, isPartOf) )).
%--------------------------------------------------------------------------
