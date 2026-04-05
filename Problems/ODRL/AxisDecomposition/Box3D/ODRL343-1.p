%--------------------------------------------------------------------------
% File     : ODRL343-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Depth conflict × width+height compatible → box Conflict
% Version  : 1.0
% English  : Width:  lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible
%           : Height: lteq 600 → (0,600]  ∩  gteq 100 → [100,∞) = [100,600] ≠ ∅  Compatible
%           : Depth:  lteq 8   → (0,8]    ∩  gteq 24  → [24,∞)  = ∅               Conflict
%           : box_verdict(Compatible, box_verdict(Compatible, Conflict)) = Conflict
%           : Tests commutativity: conflict at position 3 kills the box.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL343-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL343-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v8,        axiom, val(v8)).
fof(val_v24,       axiom, val(v24)).
fof(val_v100,      axiom, val(v100)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v8,     axiom, less(v0,   v8)).
fof(ord_v0_v24,    axiom, less(v0,   v24)).
fof(ord_v0_v100,   axiom, less(v0,   v100)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v8_v24,    axiom, less(v8,   v24)).
fof(ord_v8_v100,   axiom, less(v8,   v100)).
fof(ord_v8_v200,   axiom, less(v8,   v200)).
fof(ord_v8_v600,   axiom, less(v8,   v600)).
fof(ord_v8_v800,   axiom, less(v8,   v800)).
fof(ord_v24_v100,  axiom, less(v24,  v100)).
fof(ord_v24_v200,  axiom, less(v24,  v200)).
fof(ord_v24_v600,  axiom, less(v24,  v600)).
fof(ord_v24_v800,  axiom, less(v24,  v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v24, v100, v200, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl343, conjecture,
    ~?[X,Y,Z]: (in_lopen(X, v0, v800) & leq(v200, X) &
            in_lopen(Y, v0, v600) & leq(v100, Y) &
            in_lopen(Z, v0, v8)   & leq(v24,  Z))).
%--------------------------------------------------------------------------
