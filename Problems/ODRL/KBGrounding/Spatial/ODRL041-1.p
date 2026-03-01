%--------------------------------------------------------------------------
% File     : ODRL041-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : AND-Conflict: V_spatial=Compatible ∧ V_purpose=Conflict
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 6 (Composition, and)
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ; odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] ;
%       odrl:constraint [ odrl:leftOperand odrl:hasPurpose ; odrl:operator odrl:isA ; odrl:rightOperand dpv:AcademicResearch ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ; odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] ;
%       odrl:constraint [ odrl:leftOperand odrl:hasPurpose ; odrl:operator odrl:isA ; odrl:rightOperand dpv:AcademicResearch ] ] .
%
% Formal:
%   purpose: isA(academicResearch) ∩ isA(marketing)
%   disj(academicResearch, marketing) in DPV000-0.ax
%   → disj_downward → ∀X: leq(X,aR) ∧ leq(X,mk) → contradiction
%   AND: purpose conflict → overall Conflict
%
% Notes    : flip_conj targets purpose dimension only — sufficient for AND-Conflict.
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl041, conjecture,
    ![Xp]: ~( in_denotation(Xp, academicResearch, isA)
            & in_denotation(Xp, marketing, isA) )).
%--------------------------------------------------------------------------
