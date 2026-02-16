%--------------------------------------------------------------------------
% File     : ODRL036-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-operator subsumption: isPartOf(germany) ⊆ neq(france)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:germany ] .
%   c2: [ odrl:operator odrl:neq ; odrl:rightOperand geo:france ] .
%
% Denotation analysis:
%   germany≠france (UNA) → {germany} ⊆ C\{france}
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl036, conjecture,
    ![X]: ( in_denotation(X, germany, isPartOf)
          => in_denotation(X, france, neq) )).
%--------------------------------------------------------------------------
