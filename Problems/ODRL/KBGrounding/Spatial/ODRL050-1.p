%--------------------------------------------------------------------------
% File     : ODRL050-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Self-compatible: isPartOf(europe) ∩ isPartOf(europe) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 5 (identity)
%
% ODRL Policy (Turtle):
%   Identical constraints on two rules.
%
% Denotation analysis:
%   ⟦isPartOf(eu)⟧ ∩ ⟦isPartOf(eu)⟧ = ⟦isPartOf(eu)⟧ ≠ ∅
%
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl050, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
