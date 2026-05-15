%--------------------------------------------------------------------------
% File     : ODRL715-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA SingleAxis: claim gteq∩lteq compatible when disjoint (wrong)
% Version  : 1.0
% English  : gteq 800 vs lteq 400: [800,∞)∩(0,400]=∅.
%           : Wrong claim: overlap exists.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL715-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL715-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v400,axiom,val(v400)).
fof(val_v800,axiom,val(v800)).
fof(ord_v0_v400,axiom,less(v0,v400)).
fof(ord_v400_v800,axiom,less(v400,v800)).
fof(distinct,axiom,$distinct(v0,v400,v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl715, conjecture,
    ?[X]: (leq(v800,X) & in_lopen(X,v0,v400))).
%--------------------------------------------------------------------------
