%--------------------------------------------------------------------------
% File     : ODRL057-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : DAG-safe: suppressed pair allows multi-parent witness
% Expected : Theorem
% Verdict  : Consistent
% Paper    : Note 1 — DAG-Safe Preserves Consistency
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
%   DPV000-0.ax (DAG-SAFE) suppresses problematic pair:
%   disjoint(commercialPurpose, researchAndDevelopment) NOT asserted
%   because ↓commercialPurpose ∩ ↓researchAndDevelopment ≠ ∅
% Witness: commercialResearch ∈ both closures
% Result: KB is CONSISTENT, multi-parent concept works correctly
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl057, conjecture,
    ?[X]: ( in_denotation(X, commercialPurpose, isA)
          & in_denotation(X, researchAndDevelopment, isA) )).
%--------------------------------------------------------------------------
