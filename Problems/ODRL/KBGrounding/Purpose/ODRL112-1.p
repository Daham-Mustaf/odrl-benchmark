%--------------------------------------------------------------------------
% File     : ODRL112-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Transitive subsumption: isA(targetedAdv) ⊆ isA(adv) ⊆ isA(marketing)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7 (transitivity)
% Category : subsumption
%
% ODRL Policy (Turtle):
%   c1: isA(targetedAdvertising) ⊆ c2: isA(advertising) ⊆ c3: isA(marketing)
%
% Denotation analysis:
%   Subsumption transitivity over 3 constraints.
%
% Difficulty: Medium-Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl112, conjecture,
    ![X]: ( in_denotation(X, targetedAdvertising, isA)
          => in_denotation(X, marketing, isA) )).
%--------------------------------------------------------------------------
