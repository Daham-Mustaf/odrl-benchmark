%--------------------------------------------------------------------------
% File     : ODRL030-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption: isPartOf(germany) ⊆ isPartOf(europe)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7 (Constraint Subsumption)
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:germany ] .
%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .
%
% Denotation analysis:
%   {germany} ⊆ {x|x≤europe} → Confirmed
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl030, conjecture,
    ![X]: ( in_denotation(X, germany, isPartOf)
          => in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
