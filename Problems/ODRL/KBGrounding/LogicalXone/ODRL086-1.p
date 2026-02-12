%--------------------------------------------------------------------------
% File     : ODRL086-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE Unknown: missing explicit disjointness for commRes
% Status   : CounterSatisfiable
%
% xone(isA commercialPurpose, isA nonCommercialPurpose) vs eq commRes
%   commRes ⊑ commercialPurpose ✓ (branch 1)
%   commRes ⊄ nonCommPurpose? NOT explicit in KB!
%   Open world: commRes COULD be under both → can't confirm exclusivity
%   → Unknown
%
%   Contrast with ODRL085: nonCommRes HAS explicit ¬⊑ commercialPurpose.
%   Insight: xone requires explicit disjointness axioms.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, purpose) & has_operator(c1, isA) & has_value(c1, commercialPurpose)).
fof(c2_def, axiom, has_operand(c2, purpose) & has_operator(c2, isA) & has_value(c2, nonCommercialPurpose)).
fof(c3_def, axiom, has_operand(c3, purpose) & has_operator(c3, eq) & has_value(c3, commercialResearch)).

fof(xone_compatible, conjecture,
    (?[X]: (in_denotation(X, c1) & ~in_denotation(X, c2) & in_denotation(X, c3)))
  | (?[Y]: (in_denotation(Y, c2) & ~in_denotation(Y, c1) & in_denotation(Y, c3)))).
%--------------------------------------------------------------------------
