%--------------------------------------------------------------------------
% File     : ODRL635-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : unknown_sound: box verdict is Unknown when axis unconstrained
% Version  : 1.0
% English  : thm:unknown-sound: box_verdict(compatible, unknown) = unknown.
%           : One axis compatible, one axis unconstrained => Unknown overall.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL635-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL635-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMPL000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl635, conjecture,
    box_verdict(compatible, unknown) = unknown).
%--------------------------------------------------------------------------
