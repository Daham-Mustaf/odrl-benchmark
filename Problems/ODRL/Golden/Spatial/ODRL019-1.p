%--------------------------------------------------------------------------
% File     : ODRL019-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isPartOf(northernEurope) ∩ isPartOf(southernEurope) = ∅
% Expected : CounterSatisfiable (Conflict)
% Verdict  : Conflict
% Paper    : Definition 2 (disj_downward), Definition 5
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/northernEurope" }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/southernEurope" }
%
% Denotation analysis:
%   ⟦isPartOf(northernEurope)⟧ = {nE, denmark, estonia, ..., channelIslands, ...}
%   ⟦isPartOf(southernEurope)⟧ = {sE, albania, croatia, greece, italy, spain, ...}
%   disjoint(northernEurope, southernEurope) [sibling regions]
%   Intersection = ∅ → Conflict
%
% Proof: Same pattern as ODRL013: disj_downward + disj_irrefl.
%        Tests with different disjoint pair.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl019, conjecture,
    ?[X]: ( in_denotation(X, northernEurope, isPartOf)
          & in_denotation(X, southernEurope, isPartOf) )).
%--------------------------------------------------------------------------
