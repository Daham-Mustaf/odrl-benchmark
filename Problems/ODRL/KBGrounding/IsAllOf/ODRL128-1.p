%--------------------------------------------------------------------------
% File     : ODRL128-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAllOf vs isAnyOf: cross-operator Unknown
% Status   : CounterSatisfiable
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,isAllOf) & has_value(c1,researchAndDevelopment) & has_value(c1,commercialPurpose)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,isAnyOf) & has_value(c2,nonCommercialPurpose) & has_value(c2,marketing)).

% --- Per-problem grounding (if/only-if direction) ---
fof(c1_isAllOf_if, axiom,
    ![X]: ((subClassOf(X,researchAndDevelopment) & subClassOf(X,commercialPurpose) & taxonomic(purpose)) => in_denotation(X,c1))).
fof(c2_isAnyOf_onlyif, axiom,
    ![X]: (in_denotation(X,c2) => (subClassOf(X,nonCommercialPurpose) | subClassOf(X,marketing)))).

% --- Conjecture ---
fof(conflict, conjecture,
    ~(?[X]: (in_denotation(X,c1) & in_denotation(X,c2)))).

%--------------------------------------------------------------------------