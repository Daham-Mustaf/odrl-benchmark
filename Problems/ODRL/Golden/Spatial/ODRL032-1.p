%--------------------------------------------------------------------------
% File     : ODRL032-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption: eq(germany) ⊆ isPartOf(europe) (cross-operator refinement)
% Expected : Theorem (Confirmed)
% Verdict  : Confirmed
% Paper    : Definition 7 (Constraint Subsumption)
%
% ODRL Scenario:
%   Constraint c1 (exact):
%     { "leftOperand": "spatial",
%       "operator": "eq",
%       "rightOperand": "http://example.org/geo/germany" }
%   Constraint c2 (range):
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/europe" }
%
% Denotation analysis:
%   ⟦eq(germany)⟧ = {germany}
%   ⟦isPartOf(europe)⟧ = {x | x ≤ europe} ⊇ {germany}
%   {germany} ⊆ {x | x ≤ europe} → Confirmed
%   Policy meaning: "exactly germany" is redundant when the other
%   rule already accepts "anywhere in europe".
%
% Encoding: ∀X: in_denotation(X, germany, eq) → in_denotation(X, europe, isPartOf)
% Proof: den_eq_onlyif gives X=germany. leq_trans: germany ≤ europe.
%        den_isPartOf_if.
% Difficulty: Easy — cross-operator, same hierarchy path
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl032, conjecture,
    ![X]: ( in_denotation(X, germany, eq)
          => in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
