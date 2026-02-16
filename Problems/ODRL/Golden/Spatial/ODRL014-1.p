%--------------------------------------------------------------------------
% File     : ODRL014-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: hasPart(germany) ∩ isPartOf(europe) ≠ ∅
% Expected : Theorem (Compatible — witnesses: westernEurope, europe)
% Verdict  : Compatible
% Paper    : Definition 3 (hasPart/isPartOf), Definition 5
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/germany" }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/europe" }
%
% Denotation analysis:
%   ⟦hasPart(germany)⟧ = {x | germany ≤ x}
%     = {germany, westernEurope, europe, world}  [upward closure]
%   ⟦isPartOf(europe)⟧ = {x | x ≤ europe}
%     = {europe, easternEurope, ..., germany, ...}  [downward closure]
%   Witnesses: westernEurope (≤ europe ∧ germany ≤ westernEurope)
%              europe (≤ europe by refl ∧ germany ≤ europe by trans)
%
% Proof: X=westernEurope. den_hasPart_if: germany ≤ westernEurope (L0).
%        den_isPartOf_if: westernEurope ≤ europe (L0).
% Difficulty: Medium — tests upward vs downward traversal interaction
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl014, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
