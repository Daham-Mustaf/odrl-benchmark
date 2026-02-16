%--------------------------------------------------------------------------
% File     : ODRL063-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Redundancy: isPartOf(europe) redundant under ∧ with isPartOf(germany)
% Expected : Theorem
% Verdict  : Redundant
% Paper    : Redundancy Detection (intra-rule ∧)
%
% ODRL Policy (Turtle):
%   ex:rule a odrl:Permission ;
%     odrl:action odrl:use ;
%     odrl:constraint [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:germany ] ;
%     odrl:constraint [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .
%
% Denotation analysis:
%   Under conjunction: ⟦isPartOf(de)⟧ ⊆ ⟦isPartOf(eu)⟧
%   Chain: leq(X, de) → leq(de, wE) [h_0017] → leq(wE, eu) [h_0056] → leq(X, eu)
%   → the europe constraint adds no restriction → REDUNDANT
%   The STRICTER constraint (germany) makes the WEAKER one (europe) redundant.
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl063, conjecture,
    ![X]: ( in_denotation(X, germany, isPartOf)
          => in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
