%--------------------------------------------------------------------------
% File     : ODRL769-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT PolicyQuality: 4-axis drone policy is satisfiable
% Version  : 1.0
% English  : Drone: W [200,800], H [100,600], D [8,32], Alt [72,300]. Witness: (400,300,16,150).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL769-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : SAT — axiom layer consistency witness.
%           : No conjecture; model finder confirms satisfiability.
%           : Policy source: Policies/ODRL769-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and witness axioms ────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v8,axiom,val(v8)).
fof(val_v16,axiom,val(v16)).
fof(val_v32,axiom,val(v32)).
fof(val_v72,axiom,val(v72)).
fof(val_v100,axiom,val(v100)).
fof(val_v150,axiom,val(v150)).
fof(val_v200,axiom,val(v200)).
fof(val_v300,axiom,val(v300)).
fof(val_v400,axiom,val(v400)).
fof(val_v600,axiom,val(v600)).
fof(val_v800,axiom,val(v800)).
fof(ord_v0_v8,axiom,less(v0,v8)).
fof(ord_v8_v16,axiom,less(v8,v16)).
fof(ord_v16_v32,axiom,less(v16,v32)).
fof(ord_v32_v72,axiom,less(v32,v72)).
fof(ord_v72_v100,axiom,less(v72,v100)).
fof(ord_v100_v150,axiom,less(v100,v150)).
fof(ord_v150_v200,axiom,less(v150,v200)).
fof(ord_v200_v300,axiom,less(v200,v300)).
fof(ord_v300_v400,axiom,less(v300,v400)).
fof(ord_v400_v600,axiom,less(v400,v600)).
fof(ord_v600_v800,axiom,less(v600,v800)).
fof(distinct,axiom,$distinct(v0,v8,v16,v32,v72,v100,v150,v200,v300,v400,v600,v800)).
fof(witness,axiom,leq(v200,v400) & leq(v400,v800) & leq(v100,v300) & leq(v300,v600) & leq(v8,v16) & leq(v16,v32) & leq(v72,v150) & leq(v150,v300)).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
