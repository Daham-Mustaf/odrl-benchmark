%--------------------------------------------------------------------------
% File     : ODRL056-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : KB inconsistency: naive sibling disjointness violates Lemma 1
% Expected : ContradictoryAxioms
% Verdict  : Inconsistent
% Paper    : Note 1 — Multi-Parent Contradiction (NAIVE mode)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:commercialResearch ] ] .
%
% Denotation analysis:
%   DPV-NAIVE.ax contains ALL 285 sibling pairs including:
%   disjoint(commercialPurpose, researchAndDevelopment) [d_0044]
%   leq(commercialResearch, commercialPurpose) [h_0006]
%   leq(commercialResearch, researchAndDevelopment) [h_0007]
% Proof: disj_downward(d_0044, h_0006) + disj_downward(d_0044, h_0007)
%   → disjoint(commercialResearch, commercialResearch)
%   → contradicts disj_irrefl (Lemma 1) → UNSATISFIABLE
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV-NAIVE.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl056, conjecture, false).
%--------------------------------------------------------------------------
