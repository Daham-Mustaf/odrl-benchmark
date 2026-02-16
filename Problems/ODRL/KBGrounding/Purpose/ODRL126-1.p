%--------------------------------------------------------------------------
% File     : ODRL126-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Root coverage: isA(purpose) = C → always compatible
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (root)
% Category : edge
%
% ODRL Policy (Turtle):
%   isA(purpose) covers entire concept space → compatible with anything grounded.
%
% Denotation analysis:
%   ⟦isA(purpose)⟧ = C, ⟦eq(advertising)⟧ = {advertising}. Witness: advertising
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl126, conjecture,
    ?[X]: ( in_denotation(X, purpose, isA)
          & in_denotation(X, advertising, eq) )).
%--------------------------------------------------------------------------
