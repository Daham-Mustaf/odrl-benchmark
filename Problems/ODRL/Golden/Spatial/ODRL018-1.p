%--------------------------------------------------------------------------
% File     : ODRL018-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isPartOf(northernEurope) ∩ hasPart(channelIslands) ≠ ∅
% Expected : Theorem (Compatible — witness: northernEurope)
% Verdict  : Compatible
% Paper    : Definition 2 (reflexivity), Definition 3 (isPartOf/hasPart)
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/northernEurope" }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/channelIslands" }
%
% Denotation analysis:
%   ⟦isPartOf(northernEurope)⟧ = {x | x ≤ northernEurope}
%     = {northernEurope, denmark, ..., channelIslands, guernsey, ...}
%   ⟦hasPart(channelIslands)⟧ = {x | channelIslands ≤ x}
%     = {channelIslands, northernEurope, europe, world}
%   Witness: northernEurope
%     (northernEurope ≤ northernEurope by reflexivity,
%      channelIslands ≤ northernEurope by L0 edge)
%
% Proof: X=northernEurope. leq_refl + L0 edge.
%        Tests 4-level hierarchy with intermediate region.
% Difficulty: Medium-Hard — intermediate region + inverse operator
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl018, conjecture,
    ?[X]: ( in_denotation(X, northernEurope, isPartOf)
          & in_denotation(X, channelIslands, hasPart) )).
%--------------------------------------------------------------------------
