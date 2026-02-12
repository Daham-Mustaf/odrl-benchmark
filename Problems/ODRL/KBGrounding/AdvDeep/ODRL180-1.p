%--------------------------------------------------------------------------
% File     : ODRL180-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Chain: isAnyOf {A,E} vs eq C: A below C
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/CHN000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,isAnyOf) & has_value(c1,chainA) & has_value(c1,chainE)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,eq) & has_value(c2,chainC)).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------