%--------------------------------------------------------------------------
% File     : ODRL649-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : or vs xone: differ when two branch pairs compatible
% Version  : 1.0
% English  : sec:composition: or and xone give different verdicts when
%           : both branch pairs are compatible:
%           : or_verdict(compat,compat)=compat but xone_verdict(compat,compat)=unknown.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL649-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL649-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl649, conjecture,
    or_verdict(compatible, compatible) = compatible &
    xone_verdict(compatible, compatible) = unknown).
%--------------------------------------------------------------------------
