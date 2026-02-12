%--------------------------------------------------------------------------
% File     : ODRL073-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Runtime Semantics
% Problem  : Runtime exhaustive: no KB language concept satisfies both
% Status   : Theorem
% Expected : Theorem — universal rejection across all named concepts
%
% Validates: Theorem 2 (Runtime Soundness) — exhaustive verification
%            For Conflict pair (isA de) vs (eq fr), every named
%            concept in LNG KB fails at least one constraint.
%
% Parallel : ODRL051-1.p (design-time: de vs fr → Conflict)
%
% Scenario : After detecting Conflict at design time, verify that
%            EVERY concrete value in the language KB would be
%            rejected at runtime. This is finite model checking
%            of the universal soundness claim.
%
% Concepts tested: de, de_AT, de_CH, en, en_US, en_GB, fr, ar, arb, arz
% Only fr ∈ ⟦eq fr⟧, and fr ∉ ⟦isA de⟧ → no concept works.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, language) & has_operator(c1, isA) & has_value(c1, de)).
fof(c2_def, axiom, has_operand(c2, language) & has_operator(c2, eq) & has_value(c2, fr)).

% No named concept satisfies both (finite runtime check)
% Each conjunct: concept x fails at least one of c1, c2
fof(exhaustive_rejection, conjecture,
    ~(in_denotation(de, c1)    & in_denotation(de, c2))
  & ~(in_denotation(de_AT, c1) & in_denotation(de_AT, c2))
  & ~(in_denotation(de_CH, c1) & in_denotation(de_CH, c2))
  & ~(in_denotation(en, c1)    & in_denotation(en, c2))
  & ~(in_denotation(en_US, c1) & in_denotation(en_US, c2))
  & ~(in_denotation(en_GB, c1) & in_denotation(en_GB, c2))
  & ~(in_denotation(fr, c1)    & in_denotation(fr, c2))
  & ~(in_denotation(ar, c1)    & in_denotation(ar, c2))
  & ~(in_denotation(arb, c1)   & in_denotation(arb, c2))
  & ~(in_denotation(arz, c1)   & in_denotation(arz, c2))).

%--------------------------------------------------------------------------
