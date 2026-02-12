%--------------------------------------------------------------------------
% File     : ODRL094-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : neq de vs isA de: overlap on de_AT, de_CH
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer0-DomainKB/LNG002-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,language) & has_operator(c1,neq) & has_value(c1,de)).
fof(c2_def, axiom,
    has_operand(c2,language) & has_operator(c2,isA) & has_value(c2,de)).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------