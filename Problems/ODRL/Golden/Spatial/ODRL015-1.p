%--------------------------------------------------------------------------
% File     : ODRL015-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: hasPart(germany) ∩ eq(poland) = ∅
% Expected : CounterSatisfiable (Conflict)
% Verdict  : Conflict
% Paper    : Definition 3 (hasPart/eq), Definition 5, Lemma 1
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/germany" }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "eq",
%       "rightOperand": "http://example.org/geo/poland" }
%
% Denotation analysis:
%   ⟦hasPart(germany)⟧ = {x | germany ≤ x}
%     = {germany, westernEurope, europe, world}
%   ⟦eq(poland)⟧ = {poland}
%   Is poland ∈ {germany, westernEurope, europe, world}?
%   poland ≤ easternEurope, germany ≤ westernEurope,
%   disjoint(easternEurope, westernEurope) [siblings],
%   so disjoint(poland, germany) by disj_downward.
%   Lemma 1: leq(x,y) → ¬disjoint(x,y), contrapositive:
%     disjoint(poland, germany) → ¬leq(germany, poland)
%   ⟹ poland ∉ ⟦hasPart(germany)⟧. UNA excludes wE, europe, world.
%   Intersection = ∅ → Conflict
%
% Proof: den_eq_onlyif forces X=poland. den_hasPart_onlyif requires
%        germany ≤ poland. But disj_downward + disj_implies_not_leq
%        gives ¬leq(germany, poland) → contradiction.
% Difficulty: Hard — combines hasPart, UNA, cross-branch disjointness
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl015, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, poland, eq) )).
%--------------------------------------------------------------------------
