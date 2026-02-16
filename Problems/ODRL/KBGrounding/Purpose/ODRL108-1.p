%--------------------------------------------------------------------------
% File     : ODRL108-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Subsumption refuted: hasPart(advertising) ⊄ hasPart(marketing)
% Expected : Theorem
% Verdict  : Refuted
% Paper    : Definition 7
% Category : subsumption
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   c1: hasPart(advertising), c2: hasPart(marketing)
%
% Denotation analysis:
%   Counterexample: advertising ∈ ⟦hasPart(adv)⟧ but advertising ∉ ⟦hasPart(mkt)⟧
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl108, conjecture,
    ?[X]: ( in_denotation(X, advertising, hasPart)
          & ~in_denotation(X, marketing, hasPart) )).
%--------------------------------------------------------------------------
