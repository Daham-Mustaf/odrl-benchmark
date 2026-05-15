%--------------------------------------------------------------------------
% File     : ODRL605-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : disjoint cc: [v0,v5] vs [v6,v10] strictly separated
% Version  : 1.0
% English  : thm:criterion: less(v5,v6) => disjoint([v0,v5],[v6,v10],cc)
%           : Strict gap between v5 and v6: both closed, separated.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL605-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL605-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PREC000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,     axiom, val(v0)).
fof(val_v5,     axiom, val(v5)).
fof(val_v6,     axiom, val(v6)).
fof(val_v10,    axiom, val(v10)).
fof(ord_v0_v5,  axiom, less(v0, v5)).
fof(ord_v5_v6,  axiom, less(v5, v6)).
fof(ord_v6_v10, axiom, less(v6, v10)).
fof(distinct,   axiom, $distinct(v0, v5, v6, v10)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl605, conjecture,
    disjoint(v0, v5, c, c, v6, v10, c, c)).
%--------------------------------------------------------------------------
