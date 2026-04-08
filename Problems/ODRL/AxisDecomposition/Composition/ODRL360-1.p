%--------------------------------------------------------------------------
% File     : ODRL360-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : All 4 axes compatible → box Compatible
% Version  : 1.0
% English  : Width:  lteq 800 ∩ gteq 200 = [200,800] ≠ ∅  Compatible
%           : Height: lteq 600 ∩ gteq 100 = [100,600] ≠ ∅  Compatible
%           : Depth:  lteq 32  ∩ gteq 8   = [8,32]    ≠ ∅  Compatible
%           : Alt:    lteq 300 ∩ gteq 72  = [72,300]  ≠ ∅  Compatible
%           : box_verdict(C,box_verdict(C,box_verdict(C,C)))=Compatible [Rule 2]
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL360-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL360-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v72, axiom, val(v72)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v72, axiom, less(v0, v72)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v72, axiom, less(v8, v72)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v200, axiom, less(v8, v200)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v600, axiom, less(v8, v600)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v72, axiom, less(v32, v72)).
fof(ord_v32_v100, axiom, less(v32, v100)).
fof(ord_v32_v200, axiom, less(v32, v200)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v72_v100, axiom, less(v72, v100)).
fof(ord_v72_v200, axiom, less(v72, v200)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v72_v800, axiom, less(v72, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v72, v100, v200, v300, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl360, conjecture,
    ?[X,Y,Z,W]: (in_lopen(X, v0, v800) & leq(v200, X) &           in_lopen(Y, v0, v600) & leq(v100, Y) &
           in_lopen(Z, v0, v32)  & leq(v8,   Z) &
           in_lopen(W, v0, v300) & leq(v72,  W))).
%--------------------------------------------------------------------------
