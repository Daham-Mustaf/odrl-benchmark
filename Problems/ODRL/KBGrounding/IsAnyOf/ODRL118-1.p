%--------------------------------------------------------------------------
% File     : ODRL118-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAnyOf {de,ar} vs isAnyOf {en,ar}: overlap on ar
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,language) & has_operator(c1,isAnyOf) & has_value(c1,de) & has_value(c1,ar)).
fof(c2_def, axiom,
    has_operand(c2,language) & has_operator(c2,isAnyOf) & has_value(c2,en) & has_value(c2,ar)).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------