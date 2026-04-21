%--------------------------------------------------------------------------
% File     : ODRL406-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 2D near-miss gap=1 both axes (5 constants)
% Version  : 1.0
% English  : Width: lteq 599 ∩ gteq 601 = (0,599]∩[601,∞) = ∅ Conflict (599<601)
%           : Height: lteq 399 ∩ gteq 401 = (0,399]∩[401,∞) = ∅ Conflict (399<401)
%           : Both axes conflict, minimum integer gap.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL406-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL406-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v399, axiom, val(v399)).
fof(val_v401, axiom, val(v401)).
fof(val_v599, axiom, val(v599)).
fof(val_v601, axiom, val(v601)).
fof(ord_v0_v399, axiom, less(v0, v399)).
fof(ord_v0_v401, axiom, less(v0, v401)).
fof(ord_v0_v599, axiom, less(v0, v599)).
fof(ord_v0_v601, axiom, less(v0, v601)).
fof(ord_v399_v401, axiom, less(v399, v401)).
fof(ord_v399_v599, axiom, less(v399, v599)).
fof(ord_v399_v601, axiom, less(v399, v601)).
fof(ord_v401_v599, axiom, less(v401, v599)).
fof(ord_v401_v601, axiom, less(v401, v601)).
fof(ord_v599_v601, axiom, less(v599, v601)).
fof(distinct, axiom, $distinct(v0, v399, v401, v599, v601)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl406, conjecture,
    ![X,Y]: ~(in_lopen(X, v0, v599) & leq(v601, X) &
          in_lopen(Y, v0, v399) & leq(v401, Y))).
%--------------------------------------------------------------------------
