%--------------------------------------------------------------------------
% File     : ODRL106-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Cross-operator: eq(directMarketing) ⊆ isA(marketing)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7 (cross-operator)
% Category : subsumption
%
% ODRL Policy (Turtle):
%   c1: eq(directMarketing), c2: isA(marketing)
%
% Denotation analysis:
%   directMarketing ≤ marketing → {directMarketing} ⊆ ↓mkt
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl106, conjecture,
    ![X]: ( in_denotation(X, directMarketing, eq)
          => in_denotation(X, marketing, isA) )).
%--------------------------------------------------------------------------
