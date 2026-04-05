%--------------------------------------------------------------------------
% File     : ODRL304-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : width ≤ 600 vs width ≥ 200: overlapping intervals
% Version  : 1.0
% English  : width lteq 600 → (0, 600]   [def:interval-denotation, lteq]
%           : width gteq 200 → [200, ∞)   [def:interval-denotation, gteq]
%           : (0, 600] ∩ [200, ∞) = [200, 600] ≠ ∅
%           : Witness: X = v200 (named constant, no density needed).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL304-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL304-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% v0 = domain lower bound (excluded); v200, v600 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0, v200)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl304, conjecture,
    ?[X]: (in_lopen(X, v0, v600) & leq(v200, X))).
%--------------------------------------------------------------------------
