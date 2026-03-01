%--------------------------------------------------------------------------
% File     : ODRL018-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isPartOf(westernEurope) ∩ hasPart(bavaria) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 2, Definition 3
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
%         odrl:operator odrl:hasPart ;
%         odrl:rightOperand geo:bavaria ] ] .
%
% Formal:
%   ⟦isPartOf(wE)⟧  = {x | leq(x,wE)}
%   ⟦hasPart(bavaria)⟧ = {x | leq(bavaria,x)}
%   Witness: germany  [leq(bavaria,germany) ∧ leq(germany,wE)]
%
% Notes    : Requires 2-hop witness chain via sub-national concept.
% Difficulty: Medium-Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl018, conjecture,
    ?[X]: ( in_denotation(X, westernEurope, isPartOf)
          & in_denotation(X, bavaria, hasPart) )).
%--------------------------------------------------------------------------
