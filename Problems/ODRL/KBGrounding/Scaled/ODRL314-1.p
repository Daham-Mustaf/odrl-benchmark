%--------------------------------------------------------------------------
% File     : ODRL314-1 : TPTP v9.0.0. Released v9.1.0.
% Domain   : Policy (ODRL)
% Problem  : ValueSet-30 conflict
% Version  : [Mus26] axioms : Scaled.
% English  : Scaled benchmark with 30 concepts.
% Refs     : [Mus26] Mustafa, D. (2026), Grounding ODRL Constraints.
% Source   : [Mus26]
% Names    : ODRL314-1 [Mus26]
%
% Status   : Theorem
% Rating   : ? v9.1.0
% SPC      : FOF_THM_EPR
%
% Comments : Scaled benchmark. Category: Scaled/ValueSet
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
fof(c20_concept, axiom, concept(c20)).
fof(c21_concept, axiom, concept(c21)).
fof(c22_concept, axiom, concept(c22)).
fof(c23_concept, axiom, concept(c23)).
fof(c24_concept, axiom, concept(c24)).
fof(c25_concept, axiom, concept(c25)).
fof(c26_concept, axiom, concept(c26)).
fof(c27_concept, axiom, concept(c27)).
fof(c28_concept, axiom, concept(c28)).
fof(c29_concept, axiom, concept(c29)).
fof(root_concept, axiom, concept(root)).
fof(c0_sub, axiom, subclass(c0, root)).
fof(c1_sub, axiom, subclass(c1, root)).
fof(c2_sub, axiom, subclass(c2, root)).
fof(c3_sub, axiom, subclass(c3, root)).
fof(c4_sub, axiom, subclass(c4, root)).
fof(c5_sub, axiom, subclass(c5, root)).
fof(c6_sub, axiom, subclass(c6, root)).
fof(c7_sub, axiom, subclass(c7, root)).
fof(c8_sub, axiom, subclass(c8, root)).
fof(c9_sub, axiom, subclass(c9, root)).
fof(c10_sub, axiom, subclass(c10, root)).
fof(c11_sub, axiom, subclass(c11, root)).
fof(c12_sub, axiom, subclass(c12, root)).
fof(c13_sub, axiom, subclass(c13, root)).
fof(c14_sub, axiom, subclass(c14, root)).
fof(c15_sub, axiom, subclass(c15, root)).
fof(c16_sub, axiom, subclass(c16, root)).
fof(c17_sub, axiom, subclass(c17, root)).
fof(c18_sub, axiom, subclass(c18, root)).
fof(c19_sub, axiom, subclass(c19, root)).
fof(c20_sub, axiom, subclass(c20, root)).
fof(c21_sub, axiom, subclass(c21, root)).
fof(c22_sub, axiom, subclass(c22, root)).
fof(c23_sub, axiom, subclass(c23, root)).
fof(c24_sub, axiom, subclass(c24, root)).
fof(c25_sub, axiom, subclass(c25, root)).
fof(c26_sub, axiom, subclass(c26, root)).
fof(c27_sub, axiom, subclass(c27, root)).
fof(c28_sub, axiom, subclass(c28, root)).
fof(c29_sub, axiom, subclass(c29, root)).
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
fof(una_c0_c20, axiom, c0 != c20).
fof(una_c0_c21, axiom, c0 != c21).
fof(una_c0_c22, axiom, c0 != c22).
fof(una_c0_c23, axiom, c0 != c23).
fof(una_c0_c24, axiom, c0 != c24).
fof(una_c0_c25, axiom, c0 != c25).
fof(una_c0_c26, axiom, c0 != c26).
fof(una_c0_c27, axiom, c0 != c27).
fof(una_c0_c28, axiom, c0 != c28).
fof(una_c0_c29, axiom, c0 != c29).
fof(una_c0_root, axiom, c0 != root).
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
fof(una_c1_c20, axiom, c1 != c20).
fof(una_c1_c21, axiom, c1 != c21).
fof(una_c1_c22, axiom, c1 != c22).
fof(una_c1_c23, axiom, c1 != c23).
fof(una_c1_c24, axiom, c1 != c24).
fof(una_c1_c25, axiom, c1 != c25).
fof(una_c1_c26, axiom, c1 != c26).
fof(una_c1_c27, axiom, c1 != c27).
fof(una_c1_c28, axiom, c1 != c28).
fof(una_c1_c29, axiom, c1 != c29).
fof(una_c1_root, axiom, c1 != root).
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
fof(una_c2_c20, axiom, c2 != c20).
fof(una_c2_c21, axiom, c2 != c21).
fof(una_c2_c22, axiom, c2 != c22).
fof(una_c2_c23, axiom, c2 != c23).
fof(una_c2_c24, axiom, c2 != c24).
fof(una_c2_c25, axiom, c2 != c25).
fof(una_c2_c26, axiom, c2 != c26).
fof(una_c2_c27, axiom, c2 != c27).
fof(una_c2_c28, axiom, c2 != c28).
fof(una_c2_c29, axiom, c2 != c29).
fof(una_c2_root, axiom, c2 != root).
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
fof(una_c3_c20, axiom, c3 != c20).
fof(una_c3_c21, axiom, c3 != c21).
fof(una_c3_c22, axiom, c3 != c22).
fof(una_c3_c23, axiom, c3 != c23).
fof(una_c3_c24, axiom, c3 != c24).
fof(una_c3_c25, axiom, c3 != c25).
fof(una_c3_c26, axiom, c3 != c26).
fof(una_c3_c27, axiom, c3 != c27).
fof(una_c3_c28, axiom, c3 != c28).
fof(una_c3_c29, axiom, c3 != c29).
fof(una_c3_root, axiom, c3 != root).
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
fof(una_c4_c20, axiom, c4 != c20).
fof(una_c4_c21, axiom, c4 != c21).
fof(una_c4_c22, axiom, c4 != c22).
fof(una_c4_c23, axiom, c4 != c23).
fof(una_c4_c24, axiom, c4 != c24).
fof(una_c4_c25, axiom, c4 != c25).
fof(una_c4_c26, axiom, c4 != c26).
fof(una_c4_c27, axiom, c4 != c27).
fof(una_c4_c28, axiom, c4 != c28).
fof(una_c4_c29, axiom, c4 != c29).
fof(una_c4_root, axiom, c4 != root).
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
fof(una_c5_c20, axiom, c5 != c20).
fof(una_c5_c21, axiom, c5 != c21).
fof(una_c5_c22, axiom, c5 != c22).
fof(una_c5_c23, axiom, c5 != c23).
fof(una_c5_c24, axiom, c5 != c24).
fof(una_c5_c25, axiom, c5 != c25).
fof(una_c5_c26, axiom, c5 != c26).
fof(una_c5_c27, axiom, c5 != c27).
fof(una_c5_c28, axiom, c5 != c28).
fof(una_c5_c29, axiom, c5 != c29).
fof(una_c5_root, axiom, c5 != root).
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
fof(una_c6_c20, axiom, c6 != c20).
fof(una_c6_c21, axiom, c6 != c21).
fof(una_c6_c22, axiom, c6 != c22).
fof(una_c6_c23, axiom, c6 != c23).
fof(una_c6_c24, axiom, c6 != c24).
fof(una_c6_c25, axiom, c6 != c25).
fof(una_c6_c26, axiom, c6 != c26).
fof(una_c6_c27, axiom, c6 != c27).
fof(una_c6_c28, axiom, c6 != c28).
fof(una_c6_c29, axiom, c6 != c29).
fof(una_c6_root, axiom, c6 != root).
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
fof(una_c7_c20, axiom, c7 != c20).
fof(una_c7_c21, axiom, c7 != c21).
fof(una_c7_c22, axiom, c7 != c22).
fof(una_c7_c23, axiom, c7 != c23).
fof(una_c7_c24, axiom, c7 != c24).
fof(una_c7_c25, axiom, c7 != c25).
fof(una_c7_c26, axiom, c7 != c26).
fof(una_c7_c27, axiom, c7 != c27).
fof(una_c7_c28, axiom, c7 != c28).
fof(una_c7_c29, axiom, c7 != c29).
fof(una_c7_root, axiom, c7 != root).
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
fof(una_c8_c20, axiom, c8 != c20).
fof(una_c8_c21, axiom, c8 != c21).
fof(una_c8_c22, axiom, c8 != c22).
fof(una_c8_c23, axiom, c8 != c23).
fof(una_c8_c24, axiom, c8 != c24).
fof(una_c8_c25, axiom, c8 != c25).
fof(una_c8_c26, axiom, c8 != c26).
fof(una_c8_c27, axiom, c8 != c27).
fof(una_c8_c28, axiom, c8 != c28).
fof(una_c8_c29, axiom, c8 != c29).
fof(una_c8_root, axiom, c8 != root).
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
fof(una_c9_c20, axiom, c9 != c20).
fof(una_c9_c21, axiom, c9 != c21).
fof(una_c9_c22, axiom, c9 != c22).
fof(una_c9_c23, axiom, c9 != c23).
fof(una_c9_c24, axiom, c9 != c24).
fof(una_c9_c25, axiom, c9 != c25).
fof(una_c9_c26, axiom, c9 != c26).
fof(una_c9_c27, axiom, c9 != c27).
fof(una_c9_c28, axiom, c9 != c28).
fof(una_c9_c29, axiom, c9 != c29).
fof(una_c9_root, axiom, c9 != root).
fof(una_c10_c11, axiom, c10 != c11).
fof(una_c10_c12, axiom, c10 != c12).
fof(una_c10_c13, axiom, c10 != c13).
fof(una_c10_c14, axiom, c10 != c14).
fof(una_c10_c15, axiom, c10 != c15).
fof(una_c10_c16, axiom, c10 != c16).
fof(una_c10_c17, axiom, c10 != c17).
fof(una_c10_c18, axiom, c10 != c18).
fof(una_c10_c19, axiom, c10 != c19).
fof(una_c10_c20, axiom, c10 != c20).
fof(una_c10_c21, axiom, c10 != c21).
fof(una_c10_c22, axiom, c10 != c22).
fof(una_c10_c23, axiom, c10 != c23).
fof(una_c10_c24, axiom, c10 != c24).
fof(una_c10_c25, axiom, c10 != c25).
fof(una_c10_c26, axiom, c10 != c26).
fof(una_c10_c27, axiom, c10 != c27).
fof(una_c10_c28, axiom, c10 != c28).
fof(una_c10_c29, axiom, c10 != c29).
fof(una_c10_root, axiom, c10 != root).
fof(una_c11_c12, axiom, c11 != c12).
fof(una_c11_c13, axiom, c11 != c13).
fof(una_c11_c14, axiom, c11 != c14).
fof(una_c11_c15, axiom, c11 != c15).
fof(una_c11_c16, axiom, c11 != c16).
fof(una_c11_c17, axiom, c11 != c17).
fof(una_c11_c18, axiom, c11 != c18).
fof(una_c11_c19, axiom, c11 != c19).
fof(una_c11_c20, axiom, c11 != c20).
fof(una_c11_c21, axiom, c11 != c21).
fof(una_c11_c22, axiom, c11 != c22).
fof(una_c11_c23, axiom, c11 != c23).
fof(una_c11_c24, axiom, c11 != c24).
fof(una_c11_c25, axiom, c11 != c25).
fof(una_c11_c26, axiom, c11 != c26).
fof(una_c11_c27, axiom, c11 != c27).
fof(una_c11_c28, axiom, c11 != c28).
fof(una_c11_c29, axiom, c11 != c29).
fof(una_c11_root, axiom, c11 != root).
fof(una_c12_c13, axiom, c12 != c13).
fof(una_c12_c14, axiom, c12 != c14).
fof(una_c12_c15, axiom, c12 != c15).
fof(una_c12_c16, axiom, c12 != c16).
fof(una_c12_c17, axiom, c12 != c17).
fof(una_c12_c18, axiom, c12 != c18).
fof(una_c12_c19, axiom, c12 != c19).
fof(una_c12_c20, axiom, c12 != c20).
fof(una_c12_c21, axiom, c12 != c21).
fof(una_c12_c22, axiom, c12 != c22).
fof(una_c12_c23, axiom, c12 != c23).
fof(una_c12_c24, axiom, c12 != c24).
fof(una_c12_c25, axiom, c12 != c25).
fof(una_c12_c26, axiom, c12 != c26).
fof(una_c12_c27, axiom, c12 != c27).
fof(una_c12_c28, axiom, c12 != c28).
fof(una_c12_c29, axiom, c12 != c29).
fof(una_c12_root, axiom, c12 != root).
fof(una_c13_c14, axiom, c13 != c14).
fof(una_c13_c15, axiom, c13 != c15).
fof(una_c13_c16, axiom, c13 != c16).
fof(una_c13_c17, axiom, c13 != c17).
fof(una_c13_c18, axiom, c13 != c18).
fof(una_c13_c19, axiom, c13 != c19).
fof(una_c13_c20, axiom, c13 != c20).
fof(una_c13_c21, axiom, c13 != c21).
fof(una_c13_c22, axiom, c13 != c22).
fof(una_c13_c23, axiom, c13 != c23).
fof(una_c13_c24, axiom, c13 != c24).
fof(una_c13_c25, axiom, c13 != c25).
fof(una_c13_c26, axiom, c13 != c26).
fof(una_c13_c27, axiom, c13 != c27).
fof(una_c13_c28, axiom, c13 != c28).
fof(una_c13_c29, axiom, c13 != c29).
fof(una_c13_root, axiom, c13 != root).
fof(una_c14_c15, axiom, c14 != c15).
fof(una_c14_c16, axiom, c14 != c16).
fof(una_c14_c17, axiom, c14 != c17).
fof(una_c14_c18, axiom, c14 != c18).
fof(una_c14_c19, axiom, c14 != c19).
fof(una_c14_c20, axiom, c14 != c20).
fof(una_c14_c21, axiom, c14 != c21).
fof(una_c14_c22, axiom, c14 != c22).
fof(una_c14_c23, axiom, c14 != c23).
fof(una_c14_c24, axiom, c14 != c24).
fof(una_c14_c25, axiom, c14 != c25).
fof(una_c14_c26, axiom, c14 != c26).
fof(una_c14_c27, axiom, c14 != c27).
fof(una_c14_c28, axiom, c14 != c28).
fof(una_c14_c29, axiom, c14 != c29).
fof(una_c14_root, axiom, c14 != root).
fof(una_c15_c16, axiom, c15 != c16).
fof(una_c15_c17, axiom, c15 != c17).
fof(una_c15_c18, axiom, c15 != c18).
fof(una_c15_c19, axiom, c15 != c19).
fof(una_c15_c20, axiom, c15 != c20).
fof(una_c15_c21, axiom, c15 != c21).
fof(una_c15_c22, axiom, c15 != c22).
fof(una_c15_c23, axiom, c15 != c23).
fof(una_c15_c24, axiom, c15 != c24).
fof(una_c15_c25, axiom, c15 != c25).
fof(una_c15_c26, axiom, c15 != c26).
fof(una_c15_c27, axiom, c15 != c27).
fof(una_c15_c28, axiom, c15 != c28).
fof(una_c15_c29, axiom, c15 != c29).
fof(una_c15_root, axiom, c15 != root).
fof(una_c16_c17, axiom, c16 != c17).
fof(una_c16_c18, axiom, c16 != c18).
fof(una_c16_c19, axiom, c16 != c19).
fof(una_c16_c20, axiom, c16 != c20).
fof(una_c16_c21, axiom, c16 != c21).
fof(una_c16_c22, axiom, c16 != c22).
fof(una_c16_c23, axiom, c16 != c23).
fof(una_c16_c24, axiom, c16 != c24).
fof(una_c16_c25, axiom, c16 != c25).
fof(una_c16_c26, axiom, c16 != c26).
fof(una_c16_c27, axiom, c16 != c27).
fof(una_c16_c28, axiom, c16 != c28).
fof(una_c16_c29, axiom, c16 != c29).
fof(una_c16_root, axiom, c16 != root).
fof(una_c17_c18, axiom, c17 != c18).
fof(una_c17_c19, axiom, c17 != c19).
fof(una_c17_c20, axiom, c17 != c20).
fof(una_c17_c21, axiom, c17 != c21).
fof(una_c17_c22, axiom, c17 != c22).
fof(una_c17_c23, axiom, c17 != c23).
fof(una_c17_c24, axiom, c17 != c24).
fof(una_c17_c25, axiom, c17 != c25).
fof(una_c17_c26, axiom, c17 != c26).
fof(una_c17_c27, axiom, c17 != c27).
fof(una_c17_c28, axiom, c17 != c28).
fof(una_c17_c29, axiom, c17 != c29).
fof(una_c17_root, axiom, c17 != root).
fof(una_c18_c19, axiom, c18 != c19).
fof(una_c18_c20, axiom, c18 != c20).
fof(una_c18_c21, axiom, c18 != c21).
fof(una_c18_c22, axiom, c18 != c22).
fof(una_c18_c23, axiom, c18 != c23).
fof(una_c18_c24, axiom, c18 != c24).
fof(una_c18_c25, axiom, c18 != c25).
fof(una_c18_c26, axiom, c18 != c26).
fof(una_c18_c27, axiom, c18 != c27).
fof(una_c18_c28, axiom, c18 != c28).
fof(una_c18_c29, axiom, c18 != c29).
fof(una_c18_root, axiom, c18 != root).
fof(una_c19_c20, axiom, c19 != c20).
fof(una_c19_c21, axiom, c19 != c21).
fof(una_c19_c22, axiom, c19 != c22).
fof(una_c19_c23, axiom, c19 != c23).
fof(una_c19_c24, axiom, c19 != c24).
fof(una_c19_c25, axiom, c19 != c25).
fof(una_c19_c26, axiom, c19 != c26).
fof(una_c19_c27, axiom, c19 != c27).
fof(una_c19_c28, axiom, c19 != c28).
fof(una_c19_c29, axiom, c19 != c29).
fof(una_c19_root, axiom, c19 != root).
fof(una_c20_c21, axiom, c20 != c21).
fof(una_c20_c22, axiom, c20 != c22).
fof(una_c20_c23, axiom, c20 != c23).
fof(una_c20_c24, axiom, c20 != c24).
fof(una_c20_c25, axiom, c20 != c25).
fof(una_c20_c26, axiom, c20 != c26).
fof(una_c20_c27, axiom, c20 != c27).
fof(una_c20_c28, axiom, c20 != c28).
fof(una_c20_c29, axiom, c20 != c29).
fof(una_c20_root, axiom, c20 != root).
fof(una_c21_c22, axiom, c21 != c22).
fof(una_c21_c23, axiom, c21 != c23).
fof(una_c21_c24, axiom, c21 != c24).
fof(una_c21_c25, axiom, c21 != c25).
fof(una_c21_c26, axiom, c21 != c26).
fof(una_c21_c27, axiom, c21 != c27).
fof(una_c21_c28, axiom, c21 != c28).
fof(una_c21_c29, axiom, c21 != c29).
fof(una_c21_root, axiom, c21 != root).
fof(una_c22_c23, axiom, c22 != c23).
fof(una_c22_c24, axiom, c22 != c24).
fof(una_c22_c25, axiom, c22 != c25).
fof(una_c22_c26, axiom, c22 != c26).
fof(una_c22_c27, axiom, c22 != c27).
fof(una_c22_c28, axiom, c22 != c28).
fof(una_c22_c29, axiom, c22 != c29).
fof(una_c22_root, axiom, c22 != root).
fof(una_c23_c24, axiom, c23 != c24).
fof(una_c23_c25, axiom, c23 != c25).
fof(una_c23_c26, axiom, c23 != c26).
fof(una_c23_c27, axiom, c23 != c27).
fof(una_c23_c28, axiom, c23 != c28).
fof(una_c23_c29, axiom, c23 != c29).
fof(una_c23_root, axiom, c23 != root).
fof(una_c24_c25, axiom, c24 != c25).
fof(una_c24_c26, axiom, c24 != c26).
fof(una_c24_c27, axiom, c24 != c27).
fof(una_c24_c28, axiom, c24 != c28).
fof(una_c24_c29, axiom, c24 != c29).
fof(una_c24_root, axiom, c24 != root).
fof(una_c25_c26, axiom, c25 != c26).
fof(una_c25_c27, axiom, c25 != c27).
fof(una_c25_c28, axiom, c25 != c28).
fof(una_c25_c29, axiom, c25 != c29).
fof(una_c25_root, axiom, c25 != root).
fof(una_c26_c27, axiom, c26 != c27).
fof(una_c26_c28, axiom, c26 != c28).
fof(una_c26_c29, axiom, c26 != c29).
fof(una_c26_root, axiom, c26 != root).
fof(una_c27_c28, axiom, c27 != c28).
fof(una_c27_c29, axiom, c27 != c29).
fof(una_c27_root, axiom, c27 != root).
fof(una_c28_c29, axiom, c28 != c29).
fof(una_c28_root, axiom, c28 != root).
fof(una_c29_root, axiom, c29 != root).
fof(nosub_c0_c1, axiom, ~subclass(c0, c1)).
fof(nosub_c1_c0, axiom, ~subclass(c1, c0)).
fof(nosub_c0_c2, axiom, ~subclass(c0, c2)).
fof(nosub_c2_c0, axiom, ~subclass(c2, c0)).
fof(nosub_c0_c3, axiom, ~subclass(c0, c3)).
fof(nosub_c3_c0, axiom, ~subclass(c3, c0)).
fof(nosub_c0_c4, axiom, ~subclass(c0, c4)).
fof(nosub_c4_c0, axiom, ~subclass(c4, c0)).
fof(nosub_c0_c5, axiom, ~subclass(c0, c5)).
fof(nosub_c5_c0, axiom, ~subclass(c5, c0)).
fof(nosub_c0_c6, axiom, ~subclass(c0, c6)).
fof(nosub_c6_c0, axiom, ~subclass(c6, c0)).
fof(nosub_c0_c7, axiom, ~subclass(c0, c7)).
fof(nosub_c7_c0, axiom, ~subclass(c7, c0)).
fof(nosub_c0_c8, axiom, ~subclass(c0, c8)).
fof(nosub_c8_c0, axiom, ~subclass(c8, c0)).
fof(nosub_c0_c9, axiom, ~subclass(c0, c9)).
fof(nosub_c9_c0, axiom, ~subclass(c9, c0)).
fof(nosub_c0_c10, axiom, ~subclass(c0, c10)).
fof(nosub_c10_c0, axiom, ~subclass(c10, c0)).
fof(nosub_c0_c11, axiom, ~subclass(c0, c11)).
fof(nosub_c11_c0, axiom, ~subclass(c11, c0)).
fof(nosub_c0_c12, axiom, ~subclass(c0, c12)).
fof(nosub_c12_c0, axiom, ~subclass(c12, c0)).
fof(nosub_c0_c13, axiom, ~subclass(c0, c13)).
fof(nosub_c13_c0, axiom, ~subclass(c13, c0)).
fof(nosub_c0_c14, axiom, ~subclass(c0, c14)).
fof(nosub_c14_c0, axiom, ~subclass(c14, c0)).
fof(nosub_c0_c15, axiom, ~subclass(c0, c15)).
fof(nosub_c15_c0, axiom, ~subclass(c15, c0)).
fof(nosub_c0_c16, axiom, ~subclass(c0, c16)).
fof(nosub_c16_c0, axiom, ~subclass(c16, c0)).
fof(nosub_c0_c17, axiom, ~subclass(c0, c17)).
fof(nosub_c17_c0, axiom, ~subclass(c17, c0)).
fof(nosub_c0_c18, axiom, ~subclass(c0, c18)).
fof(nosub_c18_c0, axiom, ~subclass(c18, c0)).
fof(nosub_c0_c19, axiom, ~subclass(c0, c19)).
fof(nosub_c19_c0, axiom, ~subclass(c19, c0)).
fof(nosub_c0_c20, axiom, ~subclass(c0, c20)).
fof(nosub_c20_c0, axiom, ~subclass(c20, c0)).
fof(nosub_c0_c21, axiom, ~subclass(c0, c21)).
fof(nosub_c21_c0, axiom, ~subclass(c21, c0)).
fof(nosub_c0_c22, axiom, ~subclass(c0, c22)).
fof(nosub_c22_c0, axiom, ~subclass(c22, c0)).
fof(nosub_c0_c23, axiom, ~subclass(c0, c23)).
fof(nosub_c23_c0, axiom, ~subclass(c23, c0)).
fof(nosub_c0_c24, axiom, ~subclass(c0, c24)).
fof(nosub_c24_c0, axiom, ~subclass(c24, c0)).
fof(nosub_c0_c25, axiom, ~subclass(c0, c25)).
fof(nosub_c25_c0, axiom, ~subclass(c25, c0)).
fof(nosub_c0_c26, axiom, ~subclass(c0, c26)).
fof(nosub_c26_c0, axiom, ~subclass(c26, c0)).
fof(nosub_c0_c27, axiom, ~subclass(c0, c27)).
fof(nosub_c27_c0, axiom, ~subclass(c27, c0)).
fof(nosub_c0_c28, axiom, ~subclass(c0, c28)).
fof(nosub_c28_c0, axiom, ~subclass(c28, c0)).
fof(nosub_c0_c29, axiom, ~subclass(c0, c29)).
fof(nosub_c29_c0, axiom, ~subclass(c29, c0)).
fof(nosub_c1_c2, axiom, ~subclass(c1, c2)).
fof(nosub_c2_c1, axiom, ~subclass(c2, c1)).
fof(nosub_c1_c3, axiom, ~subclass(c1, c3)).
fof(nosub_c3_c1, axiom, ~subclass(c3, c1)).
fof(nosub_c1_c4, axiom, ~subclass(c1, c4)).
fof(nosub_c4_c1, axiom, ~subclass(c4, c1)).
fof(nosub_c1_c5, axiom, ~subclass(c1, c5)).
fof(nosub_c5_c1, axiom, ~subclass(c5, c1)).
fof(nosub_c1_c6, axiom, ~subclass(c1, c6)).
fof(nosub_c6_c1, axiom, ~subclass(c6, c1)).
fof(nosub_c1_c7, axiom, ~subclass(c1, c7)).
fof(nosub_c7_c1, axiom, ~subclass(c7, c1)).
fof(nosub_c1_c8, axiom, ~subclass(c1, c8)).
fof(nosub_c8_c1, axiom, ~subclass(c8, c1)).
fof(nosub_c1_c9, axiom, ~subclass(c1, c9)).
fof(nosub_c9_c1, axiom, ~subclass(c9, c1)).
fof(nosub_c1_c10, axiom, ~subclass(c1, c10)).
fof(nosub_c10_c1, axiom, ~subclass(c10, c1)).
fof(nosub_c1_c11, axiom, ~subclass(c1, c11)).
fof(nosub_c11_c1, axiom, ~subclass(c11, c1)).
fof(nosub_c1_c12, axiom, ~subclass(c1, c12)).
fof(nosub_c12_c1, axiom, ~subclass(c12, c1)).
fof(nosub_c1_c13, axiom, ~subclass(c1, c13)).
fof(nosub_c13_c1, axiom, ~subclass(c13, c1)).
fof(nosub_c1_c14, axiom, ~subclass(c1, c14)).
fof(nosub_c14_c1, axiom, ~subclass(c14, c1)).
fof(nosub_c1_c15, axiom, ~subclass(c1, c15)).
fof(nosub_c15_c1, axiom, ~subclass(c15, c1)).
fof(nosub_c1_c16, axiom, ~subclass(c1, c16)).
fof(nosub_c16_c1, axiom, ~subclass(c16, c1)).
fof(nosub_c1_c17, axiom, ~subclass(c1, c17)).
fof(nosub_c17_c1, axiom, ~subclass(c17, c1)).
fof(nosub_c1_c18, axiom, ~subclass(c1, c18)).
fof(nosub_c18_c1, axiom, ~subclass(c18, c1)).
fof(nosub_c1_c19, axiom, ~subclass(c1, c19)).
fof(nosub_c19_c1, axiom, ~subclass(c19, c1)).
fof(nosub_c1_c20, axiom, ~subclass(c1, c20)).
fof(nosub_c20_c1, axiom, ~subclass(c20, c1)).
fof(nosub_c1_c21, axiom, ~subclass(c1, c21)).
fof(nosub_c21_c1, axiom, ~subclass(c21, c1)).
fof(nosub_c1_c22, axiom, ~subclass(c1, c22)).
fof(nosub_c22_c1, axiom, ~subclass(c22, c1)).
fof(nosub_c1_c23, axiom, ~subclass(c1, c23)).
fof(nosub_c23_c1, axiom, ~subclass(c23, c1)).
fof(nosub_c1_c24, axiom, ~subclass(c1, c24)).
fof(nosub_c24_c1, axiom, ~subclass(c24, c1)).
fof(nosub_c1_c25, axiom, ~subclass(c1, c25)).
fof(nosub_c25_c1, axiom, ~subclass(c25, c1)).
fof(nosub_c1_c26, axiom, ~subclass(c1, c26)).
fof(nosub_c26_c1, axiom, ~subclass(c26, c1)).
fof(nosub_c1_c27, axiom, ~subclass(c1, c27)).
fof(nosub_c27_c1, axiom, ~subclass(c27, c1)).
fof(nosub_c1_c28, axiom, ~subclass(c1, c28)).
fof(nosub_c28_c1, axiom, ~subclass(c28, c1)).
fof(nosub_c1_c29, axiom, ~subclass(c1, c29)).
fof(nosub_c29_c1, axiom, ~subclass(c29, c1)).
fof(nosub_c2_c3, axiom, ~subclass(c2, c3)).
fof(nosub_c3_c2, axiom, ~subclass(c3, c2)).
fof(nosub_c2_c4, axiom, ~subclass(c2, c4)).
fof(nosub_c4_c2, axiom, ~subclass(c4, c2)).
fof(nosub_c2_c5, axiom, ~subclass(c2, c5)).
fof(nosub_c5_c2, axiom, ~subclass(c5, c2)).
fof(nosub_c2_c6, axiom, ~subclass(c2, c6)).
fof(nosub_c6_c2, axiom, ~subclass(c6, c2)).
fof(nosub_c2_c7, axiom, ~subclass(c2, c7)).
fof(nosub_c7_c2, axiom, ~subclass(c7, c2)).
fof(nosub_c2_c8, axiom, ~subclass(c2, c8)).
fof(nosub_c8_c2, axiom, ~subclass(c8, c2)).
fof(nosub_c2_c9, axiom, ~subclass(c2, c9)).
fof(nosub_c9_c2, axiom, ~subclass(c9, c2)).
fof(nosub_c2_c10, axiom, ~subclass(c2, c10)).
fof(nosub_c10_c2, axiom, ~subclass(c10, c2)).
fof(nosub_c2_c11, axiom, ~subclass(c2, c11)).
fof(nosub_c11_c2, axiom, ~subclass(c11, c2)).
fof(nosub_c2_c12, axiom, ~subclass(c2, c12)).
fof(nosub_c12_c2, axiom, ~subclass(c12, c2)).
fof(nosub_c2_c13, axiom, ~subclass(c2, c13)).
fof(nosub_c13_c2, axiom, ~subclass(c13, c2)).
fof(nosub_c2_c14, axiom, ~subclass(c2, c14)).
fof(nosub_c14_c2, axiom, ~subclass(c14, c2)).
fof(nosub_c2_c15, axiom, ~subclass(c2, c15)).
fof(nosub_c15_c2, axiom, ~subclass(c15, c2)).
fof(nosub_c2_c16, axiom, ~subclass(c2, c16)).
fof(nosub_c16_c2, axiom, ~subclass(c16, c2)).
fof(nosub_c2_c17, axiom, ~subclass(c2, c17)).
fof(nosub_c17_c2, axiom, ~subclass(c17, c2)).
fof(nosub_c2_c18, axiom, ~subclass(c2, c18)).
fof(nosub_c18_c2, axiom, ~subclass(c18, c2)).
fof(nosub_c2_c19, axiom, ~subclass(c2, c19)).
fof(nosub_c19_c2, axiom, ~subclass(c19, c2)).
fof(nosub_c2_c20, axiom, ~subclass(c2, c20)).
fof(nosub_c20_c2, axiom, ~subclass(c20, c2)).
fof(nosub_c2_c21, axiom, ~subclass(c2, c21)).
fof(nosub_c21_c2, axiom, ~subclass(c21, c2)).
fof(nosub_c2_c22, axiom, ~subclass(c2, c22)).
fof(nosub_c22_c2, axiom, ~subclass(c22, c2)).
fof(nosub_c2_c23, axiom, ~subclass(c2, c23)).
fof(nosub_c23_c2, axiom, ~subclass(c23, c2)).
fof(nosub_c2_c24, axiom, ~subclass(c2, c24)).
fof(nosub_c24_c2, axiom, ~subclass(c24, c2)).
fof(nosub_c2_c25, axiom, ~subclass(c2, c25)).
fof(nosub_c25_c2, axiom, ~subclass(c25, c2)).
fof(nosub_c2_c26, axiom, ~subclass(c2, c26)).
fof(nosub_c26_c2, axiom, ~subclass(c26, c2)).
fof(nosub_c2_c27, axiom, ~subclass(c2, c27)).
fof(nosub_c27_c2, axiom, ~subclass(c27, c2)).
fof(nosub_c2_c28, axiom, ~subclass(c2, c28)).
fof(nosub_c28_c2, axiom, ~subclass(c28, c2)).
fof(nosub_c2_c29, axiom, ~subclass(c2, c29)).
fof(nosub_c29_c2, axiom, ~subclass(c29, c2)).
fof(nosub_c3_c4, axiom, ~subclass(c3, c4)).
fof(nosub_c4_c3, axiom, ~subclass(c4, c3)).
fof(nosub_c3_c5, axiom, ~subclass(c3, c5)).
fof(nosub_c5_c3, axiom, ~subclass(c5, c3)).
fof(nosub_c3_c6, axiom, ~subclass(c3, c6)).
fof(nosub_c6_c3, axiom, ~subclass(c6, c3)).
fof(nosub_c3_c7, axiom, ~subclass(c3, c7)).
fof(nosub_c7_c3, axiom, ~subclass(c7, c3)).
fof(nosub_c3_c8, axiom, ~subclass(c3, c8)).
fof(nosub_c8_c3, axiom, ~subclass(c8, c3)).
fof(nosub_c3_c9, axiom, ~subclass(c3, c9)).
fof(nosub_c9_c3, axiom, ~subclass(c9, c3)).
fof(nosub_c3_c10, axiom, ~subclass(c3, c10)).
fof(nosub_c10_c3, axiom, ~subclass(c10, c3)).
fof(nosub_c3_c11, axiom, ~subclass(c3, c11)).
fof(nosub_c11_c3, axiom, ~subclass(c11, c3)).
fof(nosub_c3_c12, axiom, ~subclass(c3, c12)).
fof(nosub_c12_c3, axiom, ~subclass(c12, c3)).
fof(nosub_c3_c13, axiom, ~subclass(c3, c13)).
fof(nosub_c13_c3, axiom, ~subclass(c13, c3)).
fof(nosub_c3_c14, axiom, ~subclass(c3, c14)).
fof(nosub_c14_c3, axiom, ~subclass(c14, c3)).
fof(nosub_c3_c15, axiom, ~subclass(c3, c15)).
fof(nosub_c15_c3, axiom, ~subclass(c15, c3)).
fof(nosub_c3_c16, axiom, ~subclass(c3, c16)).
fof(nosub_c16_c3, axiom, ~subclass(c16, c3)).
fof(nosub_c3_c17, axiom, ~subclass(c3, c17)).
fof(nosub_c17_c3, axiom, ~subclass(c17, c3)).
fof(nosub_c3_c18, axiom, ~subclass(c3, c18)).
fof(nosub_c18_c3, axiom, ~subclass(c18, c3)).
fof(nosub_c3_c19, axiom, ~subclass(c3, c19)).
fof(nosub_c19_c3, axiom, ~subclass(c19, c3)).
fof(nosub_c3_c20, axiom, ~subclass(c3, c20)).
fof(nosub_c20_c3, axiom, ~subclass(c20, c3)).
fof(nosub_c3_c21, axiom, ~subclass(c3, c21)).
fof(nosub_c21_c3, axiom, ~subclass(c21, c3)).
fof(nosub_c3_c22, axiom, ~subclass(c3, c22)).
fof(nosub_c22_c3, axiom, ~subclass(c22, c3)).
fof(nosub_c3_c23, axiom, ~subclass(c3, c23)).
fof(nosub_c23_c3, axiom, ~subclass(c23, c3)).
fof(nosub_c3_c24, axiom, ~subclass(c3, c24)).
fof(nosub_c24_c3, axiom, ~subclass(c24, c3)).
fof(nosub_c3_c25, axiom, ~subclass(c3, c25)).
fof(nosub_c25_c3, axiom, ~subclass(c25, c3)).
fof(nosub_c3_c26, axiom, ~subclass(c3, c26)).
fof(nosub_c26_c3, axiom, ~subclass(c26, c3)).
fof(nosub_c3_c27, axiom, ~subclass(c3, c27)).
fof(nosub_c27_c3, axiom, ~subclass(c27, c3)).
fof(nosub_c3_c28, axiom, ~subclass(c3, c28)).
fof(nosub_c28_c3, axiom, ~subclass(c28, c3)).
fof(nosub_c3_c29, axiom, ~subclass(c3, c29)).
fof(nosub_c29_c3, axiom, ~subclass(c29, c3)).
fof(nosub_c4_c5, axiom, ~subclass(c4, c5)).
fof(nosub_c5_c4, axiom, ~subclass(c5, c4)).
fof(nosub_c4_c6, axiom, ~subclass(c4, c6)).
fof(nosub_c6_c4, axiom, ~subclass(c6, c4)).
fof(nosub_c4_c7, axiom, ~subclass(c4, c7)).
fof(nosub_c7_c4, axiom, ~subclass(c7, c4)).
fof(nosub_c4_c8, axiom, ~subclass(c4, c8)).
fof(nosub_c8_c4, axiom, ~subclass(c8, c4)).
fof(nosub_c4_c9, axiom, ~subclass(c4, c9)).
fof(nosub_c9_c4, axiom, ~subclass(c9, c4)).
fof(nosub_c4_c10, axiom, ~subclass(c4, c10)).
fof(nosub_c10_c4, axiom, ~subclass(c10, c4)).
fof(nosub_c4_c11, axiom, ~subclass(c4, c11)).
fof(nosub_c11_c4, axiom, ~subclass(c11, c4)).
fof(nosub_c4_c12, axiom, ~subclass(c4, c12)).
fof(nosub_c12_c4, axiom, ~subclass(c12, c4)).
fof(nosub_c4_c13, axiom, ~subclass(c4, c13)).
fof(nosub_c13_c4, axiom, ~subclass(c13, c4)).
fof(nosub_c4_c14, axiom, ~subclass(c4, c14)).
fof(nosub_c14_c4, axiom, ~subclass(c14, c4)).
fof(nosub_c4_c15, axiom, ~subclass(c4, c15)).
fof(nosub_c15_c4, axiom, ~subclass(c15, c4)).
fof(nosub_c4_c16, axiom, ~subclass(c4, c16)).
fof(nosub_c16_c4, axiom, ~subclass(c16, c4)).
fof(nosub_c4_c17, axiom, ~subclass(c4, c17)).
fof(nosub_c17_c4, axiom, ~subclass(c17, c4)).
fof(nosub_c4_c18, axiom, ~subclass(c4, c18)).
fof(nosub_c18_c4, axiom, ~subclass(c18, c4)).
fof(nosub_c4_c19, axiom, ~subclass(c4, c19)).
fof(nosub_c19_c4, axiom, ~subclass(c19, c4)).
fof(nosub_c4_c20, axiom, ~subclass(c4, c20)).
fof(nosub_c20_c4, axiom, ~subclass(c20, c4)).
fof(nosub_c4_c21, axiom, ~subclass(c4, c21)).
fof(nosub_c21_c4, axiom, ~subclass(c21, c4)).
fof(nosub_c4_c22, axiom, ~subclass(c4, c22)).
fof(nosub_c22_c4, axiom, ~subclass(c22, c4)).
fof(nosub_c4_c23, axiom, ~subclass(c4, c23)).
fof(nosub_c23_c4, axiom, ~subclass(c23, c4)).
fof(nosub_c4_c24, axiom, ~subclass(c4, c24)).
fof(nosub_c24_c4, axiom, ~subclass(c24, c4)).
fof(nosub_c4_c25, axiom, ~subclass(c4, c25)).
fof(nosub_c25_c4, axiom, ~subclass(c25, c4)).
fof(nosub_c4_c26, axiom, ~subclass(c4, c26)).
fof(nosub_c26_c4, axiom, ~subclass(c26, c4)).
fof(nosub_c4_c27, axiom, ~subclass(c4, c27)).
fof(nosub_c27_c4, axiom, ~subclass(c27, c4)).
fof(nosub_c4_c28, axiom, ~subclass(c4, c28)).
fof(nosub_c28_c4, axiom, ~subclass(c28, c4)).
fof(nosub_c4_c29, axiom, ~subclass(c4, c29)).
fof(nosub_c29_c4, axiom, ~subclass(c29, c4)).
fof(nosub_c5_c6, axiom, ~subclass(c5, c6)).
fof(nosub_c6_c5, axiom, ~subclass(c6, c5)).
fof(nosub_c5_c7, axiom, ~subclass(c5, c7)).
fof(nosub_c7_c5, axiom, ~subclass(c7, c5)).
fof(nosub_c5_c8, axiom, ~subclass(c5, c8)).
fof(nosub_c8_c5, axiom, ~subclass(c8, c5)).
fof(nosub_c5_c9, axiom, ~subclass(c5, c9)).
fof(nosub_c9_c5, axiom, ~subclass(c9, c5)).
fof(nosub_c5_c10, axiom, ~subclass(c5, c10)).
fof(nosub_c10_c5, axiom, ~subclass(c10, c5)).
fof(nosub_c5_c11, axiom, ~subclass(c5, c11)).
fof(nosub_c11_c5, axiom, ~subclass(c11, c5)).
fof(nosub_c5_c12, axiom, ~subclass(c5, c12)).
fof(nosub_c12_c5, axiom, ~subclass(c12, c5)).
fof(nosub_c5_c13, axiom, ~subclass(c5, c13)).
fof(nosub_c13_c5, axiom, ~subclass(c13, c5)).
fof(nosub_c5_c14, axiom, ~subclass(c5, c14)).
fof(nosub_c14_c5, axiom, ~subclass(c14, c5)).
fof(nosub_c5_c15, axiom, ~subclass(c5, c15)).
fof(nosub_c15_c5, axiom, ~subclass(c15, c5)).
fof(nosub_c5_c16, axiom, ~subclass(c5, c16)).
fof(nosub_c16_c5, axiom, ~subclass(c16, c5)).
fof(nosub_c5_c17, axiom, ~subclass(c5, c17)).
fof(nosub_c17_c5, axiom, ~subclass(c17, c5)).
fof(nosub_c5_c18, axiom, ~subclass(c5, c18)).
fof(nosub_c18_c5, axiom, ~subclass(c18, c5)).
fof(nosub_c5_c19, axiom, ~subclass(c5, c19)).
fof(nosub_c19_c5, axiom, ~subclass(c19, c5)).
fof(nosub_c5_c20, axiom, ~subclass(c5, c20)).
fof(nosub_c20_c5, axiom, ~subclass(c20, c5)).
fof(nosub_c5_c21, axiom, ~subclass(c5, c21)).
fof(nosub_c21_c5, axiom, ~subclass(c21, c5)).
fof(nosub_c5_c22, axiom, ~subclass(c5, c22)).
fof(nosub_c22_c5, axiom, ~subclass(c22, c5)).
fof(nosub_c5_c23, axiom, ~subclass(c5, c23)).
fof(nosub_c23_c5, axiom, ~subclass(c23, c5)).
fof(nosub_c5_c24, axiom, ~subclass(c5, c24)).
fof(nosub_c24_c5, axiom, ~subclass(c24, c5)).
fof(nosub_c5_c25, axiom, ~subclass(c5, c25)).
fof(nosub_c25_c5, axiom, ~subclass(c25, c5)).
fof(nosub_c5_c26, axiom, ~subclass(c5, c26)).
fof(nosub_c26_c5, axiom, ~subclass(c26, c5)).
fof(nosub_c5_c27, axiom, ~subclass(c5, c27)).
fof(nosub_c27_c5, axiom, ~subclass(c27, c5)).
fof(nosub_c5_c28, axiom, ~subclass(c5, c28)).
fof(nosub_c28_c5, axiom, ~subclass(c28, c5)).
fof(nosub_c5_c29, axiom, ~subclass(c5, c29)).
fof(nosub_c29_c5, axiom, ~subclass(c29, c5)).
fof(nosub_c6_c7, axiom, ~subclass(c6, c7)).
fof(nosub_c7_c6, axiom, ~subclass(c7, c6)).
fof(nosub_c6_c8, axiom, ~subclass(c6, c8)).
fof(nosub_c8_c6, axiom, ~subclass(c8, c6)).
fof(nosub_c6_c9, axiom, ~subclass(c6, c9)).
fof(nosub_c9_c6, axiom, ~subclass(c9, c6)).
fof(nosub_c6_c10, axiom, ~subclass(c6, c10)).
fof(nosub_c10_c6, axiom, ~subclass(c10, c6)).
fof(nosub_c6_c11, axiom, ~subclass(c6, c11)).
fof(nosub_c11_c6, axiom, ~subclass(c11, c6)).
fof(nosub_c6_c12, axiom, ~subclass(c6, c12)).
fof(nosub_c12_c6, axiom, ~subclass(c12, c6)).
fof(nosub_c6_c13, axiom, ~subclass(c6, c13)).
fof(nosub_c13_c6, axiom, ~subclass(c13, c6)).
fof(nosub_c6_c14, axiom, ~subclass(c6, c14)).
fof(nosub_c14_c6, axiom, ~subclass(c14, c6)).
fof(nosub_c6_c15, axiom, ~subclass(c6, c15)).
fof(nosub_c15_c6, axiom, ~subclass(c15, c6)).
fof(nosub_c6_c16, axiom, ~subclass(c6, c16)).
fof(nosub_c16_c6, axiom, ~subclass(c16, c6)).
fof(nosub_c6_c17, axiom, ~subclass(c6, c17)).
fof(nosub_c17_c6, axiom, ~subclass(c17, c6)).
fof(nosub_c6_c18, axiom, ~subclass(c6, c18)).
fof(nosub_c18_c6, axiom, ~subclass(c18, c6)).
fof(nosub_c6_c19, axiom, ~subclass(c6, c19)).
fof(nosub_c19_c6, axiom, ~subclass(c19, c6)).
fof(nosub_c6_c20, axiom, ~subclass(c6, c20)).
fof(nosub_c20_c6, axiom, ~subclass(c20, c6)).
fof(nosub_c6_c21, axiom, ~subclass(c6, c21)).
fof(nosub_c21_c6, axiom, ~subclass(c21, c6)).
fof(nosub_c6_c22, axiom, ~subclass(c6, c22)).
fof(nosub_c22_c6, axiom, ~subclass(c22, c6)).
fof(nosub_c6_c23, axiom, ~subclass(c6, c23)).
fof(nosub_c23_c6, axiom, ~subclass(c23, c6)).
fof(nosub_c6_c24, axiom, ~subclass(c6, c24)).
fof(nosub_c24_c6, axiom, ~subclass(c24, c6)).
fof(nosub_c6_c25, axiom, ~subclass(c6, c25)).
fof(nosub_c25_c6, axiom, ~subclass(c25, c6)).
fof(nosub_c6_c26, axiom, ~subclass(c6, c26)).
fof(nosub_c26_c6, axiom, ~subclass(c26, c6)).
fof(nosub_c6_c27, axiom, ~subclass(c6, c27)).
fof(nosub_c27_c6, axiom, ~subclass(c27, c6)).
fof(nosub_c6_c28, axiom, ~subclass(c6, c28)).
fof(nosub_c28_c6, axiom, ~subclass(c28, c6)).
fof(nosub_c6_c29, axiom, ~subclass(c6, c29)).
fof(nosub_c29_c6, axiom, ~subclass(c29, c6)).
fof(nosub_c7_c8, axiom, ~subclass(c7, c8)).
fof(nosub_c8_c7, axiom, ~subclass(c8, c7)).
fof(nosub_c7_c9, axiom, ~subclass(c7, c9)).
fof(nosub_c9_c7, axiom, ~subclass(c9, c7)).
fof(nosub_c7_c10, axiom, ~subclass(c7, c10)).
fof(nosub_c10_c7, axiom, ~subclass(c10, c7)).
fof(nosub_c7_c11, axiom, ~subclass(c7, c11)).
fof(nosub_c11_c7, axiom, ~subclass(c11, c7)).
fof(nosub_c7_c12, axiom, ~subclass(c7, c12)).
fof(nosub_c12_c7, axiom, ~subclass(c12, c7)).
fof(nosub_c7_c13, axiom, ~subclass(c7, c13)).
fof(nosub_c13_c7, axiom, ~subclass(c13, c7)).
fof(nosub_c7_c14, axiom, ~subclass(c7, c14)).
fof(nosub_c14_c7, axiom, ~subclass(c14, c7)).
fof(nosub_c7_c15, axiom, ~subclass(c7, c15)).
fof(nosub_c15_c7, axiom, ~subclass(c15, c7)).
fof(nosub_c7_c16, axiom, ~subclass(c7, c16)).
fof(nosub_c16_c7, axiom, ~subclass(c16, c7)).
fof(nosub_c7_c17, axiom, ~subclass(c7, c17)).
fof(nosub_c17_c7, axiom, ~subclass(c17, c7)).
fof(nosub_c7_c18, axiom, ~subclass(c7, c18)).
fof(nosub_c18_c7, axiom, ~subclass(c18, c7)).
fof(nosub_c7_c19, axiom, ~subclass(c7, c19)).
fof(nosub_c19_c7, axiom, ~subclass(c19, c7)).
fof(nosub_c7_c20, axiom, ~subclass(c7, c20)).
fof(nosub_c20_c7, axiom, ~subclass(c20, c7)).
fof(nosub_c7_c21, axiom, ~subclass(c7, c21)).
fof(nosub_c21_c7, axiom, ~subclass(c21, c7)).
fof(nosub_c7_c22, axiom, ~subclass(c7, c22)).
fof(nosub_c22_c7, axiom, ~subclass(c22, c7)).
fof(nosub_c7_c23, axiom, ~subclass(c7, c23)).
fof(nosub_c23_c7, axiom, ~subclass(c23, c7)).
fof(nosub_c7_c24, axiom, ~subclass(c7, c24)).
fof(nosub_c24_c7, axiom, ~subclass(c24, c7)).
fof(nosub_c7_c25, axiom, ~subclass(c7, c25)).
fof(nosub_c25_c7, axiom, ~subclass(c25, c7)).
fof(nosub_c7_c26, axiom, ~subclass(c7, c26)).
fof(nosub_c26_c7, axiom, ~subclass(c26, c7)).
fof(nosub_c7_c27, axiom, ~subclass(c7, c27)).
fof(nosub_c27_c7, axiom, ~subclass(c27, c7)).
fof(nosub_c7_c28, axiom, ~subclass(c7, c28)).
fof(nosub_c28_c7, axiom, ~subclass(c28, c7)).
fof(nosub_c7_c29, axiom, ~subclass(c7, c29)).
fof(nosub_c29_c7, axiom, ~subclass(c29, c7)).
fof(nosub_c8_c9, axiom, ~subclass(c8, c9)).
fof(nosub_c9_c8, axiom, ~subclass(c9, c8)).
fof(nosub_c8_c10, axiom, ~subclass(c8, c10)).
fof(nosub_c10_c8, axiom, ~subclass(c10, c8)).
fof(nosub_c8_c11, axiom, ~subclass(c8, c11)).
fof(nosub_c11_c8, axiom, ~subclass(c11, c8)).
fof(nosub_c8_c12, axiom, ~subclass(c8, c12)).
fof(nosub_c12_c8, axiom, ~subclass(c12, c8)).
fof(nosub_c8_c13, axiom, ~subclass(c8, c13)).
fof(nosub_c13_c8, axiom, ~subclass(c13, c8)).
fof(nosub_c8_c14, axiom, ~subclass(c8, c14)).
fof(nosub_c14_c8, axiom, ~subclass(c14, c8)).
fof(nosub_c8_c15, axiom, ~subclass(c8, c15)).
fof(nosub_c15_c8, axiom, ~subclass(c15, c8)).
fof(nosub_c8_c16, axiom, ~subclass(c8, c16)).
fof(nosub_c16_c8, axiom, ~subclass(c16, c8)).
fof(nosub_c8_c17, axiom, ~subclass(c8, c17)).
fof(nosub_c17_c8, axiom, ~subclass(c17, c8)).
fof(nosub_c8_c18, axiom, ~subclass(c8, c18)).
fof(nosub_c18_c8, axiom, ~subclass(c18, c8)).
fof(nosub_c8_c19, axiom, ~subclass(c8, c19)).
fof(nosub_c19_c8, axiom, ~subclass(c19, c8)).
fof(nosub_c8_c20, axiom, ~subclass(c8, c20)).
fof(nosub_c20_c8, axiom, ~subclass(c20, c8)).
fof(nosub_c8_c21, axiom, ~subclass(c8, c21)).
fof(nosub_c21_c8, axiom, ~subclass(c21, c8)).
fof(nosub_c8_c22, axiom, ~subclass(c8, c22)).
fof(nosub_c22_c8, axiom, ~subclass(c22, c8)).
fof(nosub_c8_c23, axiom, ~subclass(c8, c23)).
fof(nosub_c23_c8, axiom, ~subclass(c23, c8)).
fof(nosub_c8_c24, axiom, ~subclass(c8, c24)).
fof(nosub_c24_c8, axiom, ~subclass(c24, c8)).
fof(nosub_c8_c25, axiom, ~subclass(c8, c25)).
fof(nosub_c25_c8, axiom, ~subclass(c25, c8)).
fof(nosub_c8_c26, axiom, ~subclass(c8, c26)).
fof(nosub_c26_c8, axiom, ~subclass(c26, c8)).
fof(nosub_c8_c27, axiom, ~subclass(c8, c27)).
fof(nosub_c27_c8, axiom, ~subclass(c27, c8)).
fof(nosub_c8_c28, axiom, ~subclass(c8, c28)).
fof(nosub_c28_c8, axiom, ~subclass(c28, c8)).
fof(nosub_c8_c29, axiom, ~subclass(c8, c29)).
fof(nosub_c29_c8, axiom, ~subclass(c29, c8)).
fof(nosub_c9_c10, axiom, ~subclass(c9, c10)).
fof(nosub_c10_c9, axiom, ~subclass(c10, c9)).
fof(nosub_c9_c11, axiom, ~subclass(c9, c11)).
fof(nosub_c11_c9, axiom, ~subclass(c11, c9)).
fof(nosub_c9_c12, axiom, ~subclass(c9, c12)).
fof(nosub_c12_c9, axiom, ~subclass(c12, c9)).
fof(nosub_c9_c13, axiom, ~subclass(c9, c13)).
fof(nosub_c13_c9, axiom, ~subclass(c13, c9)).
fof(nosub_c9_c14, axiom, ~subclass(c9, c14)).
fof(nosub_c14_c9, axiom, ~subclass(c14, c9)).
fof(nosub_c9_c15, axiom, ~subclass(c9, c15)).
fof(nosub_c15_c9, axiom, ~subclass(c15, c9)).
fof(nosub_c9_c16, axiom, ~subclass(c9, c16)).
fof(nosub_c16_c9, axiom, ~subclass(c16, c9)).
fof(nosub_c9_c17, axiom, ~subclass(c9, c17)).
fof(nosub_c17_c9, axiom, ~subclass(c17, c9)).
fof(nosub_c9_c18, axiom, ~subclass(c9, c18)).
fof(nosub_c18_c9, axiom, ~subclass(c18, c9)).
fof(nosub_c9_c19, axiom, ~subclass(c9, c19)).
fof(nosub_c19_c9, axiom, ~subclass(c19, c9)).
fof(nosub_c9_c20, axiom, ~subclass(c9, c20)).
fof(nosub_c20_c9, axiom, ~subclass(c20, c9)).
fof(nosub_c9_c21, axiom, ~subclass(c9, c21)).
fof(nosub_c21_c9, axiom, ~subclass(c21, c9)).
fof(nosub_c9_c22, axiom, ~subclass(c9, c22)).
fof(nosub_c22_c9, axiom, ~subclass(c22, c9)).
fof(nosub_c9_c23, axiom, ~subclass(c9, c23)).
fof(nosub_c23_c9, axiom, ~subclass(c23, c9)).
fof(nosub_c9_c24, axiom, ~subclass(c9, c24)).
fof(nosub_c24_c9, axiom, ~subclass(c24, c9)).
fof(nosub_c9_c25, axiom, ~subclass(c9, c25)).
fof(nosub_c25_c9, axiom, ~subclass(c25, c9)).
fof(nosub_c9_c26, axiom, ~subclass(c9, c26)).
fof(nosub_c26_c9, axiom, ~subclass(c26, c9)).
fof(nosub_c9_c27, axiom, ~subclass(c9, c27)).
fof(nosub_c27_c9, axiom, ~subclass(c27, c9)).
fof(nosub_c9_c28, axiom, ~subclass(c9, c28)).
fof(nosub_c28_c9, axiom, ~subclass(c28, c9)).
fof(nosub_c9_c29, axiom, ~subclass(c9, c29)).
fof(nosub_c29_c9, axiom, ~subclass(c29, c9)).
fof(nosub_c10_c11, axiom, ~subclass(c10, c11)).
fof(nosub_c11_c10, axiom, ~subclass(c11, c10)).
fof(nosub_c10_c12, axiom, ~subclass(c10, c12)).
fof(nosub_c12_c10, axiom, ~subclass(c12, c10)).
fof(nosub_c10_c13, axiom, ~subclass(c10, c13)).
fof(nosub_c13_c10, axiom, ~subclass(c13, c10)).
fof(nosub_c10_c14, axiom, ~subclass(c10, c14)).
fof(nosub_c14_c10, axiom, ~subclass(c14, c10)).
fof(nosub_c10_c15, axiom, ~subclass(c10, c15)).
fof(nosub_c15_c10, axiom, ~subclass(c15, c10)).
fof(nosub_c10_c16, axiom, ~subclass(c10, c16)).
fof(nosub_c16_c10, axiom, ~subclass(c16, c10)).
fof(nosub_c10_c17, axiom, ~subclass(c10, c17)).
fof(nosub_c17_c10, axiom, ~subclass(c17, c10)).
fof(nosub_c10_c18, axiom, ~subclass(c10, c18)).
fof(nosub_c18_c10, axiom, ~subclass(c18, c10)).
fof(nosub_c10_c19, axiom, ~subclass(c10, c19)).
fof(nosub_c19_c10, axiom, ~subclass(c19, c10)).
fof(nosub_c10_c20, axiom, ~subclass(c10, c20)).
fof(nosub_c20_c10, axiom, ~subclass(c20, c10)).
fof(nosub_c10_c21, axiom, ~subclass(c10, c21)).
fof(nosub_c21_c10, axiom, ~subclass(c21, c10)).
fof(nosub_c10_c22, axiom, ~subclass(c10, c22)).
fof(nosub_c22_c10, axiom, ~subclass(c22, c10)).
fof(nosub_c10_c23, axiom, ~subclass(c10, c23)).
fof(nosub_c23_c10, axiom, ~subclass(c23, c10)).
fof(nosub_c10_c24, axiom, ~subclass(c10, c24)).
fof(nosub_c24_c10, axiom, ~subclass(c24, c10)).
fof(nosub_c10_c25, axiom, ~subclass(c10, c25)).
fof(nosub_c25_c10, axiom, ~subclass(c25, c10)).
fof(nosub_c10_c26, axiom, ~subclass(c10, c26)).
fof(nosub_c26_c10, axiom, ~subclass(c26, c10)).
fof(nosub_c10_c27, axiom, ~subclass(c10, c27)).
fof(nosub_c27_c10, axiom, ~subclass(c27, c10)).
fof(nosub_c10_c28, axiom, ~subclass(c10, c28)).
fof(nosub_c28_c10, axiom, ~subclass(c28, c10)).
fof(nosub_c10_c29, axiom, ~subclass(c10, c29)).
fof(nosub_c29_c10, axiom, ~subclass(c29, c10)).
fof(nosub_c11_c12, axiom, ~subclass(c11, c12)).
fof(nosub_c12_c11, axiom, ~subclass(c12, c11)).
fof(nosub_c11_c13, axiom, ~subclass(c11, c13)).
fof(nosub_c13_c11, axiom, ~subclass(c13, c11)).
fof(nosub_c11_c14, axiom, ~subclass(c11, c14)).
fof(nosub_c14_c11, axiom, ~subclass(c14, c11)).
fof(nosub_c11_c15, axiom, ~subclass(c11, c15)).
fof(nosub_c15_c11, axiom, ~subclass(c15, c11)).
fof(nosub_c11_c16, axiom, ~subclass(c11, c16)).
fof(nosub_c16_c11, axiom, ~subclass(c16, c11)).
fof(nosub_c11_c17, axiom, ~subclass(c11, c17)).
fof(nosub_c17_c11, axiom, ~subclass(c17, c11)).
fof(nosub_c11_c18, axiom, ~subclass(c11, c18)).
fof(nosub_c18_c11, axiom, ~subclass(c18, c11)).
fof(nosub_c11_c19, axiom, ~subclass(c11, c19)).
fof(nosub_c19_c11, axiom, ~subclass(c19, c11)).
fof(nosub_c11_c20, axiom, ~subclass(c11, c20)).
fof(nosub_c20_c11, axiom, ~subclass(c20, c11)).
fof(nosub_c11_c21, axiom, ~subclass(c11, c21)).
fof(nosub_c21_c11, axiom, ~subclass(c21, c11)).
fof(nosub_c11_c22, axiom, ~subclass(c11, c22)).
fof(nosub_c22_c11, axiom, ~subclass(c22, c11)).
fof(nosub_c11_c23, axiom, ~subclass(c11, c23)).
fof(nosub_c23_c11, axiom, ~subclass(c23, c11)).
fof(nosub_c11_c24, axiom, ~subclass(c11, c24)).
fof(nosub_c24_c11, axiom, ~subclass(c24, c11)).
fof(nosub_c11_c25, axiom, ~subclass(c11, c25)).
fof(nosub_c25_c11, axiom, ~subclass(c25, c11)).
fof(nosub_c11_c26, axiom, ~subclass(c11, c26)).
fof(nosub_c26_c11, axiom, ~subclass(c26, c11)).
fof(nosub_c11_c27, axiom, ~subclass(c11, c27)).
fof(nosub_c27_c11, axiom, ~subclass(c27, c11)).
fof(nosub_c11_c28, axiom, ~subclass(c11, c28)).
fof(nosub_c28_c11, axiom, ~subclass(c28, c11)).
fof(nosub_c11_c29, axiom, ~subclass(c11, c29)).
fof(nosub_c29_c11, axiom, ~subclass(c29, c11)).
fof(nosub_c12_c13, axiom, ~subclass(c12, c13)).
fof(nosub_c13_c12, axiom, ~subclass(c13, c12)).
fof(nosub_c12_c14, axiom, ~subclass(c12, c14)).
fof(nosub_c14_c12, axiom, ~subclass(c14, c12)).
fof(nosub_c12_c15, axiom, ~subclass(c12, c15)).
fof(nosub_c15_c12, axiom, ~subclass(c15, c12)).
fof(nosub_c12_c16, axiom, ~subclass(c12, c16)).
fof(nosub_c16_c12, axiom, ~subclass(c16, c12)).
fof(nosub_c12_c17, axiom, ~subclass(c12, c17)).
fof(nosub_c17_c12, axiom, ~subclass(c17, c12)).
fof(nosub_c12_c18, axiom, ~subclass(c12, c18)).
fof(nosub_c18_c12, axiom, ~subclass(c18, c12)).
fof(nosub_c12_c19, axiom, ~subclass(c12, c19)).
fof(nosub_c19_c12, axiom, ~subclass(c19, c12)).
fof(nosub_c12_c20, axiom, ~subclass(c12, c20)).
fof(nosub_c20_c12, axiom, ~subclass(c20, c12)).
fof(nosub_c12_c21, axiom, ~subclass(c12, c21)).
fof(nosub_c21_c12, axiom, ~subclass(c21, c12)).
fof(nosub_c12_c22, axiom, ~subclass(c12, c22)).
fof(nosub_c22_c12, axiom, ~subclass(c22, c12)).
fof(nosub_c12_c23, axiom, ~subclass(c12, c23)).
fof(nosub_c23_c12, axiom, ~subclass(c23, c12)).
fof(nosub_c12_c24, axiom, ~subclass(c12, c24)).
fof(nosub_c24_c12, axiom, ~subclass(c24, c12)).
fof(nosub_c12_c25, axiom, ~subclass(c12, c25)).
fof(nosub_c25_c12, axiom, ~subclass(c25, c12)).
fof(nosub_c12_c26, axiom, ~subclass(c12, c26)).
fof(nosub_c26_c12, axiom, ~subclass(c26, c12)).
fof(nosub_c12_c27, axiom, ~subclass(c12, c27)).
fof(nosub_c27_c12, axiom, ~subclass(c27, c12)).
fof(nosub_c12_c28, axiom, ~subclass(c12, c28)).
fof(nosub_c28_c12, axiom, ~subclass(c28, c12)).
fof(nosub_c12_c29, axiom, ~subclass(c12, c29)).
fof(nosub_c29_c12, axiom, ~subclass(c29, c12)).
fof(nosub_c13_c14, axiom, ~subclass(c13, c14)).
fof(nosub_c14_c13, axiom, ~subclass(c14, c13)).
fof(nosub_c13_c15, axiom, ~subclass(c13, c15)).
fof(nosub_c15_c13, axiom, ~subclass(c15, c13)).
fof(nosub_c13_c16, axiom, ~subclass(c13, c16)).
fof(nosub_c16_c13, axiom, ~subclass(c16, c13)).
fof(nosub_c13_c17, axiom, ~subclass(c13, c17)).
fof(nosub_c17_c13, axiom, ~subclass(c17, c13)).
fof(nosub_c13_c18, axiom, ~subclass(c13, c18)).
fof(nosub_c18_c13, axiom, ~subclass(c18, c13)).
fof(nosub_c13_c19, axiom, ~subclass(c13, c19)).
fof(nosub_c19_c13, axiom, ~subclass(c19, c13)).
fof(nosub_c13_c20, axiom, ~subclass(c13, c20)).
fof(nosub_c20_c13, axiom, ~subclass(c20, c13)).
fof(nosub_c13_c21, axiom, ~subclass(c13, c21)).
fof(nosub_c21_c13, axiom, ~subclass(c21, c13)).
fof(nosub_c13_c22, axiom, ~subclass(c13, c22)).
fof(nosub_c22_c13, axiom, ~subclass(c22, c13)).
fof(nosub_c13_c23, axiom, ~subclass(c13, c23)).
fof(nosub_c23_c13, axiom, ~subclass(c23, c13)).
fof(nosub_c13_c24, axiom, ~subclass(c13, c24)).
fof(nosub_c24_c13, axiom, ~subclass(c24, c13)).
fof(nosub_c13_c25, axiom, ~subclass(c13, c25)).
fof(nosub_c25_c13, axiom, ~subclass(c25, c13)).
fof(nosub_c13_c26, axiom, ~subclass(c13, c26)).
fof(nosub_c26_c13, axiom, ~subclass(c26, c13)).
fof(nosub_c13_c27, axiom, ~subclass(c13, c27)).
fof(nosub_c27_c13, axiom, ~subclass(c27, c13)).
fof(nosub_c13_c28, axiom, ~subclass(c13, c28)).
fof(nosub_c28_c13, axiom, ~subclass(c28, c13)).
fof(nosub_c13_c29, axiom, ~subclass(c13, c29)).
fof(nosub_c29_c13, axiom, ~subclass(c29, c13)).
fof(nosub_c14_c15, axiom, ~subclass(c14, c15)).
fof(nosub_c15_c14, axiom, ~subclass(c15, c14)).
fof(nosub_c14_c16, axiom, ~subclass(c14, c16)).
fof(nosub_c16_c14, axiom, ~subclass(c16, c14)).
fof(nosub_c14_c17, axiom, ~subclass(c14, c17)).
fof(nosub_c17_c14, axiom, ~subclass(c17, c14)).
fof(nosub_c14_c18, axiom, ~subclass(c14, c18)).
fof(nosub_c18_c14, axiom, ~subclass(c18, c14)).
fof(nosub_c14_c19, axiom, ~subclass(c14, c19)).
fof(nosub_c19_c14, axiom, ~subclass(c19, c14)).
fof(nosub_c14_c20, axiom, ~subclass(c14, c20)).
fof(nosub_c20_c14, axiom, ~subclass(c20, c14)).
fof(nosub_c14_c21, axiom, ~subclass(c14, c21)).
fof(nosub_c21_c14, axiom, ~subclass(c21, c14)).
fof(nosub_c14_c22, axiom, ~subclass(c14, c22)).
fof(nosub_c22_c14, axiom, ~subclass(c22, c14)).
fof(nosub_c14_c23, axiom, ~subclass(c14, c23)).
fof(nosub_c23_c14, axiom, ~subclass(c23, c14)).
fof(nosub_c14_c24, axiom, ~subclass(c14, c24)).
fof(nosub_c24_c14, axiom, ~subclass(c24, c14)).
fof(nosub_c14_c25, axiom, ~subclass(c14, c25)).
fof(nosub_c25_c14, axiom, ~subclass(c25, c14)).
fof(nosub_c14_c26, axiom, ~subclass(c14, c26)).
fof(nosub_c26_c14, axiom, ~subclass(c26, c14)).
fof(nosub_c14_c27, axiom, ~subclass(c14, c27)).
fof(nosub_c27_c14, axiom, ~subclass(c27, c14)).
fof(nosub_c14_c28, axiom, ~subclass(c14, c28)).
fof(nosub_c28_c14, axiom, ~subclass(c28, c14)).
fof(nosub_c14_c29, axiom, ~subclass(c14, c29)).
fof(nosub_c29_c14, axiom, ~subclass(c29, c14)).
fof(nosub_c15_c16, axiom, ~subclass(c15, c16)).
fof(nosub_c16_c15, axiom, ~subclass(c16, c15)).
fof(nosub_c15_c17, axiom, ~subclass(c15, c17)).
fof(nosub_c17_c15, axiom, ~subclass(c17, c15)).
fof(nosub_c15_c18, axiom, ~subclass(c15, c18)).
fof(nosub_c18_c15, axiom, ~subclass(c18, c15)).
fof(nosub_c15_c19, axiom, ~subclass(c15, c19)).
fof(nosub_c19_c15, axiom, ~subclass(c19, c15)).
fof(nosub_c15_c20, axiom, ~subclass(c15, c20)).
fof(nosub_c20_c15, axiom, ~subclass(c20, c15)).
fof(nosub_c15_c21, axiom, ~subclass(c15, c21)).
fof(nosub_c21_c15, axiom, ~subclass(c21, c15)).
fof(nosub_c15_c22, axiom, ~subclass(c15, c22)).
fof(nosub_c22_c15, axiom, ~subclass(c22, c15)).
fof(nosub_c15_c23, axiom, ~subclass(c15, c23)).
fof(nosub_c23_c15, axiom, ~subclass(c23, c15)).
fof(nosub_c15_c24, axiom, ~subclass(c15, c24)).
fof(nosub_c24_c15, axiom, ~subclass(c24, c15)).
fof(nosub_c15_c25, axiom, ~subclass(c15, c25)).
fof(nosub_c25_c15, axiom, ~subclass(c25, c15)).
fof(nosub_c15_c26, axiom, ~subclass(c15, c26)).
fof(nosub_c26_c15, axiom, ~subclass(c26, c15)).
fof(nosub_c15_c27, axiom, ~subclass(c15, c27)).
fof(nosub_c27_c15, axiom, ~subclass(c27, c15)).
fof(nosub_c15_c28, axiom, ~subclass(c15, c28)).
fof(nosub_c28_c15, axiom, ~subclass(c28, c15)).
fof(nosub_c15_c29, axiom, ~subclass(c15, c29)).
fof(nosub_c29_c15, axiom, ~subclass(c29, c15)).
fof(nosub_c16_c17, axiom, ~subclass(c16, c17)).
fof(nosub_c17_c16, axiom, ~subclass(c17, c16)).
fof(nosub_c16_c18, axiom, ~subclass(c16, c18)).
fof(nosub_c18_c16, axiom, ~subclass(c18, c16)).
fof(nosub_c16_c19, axiom, ~subclass(c16, c19)).
fof(nosub_c19_c16, axiom, ~subclass(c19, c16)).
fof(nosub_c16_c20, axiom, ~subclass(c16, c20)).
fof(nosub_c20_c16, axiom, ~subclass(c20, c16)).
fof(nosub_c16_c21, axiom, ~subclass(c16, c21)).
fof(nosub_c21_c16, axiom, ~subclass(c21, c16)).
fof(nosub_c16_c22, axiom, ~subclass(c16, c22)).
fof(nosub_c22_c16, axiom, ~subclass(c22, c16)).
fof(nosub_c16_c23, axiom, ~subclass(c16, c23)).
fof(nosub_c23_c16, axiom, ~subclass(c23, c16)).
fof(nosub_c16_c24, axiom, ~subclass(c16, c24)).
fof(nosub_c24_c16, axiom, ~subclass(c24, c16)).
fof(nosub_c16_c25, axiom, ~subclass(c16, c25)).
fof(nosub_c25_c16, axiom, ~subclass(c25, c16)).
fof(nosub_c16_c26, axiom, ~subclass(c16, c26)).
fof(nosub_c26_c16, axiom, ~subclass(c26, c16)).
fof(nosub_c16_c27, axiom, ~subclass(c16, c27)).
fof(nosub_c27_c16, axiom, ~subclass(c27, c16)).
fof(nosub_c16_c28, axiom, ~subclass(c16, c28)).
fof(nosub_c28_c16, axiom, ~subclass(c28, c16)).
fof(nosub_c16_c29, axiom, ~subclass(c16, c29)).
fof(nosub_c29_c16, axiom, ~subclass(c29, c16)).
fof(nosub_c17_c18, axiom, ~subclass(c17, c18)).
fof(nosub_c18_c17, axiom, ~subclass(c18, c17)).
fof(nosub_c17_c19, axiom, ~subclass(c17, c19)).
fof(nosub_c19_c17, axiom, ~subclass(c19, c17)).
fof(nosub_c17_c20, axiom, ~subclass(c17, c20)).
fof(nosub_c20_c17, axiom, ~subclass(c20, c17)).
fof(nosub_c17_c21, axiom, ~subclass(c17, c21)).
fof(nosub_c21_c17, axiom, ~subclass(c21, c17)).
fof(nosub_c17_c22, axiom, ~subclass(c17, c22)).
fof(nosub_c22_c17, axiom, ~subclass(c22, c17)).
fof(nosub_c17_c23, axiom, ~subclass(c17, c23)).
fof(nosub_c23_c17, axiom, ~subclass(c23, c17)).
fof(nosub_c17_c24, axiom, ~subclass(c17, c24)).
fof(nosub_c24_c17, axiom, ~subclass(c24, c17)).
fof(nosub_c17_c25, axiom, ~subclass(c17, c25)).
fof(nosub_c25_c17, axiom, ~subclass(c25, c17)).
fof(nosub_c17_c26, axiom, ~subclass(c17, c26)).
fof(nosub_c26_c17, axiom, ~subclass(c26, c17)).
fof(nosub_c17_c27, axiom, ~subclass(c17, c27)).
fof(nosub_c27_c17, axiom, ~subclass(c27, c17)).
fof(nosub_c17_c28, axiom, ~subclass(c17, c28)).
fof(nosub_c28_c17, axiom, ~subclass(c28, c17)).
fof(nosub_c17_c29, axiom, ~subclass(c17, c29)).
fof(nosub_c29_c17, axiom, ~subclass(c29, c17)).
fof(nosub_c18_c19, axiom, ~subclass(c18, c19)).
fof(nosub_c19_c18, axiom, ~subclass(c19, c18)).
fof(nosub_c18_c20, axiom, ~subclass(c18, c20)).
fof(nosub_c20_c18, axiom, ~subclass(c20, c18)).
fof(nosub_c18_c21, axiom, ~subclass(c18, c21)).
fof(nosub_c21_c18, axiom, ~subclass(c21, c18)).
fof(nosub_c18_c22, axiom, ~subclass(c18, c22)).
fof(nosub_c22_c18, axiom, ~subclass(c22, c18)).
fof(nosub_c18_c23, axiom, ~subclass(c18, c23)).
fof(nosub_c23_c18, axiom, ~subclass(c23, c18)).
fof(nosub_c18_c24, axiom, ~subclass(c18, c24)).
fof(nosub_c24_c18, axiom, ~subclass(c24, c18)).
fof(nosub_c18_c25, axiom, ~subclass(c18, c25)).
fof(nosub_c25_c18, axiom, ~subclass(c25, c18)).
fof(nosub_c18_c26, axiom, ~subclass(c18, c26)).
fof(nosub_c26_c18, axiom, ~subclass(c26, c18)).
fof(nosub_c18_c27, axiom, ~subclass(c18, c27)).
fof(nosub_c27_c18, axiom, ~subclass(c27, c18)).
fof(nosub_c18_c28, axiom, ~subclass(c18, c28)).
fof(nosub_c28_c18, axiom, ~subclass(c28, c18)).
fof(nosub_c18_c29, axiom, ~subclass(c18, c29)).
fof(nosub_c29_c18, axiom, ~subclass(c29, c18)).
fof(nosub_c19_c20, axiom, ~subclass(c19, c20)).
fof(nosub_c20_c19, axiom, ~subclass(c20, c19)).
fof(nosub_c19_c21, axiom, ~subclass(c19, c21)).
fof(nosub_c21_c19, axiom, ~subclass(c21, c19)).
fof(nosub_c19_c22, axiom, ~subclass(c19, c22)).
fof(nosub_c22_c19, axiom, ~subclass(c22, c19)).
fof(nosub_c19_c23, axiom, ~subclass(c19, c23)).
fof(nosub_c23_c19, axiom, ~subclass(c23, c19)).
fof(nosub_c19_c24, axiom, ~subclass(c19, c24)).
fof(nosub_c24_c19, axiom, ~subclass(c24, c19)).
fof(nosub_c19_c25, axiom, ~subclass(c19, c25)).
fof(nosub_c25_c19, axiom, ~subclass(c25, c19)).
fof(nosub_c19_c26, axiom, ~subclass(c19, c26)).
fof(nosub_c26_c19, axiom, ~subclass(c26, c19)).
fof(nosub_c19_c27, axiom, ~subclass(c19, c27)).
fof(nosub_c27_c19, axiom, ~subclass(c27, c19)).
fof(nosub_c19_c28, axiom, ~subclass(c19, c28)).
fof(nosub_c28_c19, axiom, ~subclass(c28, c19)).
fof(nosub_c19_c29, axiom, ~subclass(c19, c29)).
fof(nosub_c29_c19, axiom, ~subclass(c29, c19)).
fof(nosub_c20_c21, axiom, ~subclass(c20, c21)).
fof(nosub_c21_c20, axiom, ~subclass(c21, c20)).
fof(nosub_c20_c22, axiom, ~subclass(c20, c22)).
fof(nosub_c22_c20, axiom, ~subclass(c22, c20)).
fof(nosub_c20_c23, axiom, ~subclass(c20, c23)).
fof(nosub_c23_c20, axiom, ~subclass(c23, c20)).
fof(nosub_c20_c24, axiom, ~subclass(c20, c24)).
fof(nosub_c24_c20, axiom, ~subclass(c24, c20)).
fof(nosub_c20_c25, axiom, ~subclass(c20, c25)).
fof(nosub_c25_c20, axiom, ~subclass(c25, c20)).
fof(nosub_c20_c26, axiom, ~subclass(c20, c26)).
fof(nosub_c26_c20, axiom, ~subclass(c26, c20)).
fof(nosub_c20_c27, axiom, ~subclass(c20, c27)).
fof(nosub_c27_c20, axiom, ~subclass(c27, c20)).
fof(nosub_c20_c28, axiom, ~subclass(c20, c28)).
fof(nosub_c28_c20, axiom, ~subclass(c28, c20)).
fof(nosub_c20_c29, axiom, ~subclass(c20, c29)).
fof(nosub_c29_c20, axiom, ~subclass(c29, c20)).
fof(nosub_c21_c22, axiom, ~subclass(c21, c22)).
fof(nosub_c22_c21, axiom, ~subclass(c22, c21)).
fof(nosub_c21_c23, axiom, ~subclass(c21, c23)).
fof(nosub_c23_c21, axiom, ~subclass(c23, c21)).
fof(nosub_c21_c24, axiom, ~subclass(c21, c24)).
fof(nosub_c24_c21, axiom, ~subclass(c24, c21)).
fof(nosub_c21_c25, axiom, ~subclass(c21, c25)).
fof(nosub_c25_c21, axiom, ~subclass(c25, c21)).
fof(nosub_c21_c26, axiom, ~subclass(c21, c26)).
fof(nosub_c26_c21, axiom, ~subclass(c26, c21)).
fof(nosub_c21_c27, axiom, ~subclass(c21, c27)).
fof(nosub_c27_c21, axiom, ~subclass(c27, c21)).
fof(nosub_c21_c28, axiom, ~subclass(c21, c28)).
fof(nosub_c28_c21, axiom, ~subclass(c28, c21)).
fof(nosub_c21_c29, axiom, ~subclass(c21, c29)).
fof(nosub_c29_c21, axiom, ~subclass(c29, c21)).
fof(nosub_c22_c23, axiom, ~subclass(c22, c23)).
fof(nosub_c23_c22, axiom, ~subclass(c23, c22)).
fof(nosub_c22_c24, axiom, ~subclass(c22, c24)).
fof(nosub_c24_c22, axiom, ~subclass(c24, c22)).
fof(nosub_c22_c25, axiom, ~subclass(c22, c25)).
fof(nosub_c25_c22, axiom, ~subclass(c25, c22)).
fof(nosub_c22_c26, axiom, ~subclass(c22, c26)).
fof(nosub_c26_c22, axiom, ~subclass(c26, c22)).
fof(nosub_c22_c27, axiom, ~subclass(c22, c27)).
fof(nosub_c27_c22, axiom, ~subclass(c27, c22)).
fof(nosub_c22_c28, axiom, ~subclass(c22, c28)).
fof(nosub_c28_c22, axiom, ~subclass(c28, c22)).
fof(nosub_c22_c29, axiom, ~subclass(c22, c29)).
fof(nosub_c29_c22, axiom, ~subclass(c29, c22)).
fof(nosub_c23_c24, axiom, ~subclass(c23, c24)).
fof(nosub_c24_c23, axiom, ~subclass(c24, c23)).
fof(nosub_c23_c25, axiom, ~subclass(c23, c25)).
fof(nosub_c25_c23, axiom, ~subclass(c25, c23)).
fof(nosub_c23_c26, axiom, ~subclass(c23, c26)).
fof(nosub_c26_c23, axiom, ~subclass(c26, c23)).
fof(nosub_c23_c27, axiom, ~subclass(c23, c27)).
fof(nosub_c27_c23, axiom, ~subclass(c27, c23)).
fof(nosub_c23_c28, axiom, ~subclass(c23, c28)).
fof(nosub_c28_c23, axiom, ~subclass(c28, c23)).
fof(nosub_c23_c29, axiom, ~subclass(c23, c29)).
fof(nosub_c29_c23, axiom, ~subclass(c29, c23)).
fof(nosub_c24_c25, axiom, ~subclass(c24, c25)).
fof(nosub_c25_c24, axiom, ~subclass(c25, c24)).
fof(nosub_c24_c26, axiom, ~subclass(c24, c26)).
fof(nosub_c26_c24, axiom, ~subclass(c26, c24)).
fof(nosub_c24_c27, axiom, ~subclass(c24, c27)).
fof(nosub_c27_c24, axiom, ~subclass(c27, c24)).
fof(nosub_c24_c28, axiom, ~subclass(c24, c28)).
fof(nosub_c28_c24, axiom, ~subclass(c28, c24)).
fof(nosub_c24_c29, axiom, ~subclass(c24, c29)).
fof(nosub_c29_c24, axiom, ~subclass(c29, c24)).
fof(nosub_c25_c26, axiom, ~subclass(c25, c26)).
fof(nosub_c26_c25, axiom, ~subclass(c26, c25)).
fof(nosub_c25_c27, axiom, ~subclass(c25, c27)).
fof(nosub_c27_c25, axiom, ~subclass(c27, c25)).
fof(nosub_c25_c28, axiom, ~subclass(c25, c28)).
fof(nosub_c28_c25, axiom, ~subclass(c28, c25)).
fof(nosub_c25_c29, axiom, ~subclass(c25, c29)).
fof(nosub_c29_c25, axiom, ~subclass(c29, c25)).
fof(nosub_c26_c27, axiom, ~subclass(c26, c27)).
fof(nosub_c27_c26, axiom, ~subclass(c27, c26)).
fof(nosub_c26_c28, axiom, ~subclass(c26, c28)).
fof(nosub_c28_c26, axiom, ~subclass(c28, c26)).
fof(nosub_c26_c29, axiom, ~subclass(c26, c29)).
fof(nosub_c29_c26, axiom, ~subclass(c29, c26)).
fof(nosub_c27_c28, axiom, ~subclass(c27, c28)).
fof(nosub_c28_c27, axiom, ~subclass(c28, c27)).
fof(nosub_c27_c29, axiom, ~subclass(c27, c29)).
fof(nosub_c29_c27, axiom, ~subclass(c29, c27)).
fof(nosub_c28_c29, axiom, ~subclass(c28, c29)).
fof(nosub_c29_c28, axiom, ~subclass(c29, c28)).
fof(nosub_root_c0, axiom, ~subclass(root, c0)).
fof(nosub_root_c1, axiom, ~subclass(root, c1)).
fof(nosub_root_c2, axiom, ~subclass(root, c2)).
fof(nosub_root_c3, axiom, ~subclass(root, c3)).
fof(nosub_root_c4, axiom, ~subclass(root, c4)).
fof(nosub_root_c5, axiom, ~subclass(root, c5)).
fof(nosub_root_c6, axiom, ~subclass(root, c6)).
fof(nosub_root_c7, axiom, ~subclass(root, c7)).
fof(nosub_root_c8, axiom, ~subclass(root, c8)).
fof(nosub_root_c9, axiom, ~subclass(root, c9)).
fof(nosub_root_c10, axiom, ~subclass(root, c10)).
fof(nosub_root_c11, axiom, ~subclass(root, c11)).
fof(nosub_root_c12, axiom, ~subclass(root, c12)).
fof(nosub_root_c13, axiom, ~subclass(root, c13)).
fof(nosub_root_c14, axiom, ~subclass(root, c14)).
fof(nosub_root_c15, axiom, ~subclass(root, c15)).
fof(nosub_root_c16, axiom, ~subclass(root, c16)).
fof(nosub_root_c17, axiom, ~subclass(root, c17)).
fof(nosub_root_c18, axiom, ~subclass(root, c18)).
fof(nosub_root_c19, axiom, ~subclass(root, c19)).
fof(nosub_root_c20, axiom, ~subclass(root, c20)).
fof(nosub_root_c21, axiom, ~subclass(root, c21)).
fof(nosub_root_c22, axiom, ~subclass(root, c22)).
fof(nosub_root_c23, axiom, ~subclass(root, c23)).
fof(nosub_root_c24, axiom, ~subclass(root, c24)).
fof(nosub_root_c25, axiom, ~subclass(root, c25)).
fof(nosub_root_c26, axiom, ~subclass(root, c26)).
fof(nosub_root_c27, axiom, ~subclass(root, c27)).
fof(nosub_root_c28, axiom, ~subclass(root, c28)).
fof(nosub_root_c29, axiom, ~subclass(root, c29)).
fof(closure, axiom, ![X]: (concept(X) => (X = c0 | X = c1 | X = c2 | X = c3 | X = c4 | X = c5 | X = c6 | X = c7 | X = c8 | X = c9 | X = c10 | X = c11 | X = c12 | X = c13 | X = c14 | X = c15 | X = c16 | X = c17 | X = c18 | X = c19 | X = c20 | X = c21 | X = c22 | X = c23 | X = c24 | X = c25 | X = c26 | X = c27 | X = c28 | X = c29 | X = root))).
fof(den1, axiom, ![X]: (inDen1(X) <=> (concept(X) & (X = c0 | X = c1 | X = c2 | X = c3 | X = c4 | X = c5 | X = c6 | X = c7 | X = c8 | X = c9 | X = c10 | X = c11 | X = c12 | X = c13 | X = c14)))).
fof(den2, axiom, ![X]: (inDen2(X) <=> (concept(X) & (X = c15 | X = c16 | X = c17 | X = c18 | X = c19 | X = c20 | X = c21 | X = c22 | X = c23 | X = c24 | X = c25 | X = c26 | X = c27 | X = c28 | X = c29)))).
fof(conjecture, conjecture, ~?[X]: (inDen1(X) & inDen2(X))).
