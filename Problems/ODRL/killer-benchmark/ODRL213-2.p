%--------------------------------------------------------------------------
% File     : ODRL213-2.p : TPTP v0.2.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-KB spatial negated: also CounterSat (genuine Unknown)
% Version  : ISO3166-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : CounterSatisfiable
% Source   : Mustafa & Sutcliffe, 2026
%
% Notes    : Paired check for ODRL213-1.p.
%            Both CounterSat → genuine Unknown (neither direction provable).
%            westernEurope is a foreign constant in ISO3166 — no partOf
%            axioms connect it to anything, so neither the conjecture
%            nor its negation is provable.
%
%   VALIDATES: Def 5 (three-valued Unknown), Def 8 (strengthened).
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').
% --- Same constraint setup as ODRL213-1.p ---
fof(cA2_constraint, axiom, has_constraint(branch_a, c_A2)).
fof(cA2_operand,    axiom, has_operand(c_A2, spatial)).
fof(cA2_operator,   axiom, has_operator(c_A2, isPartOf)).
fof(cA2_value,      axiom, has_value(c_A2, westernEurope)).
fof(cR2_constraint, axiom, has_constraint(request, c_R2)).
fof(cR2_operand,    axiom, has_operand(c_R2, spatial)).
fof(cR2_operator,   axiom, has_operator(c_R2, eq)).
fof(cR2_value,      axiom, has_value(c_R2, france)).
% --- Conjecture: NEGATED (conflict check) ---
fof(odrl213_cross_spatial_conflict, conjecture,
    ~?[X]: (in_denotation(X, c_A2) & in_denotation(X, c_R2))).
%--------------------------------------------------------------------------
