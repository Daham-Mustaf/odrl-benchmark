%--------------------------------------------------------------------------
% File     : ODRL320-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : BSB: width conflict × height compatible → box Conflict
% Version  : 1.0
% English  : Width:  lteq 600 → (0,600]   ∩   gteq 1200 → [1200,∞) = ∅  Conflict
%           : Height: lteq 600 → (0,600]   ∩   gteq  400 → [400,∞)  ≠ ∅  Compatible
%           : box_verdict(Conflict, Compatible) = Conflict  [def:box-verdict Rule 1]
%           : Paper running example (BSB scenario, ex:bsb).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL320-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL320-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,         axiom, val(v0)).
fof(val_v400,       axiom, val(v400)).
fof(val_v600,       axiom, val(v600)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v400,    axiom, less(v0,   v400)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v400_v600,  axiom, less(v400, v600)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct,       axiom, $distinct(v0, v400, v600, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl320, conjecture,
    ~?[X,Y]: (in_lopen(X, v0, v600) & leq(v1200, X) &
           in_lopen(Y, v0, v600) & leq(v400,  Y))).
%--------------------------------------------------------------------------
