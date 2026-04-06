%--------------------------------------------------------------------------
% File     : ODRL333-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : prop:monotone: narrowing an axis propagates Conflict
% Version  : 1.0
% English  : axis_subsumes(v200,v600, v0,v800):  [200,600] ⊆ [0,800]
%           : axis_conflict(v0,v800, v900,v1200): [0,800] ∩ [900,1200] = ∅
%           : Therefore: axis_conflict(v200,v600, v900,v1200)  [prop:monotone]
%           : Tests Section B predicates directly. No geometry primitives.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL333-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL333-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,          axiom, val(v0)).
fof(val_v200,        axiom, val(v200)).
fof(val_v600,        axiom, val(v600)).
fof(val_v800,        axiom, val(v800)).
fof(val_v900,        axiom, val(v900)).
fof(val_v1200,       axiom, val(v1200)).
fof(ord_v0_v200,     axiom, less(v0,   v200)).
fof(ord_v0_v600,     axiom, less(v0,   v600)).
fof(ord_v0_v800,     axiom, less(v0,   v800)).
fof(ord_v0_v900,     axiom, less(v0,   v900)).
fof(ord_v0_v1200,    axiom, less(v0,   v1200)).
fof(ord_v200_v600,   axiom, less(v200, v600)).
fof(ord_v200_v800,   axiom, less(v200, v800)).
fof(ord_v200_v900,   axiom, less(v200, v900)).
fof(ord_v200_v1200,  axiom, less(v200, v1200)).
fof(ord_v600_v800,   axiom, less(v600, v800)).
fof(ord_v600_v900,   axiom, less(v600, v900)).
fof(ord_v600_v1200,  axiom, less(v600, v1200)).
fof(ord_v800_v900,   axiom, less(v800, v900)).
fof(ord_v800_v1200,  axiom, less(v800, v1200)).
fof(ord_v900_v1200,  axiom, less(v900, v1200)).
fof(distinct, axiom, $distinct(v0, v200, v600, v800, v900, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl333, conjecture,
    (axis_subsumes(v200, v600, v0, v800) &
  axis_conflict(v0, v800, v900, v1200))
=> axis_conflict(v200, v600, v900, v1200)).
%--------------------------------------------------------------------------
