%--------------------------------------------------------------------------
% File     : ODRL022-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : DAG multi-parent: commercialResearch isA commercialPurpose
% Version  : DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : Theorem
% Source   : Mustafa & Sutcliffe,  2026
% Notes    : Policy: purpose isA commercialPurpose
%            Request: purpose eq commercialResearch
%            commercialResearch has two parents in DPV DAG:
%            researchAndDevelopment AND commercialPurpose.
%            Tests that multi-parent subsumption works.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(policy_a_constraint, axiom, has_constraint(policy_a, c1)).
fof(c1_operand,  axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isA)).
fof(c1_value,    axiom, has_value(c1, commercialPurpose)).

fof(request_b_constraint, axiom, has_constraint(request_b, c2)).
fof(c2_operand,  axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, commercialResearch)).

fof(odrl022_compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
