%--------------------------------------------------------------------------
% File     : ODRL715-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA SingleAxis: claim gteq∩lteq compatible when disjoint (wrong)
% Version  : 1.0
% English  : gteq 800 vs lteq 400: [800,∞)∩(0,400]=∅.
%           : Wrong claim: overlap exists.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL715-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL715-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v400,axiom,val(v400)).
fof(val_v800,axiom,val(v800)).
fof(ord_v0_v400,axiom,less(v0,v400)).
fof(ord_v400_v800,axiom,less(v400,v800)).
fof(distinct,axiom,$distinct(v0,v400,v800)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl715, conjecture,
    ?[X]: (leq(v800,X) & in_lopen(X,v0,v400))).
%--------------------------------------------------------------------------
