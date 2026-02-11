%--------------------------------------------------------------------------
% File     : ODRL015-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Transitive conflict gap: bavaria vs france
% Version  : GEO000-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : CounterSatisfiable
% Source   : Mustafa & Sutcliffe, 
% Notes    : Policy A: spatial isPartOf france
%            Request B: spatial eq bavaria
%            No axiom ~partOf(bavaria, france) exists.
%            KB is incomplete — cannot prove conflict.
%            Demonstrates open-world limitation.
%            Maps to paper verdict: Unknown.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy A: spatial isPartOf france ---

fof(policy_a_constraint, axiom, has_constraint(policy_a, c1)).
fof(c1_operand, axiom, has_operand(c1, spatial)).
fof(c1_operator, axiom, has_operator(c1, isPartOf)).
fof(c1_value, axiom, has_value(c1, france)).

% --- Request B: spatial eq bavaria ---

fof(request_b_constraint, axiom, has_constraint(request_b, c2)).
fof(c2_operand, axiom, has_operand(c2, spatial)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value, axiom, has_value(c2, bavaria)).

% --- Conjecture: no shared value (conflict) ---

fof(odrl015_conflict, conjecture,
    ~?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
