%--------------------------------------------------------------------------
% File     : ODRL194-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Aligned isNoneOf: {deu} vs eq fra: Compatible
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,language) & has_operator(c1,isNoneOf) & has_value(c1,deu)).
fof(c2_def, axiom,
    has_operand(c2,language) & has_operator(c2,eq) & has_value(c2,fra)).

% --- Per-problem grounding (if/only-if direction) ---
fof(c1_isNoneOf_if, axiom,
    ![X]: ((~subClassOf(X,deu) & taxonomic(language)) => in_denotation(X,c1))).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------