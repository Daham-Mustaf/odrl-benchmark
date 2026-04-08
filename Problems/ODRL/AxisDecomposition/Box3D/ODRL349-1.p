%--------------------------------------------------------------------------
% File     : ODRL349-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 3D box A ⊆ B on all axes → Compatible
% Version  : 1.0
% English  : Width:  (0,600]  ⊆ (0,1200]  Compatible
%           : Height: (0,400]  ⊆ (0,800]   Compatible
%           : Depth:  (0,16]   ⊆ (0,32]    Compatible
%           : box_containment: A ⊆ B on all 3 axes → Compatible  [def:box-containment]
%           : SMT: no escape witness in any axis → unsat.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL349-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL349-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,         axiom, val(v0)).
fof(val_v16,        axiom, val(v16)).
fof(val_v32,        axiom, val(v32)).
fof(val_v400,       axiom, val(v400)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v16,     axiom, less(v0,   v16)).
fof(ord_v0_v32,     axiom, less(v0,   v32)).
fof(ord_v0_v400,    axiom, less(v0,   v400)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v800,    axiom, less(v0,   v800)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v16_v32,    axiom, less(v16,  v32)).
fof(ord_v16_v400,   axiom, less(v16,  v400)).
fof(ord_v16_v600,   axiom, less(v16,  v600)).
fof(ord_v16_v800,   axiom, less(v16,  v800)).
fof(ord_v16_v1200,  axiom, less(v16,  v1200)).
fof(ord_v32_v400,   axiom, less(v32,  v400)).
fof(ord_v32_v600,   axiom, less(v32,  v600)).
fof(ord_v32_v800,   axiom, less(v32,  v800)).
fof(ord_v32_v1200,  axiom, less(v32,  v1200)).
fof(ord_v400_v600,  axiom, less(v400, v600)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v16, v32, v400, v600, v800, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl349, conjecture,
    ![X,Y,Z]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400) & in_lopen(Z, v0, v16)) =>
           (in_lopen(X, v0, v1200) & in_lopen(Y, v0, v800) & in_lopen(Z, v0, v32)))).
%--------------------------------------------------------------------------
