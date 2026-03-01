%--------------------------------------------------------------------------
% File     : ODRL088-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Downward asymmetry: ISO alone cannot detect dE ⊥ pL conflict
% Expected : Theorem
% Verdict  : Unknown
% Paper    : Proposition 2(2) — Downward Asymmetry: Flat KB Alone
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ISO 3166 has $distinct(dE, pL, ...) for UNA (dE ≠ pL).
%   BUT $distinct only enforces term inequality, NOT disjointness.
%   disjoint(X,Y) means: ¬∃Z: (leq(Z,X) ∧ leq(Z,Y)).
%   Without explicit disjoint/2, model could add leq(dE, pL) edge.
%   → disjoint(dE, pL) is NOT derivable from ISO alone.
%   Compare ODRL081 (same conjecture, adds GEO+alignment → Conflict).
%
% Denotation analysis:
%   % Conflict detection requires structured KBs with disjointness axioms. Code lists alone are insufficient.

%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl088, conjecture,
    ?[X]: ( in_denotation(X, dE, isPartOf)
          & in_denotation(X, pL, isPartOf) )).

ISO 3166 has NO disjointness axioms (flat code list).
%   disjoint(dE, pL) is NOT derivable from ISO alone.
%   Compare ODRL081 (same conjecture, adds GEO+alignment → Conflict).
%   Demonstrates: structural disjointness from a richer KB is
%   necessary for cross-dataspace conflict detection.
%--------------------------------------------------------------------------
