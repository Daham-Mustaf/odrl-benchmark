%--------------------------------------------------------------------------
% File     : ODRL205-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE: one Unknown branch: Unknown
% Status   : CounterSatisfiable
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,isA) & has_value(c1,commercialPurpose)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,isA) & has_value(c2,nonCommercialPurpose)).
fof(c3_def, axiom,
    has_operand(c3,purpose) & has_operator(c3,eq) & has_value(c3,scientificResearch)).

% --- Conjecture ---
fof(xone_compatible, conjecture,
    (?[X]: (in_denotation(X,c1) & ~in_denotation(X,c2) & in_denotation(X,c3)))
  | (?[Y]: (in_denotation(Y,c2) & ~in_denotation(Y,c1) & in_denotation(Y,c3)))).

%--------------------------------------------------------------------------