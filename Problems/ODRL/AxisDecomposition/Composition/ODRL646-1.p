%--------------------------------------------------------------------------
% File     : ODRL646-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : xone_unknown: both pairs compatible implies xone=unknown
% Version  : 1.0
% English  : sec:composition xone_unknown:
%           : xone_verdict(compatible, compatible) = unknown.
%           : Vr=MAX(rest)=compatible => >=2 branch pairs overlap => xone requires
%           : exactly one, so result is unknown.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL646-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL646-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl646, conjecture,
    xone_verdict(compatible, compatible) = unknown).
%--------------------------------------------------------------------------
