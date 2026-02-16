%--------------------------------------------------------------------------
% File     : ODRL035-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict propagation: subsumption + conflict → conflict
% Expected : CounterSatisfiable (Conflict — via Lemma 2)
% Verdict  : Conflict
% Paper    : Lemma 2 (Conflict Propagation)
%
% ODRL Scenario:
%   Given three constraints on spatial:
%     c1: { "operator": "isPartOf", "rightOperand": "germany" }
%     c2: { "operator": "isPartOf", "rightOperand": "westernEurope" }
%     c3: { "operator": "isPartOf", "rightOperand": "easternEurope" }
%
%   Known: c1 ⊑_c c2 (germany refines westernEurope — ODRL030)
%   Known: verdict(c2, c3) = Conflict (ODRL013)
%   Lemma 2: c1 ⊑_c c2 ∧ conflict(c2,c3) ⟹ conflict(c1,c3)
%
%   This tests the DERIVED conflict: c1 vs c3.
%   ⟦isPartOf(germany)⟧ = {germany}
%   ⟦isPartOf(easternEurope)⟧ = {eE, poland, czechia, ...}
%   germany ∈ westernEurope branch, disjoint from eE branch.
%   Intersection = ∅ → Conflict
%
% Proof: Direct disjointness propagation, but the scenario demonstrates
%        how Lemma 2 enables transitive conflict inference.
% Difficulty: Medium — demonstrates conflict propagation pattern
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl035, conjecture,
    ?[X]: ( in_denotation(X, germany, isPartOf)
          & in_denotation(X, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
