%--------------------------------------------------------------------------
% File     : ODRL307-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : width = 400 vs width ≤ 600: point inside interval
% Version  : 1.0
% English  : width eq 400   → {400}       [def:interval-denotation, eq]
%           : width lteq 600 → (0, 600]    [def:interval-denotation, lteq]
%           : {400} ∩ (0, 600] = {400} ≠ ∅
%           : Witness: X = v400 (named constant, no density needed).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL307-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL307-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% v0 = domain lower bound (excluded); v400, v600 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl307, conjecture,
    ?[X]: (in_closed(X, v400, v400) & in_lopen(X, v0, v600))).
%--------------------------------------------------------------------------
