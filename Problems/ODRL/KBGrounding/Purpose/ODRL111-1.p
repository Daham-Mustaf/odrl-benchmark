%--------------------------------------------------------------------------
% File     : ODRL111-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Redundancy: isA(advertising) ⊆ isA(marketing) — broader is redundant
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7 (redundancy)
% Category : subsumption
%
% ODRL Policy (Turtle):
%   Same rule, two constraints:
%   c1: isA(advertising), c2: isA(marketing)
%   c1 ⊆ c2 → c2 is redundant (subsumed by c1)
%
% Denotation analysis:
%   Policy simplification: remove redundant broader constraint.
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl111, conjecture,
    ![X]: ( in_denotation(X, advertising, isA)
          => in_denotation(X, marketing, isA) )).
%--------------------------------------------------------------------------
