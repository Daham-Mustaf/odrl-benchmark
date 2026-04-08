%--------------------------------------------------------------------------
% File     : ODRL435-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 3D eq×cc×eq — all three axes touch at named constants → Compatible
% Version  : 1.0
% English  : Width:  eq 600 ∩ lteq 600 = {600} Compatible
%           : Height: lteq 400 ∩ gteq 400 = {400} Compatible (cc)
%           : Depth:  eq 200 ∩ gteq 200 = {200} Compatible
%           : Witnesses: X=v600, Y=v400, Z=v200.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL435-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL435-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl435, conjecture,
    ?[X,Y,Z]: (in_closed(X, v600, v600) & in_lopen(X, v0, v600) &
           in_lopen(Y, v0, v400) & leq(v400, Y) &
           in_closed(Z, v200, v200) & leq(v200, Z))).
%--------------------------------------------------------------------------
