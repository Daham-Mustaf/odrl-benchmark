%--------------------------------------------------------------------------
% File     : ODRL070-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Runtime Semantics
% Problem  : Runtime witness: ω(language) = de_AT satisfies both constraints
% Status   : Theorem
% Expected : Theorem — de_AT is a valid runtime execution context value
%
% Validates: Theorem 2 (Runtime Soundness) — Compatible direction
%            Definition 8 (Constraint Satisfaction): ω ⊨ c1 ∧ ω ⊨ c2
%
% Parallel : ODRL050-1.p (design-time: de vs de_AT → Compatible)
%
% Scenario : Design-time analysis found Compatible with witness de_AT.
%            Runtime: Austrian library sends request with
%            ω(language) = de_AT. Verify this concrete context
%            satisfies BOTH the policy constraint (isA de) and
%            the request constraint (eq de_AT).
%
% This problem grounds the abstract ∃X proof to a named witness.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, language) & has_operator(c1, isA) & has_value(c1, de)).
fof(c2_def, axiom, has_operand(c2, language) & has_operator(c2, eq) & has_value(c2, de_AT)).

% Runtime: concrete execution context provides de_AT
fof(runtime_witness, conjecture,
    in_denotation(de_AT, c1) & in_denotation(de_AT, c2)).

%--------------------------------------------------------------------------
