%--------------------------------------------------------------------------
% File     : ODRL181-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Chain: isNoneOf {E} vs eq D: D below E
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/CHN000-0.ax').
include('Axioms/Layer0-DomainKB/CHN001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,isNoneOf) & has_value(c1,chainE)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,eq) & has_value(c2,chainD)).

% --- Per-problem grounding (if/only-if direction) ---
fof(c1_isNoneOf_if, axiom,
    ![X]: ((~subClassOf(X,chainE) & taxonomic(purpose)) => in_denotation(X,c1))).

% --- Conjecture ---
fof(conflict, conjecture,
    ~(?[X]: (in_denotation(X,c1) & in_denotation(X,c2)))).

%--------------------------------------------------------------------------