%--------------------------------------------------------------------------
% File     : ODRL157-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : 3-Hop Intermediate — Hop 2 Result as Prerequisite
% Expected : Theorem
% Verdict  : Conflict
% Paper    : 3-Hop Intermediate — Hop 2 Result as Prerequisite
%
% ODRL Policy (Conceptual):
%   (Proves hop 2 intermediate: disj(zoneWest, zoneEast) for ODRL154 hop 3)
%
% Formal test:
%   2-hop alignment: GEO → ISO → SYNTH
%   %   disj(wE,eE) → disj(de,pl) → disj(dE,pL) → disj(zoneWest,zoneEast)
%   %   Tests: hop 2 result that feeds into ODRL154.
%
% One-liner : Intermediate: hop 2 derives disjoint(zoneWest, zoneEast)
% Difficulty: Hard
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

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl157, conjecture, disjoint(zoneWest, zoneEast)).

%--------------------------------------------------------------------------