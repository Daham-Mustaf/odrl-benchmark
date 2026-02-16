%--------------------------------------------------------------------------
% File     : ODRL060-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Tautology: isPartOf(europe) = C (root covers all concepts)
% Expected : Theorem
% Verdict  : Tautological
% Paper    : Tautology Detection
%
% ODRL Policy (Turtle):
%   c: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .
%
% Denotation analysis:
%   ⟦isPartOf(europe)⟧ = {x ∈ C | x ≤ europe} = C
%   europe is the root of GEO KB → every concept is ≤ europe
%   via transitivity (country → sub-region → europe) → tautological
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl060, conjecture,
    ![X]: ( concept(X) => in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
