%--------------------------------------------------------------------------
% File     : ODRL022-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isNoneOf({europe}) ∩ isPartOf(westernEurope) = ∅
% Expected : CounterSatisfiable (Conflict)
% Verdict  : Conflict
% Paper    : Definition 3 (isNoneOf), Definition 5
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "isNoneOf",
%       "rightOperand": ["http://example.org/geo/europe"] }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/westernEurope" }
%
% Denotation analysis:
%   ⟦isNoneOf({europe})⟧ = C \ ↓europe = concepts NOT below europe
%   ⟦isPartOf(westernEurope)⟧ = {x | x ≤ westernEurope}
%   But westernEurope ≤ europe (L0), so by transitivity:
%     ∀x: x ≤ westernEurope ⟹ x ≤ europe
%   Therefore every x in ⟦isPartOf(wE)⟧ is also ≤ europe,
%   meaning x ∉ ⟦isNoneOf({europe})⟧.
%   Intersection = ∅ → Conflict
%
% Proof: Suppose ∃X: ¬leq(X,europe) ∧ leq(X,westernEurope).
%        leq_trans gives leq(X,europe) → contradiction.
% Difficulty: Very Hard — requires chain reasoning + isNoneOf only-if
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_022_1, axiom, in_value_list(europe, excluded022)).

fof(odrl022, conjecture,
    ?[X]: ( in_denotation_set(X, excluded022, isNoneOf)
          & in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
