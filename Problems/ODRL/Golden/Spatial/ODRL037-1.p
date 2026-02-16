%--------------------------------------------------------------------------
% File     : ODRL037-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption refuted: neq(germany) ⊄ isPartOf(westernEurope)
% Expected : CounterSatisfiable (Refuted)
% Verdict  : Refuted
% Paper    : Definition 7 (Constraint Subsumption)
%
% ODRL Scenario:
%   Constraint c1:
%     { "leftOperand": "spatial",
%       "operator": "neq",
%       "rightOperand": "http://example.org/geo/germany" }
%   Constraint c2:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/westernEurope" }
%
% Denotation analysis:
%   ⟦neq(germany)⟧ = C \ {germany} (58 concepts)
%   ⟦isPartOf(westernEurope)⟧ = {x | x ≤ westernEurope} (10 concepts)
%   Counterexample: poland ∈ ⟦neq(germany)⟧ but 
%     poland ∉ ⟦isPartOf(westernEurope)⟧
%     (poland ≤ easternEurope, disjoint from westernEurope)
%
% Encoding: ∀X: in_denotation(X, germany, neq) → in_denotation(X, westernEurope, isPartOf)
% Countermodel: X=poland.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl037, conjecture,
    ![X]: ( in_denotation(X, germany, neq)
          => in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
