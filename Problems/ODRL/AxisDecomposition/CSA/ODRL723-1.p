%--------------------------------------------------------------------------
% File     : ODRL723-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA ConflictCriterion: claim disjoint oo at equal endpoints (wrong)
% Version  : 1.0
% English  : prec(v5,v6,o,o) requires leq(v5,v6): true.
%           : Wrong claim: ~disjoint with open endpoints when they are separated.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL723-1.p
%
% Status   : CounterSatisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL723-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v5,axiom,val(v5)).
fof(val_v6,axiom,val(v6)).
fof(val_v10,axiom,val(v10)).
fof(ord_v0_v5,axiom,less(v0,v5)).
fof(ord_v5_v6,axiom,less(v5,v6)).
fof(ord_v6_v10,axiom,less(v6,v10)).
fof(distinct,axiom,$distinct(v0,v5,v6,v10)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl723, conjecture,
    ~disjoint(v0, v5, o, c, v6, v10, c, o)).
%--------------------------------------------------------------------------
