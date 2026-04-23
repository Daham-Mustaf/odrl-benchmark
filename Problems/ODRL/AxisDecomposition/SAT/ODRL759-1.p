%--------------------------------------------------------------------------
% File     : ODRL759-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT Box3D: 3D box constraint is satisfiable
% Version  : 1.0
% English  : 3D box: width [200,800], height [100,600], depth [8,32] is non-empty.
%           : Witness: (x,y,z) = (v400, v300, v16), all inside their closed intervals.
%           : Unfolded into leq primitives so Vampire-FMB closes without instantiating in_box3.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL759-1.p
%
% Status   : Satisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_SAT_RFN
%
% Comments : SAT — axiom layer consistency witness.
%           : No conjecture; model finder confirms satisfiability.
%           : Policy source: Policies/ODRL759-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and witness axioms ────────────────────────────────
fof(val_v8,   axiom, val(v8)).
fof(val_v16,  axiom, val(v16)).
fof(val_v32,  axiom, val(v32)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v8_v16,    axiom, less(v8,   v16)).
fof(ord_v16_v32,   axiom, less(v16,  v32)).
fof(ord_v32_v100,  axiom, less(v32,  v100)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v8, v16, v32, v100, v200, v300, v400, v600, v800)).
fof(witness_x, axiom, leq(v200, v400) & leq(v400, v800)).
fof(witness_y, axiom, leq(v100, v300) & leq(v300, v600)).
fof(witness_z, axiom, leq(v8,   v16)  & leq(v16,  v32)).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
