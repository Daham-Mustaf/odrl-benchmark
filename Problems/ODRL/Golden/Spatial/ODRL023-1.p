%--------------------------------------------------------------------------
% File     : ODRL023-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isAllOf({westernEurope, easternEurope}) ∩ eq(germany) = ∅
% Expected : CounterSatisfiable (Conflict)
% Verdict  : Conflict
% Paper    : Definition 3 (isAllOf), Definition 5
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "isAllOf",
%       "rightOperand": ["http://example.org/geo/westernEurope",
%                        "http://example.org/geo/easternEurope"] }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "eq",
%       "rightOperand": "http://example.org/geo/germany" }
%
% Denotation analysis:
%   ⟦isAllOf({wE, eE})⟧ = {x | x ≤ wE ∧ x ≤ eE}
%     But disjoint(wE, eE): no x can be below both.
%     By disj_downward: ∀x≤wE, y≤eE: disjoint(x,y).
%     If x≤wE ∧ x≤eE then disjoint(x,x) → contradiction.
%     Therefore ⟦isAllOf({wE, eE})⟧ = ∅
%   ⟦eq(germany)⟧ = {germany}
%   ∅ ∩ {germany} = ∅ → Conflict
%
% Proof: den_isAllOf_onlyif forces X ≤ wE ∧ X ≤ eE.
%        disj_downward + disj_irrefl → contradiction.
%        isAllOf over disjoint branches is always empty.
% Difficulty: Hard — isAllOf + disjointness = vacuity
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_023_1, axiom, in_value_list(westernEurope, allRegions023)).
fof(list_023_2, axiom, in_value_list(easternEurope, allRegions023)).

fof(odrl023, conjecture,
    ?[X]: ( in_denotation_set(X, allRegions023, isAllOf)
          & in_denotation(X, germany, eq) )).
%--------------------------------------------------------------------------
