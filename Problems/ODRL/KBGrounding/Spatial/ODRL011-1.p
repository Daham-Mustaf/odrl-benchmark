%--------------------------------------------------------------------------
% File     : ODRL011-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isPartOf(europe) ∩ eq(germany) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3, Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:europe ] ] .
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
%   ⟦isPartOf(europe)⟧ = {x | leq(x, europe)} ∋ germany
%   ⟦eq(germany)⟧ = {germany}
%   Witness: germany (leq_trans: de ≤ wE ≤ europe)
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl011, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & in_denotation(X, germany, eq) )).
%--------------------------------------------------------------------------
