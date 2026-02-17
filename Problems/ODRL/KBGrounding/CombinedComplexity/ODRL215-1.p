%--------------------------------------------------------------------------
% File     : ODRL215-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Ultimate — 4 KBs × 3 Policies × 3 Operands × Set Ops × DAG
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Ultimate — 4 KBs × 3 Policies × 3 Operands × Set Ops × DAG
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAnyOf ;
%   %         odrl:rightOperand ( comp:gdprFull ) ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand dpv:CommercialPurpose ] ;
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
%   %         odrl:rightOperand comp:complianceScope ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand dpv:ResearchAndDevelopment ] ;
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
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand comp:gdprFull ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand dpv:CommercialResearch ] ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:language ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand lang:en ] ] .
%
% Formal test:
%   Ultimate: 4 KBs + 3 policies + 3 operands + set ops + DAG.
%   %   All pairs Compatible: witness (gdprFull, cR, enGB) for all.
%   %   Extreme: maximum axiom load — GEO+ISO+SYNTH+COMP+DPV+LANG+ODRL+ALIGN.
%   %   Tests: prover scalability with all infrastructure loaded.
%
% One-liner : Ultimate: 4 KBs × 3 policies × 3 operands × set ops × DAG
% Difficulty: Extreme
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_extreme_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').
include('Axioms/Layer0-DomainKB/LANG000-0.ax').

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
% --- Synthetic KB (SYNTH) — NO native disjointness ---
fof(synth_root, axiom, concept(euZone)).
fof(synth_c1, axiom, concept(zoneWest)).
fof(synth_c2, axiom, concept(zoneEast)).
fof(synth_leq1, axiom, leq(zoneWest, euZone)).
fof(synth_leq2, axiom, leq(zoneEast, euZone)).
fof(synth_refl1, axiom, leq(euZone, euZone)).
fof(synth_refl2, axiom, leq(zoneWest, zoneWest)).
fof(synth_refl3, axiom, leq(zoneEast, zoneEast)).
fof(synth_una, axiom, $distinct(euZone, zoneWest, zoneEast)).
% Alignment: ISO 3166 → SYNTH
fof(align_iso_synth_1, axiom, align(europe, euZone)).
fof(align_iso_synth_2, axiom, align(dE, zoneWest)).
fof(align_iso_synth_3, axiom, align(pL, zoneEast)).
% --- Compliance KB (COMP) — NO native disjointness ---
fof(comp_root, axiom, concept(complianceScope)).
fof(comp_c1, axiom, concept(gdprFull)).
fof(comp_c2, axiom, concept(gdprPartial)).
fof(comp_leq1, axiom, leq(gdprFull, complianceScope)).
fof(comp_leq2, axiom, leq(gdprPartial, complianceScope)).
fof(comp_refl1, axiom, leq(complianceScope, complianceScope)).
fof(comp_refl2, axiom, leq(gdprFull, gdprFull)).
fof(comp_refl3, axiom, leq(gdprPartial, gdprPartial)).
fof(comp_una, axiom, $distinct(complianceScope, gdprFull, gdprPartial)).
% Alignment: SYNTH → COMP
fof(align_synth_comp_1, axiom, align(euZone, complianceScope)).
fof(align_synth_comp_2, axiom, align(zoneWest, gdprFull)).
fof(align_synth_comp_3, axiom, align(zoneEast, gdprPartial)).
fof(list_215, axiom, in_value_list(gdprFull, anyList215)).
fof(list_anyList215_closed, axiom,
    ![G]: (in_value_list(G, anyList215) => (G = gdprFull))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl215, conjecture,
    ( ?[Xs,Xp,Xl]: ( in_denotation_set(Xs, anyList215, isAnyOf)
                   & in_denotation(Xs, complianceScope, isPartOf)
                   & in_denotation(Xp, commercialPurpose, isA)
                   & in_denotation(Xp, researchAndDevelopment, isA)
                   & in_denotation(Xl, en, isPartOf)
                   & in_denotation(Xl, enGB, eq) )
    & ?[Ys,Yp,Yl]: ( in_denotation_set(Ys, anyList215, isAnyOf)
                   & in_denotation(Ys, gdprFull, eq)
                   & in_denotation(Yp, commercialPurpose, isA)
                   & in_denotation(Yp, commercialResearch, isA)
                   & in_denotation(Yl, en, isPartOf)
                   & in_denotation(Yl, en, isPartOf) )
    & ?[Zs,Zp,Zl]: ( in_denotation(Zs, complianceScope, isPartOf)
                   & in_denotation(Zs, gdprFull, eq)
                   & in_denotation(Zp, researchAndDevelopment, isA)
                   & in_denotation(Zp, commercialResearch, isA)
                   & in_denotation(Zl, enGB, eq)
                   & in_denotation(Zl, en, isPartOf) ) )).

%--------------------------------------------------------------------------