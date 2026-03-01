%--------------------------------------------------------------------------
% File     : ODRL013-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isPartOf(wE) ∩ isPartOf(eE) = ∅ [disj_downward]
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
%         odrl:rightOperand geo:westernEurope ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:easternEurope ] ] .
%
% Formal:
%   disjoint(westernEurope, easternEurope)  [sibling disjointness]
%   disj_downward: ∀X. leq(X,wE) ∧ leq(X,eE) → disjoint(X,X)
%   disj_irrefl: ¬disjoint(X,X)  →  contradiction  →  ∅
%
% Notes    : Core conflict pattern used in Theorem 1 proof.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl013, conjecture,
    ![X]: ~( in_denotation(X, westernEurope, isPartOf)
           & in_denotation(X, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
