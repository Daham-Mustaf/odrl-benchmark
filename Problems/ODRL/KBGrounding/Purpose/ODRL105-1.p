%--------------------------------------------------------------------------
% File     : ODRL105-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Subsumption refuted: isA(marketing) ⊄ isA(advertising)
% Expected : Theorem
% Verdict  : Refuted
% Paper    : Definition 7
% Category : subsumption
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   c1: isA(marketing), c2: isA(advertising)
%
% Denotation analysis:
%   Counterexample: directMarketing ∈ ↓mkt but directMarketing ∉ ↓adv
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl105, conjecture,
    ?[X]: ( in_denotation(X, marketing, isA)
          & ~in_denotation(X, advertising, isA) )).
%--------------------------------------------------------------------------
