%--------------------------------------------------------------------------
% File     : ODRL076-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: 4-level transitivity chain to root
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 2, Definition 3
% Category : basic
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:Purpose ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand dpv:TargetedAdvertising ] ] .
%
% Denotation analysis:
%   Depth-4 chain: targetedAdv→personalisedAdv→advertising→marketing→purpose
%   targetedAdvertising ∈ ⟦isA(purpose)⟧ via 4 transitivity steps
%
% Difficulty: Medium-Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl076, conjecture,
    ?[X]: ( in_denotation(X, purpose, isA)
          & in_denotation(X, targetedAdvertising, eq) )).
%--------------------------------------------------------------------------
