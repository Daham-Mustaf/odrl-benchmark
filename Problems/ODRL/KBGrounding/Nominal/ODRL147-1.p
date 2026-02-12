%--------------------------------------------------------------------------
% File     : ODRL147-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Nominal neq email vs eq email: Conflict
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/NOM000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,channel) & has_operator(c1,neq) & has_value(c1,email)).
fof(c2_def, axiom,
    has_operand(c2,channel) & has_operator(c2,eq) & has_value(c2,email)).

% --- Conjecture ---
fof(conflict, conjecture,
    ~(?[X]: (in_denotation(X,c1) & in_denotation(X,c2)))).

%--------------------------------------------------------------------------