%--------------------------------------------------------------------------
% File     : ODRL054-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Counterintuitive: hasPart(europe) ⊆ hasPart(germany)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] .
%   c2: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:germany ] .
%
% Denotation analysis:
%   ⟦hasPart(eu)⟧={eu,world} ⊆ ⟦hasPart(de)⟧={de,wE,eu,world}
%   Counterintuitive: MORE GENERAL concept → FEWER ancestors.
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl054, conjecture,
    ![X]: ( in_denotation(X, europe, hasPart)
          => in_denotation(X, germany, hasPart) )).
%--------------------------------------------------------------------------
