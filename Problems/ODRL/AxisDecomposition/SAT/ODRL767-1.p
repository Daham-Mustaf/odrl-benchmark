%--------------------------------------------------------------------------
% File     : ODRL767-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT Box3D: three axis_conflict facts on distinct axes are consistent
% Version  : 1.0
% English  : Three axis_conflict facts on distinct (width, height, depth) 4-tuples
%           : coexist. Each uses a different pair of disjoint intervals drawn from a
%           : shared strict chain v1 < v2 < ... < v6. No shared variable forces a
%           : contradiction; the axioms are consistent.
%           : Width:  [v1,v2] vs [v3,v4]  disjoint (less(v2,v3))
%           : Height: [v2,v3] vs [v4,v5]  disjoint (less(v3,v4))
%           : Depth:  [v3,v4] vs [v5,v6]  disjoint (less(v4,v5))
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
fof(val_v1, axiom, val(v1)).
fof(val_v2, axiom, val(v2)).
fof(val_v3, axiom, val(v3)).
fof(val_v4, axiom, val(v4)).
fof(val_v5, axiom, val(v5)).
fof(val_v6, axiom, val(v6)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v4_v5, axiom, less(v4, v5)).
fof(ord_v5_v6, axiom, less(v5, v6)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v5, v6)).
fof(cf_width,  axiom, axis_conflict(v1, v2, v3, v4)).
fof(cf_height, axiom, axis_conflict(v2, v3, v4, v5)).
fof(cf_depth,  axiom, axis_conflict(v3, v4, v5, v6)).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
