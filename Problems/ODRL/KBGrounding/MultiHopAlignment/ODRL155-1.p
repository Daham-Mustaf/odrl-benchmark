%--------------------------------------------------------------------------
% File     : ODRL155-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Proposition 2 (3-hop) — 4-Dataspace Compatible
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Proposition 2 (3-hop) — 4-Dataspace Compatible
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand comp:complianceScope ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand comp:gdprFull ] ] .
%
% Formal test:
%   isPartOf(complianceScope) ∩ eq(gdprFull) → Compatible
%   %   Witness: gdprFull (leq(gdprFull, complianceScope) ∧ gdprFull = gdprFull)
%   %   Tests: compatibility query in 4-KB context with 3 alignment bridges.
%
% One-liner : 3-hop compatible: isPartOf(complianceScope) ∩ eq(gdprFull) ≠ ∅
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
% --- Synthetic KB (SYNTH) — NO native disjointness ---
% Concepts align to ISO 3166 but have no sibling disjointness.
% Disjointness must be derived through 2-hop alignment from GEO.
fof(synth_root, axiom, concept(euZone)).
fof(synth_c1, axiom, concept(zoneWest)).
fof(synth_c2, axiom, concept(zoneEast)).

fof(synth_leq1, axiom, leq(zoneWest, euZone)).
fof(synth_leq2, axiom, leq(zoneEast, euZone)).
fof(synth_refl1, axiom, leq(euZone, euZone)).
fof(synth_refl2, axiom, leq(zoneWest, zoneWest)).
fof(synth_refl3, axiom, leq(zoneEast, zoneEast)).

% NO disjoint axiom — must come from 2-hop alignment
fof(synth_una, axiom, $distinct(euZone, zoneWest, zoneEast)).
% Alignment: ISO 3166 → SYNTH (regulatory zones)
fof(align_iso_synth_1, axiom, align(europe, euZone)).
fof(align_iso_synth_2, axiom, align(dE, zoneWest)).
fof(align_iso_synth_3, axiom, align(pL, zoneEast)).
% --- Compliance KB (COMP) — NO native disjointness ---
% 4th dataspace: GDPR compliance tier classification.
% Concepts align to SYNTH (regulatory zones) but have no sibling disjointness.
% Disjointness must be derived through 3-hop alignment: GEO → ISO → SYNTH → COMP.
fof(comp_root, axiom, concept(complianceScope)).
fof(comp_c1, axiom, concept(gdprFull)).
fof(comp_c2, axiom, concept(gdprPartial)).

fof(comp_leq1, axiom, leq(gdprFull, complianceScope)).
fof(comp_leq2, axiom, leq(gdprPartial, complianceScope)).
fof(comp_refl1, axiom, leq(complianceScope, complianceScope)).
fof(comp_refl2, axiom, leq(gdprFull, gdprFull)).
fof(comp_refl3, axiom, leq(gdprPartial, gdprPartial)).

% NO disjoint axiom — must come from 3-hop alignment
fof(comp_una, axiom, $distinct(complianceScope, gdprFull, gdprPartial)).
% Alignment: SYNTH (regulatory zones) → COMP (compliance tiers)
fof(align_synth_comp_1, axiom, align(euZone, complianceScope)).
fof(align_synth_comp_2, axiom, align(zoneWest, gdprFull)).
fof(align_synth_comp_3, axiom, align(zoneEast, gdprPartial)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl155, conjecture,
    ?[X]: ( in_denotation(X, complianceScope, isPartOf)
          & in_denotation(X, gdprFull, eq) )).

%--------------------------------------------------------------------------