%--------------------------------------------------------------------------
% File     : ODRL756-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT SingleAxis: gteq constraint is satisfiable
% Version  : 1.0
% English  : width gteq 200: [200,∞) is non-empty. Witness: v400.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL756-1.p
%
% Status   : Satisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_SAT_RFN
%
% Comments : SAT — axiom layer consistency witness.
%           : No conjecture; model finder confirms satisfiability.
%           : Policy source: Policies/ODRL756-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and witness axioms ────────────────────────────────
fof(val_v200,axiom,val(v200)).
fof(val_v400,axiom,val(v400)).
fof(ord_v200_v400,axiom,less(v200,v400)).
fof(distinct,axiom,$distinct(v200,v400)).
fof(witness,axiom,leq(v200,v400)).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
