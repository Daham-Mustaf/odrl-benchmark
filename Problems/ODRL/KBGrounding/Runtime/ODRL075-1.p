%--------------------------------------------------------------------------
% File     : ODRL075-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Runtime Semantics
% Problem  : Runtime rejection: ω(purpose) = advertising fails isA nonComm
% Status   : Theorem
% Expected : Theorem — advertising ∉ ⟦isA nonCommercialPurpose⟧
%
% Validates: Theorem 2 (Runtime Soundness) — Conflict direction
%
% Parallel : ODRL026-1.p (design-time: nonComm vs advertising → Conflict)
%
% Scenario : Design-time found Conflict. Runtime: ad agency sends
%            request with ω(purpose) = advertising. Verify this
%            concrete context FAILS the policy constraint.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, purpose) & has_operator(c1, isA) & has_value(c1, nonCommercialPurpose)).

fof(runtime_rejection, conjecture, ~in_denotation(advertising, c1)).

%--------------------------------------------------------------------------
