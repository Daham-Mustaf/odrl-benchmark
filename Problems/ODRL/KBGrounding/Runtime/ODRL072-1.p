%--------------------------------------------------------------------------
% File     : ODRL072-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Runtime Semantics
% Problem  : Runtime witness: ω(spatial) = france satisfies both constraints
% Status   : Theorem
% Expected : Theorem — france is a valid runtime context value
%
% Validates: Theorem 2 (Runtime Soundness) — Compatible direction
%
% Parallel : ODRL010-1.p (design-time: europe vs france → Compatible)
%
% Scenario : Design-time found Compatible. Runtime: French archive
%            sends request with ω(spatial) = france. Verify this
%            satisfies BOTH isPartOf europe AND eq france.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, spatial) & has_operator(c1, isPartOf) & has_value(c1, europe)).
fof(c2_def, axiom, has_operand(c2, spatial) & has_operator(c2, eq) & has_value(c2, france)).

fof(runtime_witness, conjecture,
    in_denotation(france, c1) & in_denotation(france, c2)).

%--------------------------------------------------------------------------
