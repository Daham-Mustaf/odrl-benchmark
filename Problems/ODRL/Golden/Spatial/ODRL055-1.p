%--------------------------------------------------------------------------
% File     : ODRL055-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption: hasPart(germany) ⊄ hasPart(europe) (reverse direction fails)
% Expected : CounterSatisfiable (Refuted)
% Verdict  : Refuted
% Paper    : Definition 7 (Constraint Subsumption)
%
% ODRL Scenario:
%   Constraint c1:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/germany" }
%   Constraint c2:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/europe" }
%
% Denotation analysis:
%   ⟦hasPart(germany)⟧ = {germany, westernEurope, europe, world}
%   ⟦hasPart(europe)⟧  = {europe, world}
%   {germany, wE, europe, world} ⊆ {europe, world}? NO!
%   Counterexample: germany ∈ hasPart(germany) but germany ∉ hasPart(europe)
%     (need europe ≤ germany, but ¬leq(europe, germany) — germany is below europe)
%
%   Paired with ODRL054: demonstrates subsumption asymmetry for hasPart.
%
% Encoding: ∀X: in_denotation(X, germany, hasPart) → in_denotation(X, europe, hasPart)
% Countermodel: X=germany. germany ≤ germany (refl). But ¬(europe ≤ germany).
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl055, conjecture,
    ![X]: ( in_denotation(X, germany, hasPart)
          => in_denotation(X, europe, hasPart) )).
%--------------------------------------------------------------------------
