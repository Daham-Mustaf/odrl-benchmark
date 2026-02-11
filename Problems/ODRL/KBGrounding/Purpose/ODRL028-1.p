%--------------------------------------------------------------------------
% File     : ODRL028-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : isNoneOf compatible: nonCommercialResearch ∉ {commercialPurpose}
% Version  : DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax v0.5
% Expected : Theorem
% Source   : Mustafa & Sutcliffe, DEXA 2026
% Notes    : Policy: purpose isNoneOf {commercialPurpose}
%            Request: purpose eq nonCommercialResearch
%            nonCommercialResearch ⊄ commercialPurpose (DPV disjointness)
%            → nonCommercialResearch in isNoneOf denotation → compatible.
%            Tests isNoneOf exclusion operator.
%            If-direction grounded per-problem (negation of single value).
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy: purpose isNoneOf {commercialPurpose} ---

fof(policy_a_constraint, axiom, has_constraint(policy_a, c1)).
fof(c1_operand,  axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isNoneOf)).
fof(c1_value1,   axiom, has_value(c1, commercialPurpose)).

% --- isNoneOf if-direction (grounded for single value) ---
% X in denotation of c1 iff ¬subClassOf(X, commercialPurpose)
% CNF: subClassOf(X, commercialPurpose) | in_denotation(X, c1)

fof(denotation_isNoneOf_c1_if, axiom,
    ![X]: ((~subClassOf(X, commercialPurpose) & taxonomic(purpose))
        => in_denotation(X, c1))).

% --- Request: purpose eq nonCommercialResearch ---

fof(request_b_constraint, axiom, has_constraint(request_b, c2)).
fof(c2_operand,  axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, nonCommercialResearch)).

% --- Conjecture: denotations overlap (compatible) ---

fof(odrl028_compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
