%--------------------------------------------------------------------------
% File     : ODRL600-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : prec_cc: less(U,L) implies prec(U,L,c,c)
% Version  : 1.0
% English  : thm:criterion prec_cc: less(v5,v6) => prec(v5,v6,c,c)
%           : Closed upper v5, closed lower v6: strict separation suffices.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL600-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL600-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v5,  axiom, val(v5)).
fof(val_v6,  axiom, val(v6)).
fof(ord_v5_v6, axiom, less(v5, v6)).
fof(distinct, axiom, $distinct(v5, v6)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl600, conjecture,
    prec(v5, v6, c, c)).
%--------------------------------------------------------------------------
