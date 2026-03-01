%--------------------------------------------------------------------------
% File     : E4_C2_06.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection — E4 Cross-Dataspace
% Problem  : E4_C2_06
% Expected : Unknown
% Operator : isPartOf
% Case     : Case2-AsymmetricKB: proof grounded against Consumer KB_B only
% Date     : 2026-02-28
% Purpose  : E4 — Validate no false positives across dataspace boundaries
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
% Policy pair: Provider: Permit location=germany / Consumer: Prohibit location=france
% Note: FP-RISK: de⊥fr in KB_A only; KB_B: both≤wE, no sibling disj
% KB_A (Provider, full GEO — NOT used for proof — shown for reference)
% disj(westernEurope,easternEurope)
% disj(germany,france)
% disj(germany,italy)
% disj(germany,belgium)
% disj(germany,netherlands)
% disj(germany,spain)
% disj(france,italy)
% disj(france,belgium)
% disj(france,netherlands)
% disj(france,spain)
% disj(italy,belgium)
% disj(italy,netherlands)
% disj(italy,spain)
% disj(belgium,netherlands)
% disj(belgium,spain)
% disj(netherlands,spain)
% disj(poland,czechia)
% disj(germany,poland)
% disj(germany,czechia)
% disj(france,poland)
% disj(france,czechia)
% disj(italy,poland)
% disj(italy,czechia)
% disj(belgium,poland)
% disj(belgium,czechia)
% disj(netherlands,poland)
% disj(netherlands,czechia)
% disj(spain,poland)
% disj(spain,czechia)
% disj(bavaria,france)
% disj(bavaria,poland)
% disj(bavaria,italy)

% ─── KB_B Consumer KB (GEO, root disjointness only) ───────────────────
% Architecture: conflict detection grounded against Consumer KB_B.
% KB_A richer disjointness is NOT imported (no false positive by design).
fof(geo_c_eu,  axiom, concept(europe)).
fof(geo_c_wE,  axiom, concept(westernEurope)).
fof(geo_c_eE,  axiom, concept(easternEurope)).
fof(geo_c_de,  axiom, concept(germany)).
fof(geo_c_fr,  axiom, concept(france)).
fof(geo_c_it,  axiom, concept(italy)).
fof(geo_c_be,  axiom, concept(belgium)).
fof(geo_c_nl,  axiom, concept(netherlands)).
fof(geo_c_es,  axiom, concept(spain)).
fof(geo_c_pl,  axiom, concept(poland)).
fof(geo_c_cz,  axiom, concept(czechia)).
fof(geo_c_bav, axiom, concept(bavaria)).
fof(geo_leq_wE_eu,  axiom, leq(westernEurope, europe)).
fof(geo_leq_eE_eu,  axiom, leq(easternEurope, europe)).
fof(geo_leq_de_wE,  axiom, leq(germany, westernEurope)).
fof(geo_leq_fr_wE,  axiom, leq(france, westernEurope)).
fof(geo_leq_it_wE,  axiom, leq(italy, westernEurope)).
fof(geo_leq_be_wE,  axiom, leq(belgium, westernEurope)).
fof(geo_leq_nl_wE,  axiom, leq(netherlands, westernEurope)).
fof(geo_leq_es_wE,  axiom, leq(spain, westernEurope)).
fof(geo_leq_pl_eE,  axiom, leq(poland, easternEurope)).
fof(geo_leq_cz_eE,  axiom, leq(czechia, easternEurope)).
fof(geo_leq_bav_de, axiom, leq(bavaria, germany)).
fof(geo_refl_eu,  axiom, leq(europe, europe)).
fof(geo_refl_wE,  axiom, leq(westernEurope, westernEurope)).
fof(geo_refl_eE,  axiom, leq(easternEurope, easternEurope)).
fof(geo_refl_de,  axiom, leq(germany, germany)).
fof(geo_refl_fr,  axiom, leq(france, france)).
fof(geo_refl_it,  axiom, leq(italy, italy)).
fof(geo_refl_be,  axiom, leq(belgium, belgium)).
fof(geo_refl_nl,  axiom, leq(netherlands, netherlands)).
fof(geo_refl_es,  axiom, leq(spain, spain)).
fof(geo_refl_pl,  axiom, leq(poland, poland)).
fof(geo_refl_cz,  axiom, leq(czechia, czechia)).
fof(geo_refl_bav, axiom, leq(bavaria, bavaria)).
fof(geo_trans, axiom, ![X,Y,Z]: (leq(X,Y) & leq(Y,Z) => leq(X,Z))).
fof(geo_una, axiom, $distinct(europe, westernEurope, easternEurope,
    germany, france, italy, belgium, netherlands, spain,
    poland, czechia, bavaria)).
fof(geo_disj_wE_eE, axiom, disjoint(westernEurope,easternEurope)).
fof(geo_disj_wE_eE_sym, axiom, disjoint(easternEurope,westernEurope)).
% ─── Conjecture ─────────────────────────────────────────────────────────────
fof(e4_c2_06, conjecture, ![X]: ~(in_denotation(X,germany,isPartOf) & in_denotation(X,france,isPartOf))).
%--------------------------------------------------------------------------
