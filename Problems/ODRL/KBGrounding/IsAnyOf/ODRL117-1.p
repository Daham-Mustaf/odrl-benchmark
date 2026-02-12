%--------------------------------------------------------------------------
% File     : ODRL117-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAnyOf {de,en} vs isAnyOf {fr,ar}: Unknown
% Status   : CounterSatisfiable
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,language) & has_operator(c1,isAnyOf) & has_value(c1,de) & has_value(c1,en)).
fof(c2_def, axiom,
    has_operand(c2,language) & has_operator(c2,isAnyOf) & has_value(c2,fr) & has_value(c2,ar)).

% --- Per-problem grounding (if/only-if direction) ---
fof(c1_isAnyOf_onlyif, axiom,
    ![X]: (in_denotation(X,c1) => (subClassOf(X,de) | subClassOf(X,en)))).
fof(c2_isAnyOf_onlyif, axiom,
    ![X]: (in_denotation(X,c2) => (subClassOf(X,fr) | subClassOf(X,ar)))).

% --- Conjecture ---
fof(conflict, conjecture,
    ~(?[X]: (in_denotation(X,c1) & in_denotation(X,c2)))).

%--------------------------------------------------------------------------