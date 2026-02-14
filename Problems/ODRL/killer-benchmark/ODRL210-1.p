%--------------------------------------------------------------------------
% File     : ODRL210-1.p : TPTP v0.2.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Xone Branch A purpose: isNoneOf{commercial} vs eq scientificRes
%            Base DPV (no ¬(sciRes ⊑ commercial)) → Unknown
% Version  : DPV000-0.ax, GEO003-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : CounterSatisfiable
% Source   : Mustafa & Sutcliffe, 2026
%
% Notes    : Part 1 of the killer benchmark (BSB ↔ French Archive).
%
%   BSB POLICY (xone):
%     Branch A: purpose isNoneOf {commercial} AND spatial isPartOf westernEurope
%     Branch B: purpose isA commercial      AND spatial eq germany
%
%   FRENCH REQUEST:
%     purpose eq scientificResearch AND spatial eq france
%
%   This file tests BRANCH A PURPOSE PAIR ONLY:
%     c_A1 = (purpose, isNoneOf, {commercialPurpose})
%     c_R1 = (purpose, eq, scientificResearch)
%
%   TRACE (Def 3):
%     ⟦c_A1⟧ = C \ {x | x ⊑ commercial}
%             = C \ {commercial, commRes, advertising}
%             = {purpose, nonComm, R&D, nonCommRes, sciRes, acadRes, directMkt}
%
%     ⟦c_R1⟧ = {scientificResearch}
%
%     Intersection: {sciRes} if sciRes ∈ ⟦c_A1⟧
%
%   WHY UNKNOWN:
%     The if-direction for isNoneOf is per-problem (Paper §2.2).
%     To populate ⟦isNoneOf {commercial}⟧ with sciRes, we need:
%       ¬subClassOf(scientificResearch, commercialPurpose)
%     This axiom is ABSENT in DPV000-0.ax.
%     Without it, Vampire cannot populate the denotation → CounterSatisfiable.
%
%   VALIDATES: Def 3 (isNoneOf), Def 5 (Unknown verdict),
%              Paper key finding: xone requires negative axioms.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').
% --- isNoneOf if-direction (per-problem grounded enumeration) ---
% For c_A1 = (purpose, isNoneOf, {commercialPurpose}):
% in_denotation(X, c_A1) if ¬subClassOf(X, commercialPurpose)
% This is the per-problem if-direction for isNoneOf (Paper §2.2).
fof(isNoneOf_if_cA1, axiom,
    ![X]: ((has_operand(c_A1, purpose) & has_operator(c_A1, isNoneOf)
            & has_value(c_A1, commercialPurpose) & taxonomic(purpose)
            & ~subClassOf(X, commercialPurpose))
        => in_denotation(X, c_A1))).
% --- Policy Branch A: purpose isNoneOf {commercialPurpose} ---
fof(policy_branch_a_purpose, axiom, has_constraint(branch_a, c_A1)).
fof(cA1_operand,  axiom, has_operand(c_A1, purpose)).
fof(cA1_operator, axiom, has_operator(c_A1, isNoneOf)).
fof(cA1_value,    axiom, has_value(c_A1, commercialPurpose)).
% --- Request: purpose eq scientificResearch ---
fof(request_purpose, axiom, has_constraint(request, c_R1)).
fof(cR1_operand,  axiom, has_operand(c_R1, purpose)).
fof(cR1_operator, axiom, has_operator(c_R1, eq)).
fof(cR1_value,    axiom, has_value(c_R1, scientificResearch)).
% --- Conjecture: Branch A purpose pair overlaps ---
% If Theorem → Compatible. If CounterSatisfiable → Unknown (or Conflict).
fof(odrl210_branch_a_purpose, conjecture,
    ?[X]: (in_denotation(X, c_A1) & in_denotation(X, c_R1))).
%--------------------------------------------------------------------------
