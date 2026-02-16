%--------------------------------------------------------------------------
% File     : ODRL013-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isPartOf(westernEurope) ∩ isPartOf(easternEurope) = ∅
% Expected : CounterSatisfiable (Conflict)
% Verdict  : Conflict
% Paper    : Definition 2 (disj_downward), Definition 3, Definition 5
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/westernEurope" }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/easternEurope" }
%
% Denotation analysis:
%   ⟦isPartOf(westernEurope)⟧ = {x | x ≤ westernEurope}
%     = {westernEurope, germany, france, austria, ...}
%   ⟦isPartOf(easternEurope)⟧ = {x | x ≤ easternEurope}
%     = {easternEurope, poland, czechia, hungary, ...}
%   disjoint(westernEurope, easternEurope)  [siblings in GEO KB]
%   Intersection = ∅ → Conflict
%
% Proof: Suppose ∃X: leq(X, westernEurope) ∧ leq(X, easternEurope).
%        By disj_downward: disjoint(X, X). Contradicts disj_irrefl.
% Difficulty: Medium — requires disjointness propagation + irreflexivity
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl013, conjecture,
    ?[X]: ( in_denotation(X, westernEurope, isPartOf)
          & in_denotation(X, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
