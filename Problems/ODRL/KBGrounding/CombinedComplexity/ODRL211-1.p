%--------------------------------------------------------------------------
% File     : ODRL211-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : 3-Hop + isNoneOf — Complement in 4th Dataspace
% Expected : Theorem
% Verdict  : Compatible
% Paper    : 3-Hop + isNoneOf — Complement in 4th Dataspace
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isNoneOf ;
%   %         odrl:rightOperand ( comp:gdprFull ) ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand comp:gdprPartial ] ] .
%
% Formal test:
%   isNoneOf({gdprFull}) ∩ isPartOf(gdprPartial) in 4th dataspace.
%   %   3-hop: GEO→ISO→SYNTH→COMP derives disj(gdprFull, gdprPartial)
%   %   → ↓gdprPartial ⊆ (C_comp \ ↓gdprFull) = isNoneOf({gdprFull})
%   %   → overlap = ↓gdprPartial ≠ ∅
%   %   Extreme: isNoneOf + 3-hop alignment + disjointness → complement inclusion.
%
% One-liner : 3-hop + isNoneOf: complement in 4th dataspace via alignment
% Difficulty: Extreme
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_extreme_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
% --- Synthetic KB (SYNTH) — NO native disjointness ---
fof(synth_root, axiom, concept(euZone)).
fof(synth_c1, axiom, concept(zoneWest)).
fof(synth_c2, axiom, concept(zoneEast)).
fof(synth_leq1, axiom, leq(zoneWest, euZone)).
fof(synth_leq2, axiom, leq(zoneEast, euZone)).
fof(synth_refl1, axiom, leq(euZone, euZone)).
fof(synth_refl2, axiom, leq(zoneWest, zoneWest)).
fof(synth_refl3, axiom, leq(zoneEast, zoneEast)).
fof(synth_una, axiom, $distinct(euZone, zoneWest, zoneEast)).
% Alignment: ISO 3166 → SYNTH
fof(align_iso_synth_1, axiom, align(europe, euZone)).
fof(align_iso_synth_2, axiom, align(dE, zoneWest)).
fof(align_iso_synth_3, axiom, align(pL, zoneEast)).
% --- Compliance KB (COMP) — NO native disjointness ---
fof(comp_root, axiom, concept(complianceScope)).
fof(comp_c1, axiom, concept(gdprFull)).
fof(comp_c2, axiom, concept(gdprPartial)).
fof(comp_leq1, axiom, leq(gdprFull, complianceScope)).
fof(comp_leq2, axiom, leq(gdprPartial, complianceScope)).
fof(comp_refl1, axiom, leq(complianceScope, complianceScope)).
fof(comp_refl2, axiom, leq(gdprFull, gdprFull)).
fof(comp_refl3, axiom, leq(gdprPartial, gdprPartial)).
fof(comp_una, axiom, $distinct(complianceScope, gdprFull, gdprPartial)).
% Alignment: SYNTH → COMP
fof(align_synth_comp_1, axiom, align(euZone, complianceScope)).
fof(align_synth_comp_2, axiom, align(zoneWest, gdprFull)).
fof(align_synth_comp_3, axiom, align(zoneEast, gdprPartial)).
fof(list_211, axiom, in_value_list(gdprFull, noneList211)).
fof(list_noneList211_closed, axiom,
    ![G]: (in_value_list(G, noneList211) => (G = gdprFull))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl211, conjecture,
    ?[X]: ( in_denotation_set(X, noneList211, isNoneOf)
          & in_denotation(X, gdprPartial, isPartOf) )).

%--------------------------------------------------------------------------