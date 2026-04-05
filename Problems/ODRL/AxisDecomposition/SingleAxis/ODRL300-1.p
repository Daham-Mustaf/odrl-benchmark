%--------------------------------------------------------------------------
% File     : ODRL300-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : width ≤ 600 vs width ≥ 800: disjoint intervals
% Version  : 1.0
% English  : width lteq 600 → (0, 600]   [def:interval-denotation, lteq]
%           : width gteq 800 → [800, ∞)   [def:interval-denotation, gteq]
%           : (0, 600] ∩ [800, ∞) = ∅     by less(v600, v800)
%           : Conflict Criterion (cc): u1=600 closed, l2=800 closed → u1 < l2.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL300-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL300-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% v0 = domain lower bound (excluded); v600, v800 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct,      axiom, $distinct(v0, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl300, conjecture,
    ~?[X]: (in_lopen(X, v0, v600) & leq(v800, X))).
%--------------------------------------------------------------------------
