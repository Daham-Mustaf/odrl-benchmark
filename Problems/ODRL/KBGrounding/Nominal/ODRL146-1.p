%--------------------------------------------------------------------------
% File     : ODRL146-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Nominal isNoneOf {email,api} vs eq ftp: Compatible
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/NOM000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,channel) & has_operator(c1,isNoneOf) & has_value(c1,email) & has_value(c1,api)).
fof(c2_def, axiom,
    has_operand(c2,channel) & has_operator(c2,eq) & has_value(c2,ftp)).

% --- Per-problem grounding (if/only-if direction) ---
fof(c1_isNoneOf_if, axiom,
    ![X]: ((X != email & X != api) => in_denotation(X,c1))).
fof(c1_isNoneOf_onlyif, axiom,
    ![X]: (in_denotation(X,c1) => (X != email & X != api))).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------