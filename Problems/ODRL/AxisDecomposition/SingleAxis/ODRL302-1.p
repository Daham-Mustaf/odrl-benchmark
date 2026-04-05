%--------------------------------------------------------------------------
% File     : ODRL302-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : width < 600 vs width ≥ 600: open/closed boundary
% Version  : 1.0
% English  : width lt 600   → (0, 600)
%           : width gteq 600 → [600, ∞)
%           : (0, 600) ∩ [600, ∞) = ∅ → Conflict
%           : Requires density: open interval (0,600) is non-empty.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL302-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL302-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD001-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl302, conjecture,
    ~?[X]: (in_ropen(X, v0, v600) & leq(v600, X))).
%--------------------------------------------------------------------------
