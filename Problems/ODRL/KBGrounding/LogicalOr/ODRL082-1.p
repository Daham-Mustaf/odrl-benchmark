%--------------------------------------------------------------------------
% File     : ODRL082-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : OR Unknown: both branches indeterminate
% Status   : CounterSatisfiable
%
% or(isA nonCommercialPurpose, isA marketing) vs eq scientificResearch
%   Branch 1: sciRes ⊑? nonComm → Unknown (KB gap)
%   Branch 2: sciRes ⊑? marketing → Unknown (KB gap)
%   or: both indeterminate → Unknown
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, purpose) & has_operator(c1, isA) & has_value(c1, nonCommercialPurpose)).
fof(c2_def, axiom, has_operand(c2, purpose) & has_operator(c2, isA) & has_value(c2, marketing)).
fof(c3_def, axiom, has_operand(c3, purpose) & has_operator(c3, eq) & has_value(c3, scientificResearch)).

fof(or_compatible, conjecture,
    (?[X]: (in_denotation(X, c1) & in_denotation(X, c3)))
  | (?[Y]: (in_denotation(Y, c2) & in_denotation(Y, c3)))).
%--------------------------------------------------------------------------
