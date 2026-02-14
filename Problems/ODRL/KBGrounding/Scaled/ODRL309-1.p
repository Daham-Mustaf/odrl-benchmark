%--------------------------------------------------------------------------
% File     : ODRL309-1 : TPTP v9.0.0. Released v9.1.0.
% Domain   : Policy (ODRL)
% Problem  : Chain-20 conflict
% Version  : [Mus26] axioms : Scaled.
% English  : Scaled benchmark with 20 concepts.
% Refs     : [Mus26] Mustafa, D. (2026), Grounding ODRL Constraints.
% Source   : [Mus26]
% Names    : ODRL309-1 [Mus26]
%
% Status   : Theorem
% Rating   : ? v9.1.0
% SPC      : FOF_THM_EPR
%
% Comments : Scaled benchmark. Category: Scaled/Deep
%--------------------------------------------------------------------------

fof(c0_concept, axiom, concept(c0)).
fof(c1_concept, axiom, concept(c1)).
fof(c2_concept, axiom, concept(c2)).
fof(c3_concept, axiom, concept(c3)).
fof(c4_concept, axiom, concept(c4)).
fof(c5_concept, axiom, concept(c5)).
fof(c6_concept, axiom, concept(c6)).
fof(c7_concept, axiom, concept(c7)).
fof(c8_concept, axiom, concept(c8)).
fof(c9_concept, axiom, concept(c9)).
fof(c10_concept, axiom, concept(c10)).
fof(c11_concept, axiom, concept(c11)).
fof(c12_concept, axiom, concept(c12)).
fof(c13_concept, axiom, concept(c13)).
fof(c14_concept, axiom, concept(c14)).
fof(c15_concept, axiom, concept(c15)).
fof(c16_concept, axiom, concept(c16)).
fof(c17_concept, axiom, concept(c17)).
fof(c18_concept, axiom, concept(c18)).
fof(c19_concept, axiom, concept(c19)).
fof(chain_0, axiom, subclass(c0, c1)).
fof(chain_1, axiom, subclass(c1, c2)).
fof(chain_2, axiom, subclass(c2, c3)).
fof(chain_3, axiom, subclass(c3, c4)).
fof(chain_4, axiom, subclass(c4, c5)).
fof(chain_5, axiom, subclass(c5, c6)).
fof(chain_6, axiom, subclass(c6, c7)).
fof(chain_7, axiom, subclass(c7, c8)).
fof(chain_8, axiom, subclass(c8, c9)).
fof(chain_9, axiom, subclass(c9, c10)).
fof(chain_10, axiom, subclass(c10, c11)).
fof(chain_11, axiom, subclass(c11, c12)).
fof(chain_12, axiom, subclass(c12, c13)).
fof(chain_13, axiom, subclass(c13, c14)).
fof(chain_14, axiom, subclass(c14, c15)).
fof(chain_15, axiom, subclass(c15, c16)).
fof(chain_16, axiom, subclass(c16, c17)).
fof(chain_17, axiom, subclass(c17, c18)).
fof(chain_18, axiom, subclass(c18, c19)).
fof(refl, axiom, ![X]: (concept(X) => subclass(X, X))).
fof(trans, axiom, ![X,Y,Z]: ((subclass(X,Y) & subclass(Y,Z)) => subclass(X,Z))).
fof(una_c0_c1, axiom, c0 != c1).
fof(una_c0_c2, axiom, c0 != c2).
fof(una_c0_c3, axiom, c0 != c3).
fof(una_c0_c4, axiom, c0 != c4).
fof(una_c0_c5, axiom, c0 != c5).
fof(una_c0_c6, axiom, c0 != c6).
fof(una_c0_c7, axiom, c0 != c7).
fof(una_c0_c8, axiom, c0 != c8).
fof(una_c0_c9, axiom, c0 != c9).
fof(una_c0_c10, axiom, c0 != c10).
fof(una_c0_c11, axiom, c0 != c11).
fof(una_c0_c12, axiom, c0 != c12).
fof(una_c0_c13, axiom, c0 != c13).
fof(una_c0_c14, axiom, c0 != c14).
fof(una_c0_c15, axiom, c0 != c15).
fof(una_c0_c16, axiom, c0 != c16).
fof(una_c0_c17, axiom, c0 != c17).
fof(una_c0_c18, axiom, c0 != c18).
fof(una_c0_c19, axiom, c0 != c19).
fof(una_c1_c2, axiom, c1 != c2).
fof(una_c1_c3, axiom, c1 != c3).
fof(una_c1_c4, axiom, c1 != c4).
fof(una_c1_c5, axiom, c1 != c5).
fof(una_c1_c6, axiom, c1 != c6).
fof(una_c1_c7, axiom, c1 != c7).
fof(una_c1_c8, axiom, c1 != c8).
fof(una_c1_c9, axiom, c1 != c9).
fof(una_c1_c10, axiom, c1 != c10).
fof(una_c1_c11, axiom, c1 != c11).
fof(una_c1_c12, axiom, c1 != c12).
fof(una_c1_c13, axiom, c1 != c13).
fof(una_c1_c14, axiom, c1 != c14).
fof(una_c1_c15, axiom, c1 != c15).
fof(una_c1_c16, axiom, c1 != c16).
fof(una_c1_c17, axiom, c1 != c17).
fof(una_c1_c18, axiom, c1 != c18).
fof(una_c1_c19, axiom, c1 != c19).
fof(una_c2_c3, axiom, c2 != c3).
fof(una_c2_c4, axiom, c2 != c4).
fof(una_c2_c5, axiom, c2 != c5).
fof(una_c2_c6, axiom, c2 != c6).
fof(una_c2_c7, axiom, c2 != c7).
fof(una_c2_c8, axiom, c2 != c8).
fof(una_c2_c9, axiom, c2 != c9).
fof(una_c2_c10, axiom, c2 != c10).
fof(una_c2_c11, axiom, c2 != c11).
fof(una_c2_c12, axiom, c2 != c12).
fof(una_c2_c13, axiom, c2 != c13).
fof(una_c2_c14, axiom, c2 != c14).
fof(una_c2_c15, axiom, c2 != c15).
fof(una_c2_c16, axiom, c2 != c16).
fof(una_c2_c17, axiom, c2 != c17).
fof(una_c2_c18, axiom, c2 != c18).
fof(una_c2_c19, axiom, c2 != c19).
fof(una_c3_c4, axiom, c3 != c4).
fof(una_c3_c5, axiom, c3 != c5).
fof(una_c3_c6, axiom, c3 != c6).
fof(una_c3_c7, axiom, c3 != c7).
fof(una_c3_c8, axiom, c3 != c8).
fof(una_c3_c9, axiom, c3 != c9).
fof(una_c3_c10, axiom, c3 != c10).
fof(una_c3_c11, axiom, c3 != c11).
fof(una_c3_c12, axiom, c3 != c12).
fof(una_c3_c13, axiom, c3 != c13).
fof(una_c3_c14, axiom, c3 != c14).
fof(una_c3_c15, axiom, c3 != c15).
fof(una_c3_c16, axiom, c3 != c16).
fof(una_c3_c17, axiom, c3 != c17).
fof(una_c3_c18, axiom, c3 != c18).
fof(una_c3_c19, axiom, c3 != c19).
fof(una_c4_c5, axiom, c4 != c5).
fof(una_c4_c6, axiom, c4 != c6).
fof(una_c4_c7, axiom, c4 != c7).
fof(una_c4_c8, axiom, c4 != c8).
fof(una_c4_c9, axiom, c4 != c9).
fof(una_c4_c10, axiom, c4 != c10).
fof(una_c4_c11, axiom, c4 != c11).
fof(una_c4_c12, axiom, c4 != c12).
fof(una_c4_c13, axiom, c4 != c13).
fof(una_c4_c14, axiom, c4 != c14).
fof(una_c4_c15, axiom, c4 != c15).
fof(una_c4_c16, axiom, c4 != c16).
fof(una_c4_c17, axiom, c4 != c17).
fof(una_c4_c18, axiom, c4 != c18).
fof(una_c4_c19, axiom, c4 != c19).
fof(una_c5_c6, axiom, c5 != c6).
fof(una_c5_c7, axiom, c5 != c7).
fof(una_c5_c8, axiom, c5 != c8).
fof(una_c5_c9, axiom, c5 != c9).
fof(una_c5_c10, axiom, c5 != c10).
fof(una_c5_c11, axiom, c5 != c11).
fof(una_c5_c12, axiom, c5 != c12).
fof(una_c5_c13, axiom, c5 != c13).
fof(una_c5_c14, axiom, c5 != c14).
fof(una_c5_c15, axiom, c5 != c15).
fof(una_c5_c16, axiom, c5 != c16).
fof(una_c5_c17, axiom, c5 != c17).
fof(una_c5_c18, axiom, c5 != c18).
fof(una_c5_c19, axiom, c5 != c19).
fof(una_c6_c7, axiom, c6 != c7).
fof(una_c6_c8, axiom, c6 != c8).
fof(una_c6_c9, axiom, c6 != c9).
fof(una_c6_c10, axiom, c6 != c10).
fof(una_c6_c11, axiom, c6 != c11).
fof(una_c6_c12, axiom, c6 != c12).
fof(una_c6_c13, axiom, c6 != c13).
fof(una_c6_c14, axiom, c6 != c14).
fof(una_c6_c15, axiom, c6 != c15).
fof(una_c6_c16, axiom, c6 != c16).
fof(una_c6_c17, axiom, c6 != c17).
fof(una_c6_c18, axiom, c6 != c18).
fof(una_c6_c19, axiom, c6 != c19).
fof(una_c7_c8, axiom, c7 != c8).
fof(una_c7_c9, axiom, c7 != c9).
fof(una_c7_c10, axiom, c7 != c10).
fof(una_c7_c11, axiom, c7 != c11).
fof(una_c7_c12, axiom, c7 != c12).
fof(una_c7_c13, axiom, c7 != c13).
fof(una_c7_c14, axiom, c7 != c14).
fof(una_c7_c15, axiom, c7 != c15).
fof(una_c7_c16, axiom, c7 != c16).
fof(una_c7_c17, axiom, c7 != c17).
fof(una_c7_c18, axiom, c7 != c18).
fof(una_c7_c19, axiom, c7 != c19).
fof(una_c8_c9, axiom, c8 != c9).
fof(una_c8_c10, axiom, c8 != c10).
fof(una_c8_c11, axiom, c8 != c11).
fof(una_c8_c12, axiom, c8 != c12).
fof(una_c8_c13, axiom, c8 != c13).
fof(una_c8_c14, axiom, c8 != c14).
fof(una_c8_c15, axiom, c8 != c15).
fof(una_c8_c16, axiom, c8 != c16).
fof(una_c8_c17, axiom, c8 != c17).
fof(una_c8_c18, axiom, c8 != c18).
fof(una_c8_c19, axiom, c8 != c19).
fof(una_c9_c10, axiom, c9 != c10).
fof(una_c9_c11, axiom, c9 != c11).
fof(una_c9_c12, axiom, c9 != c12).
fof(una_c9_c13, axiom, c9 != c13).
fof(una_c9_c14, axiom, c9 != c14).
fof(una_c9_c15, axiom, c9 != c15).
fof(una_c9_c16, axiom, c9 != c16).
fof(una_c9_c17, axiom, c9 != c17).
fof(una_c9_c18, axiom, c9 != c18).
fof(una_c9_c19, axiom, c9 != c19).
fof(una_c10_c11, axiom, c10 != c11).
fof(una_c10_c12, axiom, c10 != c12).
fof(una_c10_c13, axiom, c10 != c13).
fof(una_c10_c14, axiom, c10 != c14).
fof(una_c10_c15, axiom, c10 != c15).
fof(una_c10_c16, axiom, c10 != c16).
fof(una_c10_c17, axiom, c10 != c17).
fof(una_c10_c18, axiom, c10 != c18).
fof(una_c10_c19, axiom, c10 != c19).
fof(una_c11_c12, axiom, c11 != c12).
fof(una_c11_c13, axiom, c11 != c13).
fof(una_c11_c14, axiom, c11 != c14).
fof(una_c11_c15, axiom, c11 != c15).
fof(una_c11_c16, axiom, c11 != c16).
fof(una_c11_c17, axiom, c11 != c17).
fof(una_c11_c18, axiom, c11 != c18).
fof(una_c11_c19, axiom, c11 != c19).
fof(una_c12_c13, axiom, c12 != c13).
fof(una_c12_c14, axiom, c12 != c14).
fof(una_c12_c15, axiom, c12 != c15).
fof(una_c12_c16, axiom, c12 != c16).
fof(una_c12_c17, axiom, c12 != c17).
fof(una_c12_c18, axiom, c12 != c18).
fof(una_c12_c19, axiom, c12 != c19).
fof(una_c13_c14, axiom, c13 != c14).
fof(una_c13_c15, axiom, c13 != c15).
fof(una_c13_c16, axiom, c13 != c16).
fof(una_c13_c17, axiom, c13 != c17).
fof(una_c13_c18, axiom, c13 != c18).
fof(una_c13_c19, axiom, c13 != c19).
fof(una_c14_c15, axiom, c14 != c15).
fof(una_c14_c16, axiom, c14 != c16).
fof(una_c14_c17, axiom, c14 != c17).
fof(una_c14_c18, axiom, c14 != c18).
fof(una_c14_c19, axiom, c14 != c19).
fof(una_c15_c16, axiom, c15 != c16).
fof(una_c15_c17, axiom, c15 != c17).
fof(una_c15_c18, axiom, c15 != c18).
fof(una_c15_c19, axiom, c15 != c19).
fof(una_c16_c17, axiom, c16 != c17).
fof(una_c16_c18, axiom, c16 != c18).
fof(una_c16_c19, axiom, c16 != c19).
fof(una_c17_c18, axiom, c17 != c18).
fof(una_c17_c19, axiom, c17 != c19).
fof(una_c18_c19, axiom, c18 != c19).
fof(nosub_c1_c0, axiom, ~subclass(c1, c0)).
fof(nosub_c2_c0, axiom, ~subclass(c2, c0)).
fof(nosub_c2_c1, axiom, ~subclass(c2, c1)).
fof(nosub_c3_c0, axiom, ~subclass(c3, c0)).
fof(nosub_c3_c1, axiom, ~subclass(c3, c1)).
fof(nosub_c3_c2, axiom, ~subclass(c3, c2)).
fof(nosub_c4_c0, axiom, ~subclass(c4, c0)).
fof(nosub_c4_c1, axiom, ~subclass(c4, c1)).
fof(nosub_c4_c2, axiom, ~subclass(c4, c2)).
fof(nosub_c4_c3, axiom, ~subclass(c4, c3)).
fof(nosub_c5_c0, axiom, ~subclass(c5, c0)).
fof(nosub_c5_c1, axiom, ~subclass(c5, c1)).
fof(nosub_c5_c2, axiom, ~subclass(c5, c2)).
fof(nosub_c5_c3, axiom, ~subclass(c5, c3)).
fof(nosub_c5_c4, axiom, ~subclass(c5, c4)).
fof(nosub_c6_c0, axiom, ~subclass(c6, c0)).
fof(nosub_c6_c1, axiom, ~subclass(c6, c1)).
fof(nosub_c6_c2, axiom, ~subclass(c6, c2)).
fof(nosub_c6_c3, axiom, ~subclass(c6, c3)).
fof(nosub_c6_c4, axiom, ~subclass(c6, c4)).
fof(nosub_c6_c5, axiom, ~subclass(c6, c5)).
fof(nosub_c7_c0, axiom, ~subclass(c7, c0)).
fof(nosub_c7_c1, axiom, ~subclass(c7, c1)).
fof(nosub_c7_c2, axiom, ~subclass(c7, c2)).
fof(nosub_c7_c3, axiom, ~subclass(c7, c3)).
fof(nosub_c7_c4, axiom, ~subclass(c7, c4)).
fof(nosub_c7_c5, axiom, ~subclass(c7, c5)).
fof(nosub_c7_c6, axiom, ~subclass(c7, c6)).
fof(nosub_c8_c0, axiom, ~subclass(c8, c0)).
fof(nosub_c8_c1, axiom, ~subclass(c8, c1)).
fof(nosub_c8_c2, axiom, ~subclass(c8, c2)).
fof(nosub_c8_c3, axiom, ~subclass(c8, c3)).
fof(nosub_c8_c4, axiom, ~subclass(c8, c4)).
fof(nosub_c8_c5, axiom, ~subclass(c8, c5)).
fof(nosub_c8_c6, axiom, ~subclass(c8, c6)).
fof(nosub_c8_c7, axiom, ~subclass(c8, c7)).
fof(nosub_c9_c0, axiom, ~subclass(c9, c0)).
fof(nosub_c9_c1, axiom, ~subclass(c9, c1)).
fof(nosub_c9_c2, axiom, ~subclass(c9, c2)).
fof(nosub_c9_c3, axiom, ~subclass(c9, c3)).
fof(nosub_c9_c4, axiom, ~subclass(c9, c4)).
fof(nosub_c9_c5, axiom, ~subclass(c9, c5)).
fof(nosub_c9_c6, axiom, ~subclass(c9, c6)).
fof(nosub_c9_c7, axiom, ~subclass(c9, c7)).
fof(nosub_c9_c8, axiom, ~subclass(c9, c8)).
fof(nosub_c10_c0, axiom, ~subclass(c10, c0)).
fof(nosub_c10_c1, axiom, ~subclass(c10, c1)).
fof(nosub_c10_c2, axiom, ~subclass(c10, c2)).
fof(nosub_c10_c3, axiom, ~subclass(c10, c3)).
fof(nosub_c10_c4, axiom, ~subclass(c10, c4)).
fof(nosub_c10_c5, axiom, ~subclass(c10, c5)).
fof(nosub_c10_c6, axiom, ~subclass(c10, c6)).
fof(nosub_c10_c7, axiom, ~subclass(c10, c7)).
fof(nosub_c10_c8, axiom, ~subclass(c10, c8)).
fof(nosub_c10_c9, axiom, ~subclass(c10, c9)).
fof(nosub_c11_c0, axiom, ~subclass(c11, c0)).
fof(nosub_c11_c1, axiom, ~subclass(c11, c1)).
fof(nosub_c11_c2, axiom, ~subclass(c11, c2)).
fof(nosub_c11_c3, axiom, ~subclass(c11, c3)).
fof(nosub_c11_c4, axiom, ~subclass(c11, c4)).
fof(nosub_c11_c5, axiom, ~subclass(c11, c5)).
fof(nosub_c11_c6, axiom, ~subclass(c11, c6)).
fof(nosub_c11_c7, axiom, ~subclass(c11, c7)).
fof(nosub_c11_c8, axiom, ~subclass(c11, c8)).
fof(nosub_c11_c9, axiom, ~subclass(c11, c9)).
fof(nosub_c11_c10, axiom, ~subclass(c11, c10)).
fof(nosub_c12_c0, axiom, ~subclass(c12, c0)).
fof(nosub_c12_c1, axiom, ~subclass(c12, c1)).
fof(nosub_c12_c2, axiom, ~subclass(c12, c2)).
fof(nosub_c12_c3, axiom, ~subclass(c12, c3)).
fof(nosub_c12_c4, axiom, ~subclass(c12, c4)).
fof(nosub_c12_c5, axiom, ~subclass(c12, c5)).
fof(nosub_c12_c6, axiom, ~subclass(c12, c6)).
fof(nosub_c12_c7, axiom, ~subclass(c12, c7)).
fof(nosub_c12_c8, axiom, ~subclass(c12, c8)).
fof(nosub_c12_c9, axiom, ~subclass(c12, c9)).
fof(nosub_c12_c10, axiom, ~subclass(c12, c10)).
fof(nosub_c12_c11, axiom, ~subclass(c12, c11)).
fof(nosub_c13_c0, axiom, ~subclass(c13, c0)).
fof(nosub_c13_c1, axiom, ~subclass(c13, c1)).
fof(nosub_c13_c2, axiom, ~subclass(c13, c2)).
fof(nosub_c13_c3, axiom, ~subclass(c13, c3)).
fof(nosub_c13_c4, axiom, ~subclass(c13, c4)).
fof(nosub_c13_c5, axiom, ~subclass(c13, c5)).
fof(nosub_c13_c6, axiom, ~subclass(c13, c6)).
fof(nosub_c13_c7, axiom, ~subclass(c13, c7)).
fof(nosub_c13_c8, axiom, ~subclass(c13, c8)).
fof(nosub_c13_c9, axiom, ~subclass(c13, c9)).
fof(nosub_c13_c10, axiom, ~subclass(c13, c10)).
fof(nosub_c13_c11, axiom, ~subclass(c13, c11)).
fof(nosub_c13_c12, axiom, ~subclass(c13, c12)).
fof(nosub_c14_c0, axiom, ~subclass(c14, c0)).
fof(nosub_c14_c1, axiom, ~subclass(c14, c1)).
fof(nosub_c14_c2, axiom, ~subclass(c14, c2)).
fof(nosub_c14_c3, axiom, ~subclass(c14, c3)).
fof(nosub_c14_c4, axiom, ~subclass(c14, c4)).
fof(nosub_c14_c5, axiom, ~subclass(c14, c5)).
fof(nosub_c14_c6, axiom, ~subclass(c14, c6)).
fof(nosub_c14_c7, axiom, ~subclass(c14, c7)).
fof(nosub_c14_c8, axiom, ~subclass(c14, c8)).
fof(nosub_c14_c9, axiom, ~subclass(c14, c9)).
fof(nosub_c14_c10, axiom, ~subclass(c14, c10)).
fof(nosub_c14_c11, axiom, ~subclass(c14, c11)).
fof(nosub_c14_c12, axiom, ~subclass(c14, c12)).
fof(nosub_c14_c13, axiom, ~subclass(c14, c13)).
fof(nosub_c15_c0, axiom, ~subclass(c15, c0)).
fof(nosub_c15_c1, axiom, ~subclass(c15, c1)).
fof(nosub_c15_c2, axiom, ~subclass(c15, c2)).
fof(nosub_c15_c3, axiom, ~subclass(c15, c3)).
fof(nosub_c15_c4, axiom, ~subclass(c15, c4)).
fof(nosub_c15_c5, axiom, ~subclass(c15, c5)).
fof(nosub_c15_c6, axiom, ~subclass(c15, c6)).
fof(nosub_c15_c7, axiom, ~subclass(c15, c7)).
fof(nosub_c15_c8, axiom, ~subclass(c15, c8)).
fof(nosub_c15_c9, axiom, ~subclass(c15, c9)).
fof(nosub_c15_c10, axiom, ~subclass(c15, c10)).
fof(nosub_c15_c11, axiom, ~subclass(c15, c11)).
fof(nosub_c15_c12, axiom, ~subclass(c15, c12)).
fof(nosub_c15_c13, axiom, ~subclass(c15, c13)).
fof(nosub_c15_c14, axiom, ~subclass(c15, c14)).
fof(nosub_c16_c0, axiom, ~subclass(c16, c0)).
fof(nosub_c16_c1, axiom, ~subclass(c16, c1)).
fof(nosub_c16_c2, axiom, ~subclass(c16, c2)).
fof(nosub_c16_c3, axiom, ~subclass(c16, c3)).
fof(nosub_c16_c4, axiom, ~subclass(c16, c4)).
fof(nosub_c16_c5, axiom, ~subclass(c16, c5)).
fof(nosub_c16_c6, axiom, ~subclass(c16, c6)).
fof(nosub_c16_c7, axiom, ~subclass(c16, c7)).
fof(nosub_c16_c8, axiom, ~subclass(c16, c8)).
fof(nosub_c16_c9, axiom, ~subclass(c16, c9)).
fof(nosub_c16_c10, axiom, ~subclass(c16, c10)).
fof(nosub_c16_c11, axiom, ~subclass(c16, c11)).
fof(nosub_c16_c12, axiom, ~subclass(c16, c12)).
fof(nosub_c16_c13, axiom, ~subclass(c16, c13)).
fof(nosub_c16_c14, axiom, ~subclass(c16, c14)).
fof(nosub_c16_c15, axiom, ~subclass(c16, c15)).
fof(nosub_c17_c0, axiom, ~subclass(c17, c0)).
fof(nosub_c17_c1, axiom, ~subclass(c17, c1)).
fof(nosub_c17_c2, axiom, ~subclass(c17, c2)).
fof(nosub_c17_c3, axiom, ~subclass(c17, c3)).
fof(nosub_c17_c4, axiom, ~subclass(c17, c4)).
fof(nosub_c17_c5, axiom, ~subclass(c17, c5)).
fof(nosub_c17_c6, axiom, ~subclass(c17, c6)).
fof(nosub_c17_c7, axiom, ~subclass(c17, c7)).
fof(nosub_c17_c8, axiom, ~subclass(c17, c8)).
fof(nosub_c17_c9, axiom, ~subclass(c17, c9)).
fof(nosub_c17_c10, axiom, ~subclass(c17, c10)).
fof(nosub_c17_c11, axiom, ~subclass(c17, c11)).
fof(nosub_c17_c12, axiom, ~subclass(c17, c12)).
fof(nosub_c17_c13, axiom, ~subclass(c17, c13)).
fof(nosub_c17_c14, axiom, ~subclass(c17, c14)).
fof(nosub_c17_c15, axiom, ~subclass(c17, c15)).
fof(nosub_c17_c16, axiom, ~subclass(c17, c16)).
fof(nosub_c18_c0, axiom, ~subclass(c18, c0)).
fof(nosub_c18_c1, axiom, ~subclass(c18, c1)).
fof(nosub_c18_c2, axiom, ~subclass(c18, c2)).
fof(nosub_c18_c3, axiom, ~subclass(c18, c3)).
fof(nosub_c18_c4, axiom, ~subclass(c18, c4)).
fof(nosub_c18_c5, axiom, ~subclass(c18, c5)).
fof(nosub_c18_c6, axiom, ~subclass(c18, c6)).
fof(nosub_c18_c7, axiom, ~subclass(c18, c7)).
fof(nosub_c18_c8, axiom, ~subclass(c18, c8)).
fof(nosub_c18_c9, axiom, ~subclass(c18, c9)).
fof(nosub_c18_c10, axiom, ~subclass(c18, c10)).
fof(nosub_c18_c11, axiom, ~subclass(c18, c11)).
fof(nosub_c18_c12, axiom, ~subclass(c18, c12)).
fof(nosub_c18_c13, axiom, ~subclass(c18, c13)).
fof(nosub_c18_c14, axiom, ~subclass(c18, c14)).
fof(nosub_c18_c15, axiom, ~subclass(c18, c15)).
fof(nosub_c18_c16, axiom, ~subclass(c18, c16)).
fof(nosub_c18_c17, axiom, ~subclass(c18, c17)).
fof(nosub_c19_c0, axiom, ~subclass(c19, c0)).
fof(nosub_c19_c1, axiom, ~subclass(c19, c1)).
fof(nosub_c19_c2, axiom, ~subclass(c19, c2)).
fof(nosub_c19_c3, axiom, ~subclass(c19, c3)).
fof(nosub_c19_c4, axiom, ~subclass(c19, c4)).
fof(nosub_c19_c5, axiom, ~subclass(c19, c5)).
fof(nosub_c19_c6, axiom, ~subclass(c19, c6)).
fof(nosub_c19_c7, axiom, ~subclass(c19, c7)).
fof(nosub_c19_c8, axiom, ~subclass(c19, c8)).
fof(nosub_c19_c9, axiom, ~subclass(c19, c9)).
fof(nosub_c19_c10, axiom, ~subclass(c19, c10)).
fof(nosub_c19_c11, axiom, ~subclass(c19, c11)).
fof(nosub_c19_c12, axiom, ~subclass(c19, c12)).
fof(nosub_c19_c13, axiom, ~subclass(c19, c13)).
fof(nosub_c19_c14, axiom, ~subclass(c19, c14)).
fof(nosub_c19_c15, axiom, ~subclass(c19, c15)).
fof(nosub_c19_c16, axiom, ~subclass(c19, c16)).
fof(nosub_c19_c17, axiom, ~subclass(c19, c17)).
fof(nosub_c19_c18, axiom, ~subclass(c19, c18)).
fof(closure, axiom, ![X]: (concept(X) => (X = c0 | X = c1 | X = c2 | X = c3 | X = c4 | X = c5 | X = c6 | X = c7 | X = c8 | X = c9 | X = c10 | X = c11 | X = c12 | X = c13 | X = c14 | X = c15 | X = c16 | X = c17 | X = c18 | X = c19))).
fof(den1, axiom, ![X]: (inDen1(X) <=> (concept(X) & subclass(X, c10)))).
fof(den2, axiom, ![X]: (inDen2(X) <=> (concept(X) & ~subclass(X, c10)))).
fof(conjecture, conjecture, ~?[X]: (inDen1(X) & inDen2(X))).
