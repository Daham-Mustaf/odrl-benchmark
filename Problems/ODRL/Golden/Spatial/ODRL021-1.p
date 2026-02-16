%--------------------------------------------------------------------------
% File     : ODRL021-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isNoneOf({easternEurope, southernEurope}) ∩ isPartOf(westernEurope) ≠ ∅
% Expected : Theorem (Compatible — witness: germany)
% Verdict  : Compatible
% Paper    : Definition 3 (isNoneOf), Definition 5
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "isNoneOf",
%       "rightOperand": ["http://example.org/geo/easternEurope",
%                        "http://example.org/geo/southernEurope"] }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/westernEurope" }
%
% Denotation analysis:
%   ⟦isNoneOf({eE, sE})⟧ = C \ (↓eE ∪ ↓sE)
%     = concepts NOT below easternEurope AND NOT below southernEurope
%   ⟦isPartOf(westernEurope)⟧ = {x | x ≤ westernEurope}
%   Witness: germany
%     germany ≤ westernEurope (L0 edge)
%     ¬leq(germany, easternEurope): disj(wE,eE) + disj_downward → disj(germany,eE)
%       → disj_implies_not_leq
%     ¬leq(germany, southernEurope): disj(wE,sE) + disj_downward → disj(germany,sE)
%       → disj_implies_not_leq
%
% Proof: Hardest single-operand test. Combines isNoneOf (∀-elimination),
%        disjointness propagation, and negative reasoning.
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_021_1, axiom, in_value_list(easternEurope, excluded021)).
fof(list_021_2, axiom, in_value_list(southernEurope, excluded021)).

fof(odrl021, conjecture,
    ?[X]: ( in_denotation_set(X, excluded021, isNoneOf)
          & in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
