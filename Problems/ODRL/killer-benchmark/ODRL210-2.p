%--------------------------------------------------------------------------
% File     : ODRL210-2.p : TPTP v0.2.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Xone Branch A purpose: negated conjecture (conflict check)
%            Base DPV → also CounterSatisfiable (confirms genuine Unknown)
% Version  : DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : CounterSatisfiable
% Source   : Mustafa & Sutcliffe, 2026
%
% Notes    : Paired check for ODRL210-1.p.
%            ODRL210-1.p tests: ∃X(in_den(X,c_A1) ∧ in_den(X,c_R1))
%            This file tests: ¬∃X(in_den(X,c_A1) ∧ in_den(X,c_R1))
%
%            BOTH return CounterSatisfiable → verdict is genuinely Unknown
%            (neither Compatible nor Conflict is provable).
%
%            If only ODRL210-1.p were CounterSat and this were Theorem,
%            the verdict would be Conflict. But the absence of
%            ¬(sciRes ⊑ commercial) means neither direction is provable.
%
%   VALIDATES: Def 5 (three-valued Unknown), Table 3 (verdict encoding)
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').
% --- isNoneOf if-direction (per-problem, same as ODRL210-1.p) ---
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
% --- Conjecture: NEGATED — no overlap (conflict check) ---
fof(odrl210_branch_a_purpose_conflict, conjecture,
    ~?[X]: (in_denotation(X, c_A1) & in_denotation(X, c_R1))).
%--------------------------------------------------------------------------
