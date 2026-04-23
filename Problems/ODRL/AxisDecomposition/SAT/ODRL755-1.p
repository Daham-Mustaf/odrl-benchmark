%--------------------------------------------------------------------------
% File     : ODRL755-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT SingleAxis: lteq constraint is satisfiable
% Version  : 1.0
% English  : width lteq 800: (0,800] is non-empty. Witness: v400.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL755-1.p
%
% Status   : Satisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_SAT_RFN
%
% Comments : SAT — axiom layer consistency witness.
%           : No conjecture; model finder confirms satisfiability.
%           : Policy source: Policies/ODRL755-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and witness axioms ────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct, axiom, $distinct(v0, v400, v800)).
fof(witness,  axiom, in_lopen(v400, v0, v800)).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
