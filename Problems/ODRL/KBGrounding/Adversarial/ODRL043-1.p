%--------------------------------------------------------------------------
% File     : ODRL043-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : ATTACK: Phantom entity via impossible isAllOf
% Status   : CounterSatisfiable
% Expected : Unknown — no named entity satisfies both branches
%
% Attack vector: Can the open world create a phantom witness
%   that is subClassOf BOTH commercialPurpose AND nonCommercialPurpose?
%
%   c1: purpose isAllOf {commercialPurpose, nonCommercialPurpose}
%   c2: purpose eq commercialResearch
%
%   No DPV concept is under both branches:
%     commercialResearch ⊑ commercialPurpose ✓
%     commercialResearch ⊑ nonCommercialPurpose ✗ (no path)
%
%   The KB has ~subClassOf(commercialPurpose, nonCommercialPurpose)
%   but NOT ~subClassOf(commercialResearch, nonCommercialPurpose).
%   However, the prover cannot PROVE subClassOf(commercialResearch,
%   nonCommercialPurpose) either, so the if-direction doesn't fire.
%
%   Failure mode: If Theorem → the open world created a phantom entity
%   satisfying an impossible intersection. This would be unsound.
%
%   Why this matters: isAllOf narrows denotations. If the encoding
%   allows phantom witnesses, intersection constraints are meaningless.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_operand, axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isAllOf)).
fof(c1_value1,   axiom, has_value(c1, commercialPurpose)).
fof(c1_value2,   axiom, has_value(c1, nonCommercialPurpose)).

% isAllOf if-direction (grounded for this problem)
fof(isAllOf_if_c1, axiom,
    ![X]: ((subClassOf(X, commercialPurpose) & subClassOf(X, nonCommercialPurpose)
             & taxonomic(purpose))
        => in_denotation(X, c1))).

% isAllOf only-if is in Layer 2 (GROUND000-1.ax)

fof(c2_operand, axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, commercialResearch)).

% Conjecture: denotations overlap — should FAIL (no phantom witness)
fof(compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
