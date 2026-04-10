%--------------------------------------------------------------------------
% File     : ODRL631-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : completion_conflict: U<V in domain gives conflict completion
% Version  : 1.0
% English  : def:completion: less(v400,v800) & both in [v0,v1200]
%           : => completion_conflict(v400, v800, v0, v1200).
%           : Policy1 gets lteq v400, Policy2 gets gteq v800 => disjoint.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL631-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL631-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMPL000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v400,  axiom, val(v400)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v400,    axiom, less(v0, v400)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v400, v800, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl631, conjecture,
    completion_conflict(v400, v800, v0, v1200)).
%--------------------------------------------------------------------------
