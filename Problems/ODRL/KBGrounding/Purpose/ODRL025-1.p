%--------------------------------------------------------------------------
% File     : ODRL025-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAnyOf Unknown: commercialResearch not reachable
% Version  : DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax v0.3
% Expected : CounterSatisfiable
% Source   : Mustafa & Sutcliffe, DEXA 2026
% Notes    : Policy: purpose isAnyOf {nonCommercialPurpose, marketing}
%            Request: purpose eq commercialResearch
%            commercialResearch ⊑ commercialPurpose and R&D,
%            neither is nonCommercialPurpose or marketing.
%            No path in KB → Unknown.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy: purpose isAnyOf {nonCommercialPurpose, marketing} ---

fof(policy_a_constraint, axiom, has_constraint(policy_a, c1)).
fof(c1_operand,  axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isAnyOf)).
fof(c1_value1,   axiom, has_value(c1, nonCommercialPurpose)).
fof(c1_value2,   axiom, has_value(c1, marketing)).

% --- Request: purpose eq commercialResearch ---

fof(request_b_constraint, axiom, has_constraint(request_b, c2)).
fof(c2_operand,  axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, commercialResearch)).

% --- Conjecture: denotations overlap (compatible) ---

fof(odrl025_compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
