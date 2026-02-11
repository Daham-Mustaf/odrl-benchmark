%--------------------------------------------------------------------------
% File     : ODRL029-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : isNoneOf conflict: commercialResearch ∈ {commercialPurpose}
% Version  : DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax v0.5
% Expected : Theorem
% Source   : Mustafa & Sutcliffe,  2026
% Notes    : Policy: purpose isNoneOf {commercialPurpose}
%            Request: purpose eq commercialResearch
%            commercialResearch ⊑ commercialPurpose → excluded by isNoneOf
%            → empty intersection → conflict.
%            Only-if direction sufficient for conflict proof:
%            Skolem witness forced to commercialResearch (eq),
%            isNoneOf only-if forces ¬subClassOf(commercialResearch, commercialPurpose),
%            contradicts DPV positive axiom.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy: purpose isNoneOf {commercialPurpose} ---

fof(policy_a_constraint, axiom, has_constraint(policy_a, c1)).
fof(c1_operand,  axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isNoneOf)).
fof(c1_value1,   axiom, has_value(c1, commercialPurpose)).

% --- Request: purpose eq commercialResearch ---

fof(request_b_constraint, axiom, has_constraint(request_b, c2)).
fof(c2_operand,  axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, commercialResearch)).

% --- Conjecture: no shared value (conflict) ---

fof(odrl029_conflict, conjecture,
    ~?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
