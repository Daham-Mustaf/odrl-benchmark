%--------------------------------------------------------------------------
% File     : ODRL087-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE both-in: nonCommRes satisfies both branches
% Status   : CounterSatisfiable
%
% xone(isA researchAndDevelopment, isA nonCommercialPurpose) vs eq nonCommRes
%   nonCommRes ⊑ R&D ✓ (branch 1)
%   nonCommRes ⊑ nonCommPurpose ✓ (branch 2)
%   BOTH branches hold → violates exclusive-or
%   Open world: maybe other values satisfy exactly one? → Unknown
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, purpose) & has_operator(c1, isA) & has_value(c1, researchAndDevelopment)).
fof(c2_def, axiom, has_operand(c2, purpose) & has_operator(c2, isA) & has_value(c2, nonCommercialPurpose)).
fof(c3_def, axiom, has_operand(c3, purpose) & has_operator(c3, eq) & has_value(c3, nonCommercialResearch)).

fof(xone_compatible, conjecture,
    (?[X]: (in_denotation(X, c1) & ~in_denotation(X, c2) & in_denotation(X, c3)))
  | (?[Y]: (in_denotation(Y, c2) & ~in_denotation(Y, c1) & in_denotation(Y, c3)))).
%--------------------------------------------------------------------------
