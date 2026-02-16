%--------------------------------------------------------------------------
% File     : ODRL051-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Root reachability: hasPart(germany) always includes world
% Expected : Theorem (world is always in hasPart denotation)
% Verdict  : Compatible (with any constraint accepting world)
% Paper    : Definition 3 (hasPart), KB structure
%
% ODRL Scenario:
%   Constraint:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/germany" }
%
%   ⟦hasPart(germany)⟧ = {x | germany ≤ x}
%     = {germany, westernEurope, europe, world}
%   world ∈ ⟦hasPart(germany)⟧ always (germany ≤ ... ≤ world by trans)
%
%   Combined with: eq(world)
%   ⟦eq(world)⟧ = {world}
%   Witness: world
%
% Proof: X=world. germany ≤ westernEurope ≤ europe ≤ world (3 trans steps).
% Difficulty: Medium — longest transitivity chain in Europe KB (depth 3)
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl051, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, world, eq) )).
%--------------------------------------------------------------------------
