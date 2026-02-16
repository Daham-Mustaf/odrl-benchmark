%--------------------------------------------------------------------------
% File     : ODRL031-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption refuted: isPartOf(europe) ⊄ isPartOf(germany)
% Expected : Theorem
% Verdict  : Refuted
% Paper    : Definition 7
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .
%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:germany ] .
%
% Denotation analysis:
%   Counterexample: france ∈ ⟦c1⟧ but france ∉ ⟦c2⟧
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl031, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & ~in_denotation(X, germany, isPartOf) )).
%--------------------------------------------------------------------------
