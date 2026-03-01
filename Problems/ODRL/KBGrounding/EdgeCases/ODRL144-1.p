%--------------------------------------------------------------------------
% File     : ODRL144-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Definition 2 (disj_symm) — Bidirectional Conflict
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 2 (disj_symm) — Bidirectional Conflict
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:westernEurope ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:easternEurope ] ] .
%
% Formal test:
%   disjoint is symmetric: disj(wE, eE) → disj(eE, wE).
%   %   Proves BOTH directions of the conflict in one conjecture.
%
% One-liner : Bidirectional conflict: disj(wE,eE) ∧ disj(eE,wE)
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl144, conjecture,
    ( ![X]: ~( in_denotation(X, westernEurope, isPartOf)
             & in_denotation(X, easternEurope, isPartOf) )
    & ![Y]: ~( in_denotation(Y, easternEurope, isPartOf)
             & in_denotation(Y, westernEurope, isPartOf) ) )).

%--------------------------------------------------------------------------