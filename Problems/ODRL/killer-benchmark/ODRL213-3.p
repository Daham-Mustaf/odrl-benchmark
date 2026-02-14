%--------------------------------------------------------------------------
% File     : ODRL213-3.p : TPTP v0.2.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-KB Branch B spatial: Conflict preserved (eq germany ≠ eq france)
% Version  : ISO3166-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : Theorem
% Source   : Mustafa & Sutcliffe, 2026
%
% Notes    : Tests Prop 1.1 (Conflict Preservation) through alignment.
%
%   ORIGINAL (in KB_A = GEO003):
%     c_B2 = (spatial, eq, germany)
%     c_R2 = (spatial, eq, france)
%     germany ≠ france → Conflict ✓
%
%   ALIGNED TO KB_B (ISO3166):
%     α(germany) = germany, α(france) = france  (identity mapping)
%     Both values fully mapped, ⟦c_B2⟧ = {germany} ⊆ dom(α)
%     → Def 8 applies normally (no ⊤)
%     → same conflict test in KB_B
%     germany ≠ france [una_fr_de in ISO3166] → Conflict preserved ✓
%
%   TRACE:
%     eq only-if: in_den(X, c_B2) → X = germany
%     eq only-if: in_den(X, c_R2) → X = france
%     X = germany ∧ X = france → germany = france
%     UNA: germany ≠ france → ⊥ → negated conjecture proved
%
%   VALIDATES: Def 3 (eq bidirectional), Prop 1.1 (Conflict preservation),
%              Thm 1 (soundness — aligned Conflict is genuine).
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').
% --- Branch B: spatial eq germany ---
fof(cB2_constraint, axiom, has_constraint(branch_b, c_B2)).
fof(cB2_operand,    axiom, has_operand(c_B2, spatial)).
fof(cB2_operator,   axiom, has_operator(c_B2, eq)).
fof(cB2_value,      axiom, has_value(c_B2, germany)).
% --- Request: spatial eq france ---
fof(cR2_constraint, axiom, has_constraint(request, c_R2)).
fof(cR2_operand,    axiom, has_operand(c_R2, spatial)).
fof(cR2_operator,   axiom, has_operator(c_R2, eq)).
fof(cR2_value,      axiom, has_value(c_R2, france)).
% --- Conjecture: no overlap (proves Conflict) ---
fof(odrl213_cross_branchb_conflict, conjecture,
    ~?[X]: (in_denotation(X, c_B2) & in_denotation(X, c_R2))).
%--------------------------------------------------------------------------
