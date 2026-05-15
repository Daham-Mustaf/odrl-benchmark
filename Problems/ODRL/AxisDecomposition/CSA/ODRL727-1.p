%--------------------------------------------------------------------------
% File     : ODRL727-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Composition: claim xone(conflict,conflict)=compatible (wrong)
% Version  : 1.0
% English  : xone_verdict(conflict,conflict)=conflict.
%           : Wrong claim: =compatible.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL727-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% Relation : verdict_algebra
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL727-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl727, conjecture,
    xone_verdict(conflict, conflict) = compatible).
%--------------------------------------------------------------------------
