%--------------------------------------------------------------------------
% File     : ODRL014-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: hasPart(germany) ∩ isPartOf(europe) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (hasPart/isPartOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:hasPart ;
%         odrl:rightOperand geo:germany ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:europe ] ] .
%
% Formal:
%   ⟦hasPart(germany)⟧  = {x | leq(germany,x)} = {germany,wE,europe,world}
%   ⟦isPartOf(europe)⟧ = {x | leq(x,europe)}
%   Witnesses: westernEurope ∈ both (leq(de,wE) ∧ leq(wE,eu))
%
% Notes    : hasPart traverses UPWARD — important for understanding direction.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl014, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
