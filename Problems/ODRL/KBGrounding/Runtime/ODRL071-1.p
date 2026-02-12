%--------------------------------------------------------------------------
% File     : ODRL071-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Runtime Semantics
% Problem  : Runtime rejection: ω(language) = fr cannot satisfy isA de
% Status   : Theorem
% Expected : Theorem — fr is NOT in denotation of (language isA de)
%
% Validates: Theorem 2 (Runtime Soundness) — Conflict direction
%            No execution context with ω(language) = fr can satisfy
%            the policy constraint c1: language isA de.
%
% Parallel : ODRL051-1.p (design-time: de vs fr → Conflict)
%
% Scenario : Design-time analysis found Conflict between German policy
%            and French request. Runtime: French archive sends request
%            with ω(language) = fr. Verify this concrete context
%            FAILS the policy constraint (isA de). The request
%            constraint (eq fr) trivially succeeds, but the policy
%            constraint blocks — confirming the design-time verdict.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, language) & has_operator(c1, isA) & has_value(c1, de)).

% Runtime: try to put fr into the policy's denotation → should fail
fof(runtime_rejection, conjecture, ~in_denotation(fr, c1)).

%--------------------------------------------------------------------------
