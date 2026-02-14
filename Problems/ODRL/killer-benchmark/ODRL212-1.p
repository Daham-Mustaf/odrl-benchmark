%--------------------------------------------------------------------------
% File     : ODRL212-1.p : TPTP v0.2.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Minimal killer: old Def 8 fabricates false Conflict
% Version  : MINI000-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : CounterSatisfiable
% Source   : Mustafa & Sutcliffe, 2026
%
% Notes    : MINIMAL SCENARIO EXPOSING OLD DEF 8 BUG.
%
%   KB_A = {root, a, b, d}
%     Taxonomy: root > a, root > b, root > d
%     All siblings pairwise disjoint.
%
%   KB_B = {a', b'}   (root, d UNMAPPED)
%   Alignment α: a ↦ a', b ↦ b', root ↦ ⊥, d ↦ ⊥
%
%   CONSTRAINTS (both on same operand ℓ):
%     c₁ = (ℓ, isNoneOf, {a})  →  ⟦c₁⟧_A = {root, b, d}
%     c₂ = (ℓ, isNoneOf, {b})  →  ⟦c₂⟧_A = {root, a, d}
%
%   REQUEST (implicit via eq):
%     r₁ = (ℓ, eq, d)          →  ⟦r₁⟧_A = {d}
%
%   IN KB_A:
%     ⟦c₁⟧_A ∩ ⟦r₁⟧_A = {d}  → Compatible
%
%   OLD DEF 8 (BUGGY):
%     α(a) ≠ ⊥  → apply α pointwise:
%       ⟦α(c₁)⟧_B = {b'}  (everyone except a' = just b')
%       ⟦α(c₂)⟧_B = {a'}  (everyone except b' = just a')
%       ⟦α(r₁)⟧_B = α(d) = ⊥  (d unmapped)
%     ⟦α(c₁)⟧_B ∩ ⟦α(c₂)⟧_B = {b'} ∩ {a'} = ∅
%     → 💥 FALSE CONFLICT (d was a valid witness but got lost)
%
%   NEW DEF 8 (STRENGTHENED):
%     ⟦c₁⟧_A = {root, b, d} ⊄ dom(α) = {a, b}
%       (root, d ∉ dom(α))  →  α̂(c₁) = ⊤
%     ⟦c₂⟧_A = {root, a, d} ⊄ dom(α) = {a, b}
%       (root, d ∉ dom(α))  →  α̂(c₂) = ⊤
%     ⊤ ⊓ ⊤ = ⊤  →  UNKNOWN  ✓
%
%   VALIDATES: Def 8 (strengthened), Prop 1.2 (graceful degradation),
%              Thm 1 (soundness — no false Conflict).
%
%   ENCODING:
%     This file tests ∃X(in_den(X,c1) ∧ in_den(X,r1)) under KB_B.
%     KB_B is too impoverished to prove or refute → CounterSatisfiable.
%     The companion ODRL212-2.p checks that ¬∃X is also CounterSat
%     (genuine Unknown, not Conflict).
%
%     We use KB_B directly (MINI001-0.ax) with only {a', b'},
%     and the aligned constraints. If the prover returns Theorem,
%     the old Def 8 bug is present.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/MINI001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').
% --- isNoneOf if-direction for c1_aligned (per-problem) ---
% α(c₁) = (ℓ, isNoneOf, {a'})  in KB_B
% in_denotation(X, c1_al) if ¬subClassOf(X, aPrime)
fof(isNoneOf_if_c1al, axiom,
    ![X]: ((has_operand(c1_al, ell) & has_operator(c1_al, isNoneOf)
            & has_value(c1_al, aPrime) & taxonomic(ell)
            & ~subClassOf(X, aPrime))
        => in_denotation(X, c1_al))).
% --- isNoneOf if-direction for c2_aligned ---
% α(c₂) = (ℓ, isNoneOf, {b'})  in KB_B
fof(isNoneOf_if_c2al, axiom,
    ![X]: ((has_operand(c2_al, ell) & has_operator(c2_al, isNoneOf)
            & has_value(c2_al, bPrime) & taxonomic(ell)
            & ~subClassOf(X, bPrime))
        => in_denotation(X, c2_al))).
% --- Aligned constraint c1: isNoneOf {a'} ---
fof(c1al_constraint, axiom, has_constraint(policy_al, c1_al)).
fof(c1al_operand,    axiom, has_operand(c1_al, ell)).
fof(c1al_operator,   axiom, has_operator(c1_al, isNoneOf)).
fof(c1al_value,      axiom, has_value(c1_al, aPrime)).
% --- Aligned constraint c2: isNoneOf {b'} ---
fof(c2al_constraint, axiom, has_constraint(policy_al, c2_al)).
fof(c2al_operand,    axiom, has_operand(c2_al, ell)).
fof(c2al_operator,   axiom, has_operator(c2_al, isNoneOf)).
fof(c2al_value,      axiom, has_value(c2_al, bPrime)).
% --- Request aligned: eq α(d) = ⊥ → no aligned request ---
% Since d is unmapped, there is no valid aligned request constraint.
% Under new Def 8: ⟦c₁⟧ ⊄ dom(α) → ⊤ already.
% Under old Def 8: this tests the intersection ⟦α(c₁)⟧ ∩ ⟦α(c₂)⟧
%
% We test: can we find X in BOTH aligned denotations?
fof(odrl212_minimal_killer, conjecture,
    ?[X]: (in_denotation(X, c1_al) & in_denotation(X, c2_al))).
%--------------------------------------------------------------------------
