%--------------------------------------------------------------------------
% File     : ODRL350-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Depth breaks 3D subsumption → Conflict
% Version  : 1.0
% English  : Width:  (0,600]  ⊆ (0,1200]  Compatible
%           : Height: (0,400]  ⊆ (0,800]   Compatible
%           : Depth:  (0,32]   ⊄ (0,16]    Conflict — escape Z=v32 ∈ A_d, Z ∉ B_d
%           : box_containment: depth escape → Conflict  [def:box-containment]
%           : SMT: escape witness (any x∈A_w, any y∈A_h, z=32) → sat.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL350-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL350-policy.ttl
%--------------------------------------------------------------------------
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
fof(odrl350, conjecture,
    ?[X,Y,Z]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400) & in_lopen(Z, v0, v32)) &
           ~(in_lopen(X, v0, v1200) & in_lopen(Y, v0, v800) & in_lopen(Z, v0, v16)))).
%--------------------------------------------------------------------------
