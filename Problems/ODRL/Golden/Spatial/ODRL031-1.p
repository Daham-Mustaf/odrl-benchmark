%--------------------------------------------------------------------------
% File     : ODRL031-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption refuted: isPartOf(europe) ⊄ isPartOf(germany)
% Expected : CounterSatisfiable (Refuted — europe does NOT refine germany)
% Verdict  : Refuted
% Paper    : Definition 7 (Constraint Subsumption)
%
% ODRL Scenario:
%   Constraint c1:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/europe" }
%   Constraint c2:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/germany" }
%
% Denotation analysis:
%   ⟦isPartOf(europe)⟧  = {x | x ≤ europe} (59 concepts)
%   ⟦isPartOf(germany)⟧ = {x | x ≤ germany} = {germany}  (leaf)
%   {europe, france, ...} ⊄ {germany} → Refuted
%   Counterexample: france ∈ ⟦isPartOf(europe)⟧ but france ∉ ⟦isPartOf(germany)⟧
%
% Encoding: ∀X: in_denotation(X, europe, isPartOf) → in_denotation(X, germany, isPartOf)
% Countermodel: X=france satisfies LHS (france ≤ europe) but not RHS
%               (¬leq(france, germany) by disjointness).
% Difficulty: Medium — prover finds countermodel via sibling disjointness
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl031, conjecture,
    ![X]: ( in_denotation(X, europe, isPartOf)
          => in_denotation(X, germany, isPartOf) )).
%--------------------------------------------------------------------------
