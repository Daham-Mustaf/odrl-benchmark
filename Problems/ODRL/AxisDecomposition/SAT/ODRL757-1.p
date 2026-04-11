%--------------------------------------------------------------------------
% File     : ODRL757-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT Box2D: 2D box constraint is satisfiable
% Version  : 1.0
% English  : Width [200,800], Height [100,600]. Box non-empty. Witness: (400,300).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL757-1.p
%
% Status   : Satisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_SAT_RFN
%
% Comments : SAT — axiom layer consistency witness.
%           : No conjecture; model finder confirms satisfiability.
%           : Policy source: Policies/ODRL757-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PROJ000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and witness axioms ────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v100,axiom,val(v100)).
fof(val_v200,axiom,val(v200)).
fof(val_v300,axiom,val(v300)).
fof(val_v400,axiom,val(v400)).
fof(val_v600,axiom,val(v600)).
fof(val_v800,axiom,val(v800)).
fof(ord_v0_v100,axiom,less(v0,v100)).
fof(ord_v100_v200,axiom,less(v100,v200)).
fof(ord_v200_v300,axiom,less(v200,v300)).
fof(ord_v300_v400,axiom,less(v300,v400)).
fof(ord_v400_v600,axiom,less(v400,v600)).
fof(ord_v600_v800,axiom,less(v600,v800)).
fof(distinct,axiom,$distinct(v0,v100,v200,v300,v400,v600,v800)).
fof(witness,axiom,in_box2(v400,v300,v200,v800,v100,v600)).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
