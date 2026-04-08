%--------------------------------------------------------------------------
% File     : ODRL607-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : disjoint co: [v0,v5] vs (v5,v10] open lower kills overlap
% Version  : 1.0
% English  : thm:criterion co: leq(v5,v5) => prec(v5,v5,c,o)
%           : [v0,v5] ends at v5 closed; (v5,v10] starts strictly above v5.
%           : They share no point: disjoint.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL607-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL607-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,     axiom, val(v0)).
fof(val_v5,     axiom, val(v5)).
fof(val_v10,    axiom, val(v10)).
fof(ord_v0_v5,  axiom, less(v0, v5)).
fof(ord_v5_v10, axiom, less(v5, v10)).
fof(distinct,   axiom, $distinct(v0, v5, v10)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl607, conjecture,
    disjoint(v0, v5, c, c, v5, v10, o, c)).
%--------------------------------------------------------------------------
