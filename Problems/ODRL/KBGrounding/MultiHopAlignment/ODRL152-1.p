%--------------------------------------------------------------------------
% File     : ODRL152-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : 2-Hop Ablation — SYNTH Alone Cannot Detect Conflict
% Expected : CounterSatisfiable
% Verdict  : Unknown
% Paper    : 2-Hop Ablation — SYNTH Alone Cannot Detect Conflict
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
%   Same query as ODRL150 but WITHOUT GEO/ISO/alignment.
%   %   SYNTH_NO_DISJ has no disjoint axioms → prover cannot derive disjoint(zoneWest, zoneEast).
%   %   → Unknown (CounterSatisfiable timeout).
%
% One-liner : Ablation: SYNTH alone → Unknown (no disjointness)
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

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

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl152, conjecture,
    ?[X]: ( in_denotation(X, zoneWest, isPartOf)
          & in_denotation(X, zoneEast, isPartOf) )).

%--------------------------------------------------------------------------