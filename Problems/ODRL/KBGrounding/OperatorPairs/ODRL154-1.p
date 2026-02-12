%--------------------------------------------------------------------------
% File     : ODRL154-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : isNoneOf {de} vs isNoneOf {en}: shared exclusion
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,language) & has_operator(c1,isNoneOf) & has_value(c1,de)).
fof(c2_def, axiom,
    has_operand(c2,language) & has_operator(c2,isNoneOf) & has_value(c2,en)).

% --- Per-problem grounding (if/only-if direction) ---
fof(c1_isNoneOf_if, axiom,
    ![X]: ((~subClassOf(X,de) & taxonomic(language)) => in_denotation(X,c1))).
fof(c2_isNoneOf_if, axiom,
    ![X]: ((~subClassOf(X,en) & taxonomic(language)) => in_denotation(X,c2))).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------