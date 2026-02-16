%--------------------------------------------------------------------------
% File     : ODRL037-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption refuted: neq(germany) ⊄ isPartOf(westernEurope)
% Expected : Theorem
% Verdict  : Refuted
% Paper    : Definition 7
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:neq ; odrl:rightOperand geo:germany ] .
%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] .
%
% Denotation analysis:
%   Counterexample: poland ∈ ⟦neq(de)⟧ but poland ∉ ⟦isPartOf(wE)⟧
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl037, conjecture,
    ?[X]: ( in_denotation(X, germany, neq)
          & ~in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
