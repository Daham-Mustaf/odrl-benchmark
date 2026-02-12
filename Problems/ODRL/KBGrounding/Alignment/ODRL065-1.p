%--------------------------------------------------------------------------
% File     : ODRL065-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : Purpose graceful degradation: scientificResearch unmapped
% Status   : CounterSatisfiable
% Expected : Unknown — scientificResearch has no grounding in GDPR KB
%
% Validates: Proposition 1(2) — Graceful Degradation (partial alignment)
%
% Parallel : ODRL024-1.p (DPV: R&D vs scientificResearch → Compatible)
%
% Scenario : Dataspace A (W3C DPV) found R&D policy compatible with
%            scientific research request (scientificResearch ⊑ R&D).
%            Dataspace B (GDPR taxonomy) has no scientificResearch
%            concept. Compatible degrades to Unknown.
%
% Alignment: α(researchAndDevelopment)=forschungUndEntwicklung,
%            α(scientificResearch)=⊥ (partial — concept missing)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, purpose) & has_operator(c1, isA) & has_value(c1, forschungUndEntwicklung)).
fof(c2_def, axiom, has_operand(c2, purpose) & has_operator(c2, eq) & has_value(c2, scientificResearch)).

fof(compatible, conjecture, ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).

%--------------------------------------------------------------------------
