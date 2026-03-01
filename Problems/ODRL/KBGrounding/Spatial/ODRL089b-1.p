%--------------------------------------------------------------------------
% File     : ODRL089b-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Positive control: rich multi-KB structure enables conflict detection
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Multi-KB Positive Control — Rich Structure Enables Detection
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
%         odrl:rightOperand dpv:commercialPurpose ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:language ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand bcp47:de ] ] .
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
%         odrl:rightOperand dpv:nonCommercialPurpose ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:language ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand bcp47:en ] ] .
%
% Denotation analysis:
%   Three rich KBs with full disjointness structure:
%   GEO: disjoint(westernEurope, easternEurope) [sibling M49]
%   DPV: disjoint(commercialPurpose, nonCommercialPurpose) [sibling DPV]
%   LANG: disjoint(de, en) [base language disjointness]
%   Result: AND-composition finds conflict on ALL THREE operands.
%   Proves: Rich KBs enable multi-domain conflict detection.
%   Contrast: ODRL088 (flat ISO) cannot detect spatial conflict alone.
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/LANG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(spatial_conflict, axiom,
    ![X]: ~( in_denotation(X, westernEurope, isPartOf)
           & in_denotation(X, easternEurope, isPartOf) )).

fof(purpose_conflict, axiom,
    ![X]: ~( in_denotation(X, commercialPurpose, isA)
           & in_denotation(X, nonCommercialPurpose, isA) )).

fof(language_conflict, axiom,
    ![X]: ~( in_denotation(X, de, isA)
           & in_denotation(X, en, isA) )).

fof(odrl089b, conjecture,
    % At least one operand must conflict (AND-composition)
    ( ![Xs]: ~( in_denotation(Xs, westernEurope, isPartOf)
              & in_denotation(Xs, easternEurope, isPartOf) )
    | ![Xp]: ~( in_denotation(Xp, commercialPurpose, isA)
              & in_denotation(Xp, nonCommercialPurpose, isA) )
    | ![Xl]: ~( in_denotation(Xl, de, isA)
              & in_denotation(Xl, en, isA) ) )).
%--------------------------------------------------------------------------
