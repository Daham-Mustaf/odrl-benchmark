%--------------------------------------------------------------------------
% File     : ODRL313-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : BSB running example: width ≤ 600 vs width ≥ 1200
% Version  : 1.0
% English  : BSB license:    width lteq 600  → (0, 600]    [ex:bsb]
%           : Museum request: width gteq 1200 → [1200, ∞)  [ex:bsb]
%           : (0, 600] ∩ [1200, ∞) = ∅        by less(v600, v1200)
%           : Paper running example (Datenraum Kultur / BSB scenario).
%           : Width axis alone yields Conflict → box verdict = Conflict.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL313-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL313-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% v0 = domain lower bound (excluded); v600, v1200 = constraint values
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v1200,   axiom, less(v0, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl313, conjecture,
    ~?[X]: (in_lopen(X, v0, v600) & leq(v1200, X))).
%--------------------------------------------------------------------------
