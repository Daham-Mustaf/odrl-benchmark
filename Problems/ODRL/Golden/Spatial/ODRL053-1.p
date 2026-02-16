%--------------------------------------------------------------------------
% File     : ODRL053-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: hasPart(germany) ∩ hasPart(poland) — common ancestors exist
%            but wait — this IS compatible!
% Expected : Theorem (Compatible — witness: europe)
% Verdict  : Compatible
% Paper    : Definition 3 (hasPart)
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/germany" }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/poland" }
%
% Denotation analysis:
%   ⟦hasPart(germany)⟧ = {germany, westernEurope, europe, world}
%   ⟦hasPart(poland)⟧  = {poland, easternEurope, europe, world}
%   Despite germany ⊥ poland (cross-branch), hasPart looks UPWARD.
%   Common ancestors: {europe, world}
%   Witness: europe (germany ≤ wE ≤ europe, poland ≤ eE ≤ europe)
%
%   IMPORTANT: This is a subtle case! isPartOf(germany) ∩ isPartOf(poland)
%   would be Conflict (ODRL035), but hasPart reverses the direction.
%   Disjointness of leaves does NOT imply disjointness of ancestors.
%
% Proof: X=europe. germany ≤ europe (trans). poland ≤ europe (trans).
% Difficulty: Medium-Hard — tests understanding that hasPart is upward
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl053, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, poland, hasPart) )).
%--------------------------------------------------------------------------
