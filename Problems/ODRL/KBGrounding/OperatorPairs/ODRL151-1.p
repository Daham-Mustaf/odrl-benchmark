%--------------------------------------------------------------------------
% File     : ODRL151-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : neq comm vs isA comm: overlap on children
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/DPV002-0.ax').
include('Axioms/Layer0-DomainKB/DPV003-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,neq) & has_value(c1,commercialPurpose)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,isA) & has_value(c2,commercialPurpose)).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------