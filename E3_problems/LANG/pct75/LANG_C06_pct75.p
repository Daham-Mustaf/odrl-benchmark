%--------------------------------------------------------------------------
% File     : LANG_C06_pct75.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection — E3 Incompleteness Sweep
% KB       : LANG
% Level    : pct75 (75% disjointness removed)
% Problem  : LANG_C06
% Expected : Unknown_or_Theorem
% Operator : isPartOf
% Date     : 2026-02-28
% Purpose  : E3 — Validate graceful degradation over incomplete hierarchies
%--------------------------------------------------------------------------

include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Inline KB (LANG, 75% incomplete) ──────────────────────────
fof(lang_c_all,  axiom, concept(allLanguages)).
fof(lang_c_en,   axiom, concept(en)).
fof(lang_c_de,   axiom, concept(deLang)).
fof(lang_c_fr,   axiom, concept(frLang)).
fof(lang_c_nl,   axiom, concept(nlLang)).
fof(lang_c_es,   axiom, concept(esLang)).
fof(lang_c_enGB, axiom, concept(enGB)).
fof(lang_c_enUS, axiom, concept(enUS)).
fof(lang_c_enAU, axiom, concept(enAU)).
fof(lang_c_deAT, axiom, concept(deAT)).
fof(lang_c_deCH, axiom, concept(deCH)).
fof(lang_c_frCH, axiom, concept(frCH)).
fof(lang_c_frBE, axiom, concept(frBE)).
% Hierarchy
fof(lang_leq_en_all,   axiom, leq(en,   allLanguages)).
fof(lang_leq_de_all,   axiom, leq(deLang, allLanguages)).
fof(lang_leq_fr_all,   axiom, leq(frLang, allLanguages)).
fof(lang_leq_nl_all,   axiom, leq(nlLang, allLanguages)).
fof(lang_leq_es_all,   axiom, leq(esLang, allLanguages)).
fof(lang_leq_enGB_en,  axiom, leq(enGB, en)).
fof(lang_leq_enUS_en,  axiom, leq(enUS, en)).
fof(lang_leq_enAU_en,  axiom, leq(enAU, en)).
fof(lang_leq_deAT_de,  axiom, leq(deAT, deLang)).
fof(lang_leq_deCH_de,  axiom, leq(deCH, deLang)).
fof(lang_leq_frCH_fr,  axiom, leq(frCH, frLang)).
fof(lang_leq_frBE_fr,  axiom, leq(frBE, frLang)).
% Reflexivity
fof(lang_refl_all,  axiom, leq(allLanguages, allLanguages)).
fof(lang_refl_en,   axiom, leq(en,     en)).
fof(lang_refl_de,   axiom, leq(deLang, deLang)).
fof(lang_refl_fr,   axiom, leq(frLang, frLang)).
fof(lang_refl_nl,   axiom, leq(nlLang, nlLang)).
fof(lang_refl_es,   axiom, leq(esLang, esLang)).
fof(lang_refl_enGB, axiom, leq(enGB, enGB)).
fof(lang_refl_enUS, axiom, leq(enUS, enUS)).
fof(lang_refl_enAU, axiom, leq(enAU, enAU)).
fof(lang_refl_deAT, axiom, leq(deAT, deAT)).
fof(lang_refl_deCH, axiom, leq(deCH, deCH)).
fof(lang_refl_frCH, axiom, leq(frCH, frCH)).
fof(lang_refl_frBE, axiom, leq(frBE, frBE)).
fof(lang_trans, axiom, ![X,Y,Z]: (leq(X,Y) & leq(Y,Z) => leq(X,Z))).
fof(lang_una, axiom, $distinct(allLanguages, en, deLang, frLang, nlLang, esLang,
    enGB, enUS, enAU, deAT, deCH, frCH, frBE)).

% LANG disjointness: 6/25 kept (75% removed)
fof(lang_disj_en_de, axiom, disjoint(en,deLang)).
fof(lang_disj_en_de_sym, axiom, disjoint(deLang,en)).
fof(lang_disj_en_fr, axiom, disjoint(en,frLang)).
fof(lang_disj_en_fr_sym, axiom, disjoint(frLang,en)).
fof(lang_disj_en_nl, axiom, disjoint(en,nlLang)).
fof(lang_disj_en_nl_sym, axiom, disjoint(nlLang,en)).
fof(lang_disj_en_es, axiom, disjoint(en,esLang)).
fof(lang_disj_en_es_sym, axiom, disjoint(esLang,en)).
fof(lang_disj_de_fr, axiom, disjoint(deLang,frLang)).
fof(lang_disj_de_fr_sym, axiom, disjoint(frLang,deLang)).
fof(lang_disj_de_nl, axiom, disjoint(deLang,nlLang)).
fof(lang_disj_de_nl_sym, axiom, disjoint(nlLang,deLang)).

% ─── Conjecture ──────────────────────────────────────────────────────────
fof(lang_c06, conjecture, ![X]: ~(in_denotation(X,enUS,isPartOf) & in_denotation(X,deLang,isPartOf))).

%--------------------------------------------------------------------------
