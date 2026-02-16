%--------------------------------------------------------------------------
% File     : ODRL062-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Non-tautological: hasPart(europe) = {europe} ≠ C
% Expected : Theorem
% Verdict  : Non-Tautological
% Paper    : Tautology Detection (hasPart root)
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   c: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] .
%
% Denotation analysis:
%   ⟦hasPart(europe)⟧ = {x ∈ C | europe ≤ x} = {europe}
%   europe is maximal (root) → only europe itself satisfies hasPart(europe)
%   This is NOT tautological: |⟦hasPart(europe)⟧| = 1, |C| = 58
%   Counterexample: germany — europe ¬≤ germany
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl062, conjecture,
    ?[X]: ( concept(X) & ~in_denotation(X, europe, hasPart) )).
%--------------------------------------------------------------------------
