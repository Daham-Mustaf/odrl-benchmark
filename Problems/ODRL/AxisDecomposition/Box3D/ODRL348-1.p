%--------------------------------------------------------------------------
% File     : ODRL348-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Depth open/closed boundary conflict kills 3D box
% Version  : 1.0
% English  : Width:  lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible
%           : Height: lteq 600 → (0,600]  ∩  gteq 100 → [100,∞) = [100,600] ≠ ∅  Compatible
%           : Depth:  lt 16    → (0,16)   ∩  gteq 16  → [16,∞)  = ∅               Conflict (oc)
%           : box_verdict(Compatible, box_verdict(Compatible, Conflict)) = Conflict
%           : Depth: order contradiction (Z<16 & Z≥16), no density needed.
%           : Tests open-boundary conflict on axis 3 kills the box.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL348-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL348-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v16,       axiom, val(v16)).
fof(val_v100,      axiom, val(v100)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v16,    axiom, less(v0,   v16)).
fof(ord_v0_v100,   axiom, less(v0,   v100)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v16_v100,  axiom, less(v16,  v100)).
fof(ord_v16_v200,  axiom, less(v16,  v200)).
fof(ord_v16_v600,  axiom, less(v16,  v600)).
fof(ord_v16_v800,  axiom, less(v16,  v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v16, v100, v200, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl348, conjecture,
    ~?[X,Y,Z]: (in_lopen(X, v0, v800) & leq(v200, X) &
            in_lopen(Y, v0, v600) & leq(v100, Y) &
            in_open(Z,  v0, v16)  & leq(v16,  Z))).
%--------------------------------------------------------------------------
