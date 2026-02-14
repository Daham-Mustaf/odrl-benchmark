%--------------------------------------------------------------------------
% File     : ODRL213-1.p : TPTP v0.2.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-KB spatial: isPartOf westernEurope → Unknown in ISO3166
% Version  : ISO3166-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : CounterSatisfiable
% Source   : Mustafa & Sutcliffe, 2026
%
% Notes    : Tests Def 8 (strengthened) on spatial alignment.
%
%   ORIGINAL (in KB_A = GEO003):
%     c_A2 = (spatial, isPartOf, westernEurope)
%     c_R2 = (spatial, eq, france)
%     ⟦c_A2⟧ = {westernEurope, france, germany, austria, paris}
%     ⟦c_R2⟧ = {france}
%     Intersection = {france} → Compatible ✓
%
%   ALIGNED TO KB_B (ISO3166):
%     α(westernEurope) = ⊥  (absent from ISO 3166)
%
%   NEW DEF 8:
%     ⟦c_A2⟧_A contains westernEurope ∉ dom(α)
%     → ⟦c_A2⟧ ⊄ dom(α) → α̂(c_A2) = ⊤ → UNKNOWN
%
%   This problem encodes the aligned scenario directly in KB_B.
%   Since the constraint VALUE westernEurope doesn't exist in ISO3166,
%   the isPartOf denotation rule can't fire → no witness → CounterSat.
%   But also no proof of emptiness → genuine Unknown (both directions fail).
%
%   The problem uses 'westernEurope' as a constant not present in ISO3166.
%   No partOf(X, westernEurope) axioms exist → denotation_isPartOf can't fire.
%   No negative partOf(X, westernEurope) axioms exist → denotation_isPartOf
%   only-if can't refute either.
%
%   VALIDATES: Def 7 (alignment), Def 8 (unmapped value → ⊤),
%              Prop 1.2 (Compatible → Unknown).
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').
% --- Branch A spatial: isPartOf westernEurope (value from KB_A) ---
% The value westernEurope is foreign to KB_B (ISO3166).
fof(cA2_constraint, axiom, has_constraint(branch_a, c_A2)).
fof(cA2_operand,    axiom, has_operand(c_A2, spatial)).
fof(cA2_operator,   axiom, has_operator(c_A2, isPartOf)).
fof(cA2_value,      axiom, has_value(c_A2, westernEurope)).
% --- Request spatial: eq france ---
fof(cR2_constraint, axiom, has_constraint(request, c_R2)).
fof(cR2_operand,    axiom, has_operand(c_R2, spatial)).
fof(cR2_operator,   axiom, has_operator(c_R2, eq)).
fof(cR2_value,      axiom, has_value(c_R2, france)).
% --- Conjecture: overlap (compatibility test) ---
fof(odrl213_cross_spatial_compat, conjecture,
    ?[X]: (in_denotation(X, c_A2) & in_denotation(X, c_R2))).
%--------------------------------------------------------------------------
