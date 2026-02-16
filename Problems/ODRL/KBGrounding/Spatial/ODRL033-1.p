%--------------------------------------------------------------------------
% File     : ODRL033-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Tautological equivalence: isA(germany) ≡ isPartOf(germany)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 3 (isA=isPartOf), Definition 7
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:isA ; odrl:rightOperand geo:germany ] .
%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:germany ] .
%
% Denotation analysis:
%   TAUTOLOGY: isA and isPartOf have identical denotation.
%
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl033, conjecture,
    ![X]: ( in_denotation(X, germany, isA)
        <=> in_denotation(X, germany, isPartOf) )).
%--------------------------------------------------------------------------
