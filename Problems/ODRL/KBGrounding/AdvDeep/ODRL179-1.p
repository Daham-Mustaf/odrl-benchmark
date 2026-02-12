%--------------------------------------------------------------------------
% File     : ODRL179-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : All-Unknown conjunction: both operands Unknown
% Status   : CounterSatisfiable
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,spatial) & has_operator(c1,isPartOf) & has_value(c1,france)).
fof(c2_def, axiom,
    has_operand(c2,spatial) & has_operator(c2,eq) & has_value(c2,bavaria)).
fof(c3_def, axiom,
    has_operand(c3,purpose) & has_operator(c3,isA) & has_value(c3,nonCommercialPurpose)).
fof(c4_def, axiom,
    has_operand(c4,purpose) & has_operator(c4,eq) & has_value(c4,scientificResearch)).

% --- Conjecture ---
fof(cross_compatible, conjecture,
    (?[X]: (in_denotation(X,c1) & in_denotation(X,c2)))
  & (?[Y]: (in_denotation(Y,c3) & in_denotation(Y,c4)))).

%--------------------------------------------------------------------------