%--------------------------------------------------------------------------
% File     : ODRL030-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption confirmed: isPartOf(germany) ⊆ isPartOf(europe)
% Expected : Theorem (Confirmed — germany refines europe)
% Verdict  : Confirmed
% Paper    : Definition 7 (Constraint Subsumption)
%
% ODRL Scenario:
%   Constraint c1 (more restrictive):
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/germany" }
%   Constraint c2 (less restrictive):
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/europe" }
%
% Denotation analysis:
%   ⟦isPartOf(germany)⟧ = {x | x ≤ germany} = {germany}  (leaf)
%   ⟦isPartOf(europe)⟧  = {x | x ≤ europe}  = {europe, ..., germany, ...}
%   {germany} ⊆ {europe, ..., germany, ...} → Confirmed
%   germany refines europe: anything satisfying "in germany" also
%   satisfies "in europe". The more specific constraint is redundant
%   when paired with the more general one.
%
% Encoding: ∀X: in_denotation(X, germany, isPartOf) → in_denotation(X, europe, isPartOf)
% Proof: den_isPartOf_onlyif gives X ≤ germany. Transitivity gives X ≤ europe.
%        den_isPartOf_if gives in_denotation(X, europe, isPartOf).
% Difficulty: Easy — direct transitivity
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl030, conjecture,
    ![X]: ( in_denotation(X, germany, isPartOf)
          => in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
