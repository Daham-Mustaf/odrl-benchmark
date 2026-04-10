%--------------------------------------------------------------------------
% File     : ODRL718-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Box2D: claim 2D box compatible when width conflicts (wrong)
% Version  : 1.0
% English  : Width: (0,400]∩[800,∞)=∅. Height: [100,600] overlap.
%           : Wrong claim: box2_compatible.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL718-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL718-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v100,axiom,val(v100)).
fof(val_v400,axiom,val(v400)).
fof(val_v600,axiom,val(v600)).
fof(val_v800,axiom,val(v800)).
fof(ord_v0_v100,axiom,less(v0,v100)).
fof(ord_v0_v400,axiom,less(v0,v400)).
fof(ord_v100_v400,axiom,less(v100,v400)).
fof(ord_v400_v600,axiom,less(v400,v600)).
fof(ord_v600_v800,axiom,less(v600,v800)).
fof(distinct,axiom,$distinct(v0,v100,v400,v600,v800)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl718, conjecture,
    ?[X,Y]: (in_lopen(X,v0,v400) & leq(v800,X) & in_lopen(Y,v0,v600) & leq(v100,Y))).
%--------------------------------------------------------------------------
