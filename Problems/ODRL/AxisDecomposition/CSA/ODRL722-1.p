%--------------------------------------------------------------------------
% File     : ODRL722-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA ConflictCriterion: claim touching cc NOT disjoint is wrong (touching IS disjoint cc)
% Version  : 1.0
% English  : [v0,v5] vs [v5,v10] touching cc: NOT disjoint (v5 shared).
%           : Wrong claim: disjoint(v0,v5,c,c,v5,v10,c,c).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL722-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL722-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v5,axiom,val(v5)).
fof(val_v10,axiom,val(v10)).
fof(ord_v0_v5,axiom,less(v0,v5)).
fof(ord_v5_v10,axiom,less(v5,v10)).
fof(distinct,axiom,$distinct(v0,v5,v10)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl722, conjecture,
    disjoint(v0, v5, c, c, v5, v10, c, c)).
%--------------------------------------------------------------------------
