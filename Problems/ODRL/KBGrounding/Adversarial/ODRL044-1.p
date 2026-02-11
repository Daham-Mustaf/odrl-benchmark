%--------------------------------------------------------------------------
% File     : ODRL044-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : ATTACK: Operand type mismatch — isPartOf on taxonomic
% Status   : CounterSatisfiable
% Expected : Unknown — type guard blocks denotation, c1 is empty
%
% Attack vector: Does the mereological(L) type guard actually work?
%
%   c1: purpose isPartOf researchAndDevelopment
%   c2: purpose eq academicResearch
%
%   isPartOf requires mereological(L). purpose is taxonomic, NOT
%   mereological. So the if-direction should never fire for c1.
%   The denotation of c1 is effectively empty.
%
%   Even though academicResearch IS a subconcept of R&D in DPV,
%   the WRONG operator is used. The type guard must prevent this.
%
%   Failure mode: If Theorem → type guard bypassed. The encoding
%   would treat taxonomic and mereological operands identically,
%   conflating subClassOf and partOf — a fundamental type error.
%
%   This models a real-world scenario: a policy author mistakenly
%   uses isPartOf instead of isA for a purpose constraint.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_operand, axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isPartOf)).
fof(c1_value,    axiom, has_value(c1, researchAndDevelopment)).

fof(c2_operand, axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, academicResearch)).

% Conjecture: denotations overlap — should FAIL (type guard blocks)
fof(compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
