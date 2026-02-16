%--------------------------------------------------------------------------
% File     : ODRL020-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isAnyOf({westernEurope, northernEurope}) ∩ eq(germany) ≠ ∅
% Expected : Theorem (Compatible — witness: germany)
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf), Definition 5
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "isAnyOf",
%       "rightOperand": ["http://example.org/geo/westernEurope",
%                        "http://example.org/geo/northernEurope"] }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "eq",
%       "rightOperand": "http://example.org/geo/germany" }
%
% Denotation analysis:
%   ⟦isAnyOf({wE, nE})⟧ = ↓wE ∪ ↓nE
%     = {wE, germany, france, ...} ∪ {nE, denmark, sweden, ...}
%   ⟦eq(germany)⟧ = {germany}
%   Witness: germany (germany ≤ westernEurope, so germany ∈ ↓wE ⊂ union)
%
% Proof: X=germany. in_value_list(westernEurope, regions).
%        den_isAnyOf_if: ∃G in list s.t. X ≤ G. G=westernEurope.
% Difficulty: Medium — set-valued operator + list membership
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_020_1, axiom, in_value_list(westernEurope, regions020)).
fof(list_020_2, axiom, in_value_list(northernEurope, regions020)).

fof(odrl020, conjecture,
    ?[X]: ( in_denotation_set(X, regions020, isAnyOf)
          & in_denotation(X, germany, eq) )).
%--------------------------------------------------------------------------
