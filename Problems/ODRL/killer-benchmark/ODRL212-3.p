%--------------------------------------------------------------------------
% File     : ODRL212-3.p : TPTP v0.2.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Minimal killer in KB_A: d is witness → Compatible
% Version  : MINI000-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : Theorem
% Source   : Mustafa & Sutcliffe, 2026
%
% Notes    : Proves COMPATIBILITY in the full KB_A (source dataspace).
%            This is the baseline: d satisfies isNoneOf{a} ∧ isNoneOf{b}.
%
%   KB_A = {root, a, b, d}   (all siblings disjoint)
%
%   c₁ = (ℓ, isNoneOf, {a})  →  ⟦c₁⟧ = {root, b, d}
%   c₂ = (ℓ, isNoneOf, {b})  →  ⟦c₂⟧ = {root, a, d}
%
%   TRACE:
%     For X = d:
%       isNoneOf_if_c1: ~subClassOf(d, a) ✓ [mini_d_not_a]
%         → in_denotation(d, c1) ✓
%       isNoneOf_if_c2: ~subClassOf(d, b) ✓ [mini_d_not_b]
%         → in_denotation(d, c2) ✓
%     Witness: X = d ✓ → COMPATIBLE
%
%     (root is also a witness: ~subClassOf(root,a) ∧ ~subClassOf(root,b))
%
%   Compared to ODRL212-1.p (KB_B): d is unmapped so the Compatible
%   verdict degrades to Unknown. This file confirms the ground truth.
%
%   VALIDATES: Def 3 (isNoneOf), Def 4 (∩), Def 5 (Compatible),
%              Prop 1.2 baseline (Compatible in source KB).
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/MINI000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').
% --- isNoneOf if-direction for c1 (per-problem) ---
fof(isNoneOf_if_c1, axiom,
    ![X]: ((has_operand(c1, ell) & has_operator(c1, isNoneOf)
            & has_value(c1, a) & taxonomic(ell)
            & ~subClassOf(X, a))
        => in_denotation(X, c1))).
% --- isNoneOf if-direction for c2 (per-problem) ---
fof(isNoneOf_if_c2, axiom,
    ![X]: ((has_operand(c2, ell) & has_operator(c2, isNoneOf)
            & has_value(c2, b) & taxonomic(ell)
            & ~subClassOf(X, b))
        => in_denotation(X, c2))).
% --- Constraint c1: isNoneOf {a} ---
fof(c1_constraint, axiom, has_constraint(policy, c1)).
fof(c1_operand,    axiom, has_operand(c1, ell)).
fof(c1_operator,   axiom, has_operator(c1, isNoneOf)).
fof(c1_value,      axiom, has_value(c1, a)).
% --- Constraint c2: isNoneOf {b} ---
fof(c2_constraint, axiom, has_constraint(policy, c2)).
fof(c2_operand,    axiom, has_operand(c2, ell)).
fof(c2_operator,   axiom, has_operator(c2, isNoneOf)).
fof(c2_value,      axiom, has_value(c2, b)).
% --- Conjecture: witness exists in both denotations ---
fof(odrl212_kba_compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
