%--------------------------------------------------------------------------
% File     : ODRL020-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Taxonomic compatibility: nonCommercialResearch isA nonCommercialPurpose
% Version  : DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : Theorem
% Source   : Mustafa & Sutcliffe, DEXA 2026
% Notes    : Policy: purpose isA nonCommercialPurpose
%            Request: purpose eq nonCommercialResearch
%            nonCommercialResearch ⊑ nonCommercialPurpose (in DPV)
%            First taxonomic grounding test using isA operator.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy: purpose isA nonCommercialPurpose ---

fof(policy_a_constraint, axiom, has_constraint(policy_a, c1)).
fof(c1_operand,  axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isA)).
fof(c1_value,    axiom, has_value(c1, nonCommercialPurpose)).

% --- Request: purpose eq nonCommercialResearch ---

fof(request_b_constraint, axiom, has_constraint(request_b, c2)).
fof(c2_operand,  axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, nonCommercialResearch)).

% --- Conjecture: denotations overlap (compatible) ---

fof(odrl020_compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
