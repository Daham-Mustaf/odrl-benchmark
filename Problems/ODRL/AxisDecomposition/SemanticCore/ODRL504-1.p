%--------------------------------------------------------------------------
% File     : ODRL504-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : lem:totality — eq denotation is non-empty
% Version  : 1.0
% English  : lem:totality — eq denotation is non-empty
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL504-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL504-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl504, conjecture,
    ?[X]: in_closed(X, v200, v200)).
%--------------------------------------------------------------------------
