%--------------------------------------------------------------------------
% File     : ODRL330-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Width near-miss (gap=1) × height compatible → Conflict
% Version  : 1.0
% English  : Width:  lteq 599 → (0,599]  ∩  gteq 601 → [601,∞) = ∅  Conflict
%           : cc case: u1=599 closed, l2=601 closed, 599 < 601 → disjoint
%           : Height: lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible
%           : box_verdict(Conflict, Compatible) = Conflict  [def:box-verdict Rule 1]
%           : Tests gap of 1 unit on width kills the box.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL330-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL330-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,         axiom, val(v0)).
fof(val_v200,       axiom, val(v200)).
fof(val_v599,       axiom, val(v599)).
fof(val_v601,       axiom, val(v601)).
fof(val_v800,       axiom, val(v800)).
fof(ord_v0_v200,    axiom, less(v0,   v200)).
fof(ord_v0_v599,    axiom, less(v0,   v599)).
fof(ord_v0_v601,    axiom, less(v0,   v601)).
fof(ord_v0_v800,    axiom, less(v0,   v800)).
fof(ord_v200_v599,  axiom, less(v200, v599)).
fof(ord_v200_v601,  axiom, less(v200, v601)).
fof(ord_v200_v800,  axiom, less(v200, v800)).
fof(ord_v599_v601,  axiom, less(v599, v601)).
fof(ord_v599_v800,  axiom, less(v599, v800)).
fof(ord_v601_v800,  axiom, less(v601, v800)).
fof(distinct,       axiom, $distinct(v0, v200, v599, v601, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl330, conjecture,
    ~?[X,Y]: (in_lopen(X, v0, v599) & leq(v601, X) &
           in_lopen(Y, v0, v800) & leq(v200, Y))).
%--------------------------------------------------------------------------
