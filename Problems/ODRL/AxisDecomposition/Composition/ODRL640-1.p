%--------------------------------------------------------------------------
% File     : ODRL640-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : or_compat: V1=compatible implies or_verdict=compatible
% Version  : 1.0
% English  : sec:composition or_compat: is_verdict(V2) =>
%           : or_verdict(compatible, V2) = compatible.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL640-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL640-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl640, conjecture,
    ![V2]: (is_verdict(V2) =>
    or_verdict(compatible, V2) = compatible)).
%--------------------------------------------------------------------------
