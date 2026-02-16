%--------------------------------------------------------------------------
% File     : ODRL032-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-operator subsumption: eq(germany) ⊆ isPartOf(europe)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:eq ; odrl:rightOperand geo:germany ] .
%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .
%
% Denotation analysis:
%   "Exactly germany" refines "anywhere in europe".
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl032, conjecture,
    ![X]: ( in_denotation(X, germany, eq)
          => in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
