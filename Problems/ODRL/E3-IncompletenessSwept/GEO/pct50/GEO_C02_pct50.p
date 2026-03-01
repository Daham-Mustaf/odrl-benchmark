%--------------------------------------------------------------------------
% File     : GEO_C02_pct50.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection — E3 Incompleteness Sweep
% KB       : GEO
% Level    : pct50 (50% disjointness removed)
% Problem  : GEO_C02
% Expected : Unknown_or_Theorem
% Operator : isPartOf
% Date     : 2026-02-28
% Purpose  : E3 — Validate graceful degradation over incomplete hierarchies
%--------------------------------------------------------------------------

include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Inline KB (GEO, 50% incomplete) ──────────────────────────
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
fof(geo_refl_eu,  axiom, leq(europe,  europe)).
fof(geo_refl_wE,  axiom, leq(westernEurope, westernEurope)).
fof(geo_refl_eE,  axiom, leq(easternEurope, easternEurope)).
fof(geo_refl_de,  axiom, leq(germany, germany)).
fof(geo_refl_fr,  axiom, leq(france,  france)).
fof(geo_refl_it,  axiom, leq(italy,   italy)).
fof(geo_refl_be,  axiom, leq(belgium, belgium)).
fof(geo_refl_nl,  axiom, leq(netherlands, netherlands)).
fof(geo_refl_es,  axiom, leq(spain,   spain)).
fof(geo_refl_pl,  axiom, leq(poland,  poland)).
fof(geo_refl_cz,  axiom, leq(czechia, czechia)).
fof(geo_refl_bav, axiom, leq(bavaria, bavaria)).
fof(geo_trans, axiom, ![X,Y,Z]: (leq(X,Y) & leq(Y,Z) => leq(X,Z))).
fof(geo_una, axiom, $distinct(europe, westernEurope, easternEurope,
    germany, france, italy, belgium, netherlands, spain,
    poland, czechia, bavaria)).

% GEO disjointness: 16/32 kept (50% removed)
fof(geo_disj_wE_eE, axiom, disjoint(westernEurope,easternEurope)).
fof(geo_disj_wE_eE_sym, axiom, disjoint(easternEurope,westernEurope)).
fof(geo_disj_de_fr, axiom, disjoint(germany,france)).
fof(geo_disj_de_fr_sym, axiom, disjoint(france,germany)).
fof(geo_disj_de_it, axiom, disjoint(germany,italy)).
fof(geo_disj_de_it_sym, axiom, disjoint(italy,germany)).
fof(geo_disj_de_be, axiom, disjoint(germany,belgium)).
fof(geo_disj_de_be_sym, axiom, disjoint(belgium,germany)).
fof(geo_disj_de_nl, axiom, disjoint(germany,netherlands)).
fof(geo_disj_de_nl_sym, axiom, disjoint(netherlands,germany)).
fof(geo_disj_de_es, axiom, disjoint(germany,spain)).
fof(geo_disj_de_es_sym, axiom, disjoint(spain,germany)).
fof(geo_disj_fr_it, axiom, disjoint(france,italy)).
fof(geo_disj_fr_it_sym, axiom, disjoint(italy,france)).
fof(geo_disj_fr_be, axiom, disjoint(france,belgium)).
fof(geo_disj_fr_be_sym, axiom, disjoint(belgium,france)).
fof(geo_disj_fr_nl, axiom, disjoint(france,netherlands)).
fof(geo_disj_fr_nl_sym, axiom, disjoint(netherlands,france)).
fof(geo_disj_fr_es, axiom, disjoint(france,spain)).
fof(geo_disj_fr_es_sym, axiom, disjoint(spain,france)).
fof(geo_disj_it_be, axiom, disjoint(italy,belgium)).
fof(geo_disj_it_be_sym, axiom, disjoint(belgium,italy)).
fof(geo_disj_it_nl, axiom, disjoint(italy,netherlands)).
fof(geo_disj_it_nl_sym, axiom, disjoint(netherlands,italy)).
fof(geo_disj_it_es, axiom, disjoint(italy,spain)).
fof(geo_disj_it_es_sym, axiom, disjoint(spain,italy)).
fof(geo_disj_be_nl, axiom, disjoint(belgium,netherlands)).
fof(geo_disj_be_nl_sym, axiom, disjoint(netherlands,belgium)).
fof(geo_disj_be_es, axiom, disjoint(belgium,spain)).
fof(geo_disj_be_es_sym, axiom, disjoint(spain,belgium)).
fof(geo_disj_nl_es, axiom, disjoint(netherlands,spain)).
fof(geo_disj_nl_es_sym, axiom, disjoint(spain,netherlands)).

% ─── Conjecture ──────────────────────────────────────────────────────────
fof(geo_c02, conjecture, ![X]: ~(in_denotation(X,germany,isPartOf) & in_denotation(X,france,isPartOf))).

%--------------------------------------------------------------------------
