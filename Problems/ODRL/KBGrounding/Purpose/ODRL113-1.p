%--------------------------------------------------------------------------
% File     : ODRL113-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Subsumption refuted: neq(marketing) ⊄ isA(enforceSecurity)
% Expected : Theorem
% Verdict  : Refuted
% Paper    : Definition 7
% Category : subsumption
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   c1: neq(marketing), c2: isA(enforceSecurity)
%
% Denotation analysis:
%   Counterexample: purpose ∈ C\{marketing} but purpose ∉ ↓enforceSecurity
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl113, conjecture,
    ?[X]: ( in_denotation(X, marketing, neq)
          & ~in_denotation(X, enforceSecurity, isA) )).
%--------------------------------------------------------------------------
