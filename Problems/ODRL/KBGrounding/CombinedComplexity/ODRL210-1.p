%--------------------------------------------------------------------------
% File     : ODRL210-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Multi-Hop + Set Operators — isAnyOf in Aligned KB
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Multi-Hop + Set Operators — isAnyOf in Aligned KB
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAnyOf ;
%   %         odrl:rightOperand ( synth:zoneWest synth:zoneEast ) ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand synth:euZone ] ] .
%
% Formal test:
%   Set operator in aligned KB: isAnyOf({zoneWest,zoneEast}) ∩ isPartOf(euZone)
%   %   Both ≤ euZone → union ⊆ ↓euZone → overlap ≠ ∅
%   %   With 3 loaded KBs (GEO+ISO+SYNTH) and 2 alignment bridges.
%   %   Extreme: set operators + 3-KB context + alignment infrastructure.
%
% One-liner : Multi-hop + set ops: isAnyOf in aligned KB
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
fof(list_210_1, axiom, in_value_list(zoneWest, anyList210)).
fof(list_210_2, axiom, in_value_list(zoneEast, anyList210)).
fof(list_anyList210_closed, axiom,
    ![G]: (in_value_list(G, anyList210) => (G = zoneWest | G = zoneEast))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl210, conjecture,
    ?[X]: ( in_denotation_set(X, anyList210, isAnyOf)
          & in_denotation(X, euZone, isPartOf) )).

%--------------------------------------------------------------------------