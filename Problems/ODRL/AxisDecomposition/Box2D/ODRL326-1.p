%--------------------------------------------------------------------------
% File     : ODRL326-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Width touches (compatible), height conflicts → box Conflict
% Version  : 1.0
% English  : Width:  lteq 600 → (0,600]  ∩  gteq 600 → [600,∞) = {600} ≠ ∅  Compatible
%           : Height: lteq 300 → (0,300]  ∩  gteq 500 → [500,∞) = ∅           Conflict
%           : box_verdict(Compatible, Conflict) = Conflict  [def:box-verdict Rule 1]
%           : Width touches at 600 (Compatible) — height conflict kills the box.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL326-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL326-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v300,      axiom, val(v300)).
fof(val_v500,      axiom, val(v500)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(distinct,      axiom, $distinct(v0, v300, v500, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl326, conjecture,
    ~?[X,Y]: (in_lopen(X, v0, v600) & leq(v600, X) &
           in_lopen(Y, v0, v300) & leq(v500, Y))).
%--------------------------------------------------------------------------
