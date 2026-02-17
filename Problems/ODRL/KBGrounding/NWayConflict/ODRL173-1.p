%--------------------------------------------------------------------------
% File     : ODRL173-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : N-Way Composed — 3 Operands × 3 Policies
% Expected : Theorem
% Verdict  : Compatible
% Paper    : N-Way Composed — 3 Operands × 3 Policies
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
%   %         odrl:rightOperand dpv:ResearchAndDevelopment ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:language ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand lang:en ] ] .
%
% Formal test:
%   Maximum complexity: 3 operands × 3 policies = 9 pairwise operand checks.
%   %   Tests: Vampire's ability to find witnesses across 3 dimensions and 3 policies.
%   %   All 3 pairs compatible on all 3 dimensions.
%
% One-liner : 3-operand × 3-policy: maximum complexity test
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/LANG000-0.ax').
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
fof(odrl173, conjecture,
    ( ?[Xs,Xp,Xl]: ( in_denotation(Xs, europe, isPartOf)
                   & in_denotation(Xs, germany, eq)
                   & in_denotation(Xp, researchAndDevelopment, isA)
                   & in_denotation(Xp, academicResearch, isA)
                   & in_denotation(Xl, en, isPartOf)
                   & in_denotation(Xl, enGB, eq) )
    & ?[Ys,Yp,Yl]: ( in_denotation(Ys, europe, isPartOf)
                   & in_denotation(Ys, westernEurope, isPartOf)
                   & in_denotation(Yp, researchAndDevelopment, isA)
                   & in_denotation(Yp, researchAndDevelopment, isA)
                   & in_denotation(Yl, en, isPartOf)
                   & in_denotation(Yl, en, isPartOf) )
    & ?[Zs,Zp,Zl]: ( in_denotation(Zs, germany, eq)
                   & in_denotation(Zs, westernEurope, isPartOf)
                   & in_denotation(Zp, academicResearch, isA)
                   & in_denotation(Zp, researchAndDevelopment, isA)
                   & in_denotation(Zl, enGB, eq)
                   & in_denotation(Zl, en, isPartOf) ) )).

%--------------------------------------------------------------------------