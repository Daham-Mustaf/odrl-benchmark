%--------------------------------------------------------------------------
% File     : ODRL431-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 2D cc×oc — Y boundary excluded on left kills box → Conflict
% Version  : 1.0
% English  : Width:  cc: (0,600]∩[600,∞)={600} Compatible
%           : Height: oc: (0,400)∩[400,∞)=∅ Conflict
%           : Height contradiction kills the box.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL431-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL431-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl431, conjecture,
    ~?[X,Y]: (in_lopen(X, v0, v600) & leq(v600, X) &
            in_open(Y, v0, v400) & leq(v400, Y))).
%--------------------------------------------------------------------------
