%--------------------------------------------------------------------------
% File     : ODRL310-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : (0,1200] ⊄ (0,600]: wider does not subsume tighter
% Version  : 1.0
% English  : width lteq 1200 → (0, 1200]
%           : width lteq 600  → (0, 600]
%           : (0, 1200] ⊄ (0, 600] → Conflict (subsumption fails)
%           : Counterexample: X = 800 ∈ A, X ∉ B.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL310-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL310-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v1200,   axiom, less(v0, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl310, conjecture,
    ?[X]: (in_lopen(X, v0, v1200) & ~in_lopen(X, v0, v600))).
%--------------------------------------------------------------------------
