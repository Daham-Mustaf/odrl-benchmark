%--------------------------------------------------------------------------
% File     : ODRL736-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Projection: claim shape_point in_closed(v400,v600,v600) (wrong)
% Version  : 1.0
% English  : shape_point: in_closed(X,V,V) iff X=V.
%           : v400 ≠ v600 so in_closed(v400,v600,v600) is false.
%           : Wrong claim.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL736-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL736-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PROJ000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v400,axiom,val(v400)).
fof(val_v600,axiom,val(v600)).
fof(ord_v400_v600,axiom,less(v400,v600)).
fof(distinct,axiom,$distinct(v400,v600)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl736, conjecture,
    in_closed(v400, v600, v600)).
%--------------------------------------------------------------------------
