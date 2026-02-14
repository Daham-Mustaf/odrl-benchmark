%--------------------------------------------------------------------------
% File     : ODRL321-1 : TPTP v9.0.0. Released v9.1.0.
% Domain   : Policy (ODRL)
% Problem  : AND-10 conflict
% Version  : [Mus26] axioms : Scaled.
% English  : Scaled benchmark with 30 concepts.
% Refs     : [Mus26] Mustafa, D. (2026), Grounding ODRL Constraints.
% Source   : [Mus26]
% Names    : ODRL321-1 [Mus26]
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
fof(d5_a, axiom, concept_d5(d5_a)).
fof(d5_b, axiom, concept_d5(d5_b)).
fof(d5_root, axiom, concept_d5(d5_root)).
fof(d5_a_sub, axiom, sub_d5(d5_a, d5_root)).
fof(d5_b_sub, axiom, sub_d5(d5_b, d5_root)).
fof(d5_refl, axiom, ![X]: (concept_d5(X) => sub_d5(X, X))).
fof(d5_una_ab, axiom, d5_a != d5_b).
fof(d5_una_ar, axiom, d5_a != d5_root).
fof(d5_una_br, axiom, d5_b != d5_root).
fof(d5_nosub_ab, axiom, ~sub_d5(d5_a, d5_b)).
fof(d5_nosub_ba, axiom, ~sub_d5(d5_b, d5_a)).
fof(d6_a, axiom, concept_d6(d6_a)).
fof(d6_b, axiom, concept_d6(d6_b)).
fof(d6_root, axiom, concept_d6(d6_root)).
fof(d6_a_sub, axiom, sub_d6(d6_a, d6_root)).
fof(d6_b_sub, axiom, sub_d6(d6_b, d6_root)).
fof(d6_refl, axiom, ![X]: (concept_d6(X) => sub_d6(X, X))).
fof(d6_una_ab, axiom, d6_a != d6_b).
fof(d6_una_ar, axiom, d6_a != d6_root).
fof(d6_una_br, axiom, d6_b != d6_root).
fof(d6_nosub_ab, axiom, ~sub_d6(d6_a, d6_b)).
fof(d6_nosub_ba, axiom, ~sub_d6(d6_b, d6_a)).
fof(d7_a, axiom, concept_d7(d7_a)).
fof(d7_b, axiom, concept_d7(d7_b)).
fof(d7_root, axiom, concept_d7(d7_root)).
fof(d7_a_sub, axiom, sub_d7(d7_a, d7_root)).
fof(d7_b_sub, axiom, sub_d7(d7_b, d7_root)).
fof(d7_refl, axiom, ![X]: (concept_d7(X) => sub_d7(X, X))).
fof(d7_una_ab, axiom, d7_a != d7_b).
fof(d7_una_ar, axiom, d7_a != d7_root).
fof(d7_una_br, axiom, d7_b != d7_root).
fof(d7_nosub_ab, axiom, ~sub_d7(d7_a, d7_b)).
fof(d7_nosub_ba, axiom, ~sub_d7(d7_b, d7_a)).
fof(d8_a, axiom, concept_d8(d8_a)).
fof(d8_b, axiom, concept_d8(d8_b)).
fof(d8_root, axiom, concept_d8(d8_root)).
fof(d8_a_sub, axiom, sub_d8(d8_a, d8_root)).
fof(d8_b_sub, axiom, sub_d8(d8_b, d8_root)).
fof(d8_refl, axiom, ![X]: (concept_d8(X) => sub_d8(X, X))).
fof(d8_una_ab, axiom, d8_a != d8_b).
fof(d8_una_ar, axiom, d8_a != d8_root).
fof(d8_una_br, axiom, d8_b != d8_root).
fof(d8_nosub_ab, axiom, ~sub_d8(d8_a, d8_b)).
fof(d8_nosub_ba, axiom, ~sub_d8(d8_b, d8_a)).
fof(d9_a, axiom, concept_d9(d9_a)).
fof(d9_b, axiom, concept_d9(d9_b)).
fof(d9_root, axiom, concept_d9(d9_root)).
fof(d9_a_sub, axiom, sub_d9(d9_a, d9_root)).
fof(d9_b_sub, axiom, sub_d9(d9_b, d9_root)).
fof(d9_refl, axiom, ![X]: (concept_d9(X) => sub_d9(X, X))).
fof(d9_una_ab, axiom, d9_a != d9_b).
fof(d9_una_ar, axiom, d9_a != d9_root).
fof(d9_una_br, axiom, d9_b != d9_root).
fof(d9_nosub_ab, axiom, ~sub_d9(d9_a, d9_b)).
fof(d9_nosub_ba, axiom, ~sub_d9(d9_b, d9_a)).
fof(conjecture, conjecture, ~(?[X0]: (sub_d0(X0, d0_root)) & ?[X1]: (sub_d1(X1, d1_root)) & ?[X2]: (sub_d2(X2, d2_root)) & ?[X3]: (sub_d3(X3, d3_root)) & ?[X4]: (sub_d4(X4, d4_root)) & ?[X5]: (sub_d5(X5, d5_root)) & ?[X6]: (sub_d6(X6, d6_root)) & ?[X7]: (sub_d7(X7, d7_root)) & ?[X8]: (sub_d8(X8, d8_root)) & ?[X9]: (X9 = d9_a & X9 = d9_b))).
