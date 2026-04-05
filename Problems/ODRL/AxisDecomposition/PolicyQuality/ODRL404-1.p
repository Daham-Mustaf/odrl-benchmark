%--------------------------------------------------------------------------
% File     : ODRL404-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 2D oc boundary conflict × compatible (4 constants)
% Version  : 1.0
% English  : Width: lt 600 → (0,600) ∩ gteq 600 → [600,∞) = ∅ Conflict (oc)
%           : Height: lteq 800 ∩ gteq 200 = [200,800] ≠ ∅ Compatible
%           : Proof: order contradiction (X<600 & X≥600), no density.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL404-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL404-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v200, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl404, conjecture,
    ~?[X,Y]: (in_open(X, v0, v600) & leq(v600, X) &
            in_lopen(Y, v0, v800) & leq(v200, Y))).
%--------------------------------------------------------------------------
