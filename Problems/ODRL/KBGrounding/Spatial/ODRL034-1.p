%--------------------------------------------------------------------------
% File     : ODRL034-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Redundancy: eq(germany) ⊆ isPartOf(westernEurope)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7, policy simplification
%
% ODRL Policy (Turtle):
%   Same rule, two constraints (redundancy):
%   ex:rule1 a odrl:Permission ;
%     odrl:constraint [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] ;
%     odrl:constraint [ odrl:operator odrl:eq ; odrl:rightOperand geo:germany ] .
%
% Denotation analysis:
%   eq(de) ⊆ isPartOf(wE) → eq constraint is redundant.
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl034, conjecture,
    ![X]: ( in_denotation(X, germany, eq)
          => in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
