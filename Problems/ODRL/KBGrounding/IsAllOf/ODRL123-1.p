%--------------------------------------------------------------------------
% File     : ODRL123-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAllOf {R&D,nonComm} vs eq sciRes: Unknown
% Status   : CounterSatisfiable
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,isAllOf) & has_value(c1,researchAndDevelopment) & has_value(c1,nonCommercialPurpose)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,eq) & has_value(c2,scientificResearch)).

% --- Per-problem grounding (if/only-if direction) ---
fof(c1_isAllOf_if, axiom,
    ![X]: ((subClassOf(X,researchAndDevelopment) & subClassOf(X,nonCommercialPurpose) & taxonomic(purpose)) => in_denotation(X,c1))).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------