%--------------------------------------------------------------------------
% File     : ODRL409-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 4D all open intervals — density (9 constants)
% Version  : 1.0
% English  : Width:  gt 200 ∩ lt 800 = (200,800) ≠ ∅ Compatible
%           : Height: gt 100 ∩ lt 500 = (100,500) ≠ ∅ Compatible
%           : Depth:  gt 8   ∩ lt 32  = (8,32)    ≠ ∅ Compatible
%           : Alt:    gt 72  ∩ lt 300 = (72,300)  ≠ ∅ Compatible
%           : Witnesses available from named-constant chain; no density required.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL409-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL409-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v16, axiom, val(v16)).
fof(val_v32, axiom, val(v32)).
fof(val_v72, axiom, val(v72)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v500, axiom, val(v500)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v72, axiom, less(v0, v72)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v16, axiom, less(v8, v16)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v72, axiom, less(v8, v72)).
fof(ord_v16_v32, axiom, less(v16, v32)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v100, axiom, less(v16, v100)).
fof(ord_v16_v200, axiom, less(v16, v200)).
fof(ord_v16_v300, axiom, less(v16, v300)).
fof(ord_v16_v500, axiom, less(v16, v500)).
fof(ord_v16_v800, axiom, less(v16, v800)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v200, axiom, less(v8, v200)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v500, axiom, less(v8, v500)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v72, axiom, less(v32, v72)).
fof(ord_v32_v100, axiom, less(v32, v100)).
fof(ord_v32_v200, axiom, less(v32, v200)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v500, axiom, less(v32, v500)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v72_v100, axiom, less(v72, v100)).
fof(ord_v72_v200, axiom, less(v72, v200)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v500, axiom, less(v72, v500)).
fof(ord_v72_v800, axiom, less(v72, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(distinct, axiom, $distinct(v0, v8, v16, v32, v72, v100, v200, v300, v500, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl409, conjecture,
    ?[X,Y,Z,W]: (less(v200, X) & in_open(X, v0, v800) &
             less(v100, Y) & in_open(Y, v0, v500) &
             less(v8,   Z) & in_open(Z, v0, v32)  &
             less(v72,  W) & in_open(W, v0, v300))).
%--------------------------------------------------------------------------
