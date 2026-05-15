%--------------------------------------------------------------------------
% File     : ODRL643-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : or_verdict_total: result is always one of three verdicts
% Version  : 1.0
% English  : sec:composition or_verdict_total:
%           : For all verdicts V1,V2: or_verdict is conflict, compatible, or unknown.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL643-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL643-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl643, conjecture,
    ![V1,V2]: ((is_verdict(V1) & is_verdict(V2)) =>
    (or_verdict(V1,V2) = compatible |
     or_verdict(V1,V2) = conflict |
     or_verdict(V1,V2) = unknown))).
%--------------------------------------------------------------------------
