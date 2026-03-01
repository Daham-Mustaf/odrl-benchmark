%--------------------------------------------------------------------------
% File     : DPV_C06_full.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection — E3 Incompleteness Sweep
% KB       : DPV
% Level    : full (0% disjointness removed)
% Problem  : DPV_C06
% Expected : Theorem
% Operator : isA
% Date     : 2026-02-28
% Purpose  : E3 — Validate graceful degradation over incomplete hierarchies
%--------------------------------------------------------------------------

include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Inline KB (DPV, 0% incomplete) ──────────────────────────
fof(dpv_c_purpose,  axiom, concept(purpose)).
fof(dpv_c_cP,       axiom, concept(commercialPurpose)).
fof(dpv_c_RD,       axiom, concept(researchAndDevelopment)).
fof(dpv_c_sP,       axiom, concept(serviceProvision)).
fof(dpv_c_leg,      axiom, concept(legalCompliance)).
fof(dpv_c_mkt,      axiom, concept(marketing)).
fof(dpv_c_cR,       axiom, concept(commercialResearch)).
fof(dpv_c_acR,      axiom, concept(academicResearch)).
fof(dpv_c_pubR,     axiom, concept(publicResearch)).
fof(dpv_c_prod,     axiom, concept(productDevelopment)).
% Hierarchy
fof(dpv_leq_cP_pur,   axiom, leq(commercialPurpose, purpose)).
fof(dpv_leq_RD_pur,   axiom, leq(researchAndDevelopment, purpose)).
fof(dpv_leq_sP_pur,   axiom, leq(serviceProvision, purpose)).
fof(dpv_leq_leg_pur,  axiom, leq(legalCompliance, purpose)).
fof(dpv_leq_mkt_pur,  axiom, leq(marketing, purpose)).
fof(dpv_leq_cR_cP,    axiom, leq(commercialResearch, commercialPurpose)).
fof(dpv_leq_cR_RD,    axiom, leq(commercialResearch, researchAndDevelopment)).
fof(dpv_leq_acR_RD,   axiom, leq(academicResearch, researchAndDevelopment)).
fof(dpv_leq_pubR_RD,  axiom, leq(publicResearch, researchAndDevelopment)).
fof(dpv_leq_prod_cP,  axiom, leq(productDevelopment, commercialPurpose)).
% Reflexivity
fof(dpv_refl_pur,  axiom, leq(purpose, purpose)).
fof(dpv_refl_cP,   axiom, leq(commercialPurpose, commercialPurpose)).
fof(dpv_refl_RD,   axiom, leq(researchAndDevelopment, researchAndDevelopment)).
fof(dpv_refl_sP,   axiom, leq(serviceProvision, serviceProvision)).
fof(dpv_refl_leg,  axiom, leq(legalCompliance, legalCompliance)).
fof(dpv_refl_mkt,  axiom, leq(marketing, marketing)).
fof(dpv_refl_cR,   axiom, leq(commercialResearch, commercialResearch)).
fof(dpv_refl_acR,  axiom, leq(academicResearch, academicResearch)).
fof(dpv_refl_pubR, axiom, leq(publicResearch, publicResearch)).
fof(dpv_refl_prod, axiom, leq(productDevelopment, productDevelopment)).
fof(dpv_trans, axiom, ![X,Y,Z]: (leq(X,Y) & leq(Y,Z) => leq(X,Z))).
fof(dpv_una, axiom, $distinct(purpose, commercialPurpose, researchAndDevelopment,
    serviceProvision, legalCompliance, marketing,
    commercialResearch, academicResearch, publicResearch, productDevelopment)).

