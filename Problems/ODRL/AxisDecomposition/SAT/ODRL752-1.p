%--------------------------------------------------------------------------
% File     : ODRL752-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : PREC000 endpoint precedence is satisfiable
% Version  : 1.0
% English  : The PREC000 endpoint precedence axioms are consistent.
%           : Witness: prec(v5,v6,c,c) holds since less(v5,v6).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL752-1.p
%
% Status   : Satisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_SAT_RFN
%
% Comments : SAT — axiom layer consistency witness.
%           : No conjecture; model finder confirms satisfiability.
%           : Policy source: Policies/ODRL752-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and witness axioms ────────────────────────────────
fof(val_v5, axiom, val(v5)).
fof(val_v6, axiom, val(v6)).
fof(ord_v5_v6, axiom, less(v5, v6)).
fof(distinct, axiom, $distinct(v5, v6)).
fof(prec_witness, axiom, prec(v5, v6, c, c)).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
