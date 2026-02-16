%--------------------------------------------------------------------------
% File     : ODRL036-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption: isPartOf(germany) ⊆ neq(france) (cross-operator, confirmed)
% Expected : Theorem (Confirmed)
% Verdict  : Confirmed
% Paper    : Definition 7 (Constraint Subsumption)
%
% ODRL Scenario:
%   Constraint c1:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/germany" }
%   Constraint c2:
%     { "leftOperand": "spatial",
%       "operator": "neq",
%       "rightOperand": "http://example.org/geo/france" }
%
% Denotation analysis:
%   ⟦isPartOf(germany)⟧ = {germany}  (leaf)
%   ⟦neq(france)⟧ = C \ {france} = all concepts except france
%   {germany} ⊆ C \ {france}? Yes — germany ≠ france (UNA).
%   germany refines "not france": trivially true because they're distinct.
%
% Encoding: ∀X: in_denotation(X, germany, isPartOf) → in_denotation(X, france, neq)
% Proof: den_isPartOf_onlyif: X ≤ germany. For leaf: X = germany.
%        den_neq_if: germany ≠ france (UNA).
% Difficulty: Medium — cross-operator subsumption with neq
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl036, conjecture,
    ![X]: ( in_denotation(X, germany, isPartOf)
          => in_denotation(X, france, neq) )).
%--------------------------------------------------------------------------
