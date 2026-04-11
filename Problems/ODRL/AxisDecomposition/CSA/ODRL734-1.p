%--------------------------------------------------------------------------
% File     : ODRL734-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA BoxContainment: claim larger interval subsumes smaller (wrong direction)
% Version  : 1.0
% English  : [v0,v600] does NOT subsume [v0,v400] — wrong direction.
%           : Wrong claim: subs_verdict([v0,v600],[v0,v400])=compatible.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL734-1.p
%
% Status   : CounterSatisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL734-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/SUBS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v400,axiom,val(v400)).
fof(val_v600,axiom,val(v600)).
fof(ord_v0_v400,axiom,less(v0,v400)).
fof(ord_v400_v600,axiom,less(v400,v600)).
fof(distinct,axiom,$distinct(v0,v400,v600)).
fof(no_subs,axiom,~axis_subsumes(v0,v600,v0,v400)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl734, conjecture,
    subs_verdict(v0, v600, present, v0, v400, present) = compatible).
%--------------------------------------------------------------------------
