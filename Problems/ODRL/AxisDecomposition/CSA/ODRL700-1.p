%--------------------------------------------------------------------------
% File     : ODRL700-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA SingleAxis: claim compatible for disjoint intervals (wrong)
% Version  : 1.0
% English  : Flip of ODRL300: width lteq 600 vs gteq 800.
%           : Intervals (0,600] and [800,∞) are disjoint — Conflict.
%           : Wrong claim: ?[X]: overlap exists. Countermodel: no such X.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL700-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL700-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl700, conjecture,
    ?[X]: (in_lopen(X,v0,v600) & leq(v800,X))).
%--------------------------------------------------------------------------
