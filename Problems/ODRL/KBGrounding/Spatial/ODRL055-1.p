%--------------------------------------------------------------------------
% File     : ODRL055-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption refuted: hasPart(germany) ⊄ hasPart(europe)
% Expected : Theorem
% Verdict  : Refuted
% Paper    : Definition 7
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:germany ] .
%   c2: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] .
%
% Denotation analysis:
%   Counterexample: germany ∈ ⟦c1⟧ but germany ∉ ⟦c2⟧
%   Paired with ODRL054: hasPart subsumption asymmetry.
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl055, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & ~in_denotation(X, europe, hasPart) )).
%--------------------------------------------------------------------------
