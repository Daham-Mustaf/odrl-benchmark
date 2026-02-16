%--------------------------------------------------------------------------
% File     : ODRL041-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : AND-Conflict: spatial ✓ ∧ purpose ✗ → Conflict
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 6 (Composition, and)
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:europe ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:AcademicResearch ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:germany ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:Marketing ] ] .
%
% Denotation analysis:
%   V_spatial=Compatible, V_purpose=Conflict → AND-Conflict
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl041, conjecture,
    ![Xp]: ~( in_denotation(Xp, academicResearch, isA)
            & in_denotation(Xp, marketing, isA) )).
%--------------------------------------------------------------------------
