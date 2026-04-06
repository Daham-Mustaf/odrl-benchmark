%--------------------------------------------------------------------------
% File     : ODRL340-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : All three axes conflict → box Conflict
% Version  : 1.0
% English  : Width:  lteq 600 → (0,600]  ∩  gteq 800 → [800,∞)  = ∅  Conflict
%           : Height: lteq 300 → (0,300]  ∩  gteq 500 → [500,∞)  = ∅  Conflict
%           : Depth:  lteq 8   → (0,8]    ∩  gteq 24  → [24,∞)   = ∅  Conflict
%           : box_verdict(Conflict, box_verdict(Conflict, Conflict)) = Conflict
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL340-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL340-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v8,        axiom, val(v8)).
fof(val_v24,       axiom, val(v24)).
fof(val_v300,      axiom, val(v300)).
fof(val_v500,      axiom, val(v500)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v8,     axiom, less(v0,   v8)).
fof(ord_v0_v24,    axiom, less(v0,   v24)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v8_v24,    axiom, less(v8,   v24)).
fof(ord_v8_v300,   axiom, less(v8,   v300)).
fof(ord_v8_v500,   axiom, less(v8,   v500)).
fof(ord_v8_v600,   axiom, less(v8,   v600)).
fof(ord_v8_v800,   axiom, less(v8,   v800)).
fof(ord_v24_v300,  axiom, less(v24,  v300)).
fof(ord_v24_v500,  axiom, less(v24,  v500)).
fof(ord_v24_v600,  axiom, less(v24,  v600)).
fof(ord_v24_v800,  axiom, less(v24,  v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v24, v300, v500, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl340, conjecture,
    ~?[X,Y,Z]: (in_lopen(X, v0, v600) & leq(v800, X) &
            in_lopen(Y, v0, v300) & leq(v500, Y) &
            in_lopen(Z, v0, v8)   & leq(v24,  Z))).
%--------------------------------------------------------------------------
