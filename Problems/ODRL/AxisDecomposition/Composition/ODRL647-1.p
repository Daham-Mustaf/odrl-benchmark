%--------------------------------------------------------------------------
% File     : ODRL647-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : xone_verdict_total: result is always one of three verdicts
% Version  : 1.0
% English  : sec:composition xone_verdict_total:
%           : For all verdicts Vm,Vr: xone_verdict is compat, conflict, or unknown.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL647-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL647-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl647, conjecture,
    ![Vm,Vr]: ((is_verdict(Vm) & is_verdict(Vr)) =>
    (xone_verdict(Vm,Vr) = compatible |
     xone_verdict(Vm,Vr) = conflict |
     xone_verdict(Vm,Vr) = unknown))).
%--------------------------------------------------------------------------
