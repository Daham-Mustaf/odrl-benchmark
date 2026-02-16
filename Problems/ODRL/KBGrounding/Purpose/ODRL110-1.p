%--------------------------------------------------------------------------
% File     : ODRL110-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Cross-operator: eq(advertising) ⊆ neq(customerManagement)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7 (cross neq)
% Category : subsumption
%
% ODRL Policy (Turtle):
%   c1: eq(advertising), c2: neq(customerManagement)
%
% Denotation analysis:
%   advertising ≤ marketing, disjoint(marketing, customerManagement)
%   → advertising ≠ customerManagement → {adv} ⊆ C\{cm}
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl110, conjecture,
    ![X]: ( in_denotation(X, advertising, eq)
          => in_denotation(X, customerManagement, neq) )).
%--------------------------------------------------------------------------
