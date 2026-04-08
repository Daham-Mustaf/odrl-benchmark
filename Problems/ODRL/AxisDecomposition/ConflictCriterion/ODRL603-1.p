%--------------------------------------------------------------------------
% File     : ODRL603-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : prec_co: leq(U,L) implies prec(U,L,c,o)
% Version  : 1.0
% English  : thm:criterion prec_co: leq(v5,v5) => prec(v5,v5,c,o)
%           : Closed upper v5 (attained), open lower v5 (excluded): equal ok.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL603-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL603-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v5, axiom, val(v5)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl603, conjecture,
    prec(v5, v5, c, o)).
%--------------------------------------------------------------------------
