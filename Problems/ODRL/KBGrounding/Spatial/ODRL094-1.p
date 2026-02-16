%--------------------------------------------------------------------------
% File     : ODRL094-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Multi-operand: AND composition at runtime
% Expected : Theorem
% Verdict  : Sound
% Paper    : Theorem 2 + 3 — Multi-Operand Runtime Soundness
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:europe ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:ResearchAndDevelopment ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:germany ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:AcademicResearch ] ] .
%
% Denotation analysis:
%   AND composition: V_spatial=Compatible, V_purpose=Compatible.
%   Per-operand context constants (Assumption 2: operand independence):
%     omega094s ↦ germany (spatial), omega094p ↦ academicResearch (purpose).
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').

% Per-operand contexts (Assumption 2: operand independence)
fof(ctx_spatial, axiom, assigns(omega094s, germany)).
fof(ctx_purpose, axiom, assigns(omega094p, academicResearch)).

fof(odrl094, conjecture,
    ( satisfies(omega094s, europe, isPartOf)
    & satisfies(omega094s, germany, eq)
    & satisfies(omega094p, researchAndDevelopment, isA)
    & satisfies(omega094p, academicResearch, isA) )).
%--------------------------------------------------------------------------
