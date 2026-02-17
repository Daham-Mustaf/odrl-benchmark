%--------------------------------------------------------------------------
% File     : ODRL161-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : N-Way — 3-Policy Common Witness
% Expected : Theorem
% Verdict  : Compatible
% Paper    : N-Way — 3-Policy Common Witness
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:europe ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:westernEurope ] ] .
%   %
%   %   ex:policyC a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand geo:germany ] ] .
%
% Formal test:
%   3-way existential: ∃X in all three denotations simultaneously.
%   %   Witness: germany (leq(de,wE), leq(wE,europe) → leq(de,europe), de=de)
%   %   Tests: 3-way intersection ≠ ∅ → all 3 policies overlap at germany.
%
% One-liner : 3-policy common witness: ∃X ∈ ↓europe ∩ ↓wE ∩ {de}
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl161, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & in_denotation(X, westernEurope, isPartOf)
          & in_denotation(X, germany, eq) )).

%--------------------------------------------------------------------------