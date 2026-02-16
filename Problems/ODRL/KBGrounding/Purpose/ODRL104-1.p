%--------------------------------------------------------------------------
% File     : ODRL104-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Subsumption: isA(advertising) ⊆ isA(marketing)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7
% Category : subsumption
%
% ODRL Policy (Turtle):
%   c1: isA(advertising), c2: isA(marketing)
%
% Denotation analysis:
%   advertising ≤ marketing → ↓adv ⊆ ↓mkt
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl104, conjecture,
    ![X]: ( in_denotation(X, advertising, isA)
          => in_denotation(X, marketing, isA) )).
%--------------------------------------------------------------------------
