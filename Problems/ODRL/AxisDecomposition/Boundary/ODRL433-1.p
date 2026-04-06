%--------------------------------------------------------------------------
% File     : ODRL433-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Subsumption: lt⊆lteq on width, lteq⊆lteq on height → Compatible
% Version  : 1.0
% English  : Width:  (0,600) ⊆ (0,600] Compatible (open subset of closed)
%           : Height: (0,400] ⊆ (0,800] Compatible
%           : A ⊆ B on all axes → Compatible [def:box-containment]
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL433-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL433-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v400, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl433, conjecture,
    ![X,Y]: ((in_open(X, v0, v600) & in_lopen(Y, v0, v400)) =>
           (in_lopen(X, v0, v600) & in_lopen(Y, v0, v800)))).
%--------------------------------------------------------------------------
