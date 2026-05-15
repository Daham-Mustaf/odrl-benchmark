%--------------------------------------------------------------------------
% File     : ODRL709-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Composition: claim xone(compat,conflict)=conflict (wrong)
% Version  : 1.0
% English  : Flip of ODRL644: xone_verdict(compatible,conflict)=compatible.
%           : Wrong claim: xone_verdict(compatible,conflict)=conflict.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL709-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% Relation : verdict_algebra
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL709-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl709, conjecture,
    xone_verdict(compatible, conflict) = conflict).
%--------------------------------------------------------------------------
