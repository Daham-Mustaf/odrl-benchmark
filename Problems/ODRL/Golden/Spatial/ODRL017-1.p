%--------------------------------------------------------------------------
% File     : ODRL017-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: neq(germany) ∩ eq(germany) = ∅
% Expected : CounterSatisfiable (Conflict)
% Verdict  : Conflict
% Paper    : Definition 3 (eq/neq bidirectional), Definition 5
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "neq",
%       "rightOperand": "http://example.org/geo/germany" }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "eq",
%       "rightOperand": "http://example.org/geo/germany" }
%
% Denotation analysis:
%   ⟦neq(germany)⟧ = C \ {germany}
%   ⟦eq(germany)⟧  = {germany}
%   Intersection = ∅ (germany excluded by neq, only member of eq)
%
% Proof: den_eq_onlyif forces X=germany.
%        den_neq_onlyif forces X≠germany.
%        Direct contradiction.
% Difficulty: Easy — tests bidirectional only-if axioms
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl017, conjecture,
    ?[X]: ( in_denotation(X, germany, neq)
          & in_denotation(X, germany, eq) )).
%--------------------------------------------------------------------------
