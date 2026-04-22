%--------------------------------------------------------------------------
% File     : ODRL470-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : xone-A vs xone-B: all 4 branch-pair intersections empty → Conflict
% Version  : 1.0
% English  : PolicyA xone: width∈(0,100] XOR width∈[500,600]
%           : PolicyB xone: width∈[200,300] XOR width∈[700,800]
%           : A-support=(0,100]∪[500,600], B-support=[200,300]∪[700,800] — disjoint
%           : All 4 branch-pair intersections empty → verdictXone=Conflict
%           : Genuine xone-vs-xone Conflict: not a single-axis order contradiction.
%           : Note: xone(A1,A2) Conflict requires disjoint supports (A1∪A2)∩(B1∪B2)=∅.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL470-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL470-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(val_v700, axiom, val(v700)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v700, axiom, less(v0, v700)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v700, axiom, less(v100, v700)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v700, axiom, less(v200, v700)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v700, axiom, less(v300, v700)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v700, axiom, less(v500, v700)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(ord_v600_v700, axiom, less(v600, v700)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(ord_v700_v800, axiom, less(v700, v800)).
fof(distinct, axiom, $distinct(v0, v100, v200, v300, v500, v600, v700, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl470, conjecture,
    ![X]: ~(
  ((in_lopen(X, v0, v100) & ~(leq(v500, X) & in_lopen(X, v0, v600))) |
   (~in_lopen(X, v0, v100) & (leq(v500, X) & in_lopen(X, v0, v600)))) &
  (((leq(v200, X) & in_lopen(X, v0, v300)) & ~(leq(v700, X) & in_lopen(X, v0, v800))) |
   (~(leq(v200, X) & in_lopen(X, v0, v300)) & (leq(v700, X) & in_lopen(X, v0, v800)))))).
%--------------------------------------------------------------------------
