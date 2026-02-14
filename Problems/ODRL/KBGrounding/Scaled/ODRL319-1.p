%--------------------------------------------------------------------------
% File     : ODRL319-1 : TPTP v9.0.0. Released v9.1.0.
% Domain   : Policy (ODRL)
% Problem  : AND-5 conflict
% Version  : [Mus26] axioms : Scaled.
% English  : Scaled benchmark with 15 concepts.
% Refs     : [Mus26] Mustafa, D. (2026), Grounding ODRL Constraints.
% Source   : [Mus26]
% Names    : ODRL319-1 [Mus26]
%
% Status   : Theorem
% Rating   : ? v9.1.0
% SPC      : FOF_THM_EPR
%
% Comments : Scaled benchmark. Category: Scaled/Comp
%--------------------------------------------------------------------------

fof(d0_a, axiom, concept_d0(d0_a)).
fof(d0_b, axiom, concept_d0(d0_b)).
fof(d0_root, axiom, concept_d0(d0_root)).
fof(d0_a_sub, axiom, sub_d0(d0_a, d0_root)).
fof(d0_b_sub, axiom, sub_d0(d0_b, d0_root)).
fof(d0_refl, axiom, ![X]: (concept_d0(X) => sub_d0(X, X))).
fof(d0_una_ab, axiom, d0_a != d0_b).
fof(d0_una_ar, axiom, d0_a != d0_root).
fof(d0_una_br, axiom, d0_b != d0_root).
fof(d0_nosub_ab, axiom, ~sub_d0(d0_a, d0_b)).
fof(d0_nosub_ba, axiom, ~sub_d0(d0_b, d0_a)).
fof(d1_a, axiom, concept_d1(d1_a)).
fof(d1_b, axiom, concept_d1(d1_b)).
fof(d1_root, axiom, concept_d1(d1_root)).
fof(d1_a_sub, axiom, sub_d1(d1_a, d1_root)).
fof(d1_b_sub, axiom, sub_d1(d1_b, d1_root)).
fof(d1_refl, axiom, ![X]: (concept_d1(X) => sub_d1(X, X))).
fof(d1_una_ab, axiom, d1_a != d1_b).
fof(d1_una_ar, axiom, d1_a != d1_root).
fof(d1_una_br, axiom, d1_b != d1_root).
fof(d1_nosub_ab, axiom, ~sub_d1(d1_a, d1_b)).
fof(d1_nosub_ba, axiom, ~sub_d1(d1_b, d1_a)).
fof(d2_a, axiom, concept_d2(d2_a)).
fof(d2_b, axiom, concept_d2(d2_b)).
fof(d2_root, axiom, concept_d2(d2_root)).
fof(d2_a_sub, axiom, sub_d2(d2_a, d2_root)).
fof(d2_b_sub, axiom, sub_d2(d2_b, d2_root)).
fof(d2_refl, axiom, ![X]: (concept_d2(X) => sub_d2(X, X))).
fof(d2_una_ab, axiom, d2_a != d2_b).
fof(d2_una_ar, axiom, d2_a != d2_root).
fof(d2_una_br, axiom, d2_b != d2_root).
fof(d2_nosub_ab, axiom, ~sub_d2(d2_a, d2_b)).
fof(d2_nosub_ba, axiom, ~sub_d2(d2_b, d2_a)).
fof(d3_a, axiom, concept_d3(d3_a)).
fof(d3_b, axiom, concept_d3(d3_b)).
fof(d3_root, axiom, concept_d3(d3_root)).
fof(d3_a_sub, axiom, sub_d3(d3_a, d3_root)).
fof(d3_b_sub, axiom, sub_d3(d3_b, d3_root)).
fof(d3_refl, axiom, ![X]: (concept_d3(X) => sub_d3(X, X))).
fof(d3_una_ab, axiom, d3_a != d3_b).
fof(d3_una_ar, axiom, d3_a != d3_root).
fof(d3_una_br, axiom, d3_b != d3_root).
fof(d3_nosub_ab, axiom, ~sub_d3(d3_a, d3_b)).
fof(d3_nosub_ba, axiom, ~sub_d3(d3_b, d3_a)).
fof(d4_a, axiom, concept_d4(d4_a)).
fof(d4_b, axiom, concept_d4(d4_b)).
fof(d4_root, axiom, concept_d4(d4_root)).
fof(d4_a_sub, axiom, sub_d4(d4_a, d4_root)).
fof(d4_b_sub, axiom, sub_d4(d4_b, d4_root)).
fof(d4_refl, axiom, ![X]: (concept_d4(X) => sub_d4(X, X))).
fof(d4_una_ab, axiom, d4_a != d4_b).
fof(d4_una_ar, axiom, d4_a != d4_root).
fof(d4_una_br, axiom, d4_b != d4_root).
fof(d4_nosub_ab, axiom, ~sub_d4(d4_a, d4_b)).
fof(d4_nosub_ba, axiom, ~sub_d4(d4_b, d4_a)).
fof(conjecture, conjecture, ~(?[X0]: (sub_d0(X0, d0_root)) & ?[X1]: (sub_d1(X1, d1_root)) & ?[X2]: (sub_d2(X2, d2_root)) & ?[X3]: (sub_d3(X3, d3_root)) & ?[X4]: (X4 = d4_a & X4 = d4_b))).
