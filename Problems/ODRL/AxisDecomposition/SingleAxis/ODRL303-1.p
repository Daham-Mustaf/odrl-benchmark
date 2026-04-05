%--------------------------------------------------------------------------
% File     : ODRL303-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : width > 600 vs width ≤ 600: mirror boundary
% Version  : 1.0
% English  : width gt 600   → (600, ∞)
%           : width lteq 600 → (0, 600]
%           : (600, ∞) ∩ (0, 600] = ∅ → Conflict
%           : Symmetric to ODRL302. Requires density.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL303-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL303-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD001-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl303, conjecture,
    ~?[X]: (less(v600, X) & in_lopen(X, v0, v600))).
%--------------------------------------------------------------------------
