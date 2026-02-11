%--------------------------------------------------------------------------
% File     : ODRL033-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-dataspace double Unknown: both dimensions undecidable
% Version  : GEO000-0.ax, DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : CounterSatisfiable
% Source   : Mustafa & Sutcliffe,  2026
% Notes    : Policy A (Dataspace 1): spatial isPartOf france
%                                     AND purpose isA nonCommercialPurpose
%            Request B (Dataspace 2): spatial eq bavaria
%                                     AND purpose eq scientificResearch
%            Spatial: no ~partOf(bavaria, france) → Unknown
%            Purpose: scientificResearch ⊄ nonCommercialPurpose → Unknown
%            Both dimensions individually Unknown → conjunction Unknown.
%            Worst case for cross-dataspace reasoning.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy A: spatial isPartOf france ---

fof(policy_a_constraint_spatial, axiom, has_constraint(policy_a, c1)).
fof(c1_operand,  axiom, has_operand(c1, spatial)).
fof(c1_operator, axiom, has_operator(c1, isPartOf)).
fof(c1_value,    axiom, has_value(c1, france)).

% --- Policy A: purpose isA nonCommercialPurpose ---

fof(policy_a_constraint_purpose, axiom, has_constraint(policy_a, c3)).
fof(c3_operand,  axiom, has_operand(c3, purpose)).
fof(c3_operator, axiom, has_operator(c3, isA)).
fof(c3_value,    axiom, has_value(c3, nonCommercialPurpose)).

% --- Request B: spatial eq bavaria ---

fof(request_b_constraint_spatial, axiom, has_constraint(request_b, c2)).
fof(c2_operand,  axiom, has_operand(c2, spatial)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, bavaria)).

% --- Request B: purpose eq scientificResearch ---

fof(request_b_constraint_purpose, axiom, has_constraint(request_b, c4)).
fof(c4_operand,  axiom, has_operand(c4, purpose)).
fof(c4_operator, axiom, has_operator(c4, eq)).
fof(c4_value,    axiom, has_value(c4, scientificResearch)).

% --- Conjecture: both operand pairs overlap ---
% Expected to FAIL: neither dimension is decidable.

fof(odrl033_cross_compatible, conjecture,
    (?[X]: (in_denotation(X, c1) & in_denotation(X, c2)))
    & (?[Y]: (in_denotation(Y, c3) & in_denotation(Y, c4)))).
%--------------------------------------------------------------------------
