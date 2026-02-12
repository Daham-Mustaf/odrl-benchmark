%--------------------------------------------------------------------------
% File     : ODRL074-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Runtime Semantics
% Problem  : Runtime witness: ω(purpose) = nonCommercialResearch satisfies both
% Status   : Theorem
% Expected : Theorem — nonCommercialResearch is a valid runtime context
%
% Validates: Theorem 2 (Runtime Soundness) — Compatible direction
%
% Parallel : ODRL020-1.p (design-time: nonComm vs nonCommResearch → Compatible)
%
% Scenario : Design-time found Compatible. Runtime: university sends
%            request with ω(purpose) = nonCommercialResearch. Verify
%            this satisfies BOTH isA nonCommercialPurpose AND
%            eq nonCommercialResearch.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, purpose) & has_operator(c1, isA) & has_value(c1, nonCommercialPurpose)).
fof(c2_def, axiom, has_operand(c2, purpose) & has_operator(c2, eq) & has_value(c2, nonCommercialResearch)).

fof(runtime_witness, conjecture,
    in_denotation(nonCommercialResearch, c1) & in_denotation(nonCommercialResearch, c2)).

%--------------------------------------------------------------------------
