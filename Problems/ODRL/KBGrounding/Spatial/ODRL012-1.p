%--------------------------------------------------------------------------
% File     : ODRL012-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : End-to-end spatial compatibility (paper Table 1)
% Version  : GEO000-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : Theorem
% Source   : Mustafa & Sutcliffe, 
% Notes    : Policy A: spatial isPartOf europe (permission)
%            Request B: spatial eq france
%            France partOf europe → denotations overlap → compatible.
%            First 3-layer vertical slice.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy A: permission with spatial isPartOf europe ---

fof(policy_a_type, axiom, permission(policy_a)).
fof(policy_a_asset, axiom, has_asset(policy_a, dataset1)).
fof(policy_a_constraint, axiom, has_constraint(policy_a, c1)).
fof(c1_operand, axiom, has_operand(c1, spatial)).
fof(c1_operator, axiom, has_operator(c1, isPartOf)).
fof(c1_value, axiom, has_value(c1, europe)).

% --- Request B: spatial eq france ---

fof(request_b_constraint, axiom, has_constraint(request_b, c2)).
fof(c2_operand, axiom, has_operand(c2, spatial)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value, axiom, has_value(c2, france)).

% --- Conjecture: denotations overlap (compatible) ---

fof(odrl012_compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
