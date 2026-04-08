%--------------------------------------------------------------------------
% File     : ODRL413-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 4D fractional bounds Compatible (12 constants)
% Version  : 1.0
% English  : Width: lteq 600.5 (lb=1) ∩ gteq 600 → X∈[600,600.5] ≠ ∅ Compatible
%           : Height: lteq 480.5 ∩ gteq 480 → [480,480.5] ≠ ∅ Compatible
%           : Depth: lteq 16.5 ∩ gteq 16 → [16,16.5] ≠ ∅ Compatible
%           : Alt: lteq 72.5 ∩ gteq 72 → [72,72.5] ≠ ∅ Compatible
%           : Witnesses: X=600, Y=480, Z=16, W=72 (named constants).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL413-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL413-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v1, axiom, val(v1)).
fof(val_v2, axiom, val(v2)).
fof(val_v3, axiom, val(v3)).
fof(val_v4, axiom, val(v4)).
fof(val_v16, axiom, val(v16)).
fof(val_v16_5, axiom, val(v16_5)).
fof(val_v72, axiom, val(v72)).
fof(val_v72_5, axiom, val(v72_5)).
fof(val_v480, axiom, val(v480)).
fof(val_v480_5, axiom, val(v480_5)).
fof(val_v600, axiom, val(v600)).
fof(val_v600_5, axiom, val(v600_5)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v1_v3, axiom, less(v1, v3)).
fof(ord_v1_v4, axiom, less(v1, v4)).
fof(ord_v1_v16, axiom, less(v1, v16)).
fof(ord_v1_v16_5, axiom, less(v1, v16_5)).
fof(ord_v1_v72, axiom, less(v1, v72)).
fof(ord_v1_v72_5, axiom, less(v1, v72_5)).
fof(ord_v1_v480, axiom, less(v1, v480)).
fof(ord_v1_v480_5, axiom, less(v1, v480_5)).
fof(ord_v1_v600, axiom, less(v1, v600)).
fof(ord_v1_v600_5, axiom, less(v1, v600_5)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v2_v4, axiom, less(v2, v4)).
fof(ord_v2_v16, axiom, less(v2, v16)).
fof(ord_v2_v16_5, axiom, less(v2, v16_5)).
fof(ord_v2_v72, axiom, less(v2, v72)).
fof(ord_v2_v72_5, axiom, less(v2, v72_5)).
fof(ord_v2_v480, axiom, less(v2, v480)).
fof(ord_v2_v480_5, axiom, less(v2, v480_5)).
fof(ord_v2_v600, axiom, less(v2, v600)).
fof(ord_v2_v600_5, axiom, less(v2, v600_5)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v3_v16, axiom, less(v3, v16)).
fof(ord_v3_v16_5, axiom, less(v3, v16_5)).
fof(ord_v3_v72, axiom, less(v3, v72)).
fof(ord_v3_v72_5, axiom, less(v3, v72_5)).
fof(ord_v3_v480, axiom, less(v3, v480)).
fof(ord_v3_v480_5, axiom, less(v3, v480_5)).
fof(ord_v3_v600, axiom, less(v3, v600)).
fof(ord_v3_v600_5, axiom, less(v3, v600_5)).
fof(ord_v4_v16, axiom, less(v4, v16)).
fof(ord_v4_v16_5, axiom, less(v4, v16_5)).
fof(ord_v4_v72, axiom, less(v4, v72)).
fof(ord_v4_v72_5, axiom, less(v4, v72_5)).
fof(ord_v4_v480, axiom, less(v4, v480)).
fof(ord_v4_v480_5, axiom, less(v4, v480_5)).
fof(ord_v4_v600, axiom, less(v4, v600)).
fof(ord_v4_v600_5, axiom, less(v4, v600_5)).
fof(ord_v16_v16_5, axiom, less(v16, v16_5)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v72_5, axiom, less(v16, v72_5)).
fof(ord_v16_v480, axiom, less(v16, v480)).
fof(ord_v16_v480_5, axiom, less(v16, v480_5)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v600_5, axiom, less(v16, v600_5)).
fof(ord_v16_5_v72, axiom, less(v16_5, v72)).
fof(ord_v16_5_v72_5, axiom, less(v16_5, v72_5)).
fof(ord_v16_5_v480, axiom, less(v16_5, v480)).
fof(ord_v16_5_v480_5, axiom, less(v16_5, v480_5)).
fof(ord_v16_5_v600, axiom, less(v16_5, v600)).
fof(ord_v16_5_v600_5, axiom, less(v16_5, v600_5)).
fof(ord_v72_v72_5, axiom, less(v72, v72_5)).
fof(ord_v72_v480, axiom, less(v72, v480)).
fof(ord_v72_v480_5, axiom, less(v72, v480_5)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v72_v600_5, axiom, less(v72, v600_5)).
fof(ord_v72_5_v480, axiom, less(v72_5, v480)).
fof(ord_v72_5_v480_5, axiom, less(v72_5, v480_5)).
fof(ord_v72_5_v600, axiom, less(v72_5, v600)).
fof(ord_v72_5_v600_5, axiom, less(v72_5, v600_5)).
fof(ord_v480_v480_5, axiom, less(v480, v480_5)).
fof(ord_v480_v600, axiom, less(v480, v600)).
fof(ord_v480_v600_5, axiom, less(v480, v600_5)).
fof(ord_v480_5_v600, axiom, less(v480_5, v600)).
fof(ord_v480_5_v600_5, axiom, less(v480_5, v600_5)).
fof(ord_v600_v600_5, axiom, less(v600, v600_5)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v16, v16_5, v72, v72_5, v480, v480_5, v600, v600_5)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl413, conjecture,
    ?[X,Y,Z,W]: (in_lopen(X, v1, v600_5) & leq(v600, X) &
           in_lopen(Y, v2, v480_5) & leq(v480, Y) &
           in_lopen(Z, v3, v16_5)  & leq(v16,  Z) &
           in_lopen(W, v4, v72_5)  & leq(v72,  W))).
%--------------------------------------------------------------------------
