%--------------------------------------------------------------------------
% File     : ODRL313-1 : TPTP v9.0.0. Released v9.1.0.
% Domain   : Policy (ODRL)
% Problem  : ValueSet-10 compatible
% Version  : [Mus26] axioms : Scaled.
% English  : Scaled benchmark with 10 concepts.
% Refs     : [Mus26] Mustafa, D. (2026), Grounding ODRL Constraints.
% Source   : [Mus26]
% Names    : ODRL313-1 [Mus26]
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
fof(una_c0_root, axiom, c0 != root).
fof(una_c1_c2, axiom, c1 != c2).
fof(una_c1_c3, axiom, c1 != c3).
fof(una_c1_c4, axiom, c1 != c4).
fof(una_c1_c5, axiom, c1 != c5).
fof(una_c1_c6, axiom, c1 != c6).
fof(una_c1_c7, axiom, c1 != c7).
fof(una_c1_c8, axiom, c1 != c8).
fof(una_c1_c9, axiom, c1 != c9).
fof(una_c1_root, axiom, c1 != root).
fof(una_c2_c3, axiom, c2 != c3).
fof(una_c2_c4, axiom, c2 != c4).
fof(una_c2_c5, axiom, c2 != c5).
fof(una_c2_c6, axiom, c2 != c6).
fof(una_c2_c7, axiom, c2 != c7).
fof(una_c2_c8, axiom, c2 != c8).
fof(una_c2_c9, axiom, c2 != c9).
fof(una_c2_root, axiom, c2 != root).
fof(una_c3_c4, axiom, c3 != c4).
fof(una_c3_c5, axiom, c3 != c5).
fof(una_c3_c6, axiom, c3 != c6).
fof(una_c3_c7, axiom, c3 != c7).
fof(una_c3_c8, axiom, c3 != c8).
fof(una_c3_c9, axiom, c3 != c9).
fof(una_c3_root, axiom, c3 != root).
fof(una_c4_c5, axiom, c4 != c5).
fof(una_c4_c6, axiom, c4 != c6).
fof(una_c4_c7, axiom, c4 != c7).
fof(una_c4_c8, axiom, c4 != c8).
fof(una_c4_c9, axiom, c4 != c9).
fof(una_c4_root, axiom, c4 != root).
fof(una_c5_c6, axiom, c5 != c6).
fof(una_c5_c7, axiom, c5 != c7).
fof(una_c5_c8, axiom, c5 != c8).
fof(una_c5_c9, axiom, c5 != c9).
fof(una_c5_root, axiom, c5 != root).
fof(una_c6_c7, axiom, c6 != c7).
fof(una_c6_c8, axiom, c6 != c8).
fof(una_c6_c9, axiom, c6 != c9).
fof(una_c6_root, axiom, c6 != root).
fof(una_c7_c8, axiom, c7 != c8).
fof(una_c7_c9, axiom, c7 != c9).
fof(una_c7_root, axiom, c7 != root).
fof(una_c8_c9, axiom, c8 != c9).
fof(una_c8_root, axiom, c8 != root).
fof(una_c9_root, axiom, c9 != root).
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
fof(nosub_c5_c6, axiom, ~subclass(c5, c6)).
fof(nosub_c6_c5, axiom, ~subclass(c6, c5)).
fof(nosub_c5_c7, axiom, ~subclass(c5, c7)).
fof(nosub_c7_c5, axiom, ~subclass(c7, c5)).
fof(nosub_c5_c8, axiom, ~subclass(c5, c8)).
fof(nosub_c8_c5, axiom, ~subclass(c8, c5)).
fof(nosub_c5_c9, axiom, ~subclass(c5, c9)).
fof(nosub_c9_c5, axiom, ~subclass(c9, c5)).
fof(nosub_c6_c7, axiom, ~subclass(c6, c7)).
fof(nosub_c7_c6, axiom, ~subclass(c7, c6)).
fof(nosub_c6_c8, axiom, ~subclass(c6, c8)).
fof(nosub_c8_c6, axiom, ~subclass(c8, c6)).
fof(nosub_c6_c9, axiom, ~subclass(c6, c9)).
fof(nosub_c9_c6, axiom, ~subclass(c9, c6)).
fof(nosub_c7_c8, axiom, ~subclass(c7, c8)).
fof(nosub_c8_c7, axiom, ~subclass(c8, c7)).
fof(nosub_c7_c9, axiom, ~subclass(c7, c9)).
fof(nosub_c9_c7, axiom, ~subclass(c9, c7)).
fof(nosub_c8_c9, axiom, ~subclass(c8, c9)).
fof(nosub_c9_c8, axiom, ~subclass(c9, c8)).
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
fof(closure, axiom, ![X]: (concept(X) => (X = c0 | X = c1 | X = c2 | X = c3 | X = c4 | X = c5 | X = c6 | X = c7 | X = c8 | X = c9 | X = root))).
fof(den1, axiom, ![X]: (inDen1(X) <=> (concept(X) & (X = c0 | X = c1 | X = c2 | X = c3 | X = c4 | X = c5 | X = c6 | X = c7 | X = c8 | X = c9)))).
fof(den2, axiom, ![X]: (inDen2(X) <=> (concept(X) & ~(X = c0 | X = c1 | X = c2 | X = c3 | X = c4)))).
fof(conjecture, conjecture, ?[X]: (inDen1(X) & inDen2(X))).
