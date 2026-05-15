%--------------------------------------------------------------------------
% File     : ODRL353-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : prop:monotone in 3D: narrowing width propagates Conflict
% Version  : 1.0
% English  : axis_subsumes(v200,v600, v0,v800): [200,600] ⊆ [0,800]
%           : axis_conflict(v0,v800, v900,v1200): [0,800] ∩ [900,1200] = ∅
%           : prop:monotone → axis_conflict(v200,v600, v900,v1200)
%           : Tests Section B predicates directly — consequent is axis_conflict,
%           : not raw interval arithmetic (forces Vampire to use Section B axioms).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL353-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL353-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,         axiom, val(v0)).
fof(val_v200,       axiom, val(v200)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v900,       axiom, val(v900)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v200,    axiom, less(v0,   v200)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v800,    axiom, less(v0,   v800)).
fof(ord_v0_v900,    axiom, less(v0,   v900)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v200_v600,  axiom, less(v200, v600)).
fof(ord_v200_v800,  axiom, less(v200, v800)).
fof(ord_v200_v900,  axiom, less(v200, v900)).
fof(ord_v200_v1200, axiom, less(v200, v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v600_v900,  axiom, less(v600, v900)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v900,  axiom, less(v800, v900)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(ord_v900_v1200, axiom, less(v900, v1200)).
fof(distinct, axiom, $distinct(v0, v200, v600, v800, v900, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl353, conjecture,
    (axis_subsumes(v200, v600, v0, v800) &
 axis_conflict(v0, v800, v900, v1200))
=> axis_conflict(v200, v600, v900, v1200)).
%--------------------------------------------------------------------------
