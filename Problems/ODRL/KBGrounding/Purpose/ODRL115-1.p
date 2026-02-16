%--------------------------------------------------------------------------
% File     : ODRL115-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : AND-Conflict: purpose ✗ ∧ spatial ✓ → Conflict
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 6 (AND)
% Category : composition
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:Marketing ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:Europe ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:EnforceSecurity ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:Germany ] ] .
%
% Denotation analysis:
%   V_purpose=Conflict(mkt⊥sec), V_spatial=Compatible → AND=Conflict
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl115, conjecture,
    ![Xp]: ~( in_denotation(Xp, marketing, isA)
            & in_denotation(Xp, enforceSecurity, isA) )).
%--------------------------------------------------------------------------
