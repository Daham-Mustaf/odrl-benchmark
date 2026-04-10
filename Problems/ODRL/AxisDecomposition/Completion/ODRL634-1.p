%--------------------------------------------------------------------------
% File     : ODRL634-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : monotone_conflict: subsumes and conflict implies conflict
% Version  : 1.0
% English  : prop:monotone: [v200,v400] ⊆ [v0,v600] and [v0,v600] conflicts [v800,v1200]
%           : => [v200,v400] conflicts [v800,v1200].
%           : monotone_conflict: axis_subsumes(A1,A2) & axis_conflict(A2,B) => axis_conflict(A1,B).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL634-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL634-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMPL000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v200,  axiom, val(v200)).
fof(val_v400,  axiom, val(v400)).
fof(val_v600,  axiom, val(v600)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v200,    axiom, less(v0, v200)).
fof(ord_v0_v400,    axiom, less(v0, v400)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v200_v400,  axiom, less(v200, v400)).
fof(ord_v200_v600,  axiom, less(v200, v600)).
fof(ord_v200_v800,  axiom, less(v200, v800)).
fof(ord_v400_v600,  axiom, less(v400, v600)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600, v800, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl634, conjecture,
    axis_conflict(v200, v400, v800, v1200)).
%--------------------------------------------------------------------------
