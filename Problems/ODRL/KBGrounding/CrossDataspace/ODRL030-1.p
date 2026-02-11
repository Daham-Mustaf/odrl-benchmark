%--------------------------------------------------------------------------
% File     : ODRL030-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-dataspace compatible: spatial + purpose both align
% Version  : GEO000-0.ax, DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : Theorem
% Source   : Mustafa & Sutcliffe,  2026
% Notes    : Policy A (Dataspace 1): spatial isPartOf europe
%                                     AND purpose isA researchAndDevelopment
%            Request B (Dataspace 2): spatial eq france
%                                     AND purpose eq academicResearch
%            Spatial: france ⊑ europe → compatible
%            Purpose: academicResearch ⊑ R&D → compatible
%            Both pairs overlap → overall compatible.
%            First cross-dataspace benchmark.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy A: spatial isPartOf europe ---

fof(policy_a_constraint_spatial, axiom, has_constraint(policy_a, c1)).
fof(c1_operand,  axiom, has_operand(c1, spatial)).
fof(c1_operator, axiom, has_operator(c1, isPartOf)).
fof(c1_value,    axiom, has_value(c1, europe)).

% --- Policy A: purpose isA researchAndDevelopment ---

fof(policy_a_constraint_purpose, axiom, has_constraint(policy_a, c3)).
fof(c3_operand,  axiom, has_operand(c3, purpose)).
fof(c3_operator, axiom, has_operator(c3, isA)).
fof(c3_value,    axiom, has_value(c3, researchAndDevelopment)).

% --- Request B: spatial eq france ---

fof(request_b_constraint_spatial, axiom, has_constraint(request_b, c2)).
fof(c2_operand,  axiom, has_operand(c2, spatial)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, france)).

% --- Request B: purpose eq academicResearch ---

fof(request_b_constraint_purpose, axiom, has_constraint(request_b, c4)).
fof(c4_operand,  axiom, has_operand(c4, purpose)).
fof(c4_operator, axiom, has_operator(c4, eq)).
fof(c4_value,    axiom, has_value(c4, academicResearch)).

% --- Conjecture: BOTH operand pairs overlap (cross-dataspace compatible) ---

fof(odrl030_cross_compatible, conjecture,
    (?[X]: (in_denotation(X, c1) & in_denotation(X, c2)))
    & (?[Y]: (in_denotation(Y, c3) & in_denotation(Y, c4)))).
%--------------------------------------------------------------------------
