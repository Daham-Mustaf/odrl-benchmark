%--------------------------------------------------------------------------
% File     : ODRL130-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Definition 6 — 3-Operand AND Composition
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 6 — 3-Operand AND Composition
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:europe ] ;
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
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand geo:germany ] ;
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
%   3-operand AND: each operand Compatible → composed Compatible.
%   %   Witnesses: germany (spatial), academicResearch (purpose), enGB (language).
%   %   Tests: composition over 3 independent operands.
%
% One-liner : 3-operand AND: spatial + purpose + language all Compatible
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/LANG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl130, conjecture,
    ( ?[X]: ( in_denotation(X, europe, isPartOf)
            & in_denotation(X, germany, eq) )
    & ?[Y]: ( in_denotation(Y, researchAndDevelopment, isA)
            & in_denotation(Y, academicResearch, isA) )
    & ?[Z]: ( in_denotation(Z, en, isPartOf)
            & in_denotation(Z, enGB, eq) ) )).

%--------------------------------------------------------------------------