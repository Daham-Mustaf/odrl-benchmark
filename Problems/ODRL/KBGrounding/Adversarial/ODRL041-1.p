%--------------------------------------------------------------------------
% File     : ODRL041-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : ATTACK: Cross-operator denotation overlap (isA vs isAnyOf)
% Status   : Theorem
% Expected : Compatible — witness = commercialResearch
%
% Attack vector: Do denotation rules from DIFFERENT operators compose?
%   c1: purpose isA researchAndDevelopment
%       denotation = {x | subClassOf(x, R&D)}
%       = {R&D, academicResearch, scientificResearch, commercialResearch,
%          nonCommercialResearch}
%
%   c2: purpose isAnyOf {commercialPurpose, marketing}
%       denotation = {x | subClassOf(x, commPurpose) ∨ subClassOf(x, marketing)}
%       = {commPurpose, commResearch, marketing, advertising, directMarketing}
%
%   Intersection: commercialResearch (⊑ R&D via parent, ⊑ commPurpose via DAG)
%
%   Failure mode: CounterSat would mean operator denotations can't compose —
%   each operator's rules live in isolation.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_operand, axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isA)).
fof(c1_value,    axiom, has_value(c1, researchAndDevelopment)).

fof(c2_operand, axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, isAnyOf)).
fof(c2_value1,   axiom, has_value(c2, commercialPurpose)).
fof(c2_value2,   axiom, has_value(c2, marketing)).

% Conjecture: denotations overlap via commercialResearch
fof(compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
