%--------------------------------------------------------------------------
% File     : ODRL084-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-DS AND-OR blocked: or(purpose) indeterminate
% Status   : CounterSatisfiable
%
% spatial: isPartOf europe vs eq france → Compatible
% or(isA nonCommPurpose, isA marketing) vs eq scientificResearch
%   Both branches indeterminate → Unknown
% Conjunction blocked by purpose Unknown
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c_s1_def, axiom, has_operand(c_s1, spatial) & has_operator(c_s1, isPartOf) & has_value(c_s1, europe)).
fof(c_s2_def, axiom, has_operand(c_s2, spatial) & has_operator(c_s2, eq) & has_value(c_s2, france)).
fof(c_p1_def, axiom, has_operand(c_p1, purpose) & has_operator(c_p1, isA) & has_value(c_p1, nonCommercialPurpose)).
fof(c_p2_def, axiom, has_operand(c_p2, purpose) & has_operator(c_p2, isA) & has_value(c_p2, marketing)).
fof(c_p3_def, axiom, has_operand(c_p3, purpose) & has_operator(c_p3, eq) & has_value(c_p3, scientificResearch)).

fof(and_or_compatible, conjecture,
    (?[X]: (in_denotation(X, c_s1) & in_denotation(X, c_s2)))
  & ((?[Y]: (in_denotation(Y, c_p1) & in_denotation(Y, c_p3)))
   | (?[Z]: (in_denotation(Z, c_p2) & in_denotation(Z, c_p3))))).
%--------------------------------------------------------------------------
