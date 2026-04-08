%--------------------------------------------------------------------------
% File     : ODRL469-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : xone-A vs or-B: ~A_x & A_y branch with B satisfied → Compatible
% Version  : 1.0
% English  : PolicyA: xone(width lteq 600, height lteq 400)
%           : PolicyB: or(width gteq 800, height gteq 200)
%           : Branch (~A_x & A_y): X≥800>600→X∉(0,600] ✓, Y∈(0,400]→A_y ✓
%           : PolicyB: X≥800 ✓
%           : Witness: X=v800, Y=v200. verdictXone=Compatible
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL469-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL469-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl469, conjecture,
    ?[X,Y]: (((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400))) |
              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400))) &
          (leq(v800, X) | leq(v200, Y)))).
%--------------------------------------------------------------------------
