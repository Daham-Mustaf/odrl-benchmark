%--------------------------------------------------------------------------
% File     : ODRL732-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA BoxContainment: claim subs absent=compatible (wrong)
% Version  : 1.0
% English  : subs_verdict with C1 absent = unknown, not compatible.
%           : Wrong claim: =compatible.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL732-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% Relation : verdict_algebra
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL732-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/SUBS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v600,axiom,val(v600)).
fof(ord_v0_v600,axiom,less(v0,v600)).
fof(distinct,axiom,$distinct(v0,v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl732, conjecture,
    subs_verdict(v0, v600, absent, v0, v600, present) = compatible).
%--------------------------------------------------------------------------
