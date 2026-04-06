%--------------------------------------------------------------------------
% File     : ODRL302-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : width < 600 vs width ≥ 600: open/closed boundary
% Version  : 1.0
% English  : width lt 600   → (0, 600)    [def:interval-denotation, lt; D_k=(0,∞)]
%           : width gteq 600 → [600, ∞)   [def:interval-denotation, gteq]
%           : (0, 600) ∩ [600, ∞) = ∅
%           : Conflict Criterion (oc): u1=600 open, l2=600 closed → u1 ≤ l2.
%           : Proof is order contradiction (X<600 & X≥600); density not needed.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL302-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL302-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% v0 = domain lower bound (excluded); v600 = constraint value
% in_open(X,v0,v600) encodes (0,600) = sem(lt 600) over D_k=(0,inf)
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl302, conjecture,
    ~?[X]: (in_open(X, v0, v600) & leq(v600, X))).
%--------------------------------------------------------------------------
