%--------------------------------------------------------------------------
% File     : ODRL322-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Width compatible × height conflict → box Conflict
% Version  : 1.0
% English  : Width:  lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible
%           : Height: lteq 300 → (0,300]  ∩  gteq 500 → [500,∞) = ∅               Conflict
%           : box_verdict(Compatible, Conflict) = Conflict  [def:box-verdict Rule 1]
%           : Tests commutativity: conflict on any axis kills the box.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL322-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL322-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v300,      axiom, val(v300)).
fof(val_v500,      axiom, val(v500)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(distinct,      axiom, $distinct(v0, v200, v300, v500, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl322, conjecture,
    ~?[X,Y]: (in_lopen(X, v0, v800) & leq(v200, X) &
           in_lopen(Y, v0, v300) & leq(v500, Y))).
%--------------------------------------------------------------------------
