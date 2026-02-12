%--------------------------------------------------------------------------
% File     : ODRL193-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Aligned isAnyOf conflict: {deu,eng} vs fra
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,language) & has_operator(c1,isAnyOf) & has_value(c1,deu) & has_value(c1,eng)).
fof(c2_def, axiom,
    has_operand(c2,language) & has_operator(c2,eq) & has_value(c2,fra)).

% --- Per-problem grounding (if/only-if direction) ---
fof(c1_isAnyOf_onlyif, axiom,
    ![X]: (in_denotation(X,c1) => (subClassOf(X,deu) | subClassOf(X,eng)))).

% --- Conjecture ---
fof(conflict, conjecture,
    ~(?[X]: (in_denotation(X,c1) & in_denotation(X,c2)))).

%--------------------------------------------------------------------------