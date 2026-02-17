%--------------------------------------------------------------------------
% File     : ODRL214-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Runtime + Alignment + Set Ops — Full Stack
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Runtime + Alignment + Set Ops — Full Stack
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand synth:euZone ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand synth:zoneWest ] ] .
%
% Formal test:
%   Full-stack: runtime context + alignment infrastructure + denotation.
%   %   Runtime: assigns(omega214, zoneWest) → satisfies(omega214, euZone, isPartOf)
%   %   Denotation: isPartOf(euZone) ∩ eq(zoneWest) → witness: zoneWest
%   %   With RUNTIME + ALIGN + 3 KBs loaded simultaneously.
%   %   Extreme: tests interaction between runtime and denotation semantics.
%
% One-liner : Full stack: runtime + alignment + denotation in 3-KB context
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
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').

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

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl214_ctx, axiom, assigns(omega214, zoneWest)).

fof(odrl214, conjecture,
    ( ?[X]: ( in_denotation(X, euZone, isPartOf)
            & in_denotation(X, zoneWest, eq) )
    & satisfies(omega214, euZone, isPartOf) )).

%--------------------------------------------------------------------------