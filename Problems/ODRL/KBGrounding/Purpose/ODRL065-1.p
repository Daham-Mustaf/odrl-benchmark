%--------------------------------------------------------------------------
% File     : ODRL065-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: eq(advertising) ∩ isA(marketing) — child in subtree
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3, Definition 5
% Category : basic
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand dpv:Advertising ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:Marketing ] ] .
%
% Denotation analysis:
%   advertising ∈ ⟦isA(marketing)⟧ since advertising ≤ marketing [h_0002]
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl065, conjecture,
    ?[X]: ( in_denotation(X, advertising, eq)
          & in_denotation(X, marketing, isA) )).
%--------------------------------------------------------------------------
