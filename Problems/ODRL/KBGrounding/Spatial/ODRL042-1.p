%--------------------------------------------------------------------------
% File     : ODRL042-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : OR-Compatible: spatial ✗ ∨ purpose ✓ → Compatible
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 6 (Composition, or)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:westernEurope ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:ResearchAndDevelopment ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:easternEurope ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:AcademicResearch ] ] .
%
% Denotation analysis:
%   V_spatial=Conflict, V_purpose=Compatible → OR-Compatible
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl042, conjecture,
    ( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)
             & in_denotation(Xs, easternEurope, isPartOf) )
    | ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)
             & in_denotation(Xp, academicResearch, isA) ) )).
%--------------------------------------------------------------------------