% DPV disjointness: 22/22 kept (0% removed)
fof(dpv_disj_cP_sP, axiom, disjoint(commercialPurpose,serviceProvision)).
fof(dpv_disj_cP_sP_sym, axiom, disjoint(serviceProvision,commercialPurpose)).
fof(dpv_disj_cP_leg, axiom, disjoint(commercialPurpose,legalCompliance)).
fof(dpv_disj_cP_leg_sym, axiom, disjoint(legalCompliance,commercialPurpose)).
fof(dpv_disj_cP_mkt, axiom, disjoint(commercialPurpose,marketing)).
fof(dpv_disj_cP_mkt_sym, axiom, disjoint(marketing,commercialPurpose)).
fof(dpv_disj_RD_sP, axiom, disjoint(researchAndDevelopment,serviceProvision)).
fof(dpv_disj_RD_sP_sym, axiom, disjoint(serviceProvision,researchAndDevelopment)).
fof(dpv_disj_RD_leg, axiom, disjoint(researchAndDevelopment,legalCompliance)).
fof(dpv_disj_RD_leg_sym, axiom, disjoint(legalCompliance,researchAndDevelopment)).
fof(dpv_disj_RD_mkt, axiom, disjoint(researchAndDevelopment,marketing)).
fof(dpv_disj_RD_mkt_sym, axiom, disjoint(marketing,researchAndDevelopment)).
fof(dpv_disj_sP_leg, axiom, disjoint(serviceProvision,legalCompliance)).
fof(dpv_disj_sP_leg_sym, axiom, disjoint(legalCompliance,serviceProvision)).
fof(dpv_disj_sP_mkt, axiom, disjoint(serviceProvision,marketing)).
fof(dpv_disj_sP_mkt_sym, axiom, disjoint(marketing,serviceProvision)).
fof(dpv_disj_leg_mkt, axiom, disjoint(legalCompliance,marketing)).
fof(dpv_disj_leg_mkt_sym, axiom, disjoint(marketing,legalCompliance)).
fof(dpv_disj_cR_sP, axiom, disjoint(commercialResearch,serviceProvision)).
fof(dpv_disj_cR_sP_sym, axiom, disjoint(serviceProvision,commercialResearch)).
fof(dpv_disj_cR_leg, axiom, disjoint(commercialResearch,legalCompliance)).
fof(dpv_disj_cR_leg_sym, axiom, disjoint(legalCompliance,commercialResearch)).
fof(dpv_disj_cR_mkt, axiom, disjoint(commercialResearch,marketing)).
fof(dpv_disj_cR_mkt_sym, axiom, disjoint(marketing,commercialResearch)).
fof(dpv_disj_acR_sP, axiom, disjoint(academicResearch,serviceProvision)).
fof(dpv_disj_acR_sP_sym, axiom, disjoint(serviceProvision,academicResearch)).
fof(dpv_disj_acR_cP, axiom, disjoint(academicResearch,commercialPurpose)).
fof(dpv_disj_acR_cP_sym, axiom, disjoint(commercialPurpose,academicResearch)).
fof(dpv_disj_acR_leg, axiom, disjoint(academicResearch,legalCompliance)).
fof(dpv_disj_acR_leg_sym, axiom, disjoint(legalCompliance,academicResearch)).
fof(dpv_disj_acR_mkt, axiom, disjoint(academicResearch,marketing)).
fof(dpv_disj_acR_mkt_sym, axiom, disjoint(marketing,academicResearch)).
fof(dpv_disj_pubR_cP, axiom, disjoint(publicResearch,commercialPurpose)).
fof(dpv_disj_pubR_cP_sym, axiom, disjoint(commercialPurpose,publicResearch)).
fof(dpv_disj_pubR_sP, axiom, disjoint(publicResearch,serviceProvision)).
fof(dpv_disj_pubR_sP_sym, axiom, disjoint(serviceProvision,publicResearch)).
fof(dpv_disj_pubR_leg, axiom, disjoint(publicResearch,legalCompliance)).
fof(dpv_disj_pubR_leg_sym, axiom, disjoint(legalCompliance,publicResearch)).
fof(dpv_disj_prod_RD, axiom, disjoint(productDevelopment,researchAndDevelopment)).
fof(dpv_disj_prod_RD_sym, axiom, disjoint(researchAndDevelopment,productDevelopment)).
fof(dpv_disj_prod_sP, axiom, disjoint(productDevelopment,serviceProvision)).
fof(dpv_disj_prod_sP_sym, axiom, disjoint(serviceProvision,productDevelopment)).
fof(dpv_disj_prod_leg, axiom, disjoint(productDevelopment,legalCompliance)).
fof(dpv_disj_prod_leg_sym, axiom, disjoint(legalCompliance,productDevelopment)).

% ─── Conjecture ──────────────────────────────────────────────────────────
fof(dpv_c06, conjecture, ![X]: ~(in_denotation(X,productDevelopment,isA) & in_denotation(X,researchAndDevelopment,isA))).

%--------------------------------------------------------------------------
