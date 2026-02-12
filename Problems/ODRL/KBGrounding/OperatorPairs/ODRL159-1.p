%--------------------------------------------------------------------------
% File     : ODRL159-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : isA R&D vs isAnyOf {comm,nonComm}: overlap
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,isA) & has_value(c1,researchAndDevelopment)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,isAnyOf) & has_value(c2,commercialPurpose) & has_value(c2,nonCommercialPurpose)).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------