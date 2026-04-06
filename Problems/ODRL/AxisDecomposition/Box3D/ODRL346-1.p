%--------------------------------------------------------------------------
% File     : ODRL346-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : All three axes touch → single-point box Compatible
% Version  : 1.0
% English  : Width:  lteq 600 → (0,600] ∩ gteq 600 → [600,∞) = {600} ≠ ∅  Compatible
%           : Height: lteq 400 → (0,400] ∩ gteq 400 → [400,∞) = {400} ≠ ∅  Compatible
%           : Depth:  lteq 16  → (0,16]  ∩ gteq 16  → [16,∞)  = {16}  ≠ ∅  Compatible
%           : box_verdict(Compatible, box_verdict(Compatible, Compatible)) = Compatible
%           : Witness: (v600, v400, v16). Box intersection is a single point in R³.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL346-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL346-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v16,       axiom, val(v16)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v16,    axiom, less(v0,   v16)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v16_v400,  axiom, less(v16,  v400)).
fof(ord_v16_v600,  axiom, less(v16,  v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v16, v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl346, conjecture,
    ?[X,Y,Z]: (in_lopen(X, v0, v600) & leq(v600, X) &
           in_lopen(Y, v0, v400) & leq(v400, Y) &
           in_lopen(Z, v0, v16)  & leq(v16,  Z))).
%--------------------------------------------------------------------------
