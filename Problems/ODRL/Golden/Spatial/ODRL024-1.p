%--------------------------------------------------------------------------
% File     : ODRL024-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isAnyOf({france, germany}) ∩ isNoneOf({easternEurope}) ≠ ∅
% Expected : Theorem (Compatible — witness: france or germany)
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf/isNoneOf interaction), Definition 5
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "isAnyOf",
%       "rightOperand": ["http://example.org/geo/france",
%                        "http://example.org/geo/germany"] }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "isNoneOf",
%       "rightOperand": ["http://example.org/geo/easternEurope"] }
%
% Denotation analysis:
%   ⟦isAnyOf({france, germany})⟧ = ↓france ∪ ↓germany
%     = {france} ∪ {germany} = {france, germany}  (both leaves)
%   ⟦isNoneOf({eE})⟧ = C \ ↓eE
%     = all concepts NOT below easternEurope
%   Witness: france — france ≤ westernEurope (not ≤ eE by disjointness)
%
% Proof: X=france. isAnyOf: france ∈ ↓france. isNoneOf: need ¬leq(france,eE).
%        disj(wE,eE) + disj_downward → disj(france,eE) → disj_implies_not_leq.
% Difficulty: Hard — both set-valued operators + disjointness proof
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_024a_1, axiom, in_value_list(france, anyList024)).
fof(list_024a_2, axiom, in_value_list(germany, anyList024)).
fof(list_024b_1, axiom, in_value_list(easternEurope, noneList024)).

fof(odrl024, conjecture,
    ?[X]: ( in_denotation_set(X, anyList024, isAnyOf)
          & in_denotation_set(X, noneList024, isNoneOf) )).
%--------------------------------------------------------------------------
