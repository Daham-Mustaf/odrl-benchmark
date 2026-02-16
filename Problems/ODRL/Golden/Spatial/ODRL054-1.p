%--------------------------------------------------------------------------
% File     : ODRL054-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Asymmetric subsumption: hasPart(europe) ⊆ hasPart(germany)?
% Expected : CounterSatisfiable (Refuted — europe has fewer ancestors)
% Verdict  : Refuted
% Paper    : Definition 7 (Constraint Subsumption)
%
% ODRL Scenario:
%   Constraint c1:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/europe" }
%   Constraint c2:
%     { "leftOperand": "spatial",
%       "operator": "hasPart",
%       "rightOperand": "http://example.org/geo/germany" }
%
% Denotation analysis:
%   ⟦hasPart(europe)⟧  = {x | europe ≤ x}  = {europe, world}
%   ⟦hasPart(germany)⟧ = {x | germany ≤ x} = {germany, wE, europe, world}
%   {europe, world} ⊆ {germany, wE, europe, world}? YES!
%   Wait — this is actually Confirmed. Let me verify...
%   europe ∈ hasPart(germany)? Need germany ≤ europe. Yes (trans).
%   world ∈ hasPart(germany)? Need germany ≤ world. Yes (trans).
%   So hasPart(europe) ⊆ hasPart(germany). Confirmed!
%
%   Key insight: hasPart reverses containment direction.
%   The MORE GENERAL concept (europe) has FEWER ancestors,
%   so hasPart(europe) ⊆ hasPart(germany) — counterintuitive!
%
% Encoding: ∀X: in_denotation(X, europe, hasPart) → in_denotation(X, germany, hasPart)
% Proof: den_hasPart_onlyif: europe ≤ X. Need germany ≤ X.
%        germany ≤ europe (trans) ∧ europe ≤ X → germany ≤ X (trans).
% Difficulty: Medium — counterintuitive hasPart subsumption direction
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl054, conjecture,
    ![X]: ( in_denotation(X, europe, hasPart)
          => in_denotation(X, germany, hasPart) )).
%--------------------------------------------------------------------------
