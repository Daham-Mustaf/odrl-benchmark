%--------------------------------------------------------------------------
% File     : ODRL212-2.p : TPTP v0.2.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Minimal killer negated: confirms genuine Unknown
% Version  : MINI001-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : CounterSatisfiable
% Source   : Mustafa & Sutcliffe, 2026
%
% Notes    : Paired check for ODRL212-1.p.
%            ODRL212-1.p: ∃X(in_den(X,c1_al) ∧ in_den(X,c2_al)) → CtrSat
%            This file:   ¬∃X(in_den(X,c1_al) ∧ in_den(X,c2_al)) → CtrSat
%
%            BOTH CounterSatisfiable → genuine Unknown.
%            (Neither Compatible nor Conflict is provable.)
%
%            If the old Def 8 were implemented (applying α pointwise
%            without checking ⟦c⟧ ⊆ dom(α)), the isNoneOf denotations
%            would be:
%              ⟦isNoneOf{a'}⟧ = {b'}  (only non-a' in KB_B)
%              ⟦isNoneOf{b'}⟧ = {a'}  (only non-b' in KB_B)
%              Intersection = ∅ → THIS file would be Theorem (Conflict)
%            That Theorem would be a FALSE CONFLICT: KB_A has d as witness,
%            but d was lost in alignment. The strengthened Def 8
%            detects ⟦c⟧ ⊄ dom(α) and returns ⊤ instead.
%
%   VALIDATES: Def 5 (three-valued Unknown), Def 8 (strengthened),
%              Prop 1.2 (Compatible → Unknown, never false Conflict).
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/MINI001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').
% --- isNoneOf if-direction for c1_aligned (same as 212-1) ---
fof(isNoneOf_if_c1al, axiom,
    ![X]: ((has_operand(c1_al, ell) & has_operator(c1_al, isNoneOf)
            & has_value(c1_al, aPrime) & taxonomic(ell)
            & ~subClassOf(X, aPrime))
        => in_denotation(X, c1_al))).
fof(isNoneOf_if_c2al, axiom,
    ![X]: ((has_operand(c2_al, ell) & has_operator(c2_al, isNoneOf)
            & has_value(c2_al, bPrime) & taxonomic(ell)
            & ~subClassOf(X, bPrime))
        => in_denotation(X, c2_al))).
% --- Aligned constraints (same as 212-1) ---
fof(c1al_constraint, axiom, has_constraint(policy_al, c1_al)).
fof(c1al_operand,    axiom, has_operand(c1_al, ell)).
fof(c1al_operator,   axiom, has_operator(c1_al, isNoneOf)).
fof(c1al_value,      axiom, has_value(c1_al, aPrime)).
fof(c2al_constraint, axiom, has_constraint(policy_al, c2_al)).
fof(c2al_operand,    axiom, has_operand(c2_al, ell)).
fof(c2al_operator,   axiom, has_operator(c2_al, isNoneOf)).
fof(c2al_value,      axiom, has_value(c2_al, bPrime)).
% --- Conjecture: NEGATED — conflict check ---
fof(odrl212_minimal_killer_conflict, conjecture,
    ~?[X]: (in_denotation(X, c1_al) & in_denotation(X, c2_al))).
%--------------------------------------------------------------------------
