%--------------------------------------------------------------------------
% File     : ODRL170-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : N-Way Composed — 3 Policies All Compatible (Spatial + Purpose)
% Expected : Theorem
% Verdict  : Compatible
% Paper    : N-Way Composed — 3 Policies All Compatible (Spatial + Purpose)
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
%   %         odrl:rightOperand dpv:ResearchAndDevelopment ] ] .
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
%   %         odrl:rightOperand dpv:AcademicResearch ] ] .
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
%   %         odrl:rightOperand dpv:ResearchAndDevelopment ] ] .
%
% Formal test:
%   3-way multi-dim: all 3 pairs compatible on BOTH dimensions.
%   %   A∩B: spatial(europe∩germany=germany) ∧ purpose(R&D∩academic=academic) → Compatible
%   %   A∩C: spatial(europe∩wE=wE) ∧ purpose(R&D∩R&D=R&D) → Compatible
%   %   B∩C: spatial(germany∩wE=germany) ∧ purpose(academic∩R&D=academic) → Compatible
%   %   Witness sets: (germany, academicResearch) for all pairs
%
% One-liner : 3-policy multi-dim: all pairs Compatible on spatial+purpose
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
% --- DPV Fragment (DAG-SAFE sibling disjointness) ---
% Same hierarchy as NAIVE, but disjoint(commercialPurpose, researchAndDevelopment)
% is SUPPRESSED because ↓commercialPurpose ∩ ↓researchAndDevelopment ≠ ∅.
% DAG-safety algorithm (Note 1): suppress disj(A,B) when ∃C: C ≤ A ∧ C ≤ B.

% Hierarchy (identical to NAIVE)
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

% Reflexivity
fof(dpv_s_refl1, axiom, leq(purpose, purpose)).
fof(dpv_s_refl2, axiom, leq(commercialPurpose, commercialPurpose)).
fof(dpv_s_refl3, axiom, leq(researchAndDevelopment, researchAndDevelopment)).
fof(dpv_s_refl4, axiom, leq(commercialResearch, commercialResearch)).
fof(dpv_s_refl5, axiom, leq(academicResearch, academicResearch)).
fof(dpv_s_refl6, axiom, leq(serviceProvision, serviceProvision)).

% DAG-SAFE sibling disjointness — SUPPRESSED: commercialPurpose ⊥ R&D
% Only safe pairs remain:
fof(dpv_s_disj_safe1, axiom,
    disjoint(commercialPurpose, serviceProvision)).
fof(dpv_s_disj_safe2, axiom,
    disjoint(researchAndDevelopment, serviceProvision)).

% UNA
fof(dpv_s_una, axiom,
    $distinct(purpose, commercialPurpose, researchAndDevelopment,
              commercialResearch, academicResearch, serviceProvision)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl170, conjecture,
    ( ?[Xs,Xp]: ( in_denotation(Xs, europe, isPartOf)
                & in_denotation(Xs, germany, eq)
                & in_denotation(Xp, researchAndDevelopment, isA)
                & in_denotation(Xp, academicResearch, isA) )
    & ?[Ys,Yp]: ( in_denotation(Ys, europe, isPartOf)
                & in_denotation(Ys, westernEurope, isPartOf)
                & in_denotation(Yp, researchAndDevelopment, isA)
                & in_denotation(Yp, researchAndDevelopment, isA) )
    & ?[Zs,Zp]: ( in_denotation(Zs, germany, eq)
                & in_denotation(Zs, westernEurope, isPartOf)
                & in_denotation(Zp, academicResearch, isA)
                & in_denotation(Zp, researchAndDevelopment, isA) ) )).

%--------------------------------------------------------------------------