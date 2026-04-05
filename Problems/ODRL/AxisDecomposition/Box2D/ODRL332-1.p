%--------------------------------------------------------------------------
% File     : ODRL332-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 2D box A ⊄ B on width axis → Conflict
% Version  : 1.0
% English  : Width:  lteq 1200 → (0,1200] ⊄ (0,600] ← lteq 600  Conflict
%           : Escape witness: X=v800 ∈ (0,1200] but v800 ∉ (0,600]
%           : Height: lteq 800  → (0,800]  ⊆ (0,1200] ← lteq 1200 Compatible
%           : box_containment: width escape → Conflict  [def:box-containment]
%           : SMT: escape witness (x=800, any y∈A_h) → sat.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL332-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL332-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v800,    axiom, less(v0,   v800)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v800, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl332, conjecture,
    ?[X,Y]: ((in_lopen(X, v0, v1200) & in_lopen(Y, v0, v800)) &
          ~(in_lopen(X, v0, v600) & in_lopen(Y, v0, v1200)))).
%--------------------------------------------------------------------------
