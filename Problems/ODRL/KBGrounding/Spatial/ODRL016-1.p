%--------------------------------------------------------------------------
% File     : ODRL016-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: neq(germany) ∩ isPartOf(westernEurope) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (neq/isPartOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:neq ;
%         odrl:rightOperand geo:germany ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:westernEurope ] ] .
%
% Formal:
%   ⟦neq(germany)⟧  = C \ {germany}
%   ⟦isPartOf(wE)⟧ = {x | leq(x,wE)}
%   Witness: france  (leq(france,wE) ∧ france ≠ germany [UNA])
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl016, conjecture,
    ?[X]: ( in_denotation(X, germany, neq)
          & in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
