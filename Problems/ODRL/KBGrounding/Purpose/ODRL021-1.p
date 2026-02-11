%--------------------------------------------------------------------------
% File     : ODRL021-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Taxonomic Unknown: scientificResearch ⊄ nonCommercialPurpose
% Version  : DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : CounterSatisfiable
% Source   : Mustafa & Sutcliffe, DEXA 2026
% Notes    : Policy: purpose isA nonCommercialPurpose
%            Request: purpose eq scientificResearch
%            scientificResearch is under researchAndDevelopment,
%            NOT under nonCommercialPurpose in official DPV.
%            KB has no path → Unknown.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy: purpose isA nonCommercialPurpose ---

fof(policy_a_constraint, axiom, has_constraint(policy_a, c1)).
fof(c1_operand,  axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isA)).
fof(c1_value,    axiom, has_value(c1, nonCommercialPurpose)).

% --- Request: purpose eq scientificResearch ---

fof(request_b_constraint, axiom, has_constraint(request_b, c2)).
fof(c2_operand,  axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, scientificResearch)).

% --- Conjecture: denotations overlap (compatible) ---

fof(odrl021_compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
