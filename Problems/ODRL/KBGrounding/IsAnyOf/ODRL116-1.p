%--------------------------------------------------------------------------
% File     : ODRL116-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAnyOf {comm,mkt} vs isA R&D: cross-op overlap
% Status   : Theorem
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,isAnyOf) & has_value(c1,commercialPurpose) & has_value(c1,marketing)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,isA) & has_value(c2,researchAndDevelopment)).

% --- Conjecture ---
fof(compatible, conjecture,
    ?[X]: (in_denotation(X,c1) & in_denotation(X,c2))).

%--------------------------------------------------------------------------