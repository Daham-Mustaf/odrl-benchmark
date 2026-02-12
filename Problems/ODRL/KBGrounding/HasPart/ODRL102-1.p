%--------------------------------------------------------------------------
% File     : ODRL102-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : hasPart france vs isPartOf europe: overlap
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,spatial) & has_operator(c1,hasPart) & has_value(c1,france)).
fof(c2_def, axiom,
    has_operand(c2,spatial) & has_operator(c2,isPartOf) & has_value(c2,europe)).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------