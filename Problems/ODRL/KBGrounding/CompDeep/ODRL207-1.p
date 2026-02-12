%--------------------------------------------------------------------------
% File     : ODRL207-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : AND-of-XONE: spatial compat AND xone purpose: Unknown
% Status   : CounterSatisfiable
% Authors  : Mustafa, D. & Sutcliffe, G.

%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(cs_def, axiom,
    has_operand(cs,spatial) & has_operator(cs,isPartOf) & has_value(cs,europe)).
fof(co_def, axiom,
    has_operand(co,spatial) & has_operator(co,eq) & has_value(co,france)).
fof(c1_def, axiom,
    has_operand(c1,purpose) & has_operator(c1,isA) & has_value(c1,commercialPurpose)).
fof(c2_def, axiom,
    has_operand(c2,purpose) & has_operator(c2,isA) & has_value(c2,nonCommercialPurpose)).
fof(c3_def, axiom,
    has_operand(c3,purpose) & has_operator(c3,eq) & has_value(c3,scientificResearch)).

% --- Conjecture ---
fof(and_xone_compatible, conjecture,
    (?[X]: (in_denotation(X,cs) & in_denotation(X,co)))
  & ((?[Y]: (in_denotation(Y,c1) & ~in_denotation(Y,c2) & in_denotation(Y,c3)))
   | (?[Z]: (in_denotation(Z,c2) & ~in_denotation(Z,c1) & in_denotation(Z,c3))))).

%--------------------------------------------------------------------------