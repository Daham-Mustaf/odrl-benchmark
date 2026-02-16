%--------------------------------------------------------------------------
% File     : ODRL061-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Non-tautological: isPartOf(westernEurope) ⊂ C
% Expected : Theorem
% Verdict  : Non-Tautological
% Paper    : Tautology Detection
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   c: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] .
%
% Denotation analysis:
%   ⟦isPartOf(westernEurope)⟧ = ↓wE = {wE, austria, belgium, france,
%     germany, liechtenstein, luxembourg, monaco, netherlands, switzerland}
%   Only 10 of 58 concepts. Counterexample: poland (≤ eE, ¬≤ wE)
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl061, conjecture,
    ?[X]: ( concept(X) & ~in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
