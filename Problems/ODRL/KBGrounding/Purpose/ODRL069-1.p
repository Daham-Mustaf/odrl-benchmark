%--------------------------------------------------------------------------
% File     : ODRL069-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Tautological equivalence: isA(marketing) ≡ isPartOf(marketing)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 3 (isA≡isPartOf)
% Category : basic
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:isA ; odrl:rightOperand dpv:Marketing ] .
%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand dpv:Marketing ] .
%
% Denotation analysis:
%   TAUTOLOGY: isA and isPartOf have identical denotation (Def 3).
%
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl069, conjecture,
    ![X]: ( in_denotation(X, marketing, isA)
        <=> in_denotation(X, marketing, isPartOf) )).
%--------------------------------------------------------------------------
