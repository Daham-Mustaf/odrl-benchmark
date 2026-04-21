%--------------------------------------------------------------------------
% File     : ODRL351-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : BSB 3D: width conflict × height+depth compatible → box Conflict
% Version  : 1.0
% English  : Width:  lteq 600  → (0,600]  ∩  gteq 1200 → [1200,∞) = ∅  Conflict
%           : Height: lteq 600  → (0,600]  ∩  gteq 400  → [400,∞)  ≠ ∅  Compatible
%           : Depth:  lteq 32   → (0,32]   ∩  gteq 8    → [8,∞)    ≠ ∅  Compatible
%           : box_verdict(Conflict, box_verdict(Compatible, Compatible)) = Conflict
%           : BSB running example extended to 3 axes (ex:bsb).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL351-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL351-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,         axiom, val(v0)).
fof(val_v8,         axiom, val(v8)).
fof(val_v32,        axiom, val(v32)).
fof(val_v400,       axiom, val(v400)).
fof(val_v600,       axiom, val(v600)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v8,      axiom, less(v0,   v8)).
fof(ord_v0_v32,     axiom, less(v0,   v32)).
fof(ord_v0_v400,    axiom, less(v0,   v400)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v8_v32,     axiom, less(v8,   v32)).
fof(ord_v8_v400,    axiom, less(v8,   v400)).
fof(ord_v8_v600,    axiom, less(v8,   v600)).
fof(ord_v8_v1200,   axiom, less(v8,   v1200)).
fof(ord_v32_v400,   axiom, less(v32,  v400)).
fof(ord_v32_v600,   axiom, less(v32,  v600)).
fof(ord_v32_v1200,  axiom, less(v32,  v1200)).
fof(ord_v400_v600,  axiom, less(v400, v600)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v8, v32, v400, v600, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl351, conjecture,
    ![X,Y,Z]: ~(in_lopen(X, v0, v600)  & leq(v1200, X) &
            in_lopen(Y, v0, v600)  & leq(v400,  Y) &
            in_lopen(Z, v0, v32)   & leq(v8,    Z))).
%--------------------------------------------------------------------------
