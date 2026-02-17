%--------------------------------------------------------------------------
% File     : ODRL212-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : N-Way + DAG + Set Ops + Multi-Dim — The Full Monty
% Expected : Theorem
% Verdict  : Compatible
% Paper    : N-Way + DAG + Set Ops + Multi-Dim — The Full Monty
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAnyOf ;
%   %         odrl:rightOperand ( geo:germany geo:france ) ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand dpv:CommercialPurpose ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isNoneOf ;
%   %         odrl:rightOperand ( geo:easternEurope ) ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand dpv:ResearchAndDevelopment ] ] .
%   %
%   %   ex:policyC a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:westernEurope ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand dpv:CommercialResearch ] ] .
%
% Formal test:
%   The Full Monty: n-way + DAG multi-parent + set operators + multi-dim.
%   %   A∩B: isAnyOf({de,fr}) ∩ isNoneOf({eE}) ∧ cP∩R&D=cR (DAG!) → Compatible
%   %   A∩C: isAnyOf({de,fr}) ∩ isPartOf(wE) ∧ cP∩cR → Compatible
%   %   B∩C: isNoneOf({eE}) ∩ isPartOf(wE) ∧ R&D∩cR → Compatible
%   %   Extreme: every hard feature combined — prover must unify all patterns.
%
% One-liner : The Full Monty: n-way + DAG + isAnyOf + isNoneOf + isPartOf + multi-dim
% Difficulty: Extreme
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_extreme_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
% --- DPV Fragment (DAG-SAFE sibling disjointness) ---
fof(dpv_s_root, axiom, concept(purpose)).
fof(dpv_s_c1, axiom, concept(commercialPurpose)).
fof(dpv_s_c2, axiom, concept(researchAndDevelopment)).
fof(dpv_s_c3, axiom, concept(commercialResearch)).
fof(dpv_s_c4, axiom, concept(academicResearch)).
fof(dpv_s_c5, axiom, concept(serviceProvision)).

fof(dpv_s_leq1, axiom, leq(commercialPurpose, purpose)).
fof(dpv_s_leq2, axiom, leq(researchAndDevelopment, purpose)).
fof(dpv_s_leq3, axiom, leq(serviceProvision, purpose)).
fof(dpv_s_leq4, axiom, leq(commercialResearch, commercialPurpose)).
fof(dpv_s_leq5, axiom, leq(commercialResearch, researchAndDevelopment)).
fof(dpv_s_leq6, axiom, leq(academicResearch, researchAndDevelopment)).

fof(dpv_s_refl1, axiom, leq(purpose, purpose)).
fof(dpv_s_refl2, axiom, leq(commercialPurpose, commercialPurpose)).
fof(dpv_s_refl3, axiom, leq(researchAndDevelopment, researchAndDevelopment)).
fof(dpv_s_refl4, axiom, leq(commercialResearch, commercialResearch)).
fof(dpv_s_refl5, axiom, leq(academicResearch, academicResearch)).
fof(dpv_s_refl6, axiom, leq(serviceProvision, serviceProvision)).

fof(dpv_s_disj_safe1, axiom, disjoint(commercialPurpose, serviceProvision)).
fof(dpv_s_disj_safe2, axiom, disjoint(researchAndDevelopment, serviceProvision)).

fof(dpv_s_una, axiom,
    $distinct(purpose, commercialPurpose, researchAndDevelopment,
              commercialResearch, academicResearch, serviceProvision)).
fof(list_212a_1, axiom, in_value_list(germany, anyList212)).
fof(list_212a_2, axiom, in_value_list(france, anyList212)).
fof(list_anyList212_closed, axiom,
    ![G]: (in_value_list(G, anyList212) => (G = germany | G = france))).
fof(list_212b, axiom, in_value_list(easternEurope, noneList212)).
fof(list_noneList212_closed, axiom,
    ![G]: (in_value_list(G, noneList212) => (G = easternEurope))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl212, conjecture,
    ( ?[Xs,Xp]: ( in_denotation_set(Xs, anyList212, isAnyOf)
                & in_denotation_set(Xs, noneList212, isNoneOf)
                & in_denotation(Xp, commercialPurpose, isA)
                & in_denotation(Xp, researchAndDevelopment, isA) )
    & ?[Ys,Yp]: ( in_denotation_set(Ys, anyList212, isAnyOf)
                & in_denotation(Ys, westernEurope, isPartOf)
                & in_denotation(Yp, commercialPurpose, isA)
                & in_denotation(Yp, commercialResearch, isA) )
    & ?[Zs,Zp]: ( in_denotation_set(Zs, noneList212, isNoneOf)
                & in_denotation(Zs, westernEurope, isPartOf)
                & in_denotation(Zp, researchAndDevelopment, isA)
                & in_denotation(Zp, commercialResearch, isA) ) )).

%--------------------------------------------------------------------------