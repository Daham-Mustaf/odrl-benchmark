%--------------------------------------------------------------------------
% File     : ODRL604-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : prec_oo: leq(U,L) implies prec(U,L,o,o)
% Version  : 1.0
% English  : thm:criterion prec_oo: leq(v5,v5) => prec(v5,v5,o,o)
%           : Both endpoints open: equal value is enough for separation.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL604-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL604-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v5, axiom, val(v5)).
fof(val_v6, axiom, val(v6)).
fof(ord_v5_v6, axiom, less(v5, v6)).
fof(distinct, axiom, $distinct(v5, v6)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl604, conjecture,
    prec(v5, v5, o, o)).
%--------------------------------------------------------------------------
