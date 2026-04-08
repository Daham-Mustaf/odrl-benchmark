%--------------------------------------------------------------------------
% File     : ODRL601-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : prec_cc negative: equal endpoints not prec(cc)
% Version  : 1.0
% English  : thm:criterion prec_cc negative: ~less(v5,v5) => ~prec(v5,v5,c,c)
%           : Touching closed endpoints are NOT separated: intervals overlap.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL601-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL601-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v5, axiom, val(v5)).
fof(distinct, axiom, val(v5)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl601, conjecture,
    ~prec(v5, v5, c, c)).
%--------------------------------------------------------------------------
