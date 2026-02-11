%--------------------------------------------------------------------------
% File     : ODRL027-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAllOf Unknown: scientificResearch not in R&D ∩ nonCommercialPurpose
% Version  : DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax v0.4
% Expected : CounterSatisfiable
% Source   : Mustafa & Sutcliffe,  2026
% Notes    : Policy: purpose isAllOf {researchAndDevelopment, nonCommercialPurpose}
%            Request: purpose eq scientificResearch
%            scientificResearch ⊑ researchAndDevelopment but
%            NOT ⊑ nonCommercialPurpose in DPV → Unknown.
%            Tests isAllOf with incomplete KB.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy: purpose isAllOf {researchAndDevelopment, nonCommercialPurpose} ---

fof(policy_a_constraint, axiom, has_constraint(policy_a, c1)).
fof(c1_operand,  axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isAllOf)).
fof(c1_value1,   axiom, has_value(c1, researchAndDevelopment)).
fof(c1_value2,   axiom, has_value(c1, nonCommercialPurpose)).

% --- isAllOf if-direction (grounded for this problem's 2 values) ---

fof(denotation_isAllOf_c1_if, axiom,
    ![X]: ((subClassOf(X, researchAndDevelopment) & subClassOf(X, nonCommercialPurpose)
            & taxonomic(purpose))
        => in_denotation(X, c1))).

% --- Request: purpose eq scientificResearch ---

fof(request_b_constraint, axiom, has_constraint(request_b, c2)).
fof(c2_operand,  axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, scientificResearch)).

% --- Conjecture: denotations overlap (compatible) ---

fof(odrl027_compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
