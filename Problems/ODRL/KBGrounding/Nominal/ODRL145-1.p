%--------------------------------------------------------------------------
% File     : ODRL145-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Nominal isAnyOf {email,api} vs eq email: Compatible
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/NOM000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,channel) & has_operator(c1,isAnyOf) & has_value(c1,email) & has_value(c1,api)).
fof(c2_def, axiom,
    has_operand(c2,channel) & has_operator(c2,eq) & has_value(c2,email)).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------