%--------------------------------------------------------------------------
% File     : ODRL199-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Triple degradation: all 3 operands unmapped
% Status   : CounterSatisfiable
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO001-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/LNG001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,spatial) & has_operator(c1,isPartOf) & has_value(c1,deu)).
fof(c2_def, axiom,
    has_operand(c2,spatial) & has_operator(c2,eq) & has_value(c2,bavaria)).
fof(c3_def, axiom,
    has_operand(c3,purpose) & has_operator(c3,isA) & has_value(c3,researchAndDevelopment)).
fof(c4_def, axiom,
    has_operand(c4,purpose) & has_operator(c4,eq) & has_value(c4,scientificResearch)).
fof(c5_def, axiom,
    has_operand(c5,language) & has_operator(c5,isA) & has_value(c5,deu)).
fof(c6_def, axiom,
    has_operand(c6,language) & has_operator(c6,eq) & has_value(c6,de_AT)).

% --- Conjecture ---
fof(cross_compatible, conjecture,
    (?[X]: (in_denotation(X,c1) & in_denotation(X,c2)))
  & (?[Y]: (in_denotation(Y,c3) & in_denotation(Y,c4)))
  & (?[Z]: (in_denotation(Z,c5) & in_denotation(Z,c6)))).

%--------------------------------------------------------------------------