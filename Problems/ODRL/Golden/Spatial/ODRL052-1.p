%--------------------------------------------------------------------------
% File     : ODRL052-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Leaf isolation: hasPart(germany) ∩ hasPart(france) — compatible at common ancestor
% Expected : Theorem (Compatible — witnesses: westernEurope, europe, world)
% Verdict  : Compatible
% Paper    : Definition 3 (hasPart), hierarchical structure
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/germany" }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/france" }
%
% Denotation analysis:
%   ⟦hasPart(germany)⟧ = {x | germany ≤ x} = {germany, wE, europe, world}
%   ⟦hasPart(france)⟧  = {x | france ≤ x}  = {france, wE, europe, world}
%   Common ancestors: {westernEurope, europe, world}
%   Witness: westernEurope (both germany ≤ wE and france ≤ wE by L0)
%
%   Policy meaning: Both regions "have part" germany and france
%   respectively. They overlap at any region containing both.
%
% Proof: X=westernEurope. germany ≤ wE (L0). france ≤ wE (L0).
% Difficulty: Medium — two hasPart operators meeting at common ancestor
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl052, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, france, hasPart) )).
%--------------------------------------------------------------------------
