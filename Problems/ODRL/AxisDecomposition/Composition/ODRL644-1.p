%--------------------------------------------------------------------------
% File     : ODRL644-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : xone_compat: one match compatible rest conflict => xone=compatible
% Version  : 1.0
% English  : sec:composition xone_compat:
%           : xone_verdict(compatible, conflict) = compatible.
%           : Exactly one branch pair overlaps, rest conflict (Vr=MAX of rest=conflict).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL644-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL644-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl644, conjecture,
    xone_verdict(compatible, conflict) = compatible).
%--------------------------------------------------------------------------
