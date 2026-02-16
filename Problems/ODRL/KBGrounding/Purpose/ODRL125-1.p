%--------------------------------------------------------------------------
% File     : ODRL125-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Self-compatible: isA(marketing) ∩ isA(marketing) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 5 (identity)
% Category : edge
%
% ODRL Policy (Turtle):
%   Identical constraints on permission and prohibition.
%
% Denotation analysis:
%   ⟦isA(mkt)⟧ ∩ ⟦isA(mkt)⟧ = ⟦isA(mkt)⟧ ≠ ∅
%
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl125, conjecture,
    ?[X]: ( in_denotation(X, marketing, isA)
          & in_denotation(X, marketing, isA) )).
%--------------------------------------------------------------------------
