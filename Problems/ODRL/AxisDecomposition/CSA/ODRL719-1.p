%--------------------------------------------------------------------------
% File     : ODRL719-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Box2D: claim 2D compatible when height conflicts (wrong)
% Version  : 1.0
% English  : Width ok. Height: (0,300]∩[600,∞)=∅.
%           : Wrong: claim overlap on both axes.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL719-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL719-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v300,axiom,val(v300)).
fof(val_v400,axiom,val(v400)).
fof(val_v600,axiom,val(v600)).
fof(val_v800,axiom,val(v800)).
fof(ord_v0_v300,axiom,less(v0,v300)).
fof(ord_v0_v400,axiom,less(v0,v400)).
fof(ord_v300_v400,axiom,less(v300,v400)).
fof(ord_v300_v600,axiom,less(v300,v600)).
fof(ord_v400_v600,axiom,less(v400,v600)).
fof(ord_v600_v800,axiom,less(v600,v800)).
fof(distinct,axiom,$distinct(v0,v300,v400,v600,v800)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl719, conjecture,
    ?[X,Y]: (in_lopen(X,v0,v800) & leq(v400,X) & in_lopen(Y,v0,v300) & leq(v600,Y))).
%--------------------------------------------------------------------------
