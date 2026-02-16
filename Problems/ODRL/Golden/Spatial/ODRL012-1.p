%--------------------------------------------------------------------------
% File     : ODRL012-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: eq(germany) ∩ eq(france) = ∅
% Expected : CounterSatisfiable (Conflict)
% Verdict  : Conflict
% Paper    : Definition 3 (eq denotation), Definition 5 (conflict)
%
% ODRL Scenario:
%   Permission refinement:
%     { "leftOperand": "spatial",
%       "operator": "eq",
%       "rightOperand": "http://example.org/geo/germany" }
%   Prohibition refinement:
%     { "leftOperand": "spatial",
%       "operator": "eq",
%       "rightOperand": "http://example.org/geo/france" }
%
% Denotation analysis:
%   ⟦eq(germany)⟧ = {germany}
%   ⟦eq(france)⟧  = {france}
%   germany ≠ france (UNA in GEO KB) → Intersection = ∅ → Conflict
%
% Proof: den_eq_onlyif forces X=germany from c1, X=france from c2.
%        UNA axiom: germany ≠ france → contradiction.
% Difficulty: Trivial — UNA only
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl012, conjecture,
    ?[X]: ( in_denotation(X, germany, eq)
          & in_denotation(X, france, eq) )).
%--------------------------------------------------------------------------
