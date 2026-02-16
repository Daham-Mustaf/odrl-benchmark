%--------------------------------------------------------------------------
% File     : ODRL077-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Subsumption across 4-level chain: isA(targetedAdv) ⊆ isA(marketing)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7 (Subsumption)
% Category : basic
%
% ODRL Policy (Turtle):
%   c1: isA(targetedAdvertising), c2: isA(marketing)
%
% Denotation analysis:
%   targetedAdv ≤ personalisedAdv ≤ advertising ≤ marketing
%   ⟦isA(targetedAdv)⟧ ⊆ ⟦isA(marketing)⟧ via depth-4 chain
%
% Difficulty: Medium-Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl077, conjecture,
    ![X]: ( in_denotation(X, targetedAdvertising, isA)
          => in_denotation(X, marketing, isA) )).
%--------------------------------------------------------------------------
