%--------------------------------------------------------------------------
% File     : ODRL040-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : ATTACK: Reflexive self-overlap (eq X vs eq X)
% Status   : Theorem
% Expected : Compatible — witness = academicResearch (trivial)
%
% Attack vector: Can the encoding handle the simplest possible case?
%   If this fails, the denotation rules are fundamentally broken.
%   Failure mode: CounterSat would mean eq can't prove self-overlap.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_operand, axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, eq)).
fof(c1_value,    axiom, has_value(c1, academicResearch)).

fof(c2_operand, axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, academicResearch)).

% Conjecture: denotations overlap (trivially — same singleton)
fof(compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
