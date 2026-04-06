%--------------------------------------------------------------------------
% File     : ODRL310-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : (0,1200] ⊄ (0,600]: wider does not subsume tighter
% Version  : 1.0
% English  : width lteq 1200 → (0, 1200]  [def:interval-denotation, lteq]
%           : width lteq 600  → (0, 600]   [def:interval-denotation, lteq]
%           : (0, 1200] ⊄ (0, 600]         [def:box-containment, Conflict]
%           : Counterexample: X = v800 ∈ (0,1200] but v800 ∉ (0,600]
%           : since less(v600, v800) and less(v800, v1200).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL310-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL310-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% v0 = domain lower bound (excluded); v600, v800, v1200 = constraint/witness values
% v800 witnesses X ∈ A \ B
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v0_v1200,   axiom, less(v0, v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v800, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl310, conjecture,
    ?[X]: (in_lopen(X, v0, v1200) & ~in_lopen(X, v0, v600))).
%--------------------------------------------------------------------------
