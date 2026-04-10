%--------------------------------------------------------------------------
% File     : ODRL763-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT SemanticCore: core axioms with overlap witness are satisfiable
% Version  : 1.0
% English  : ORD000+AXIS000 consistent. Witness: in_closed(v400,v0,v600).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL763-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : SAT — axiom layer consistency witness.
%           : No conjecture; model finder confirms satisfiability.
%           : Policy source: Policies/ODRL763-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and witness axioms ────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v400,axiom,val(v400)).
fof(val_v600,axiom,val(v600)).
fof(ord_v0_v400,axiom,less(v0,v400)).
fof(ord_v400_v600,axiom,less(v400,v600)).
fof(distinct,axiom,$distinct(v0,v400,v600)).
fof(witness,axiom,in_closed(v400,v0,v600)).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
