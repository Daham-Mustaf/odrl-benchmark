%--------------------------------------------------------------------------
% File     : ODRL150-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Proposition 2 (2-hop) — Multi-Hop Alignment Conflict
% Expected : CounterSatisfiable
% Verdict  : Conflict
% Paper    : Proposition 2 (2-hop) — Multi-Hop Alignment Conflict
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand synth:zoneWest ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand synth:zoneEast ] ] .
%
% Formal test:
%   2-hop alignment chain: GEO → ISO → SYNTH
%   %   GEO: disj(wE,eE) → disj_downward → disj(de,pl)
%   %   Hop 1: align(de,dE) + align(pl,pL) + align_disj_forward → disj(dE,pL)
%   %   Hop 2: align(dE,zoneWest) + align(pL,zoneEast) + align_disj_forward
%   %          → disj(zoneWest, zoneEast)
%   %   → ⟦isPartOf(zoneWest)⟧ ∩ ⟦isPartOf(zoneEast)⟧ = ∅ → Conflict
%
% One-liner : 2-hop alignment: GEO→ISO→SYNTH conflict detection
% Difficulty: Very Hard
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
fof(odrl150, conjecture,
    ?[X]: ( in_denotation(X, zoneWest, isPartOf)
          & in_denotation(X, zoneEast, isPartOf) )).

%--------------------------------------------------------------------------