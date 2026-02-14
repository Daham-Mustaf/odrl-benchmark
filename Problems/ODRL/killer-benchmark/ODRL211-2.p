%--------------------------------------------------------------------------
% File     : ODRL211-2.p : TPTP v0.2.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Xone Branch B spatial: eq germany vs eq france → Conflict
% Version  : GEO003-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : Theorem
% Source   : Mustafa & Sutcliffe, 2026
%
% Notes    : Tests Branch B spatial pair in the killer benchmark.
%
%   Branch B spatial: (spatial, eq, germany)
%   Request spatial:  (spatial, eq, france)
%
%   TRACE (Def 3):
%     ⟦c_B2⟧ = {germany}  (eq rule)
%     ⟦c_R2⟧ = {france}   (eq rule)
%
%     Intersection: {germany} ∩ {france} = ∅
%     Only-if (denotation_eq_only): if in_den(X,c_B2) then X = germany
%                                   if in_den(X,c_R2) then X = france
%     Therefore: X = germany AND X = france → germany = france
%     But UNA: germany ≠ france → contradiction → Theorem
%
%   The negated conjecture proves no witness exists → CONFLICT ✓
%   This spatial conflict kills Branch B regardless of purpose.
%
%   VALIDATES: Def 3 (eq bidirectional), Def 5 (Conflict),
%              Def 6 (and — one Conflict blocks branch)
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO003-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').
% --- Policy Branch B: spatial eq germany ---
fof(cB2_constraint, axiom, has_constraint(branch_b, c_B2)).
fof(cB2_operand,    axiom, has_operand(c_B2, spatial)).
fof(cB2_operator,   axiom, has_operator(c_B2, eq)).
fof(cB2_value,      axiom, has_value(c_B2, germany)).
% --- Request: spatial eq france ---
fof(cR2_constraint, axiom, has_constraint(request, c_R2)).
fof(cR2_operand,    axiom, has_operand(c_R2, spatial)).
fof(cR2_operator,   axiom, has_operator(c_R2, eq)).
fof(cR2_value,      axiom, has_value(c_R2, france)).
% --- Conjecture: no spatial witness (proves Conflict) ---
fof(odrl211_branch_b_spatial_conflict, conjecture,
    ~?[X]: (in_denotation(X, c_B2) & in_denotation(X, c_R2))).
%--------------------------------------------------------------------------
