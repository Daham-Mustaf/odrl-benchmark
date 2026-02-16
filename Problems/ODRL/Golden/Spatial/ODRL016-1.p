%--------------------------------------------------------------------------
% File     : ODRL016-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: neq(germany) ∩ isPartOf(westernEurope) ≠ ∅
% Expected : Theorem (Compatible — witness: france)
% Verdict  : Compatible
% Paper    : Definition 3 (neq/isPartOf), Definition 5
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "neq",
%       "rightOperand": "http://example.org/geo/germany" }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/westernEurope" }
%
% Denotation analysis:
%   ⟦neq(germany)⟧ = C \ {germany} = all concepts except germany
%   ⟦isPartOf(westernEurope)⟧ = {x | x ≤ westernEurope}
%     = {westernEurope, austria, belgium, france, germany, ...}
%   Intersection = {westernEurope, austria, belgium, france,
%     liechtenstein, luxembourg, monaco, netherlands, switzerland}
%   Witness: france (france ≤ westernEurope ∧ france ≠ germany)
%
% Proof: X=france. den_neq_if: france ≠ germany (UNA).
%        den_isPartOf_if: france ≤ westernEurope (L0 edge).
% Difficulty: Medium — prover must find existential ≠ excluded value
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl016, conjecture,
    ?[X]: ( in_denotation(X, germany, neq)
          & in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
