%--------------------------------------------------------------------------
% File     : ODRL139-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : isNoneOf singleton on |C|=1: empty set
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/SNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,isNoneOf) & has_value(c1,singleton)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,eq) & has_value(c2,singleton)).

% --- Conjecture ---
fof(conflict, conjecture,
    ~(?[X]: (in_denotation(X,c1) & in_denotation(X,c2)))).

%--------------------------------------------------------------------------