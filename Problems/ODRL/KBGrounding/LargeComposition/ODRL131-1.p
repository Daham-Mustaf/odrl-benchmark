%--------------------------------------------------------------------------
% File     : ODRL131-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Theorem 2 — 3-Operand AND with One Conflict
% Expected : CounterSatisfiable
% Verdict  : Conflict
% Paper    : Theorem 2 — 3-Operand AND with One Conflict
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:westernEurope ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand dpv:ResearchAndDevelopment ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:language ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand lang:en ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:easternEurope ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand dpv:AcademicResearch ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:language ;
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand lang:enGB ] ] .
%
% Formal test:
%   3-operand AND: spatial Conflict → composed Conflict.
%   %   By Theorem 2: AND(Conflict, Compatible, Compatible) = Conflict.
%   %   It suffices to prove the spatial operand conflicts.
%
% One-liner : 3-operand AND: spatial Conflict → composed Conflict
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/LANG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl131, conjecture,
    ?[X]: ( in_denotation(X, westernEurope, isPartOf)
          & in_denotation(X, easternEurope, isPartOf) )).

%--------------------------------------------------------------------------