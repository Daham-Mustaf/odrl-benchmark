%--------------------------------------------------------------------------
% File     : ODRL066-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict: eq(advertising) ∩ isA(customerManagement) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3, Definition 5
% Category : basic
% Encoding : prover-friendly (flipped for refutation provers)
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
%         odrl:rightOperand dpv:CustomerManagement ] ] .
%
% Denotation analysis:
%   advertising ≤ marketing, disjoint(marketing, customerManagement) [d_0083]
%   → advertising ∉ ↓customerManagement (disj_downward) → ∅
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl066, conjecture,
    ![X]: ~( in_denotation(X, advertising, eq)
           & in_denotation(X, customerManagement, isA) )).
%--------------------------------------------------------------------------
