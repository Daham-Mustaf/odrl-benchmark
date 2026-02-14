%--------------------------------------------------------------------------
% File     : ODRL211-1.p : TPTP v0.2.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Xone Branch A: enriched DPV resolves Unknown → Compatible
% Version  : DPV004-0.ax, GEO003-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : Theorem
% Source   : Mustafa & Sutcliffe, 2026
%
% Notes    : Same scenario as ODRL210 but using DPV004-0.ax which adds:
%              ¬subClassOf(scientificResearch, commercialPurpose)
%
%   This file tests the FULL Branch A (both operands, and-composition):
%     Branch A: purpose isNoneOf {commercial} AND spatial isPartOf westernEurope
%     Request:  purpose eq scientificResearch AND spatial eq france
%
%   TRACE — PURPOSE PAIR (Def 3):
%     ⟦c_A1⟧ = C \ {x | x ⊑ commercial}
%     The isNoneOf if-direction fires because DPV004 includes:
%       ¬subClassOf(scientificResearch, commercialPurpose)
%     Therefore: in_denotation(scientificResearch, c_A1) ✓
%     ⟦c_R1⟧ = {scientificResearch}  (eq rule)
%     Witness: X = scientificResearch ✓ → COMPATIBLE
%
%   TRACE — SPATIAL PAIR (Def 3):
%     ⟦c_A2⟧ = {x | x ⊑ westernEurope}
%            = {westernEurope, france, germany, austria, paris}
%     ⟦c_R2⟧ = {france}  (eq rule)
%     Witness: Y = france ✓ → COMPATIBLE
%
%   TRACE — Def 6 (and-composition):
%     Both operands Compatible → Branch A verdict = COMPATIBLE
%
%   VALIDATES: Def 3 (isNoneOf + isPartOf + eq), Def 4 (⊓),
%              Def 5 (Compatible), Def 6 (and),
%              Paper key finding: one negative axiom resolves xone.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV004-0.ax').
include('Axioms/Layer0-DomainKB/GEO003-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').
% --- isNoneOf if-direction for c_A1 (per-problem) ---
fof(isNoneOf_if_cA1, axiom,
    ![X]: ((has_operand(c_A1, purpose) & has_operator(c_A1, isNoneOf)
            & has_value(c_A1, commercialPurpose) & taxonomic(purpose)
            & ~subClassOf(X, commercialPurpose))
        => in_denotation(X, c_A1))).
% --- Policy Branch A: purpose isNoneOf {commercialPurpose} ---
fof(cA1_constraint, axiom, has_constraint(branch_a, c_A1)).
fof(cA1_operand,    axiom, has_operand(c_A1, purpose)).
fof(cA1_operator,   axiom, has_operator(c_A1, isNoneOf)).
fof(cA1_value,      axiom, has_value(c_A1, commercialPurpose)).
% --- Policy Branch A: spatial isPartOf westernEurope ---
fof(cA2_constraint, axiom, has_constraint(branch_a, c_A2)).
fof(cA2_operand,    axiom, has_operand(c_A2, spatial)).
fof(cA2_operator,   axiom, has_operator(c_A2, isPartOf)).
fof(cA2_value,      axiom, has_value(c_A2, westernEurope)).
% --- Request: purpose eq scientificResearch ---
fof(cR1_constraint, axiom, has_constraint(request, c_R1)).
fof(cR1_operand,    axiom, has_operand(c_R1, purpose)).
fof(cR1_operator,   axiom, has_operator(c_R1, eq)).
fof(cR1_value,      axiom, has_value(c_R1, scientificResearch)).
% --- Request: spatial eq france ---
fof(cR2_constraint, axiom, has_constraint(request, c_R2)).
fof(cR2_operand,    axiom, has_operand(c_R2, spatial)).
fof(cR2_operator,   axiom, has_operator(c_R2, eq)).
fof(cR2_value,      axiom, has_value(c_R2, france)).
% --- Conjecture: Branch A AND (both operands overlap) ---
% Def 6 (and): both purpose and spatial must have witnesses.
fof(odrl211_branch_a_compatible, conjecture,
    (?[X]: (in_denotation(X, c_A1) & in_denotation(X, c_R1)))
    & (?[Y]: (in_denotation(Y, c_A2) & in_denotation(Y, c_R2)))).
%--------------------------------------------------------------------------
