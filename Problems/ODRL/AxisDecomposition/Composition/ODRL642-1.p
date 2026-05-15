%--------------------------------------------------------------------------
% File     : ODRL642-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : or_unknown: unknown and conflict implies or=unknown
% Version  : 1.0
% English  : sec:composition or_unknown:
%           : or_verdict(unknown, conflict) = unknown.
%           : Neither is compatible; not both conflict => unknown.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL642-1.p
%
% Status   : Theorem
% Verdict  : Unknown
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL642-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl642, conjecture,
    or_verdict(unknown, conflict) = unknown).
%--------------------------------------------------------------------------
