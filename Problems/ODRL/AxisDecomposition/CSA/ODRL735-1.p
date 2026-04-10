%--------------------------------------------------------------------------
% File     : ODRL735-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Projection: claim v800 in box2 [v0,v600]^2 (wrong)
% Version  : 1.0
% English  : v800 > v600 so v800 not in [v0,v600].
%           : Wrong claim: in_box2(v800,v400,v0,v600,v0,v600).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL735-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL735-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PROJ000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v400,axiom,val(v400)).
fof(val_v600,axiom,val(v600)).
fof(val_v800,axiom,val(v800)).
fof(ord_v0_v400,axiom,less(v0,v400)).
fof(ord_v400_v600,axiom,less(v400,v600)).
fof(ord_v600_v800,axiom,less(v600,v800)).
fof(distinct,axiom,$distinct(v0,v400,v600,v800)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl735, conjecture,
    in_box2(v800, v400, v0, v600, v0, v600)).
%--------------------------------------------------------------------------
