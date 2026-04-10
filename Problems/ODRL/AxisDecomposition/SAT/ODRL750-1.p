%--------------------------------------------------------------------------
% File     : ODRL750-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : ORD000 strict total order is satisfiable
% Version  : 1.0
% English  : The strict total order axioms of ORD000-0.ax are consistent.
%           : Witness: v0 < v600 < v1200 forms a valid strict total order.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL750-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : SAT — axiom layer consistency witness.
%           : No conjecture; model finder confirms satisfiability.
%           : Policy source: Policies/ODRL750-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').

% ─── Named constants and witness axioms ────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
