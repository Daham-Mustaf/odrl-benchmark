%--------------------------------------------------------------------------
% File     : ODRL138-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Double negation: isNoneOf {comm} vs isNoneOf {nonComm}
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,isNoneOf) & has_value(c1,commercialPurpose)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,isNoneOf) & has_value(c2,nonCommercialPurpose)).

% --- Per-problem grounding (if/only-if direction) ---
fof(c1_isNoneOf_if, axiom,
    ![X]: ((~subClassOf(X,commercialPurpose) & taxonomic(purpose)) => in_denotation(X,c1))).
fof(c2_isNoneOf_if, axiom,
    ![X]: ((~subClassOf(X,nonCommercialPurpose) & taxonomic(purpose)) => in_denotation(X,c2))).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------