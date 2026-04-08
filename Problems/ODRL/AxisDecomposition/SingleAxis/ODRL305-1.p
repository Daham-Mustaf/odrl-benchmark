%--------------------------------------------------------------------------
% File     : ODRL305-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : width ≤ 600 vs width ≥ 600: touching at 600
% Version  : 1.0
% English  : width lteq 600 → (0, 600]   [def:interval-denotation, lteq]
%           : width gteq 600 → [600, ∞)   [def:interval-denotation, gteq]
%           : (0, 600] ∩ [600, ∞) = {600} ≠ ∅
%           : Witness: X = v600. Tests closed-closed boundary touch (cc case).
%           : Conflict Criterion: u1=600 closed, l2=600 closed → need u1 < l2,
%           : but 600 = 600 so criterion NOT satisfied → Compatible.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL305-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL305-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% v0 = domain lower bound (excluded); v600 = boundary value (witness)
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl305, conjecture,
    ?[X]: (in_lopen(X, v0, v600) & leq(v600, X))).
%--------------------------------------------------------------------------
