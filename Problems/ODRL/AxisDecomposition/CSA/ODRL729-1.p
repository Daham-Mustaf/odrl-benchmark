%--------------------------------------------------------------------------
% File     : ODRL729-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Completion: claim completion_conflict when U=V (wrong)
% Version  : 1.0
% English  : completion_conflict requires less(U,V). U=V=v600 fails.
%           : Wrong claim.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL729-1.p
%
% Status   : CounterSatisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL729-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMPL000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v600,axiom,val(v600)).
fof(val_v1200,axiom,val(v1200)).
fof(ord_v0_v600,axiom,less(v0,v600)).
fof(ord_v600_v1200,axiom,less(v600,v1200)).
fof(distinct,axiom,$distinct(v0,v600,v1200)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl729, conjecture,
    completion_conflict(v600, v600, v0, v1200)).
%--------------------------------------------------------------------------
