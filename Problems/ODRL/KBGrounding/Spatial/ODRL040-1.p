%--------------------------------------------------------------------------
% File     : ODRL040-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : AND-Compatible: V_spatial=Compatible ∧ V_purpose=Compatible
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 6 (Composition, and)
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ; odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] ;
%       odrl:constraint [ odrl:leftOperand odrl:hasPurpose ; odrl:operator odrl:isA ; odrl:rightOperand dpv:ResearchAndDevelopment ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ; odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] ;
%       odrl:constraint [ odrl:leftOperand odrl:hasPurpose ; odrl:operator odrl:isA ; odrl:rightOperand dpv:ResearchAndDevelopment ] ] .
%
% Formal:
%   Xs=germany:   leq(germany,europe) ∧ germany=germany  ✓
%   Xp=academicResearch: leq(aR,R&D) ∧ leq(aR,aR)   ✓
%   AND: both ✓ → Compatible
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl040, conjecture,
    ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)
             & in_denotation(Xs, germany, eq) )
    & ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)
             & in_denotation(Xp, academicResearch, isA) ) )).
%--------------------------------------------------------------------------
