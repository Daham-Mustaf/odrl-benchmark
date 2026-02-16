%--------------------------------------------------------------------------
% File     : ODRL011-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isPartOf(europe) ∩ eq(germany) ≠ ∅
% Expected : Theorem (Compatible — witness: germany)
% Verdict  : Compatible
% Paper    : Definition 3 (denotation), Definition 5 (conflict)
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/europe" }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "eq",
%       "rightOperand": "http://example.org/geo/germany" }
%
% Denotation analysis:
%   ⟦isPartOf(europe)⟧ = {x ∈ C | x ≤ europe}
%     = {europe, easternEurope, westernEurope, ..., germany, france, ...}
%   ⟦eq(germany)⟧ = {germany}
%   Intersection = {germany} ≠ ∅ → Compatible
%   Witness: germany (germany ≤ westernEurope ≤ europe by transitivity)
%
% Proof: Instantiate X=germany, apply den_isPartOf_if + leq_trans,
%        apply den_eq_if with reflexivity.
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl011, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & in_denotation(X, germany, eq) )).
%--------------------------------------------------------------------------
