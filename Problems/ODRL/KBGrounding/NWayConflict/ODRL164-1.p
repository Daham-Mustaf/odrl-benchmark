%--------------------------------------------------------------------------
% File     : ODRL164-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : N-Way — 4-Policy Subsumption Chain
% Expected : Theorem
% Verdict  : Compatible
% Paper    : N-Way — 4-Policy Subsumption Chain
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
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:germany ] ] .
%   %
%   %   ex:policyD a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand geo:bavaria ] ] .
%
% Formal test:
%   4-way existential: all 4 policies overlap at single witness.
%   %   Witness: bavaria (leq(bav,de), leq(de,wE), leq(wE,europe), bav=bav)
%   %   Tests: prover must find a witness satisfying 4 constraints simultaneously.
%
% One-liner : 4-policy chain: ∃X ∈ ↓europe ∩ ↓wE ∩ ↓de ∩ {bav}
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl164, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & in_denotation(X, westernEurope, isPartOf)
          & in_denotation(X, germany, isPartOf)
          & in_denotation(X, bavaria, eq) )).

%--------------------------------------------------------------------------