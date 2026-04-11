%--------------------------------------------------------------------------
% File     : ODRL767-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT Box3D: 3-axis conflict axioms are internally consistent
% Version  : 1.0
% English  : Three separate axis_conflict facts coexist. Axioms are consistent.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL767-1.p
%
% Status   : Satisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_SAT_RFN
%
% Comments : SAT — axiom layer consistency witness.
%           : No conjecture; model finder confirms satisfiability.
%           : Policy source: Policies/ODRL767-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and witness axioms ────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v400,axiom,val(v400)).
fof(val_v600,axiom,val(v600)).
fof(val_v800,axiom,val(v800)).
fof(ord_v0_v400,axiom,less(v0,v400)).
fof(ord_v400_v600,axiom,less(v400,v600)).
fof(ord_v600_v800,axiom,less(v600,v800)).
fof(distinct,axiom,$distinct(v0,v400,v600,v800)).
fof(cf1,axiom,axis_conflict(v0,v400,v600,v800)).
fof(cf2,axiom,axis_conflict(v0,v400,v600,v800)).
fof(cf3,axiom,axis_conflict(v0,v400,v600,v800)).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
