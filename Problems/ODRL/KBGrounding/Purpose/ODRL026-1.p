%--------------------------------------------------------------------------
% File     : ODRL026-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAllOf compatible: commercialResearch in R&D ∩ commercialPurpose
% Version  : DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax v0.4
% Expected : Theorem
% Source   : Mustafa & Sutcliffe, DEXA 2026
% Notes    : Policy: purpose isAllOf {researchAndDevelopment, commercialPurpose}
%            Request: purpose eq commercialResearch
%            commercialResearch ⊑ both via DAG multi-parent → compatible.
%            Tests isAllOf intersection operator.
%            If-direction grounded per-problem (conjunction of 2 values).
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy: purpose isAllOf {researchAndDevelopment, commercialPurpose} ---

fof(policy_a_constraint, axiom, has_constraint(policy_a, c1)).
fof(c1_operand,  axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isAllOf)).
fof(c1_value1,   axiom, has_value(c1, researchAndDevelopment)).
fof(c1_value2,   axiom, has_value(c1, commercialPurpose)).

% --- isAllOf if-direction (grounded for this problem's 2 values) ---
% X in denotation of c1 iff X ⊑ researchAndDevelopment AND X ⊑ commercialPurpose

fof(denotation_isAllOf_c1_if, axiom,
    ![X]: ((subClassOf(X, researchAndDevelopment) & subClassOf(X, commercialPurpose)
            & taxonomic(purpose))
        => in_denotation(X, c1))).

% --- Request: purpose eq commercialResearch ---

fof(request_b_constraint, axiom, has_constraint(request_b, c2)).
fof(c2_operand,  axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, commercialResearch)).

% --- Conjecture: denotations overlap (compatible) ---

fof(odrl026_compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
