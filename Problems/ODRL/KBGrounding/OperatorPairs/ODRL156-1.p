%--------------------------------------------------------------------------
% File     : ODRL156-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : eq acadRes vs isNoneOf {R&D}: Conflict
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,eq) & has_value(c1,academicResearch)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,isNoneOf) & has_value(c2,researchAndDevelopment)).

% --- Conjecture ---
fof(conflict, conjecture,
    ~(?[X]: (in_denotation(X,c1) & in_denotation(X,c2)))).

%--------------------------------------------------------------------------