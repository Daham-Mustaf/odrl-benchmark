%--------------------------------------------------------------------------
% File     : ODRL025-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isAnyOf({germany, france}) ∩ isNoneOf({westernEurope}) = ∅
% Expected : CounterSatisfiable (Conflict)
% Verdict  : Conflict
% Paper    : Definition 3 (isAnyOf/isNoneOf), Definition 5
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "isAnyOf",
%       "rightOperand": ["http://example.org/geo/germany",
%                        "http://example.org/geo/france"] }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "isNoneOf",
%       "rightOperand": ["http://example.org/geo/westernEurope"] }
%
% Denotation analysis:
%   ⟦isAnyOf({de, fr})⟧ = ↓de ∪ ↓fr = {germany, france}
%   ⟦isNoneOf({wE})⟧ = C \ ↓wE = concepts NOT below westernEurope
%   But germany ≤ wE and france ≤ wE (both L0 edges),
%   so both are IN ↓wE, meaning both are EXCLUDED by isNoneOf.
%   Intersection = ∅ → Conflict
%
% Proof: isAnyOf_onlyif forces X ≤ germany ∨ X ≤ france.
%        Either case: X ≤ germany ≤ wE or X ≤ france ≤ wE (trans).
%        isNoneOf_onlyif requires ¬leq(X, wE) → contradiction.
% Difficulty: Hard — requires reasoning about all branches of union
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_025a_1, axiom, in_value_list(germany, anyList025)).
fof(list_025a_2, axiom, in_value_list(france, anyList025)).
fof(list_025b_1, axiom, in_value_list(westernEurope, noneList025)).

fof(odrl025, conjecture,
    ?[X]: ( in_denotation_set(X, anyList025, isAnyOf)
          & in_denotation_set(X, noneList025, isNoneOf) )).
%--------------------------------------------------------------------------
