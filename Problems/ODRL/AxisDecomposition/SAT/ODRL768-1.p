%--------------------------------------------------------------------------
% File     : ODRL768-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT PolicyQuality: real-world HD policy is satisfiable
% Version  : 1.0
% English  : HD: width [640,1920], height [480,1080]. Witness: (1280,720).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL768-1.p
%
% Status   : Satisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_SAT_RFN
%
% Comments : SAT — axiom layer consistency witness.
%           : No conjecture; model finder confirms satisfiability.
%           : Policy source: Policies/ODRL768-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and witness axioms ────────────────────────────────
fof(val_v640,axiom,val(v640)).
fof(val_v720,axiom,val(v720)).
fof(val_v1080,axiom,val(v1080)).
fof(val_v1280,axiom,val(v1280)).
fof(val_v1920,axiom,val(v1920)).
fof(val_v480,axiom,val(v480)).
fof(ord_v480_v640,axiom,less(v480,v640)).
fof(ord_v640_v720,axiom,less(v640,v720)).
fof(ord_v720_v1080,axiom,less(v720,v1080)).
fof(ord_v1080_v1280,axiom,less(v1080,v1280)).
fof(ord_v1280_v1920,axiom,less(v1280,v1920)).
fof(distinct,axiom,$distinct(v480,v640,v720,v1080,v1280,v1920)).
fof(witness,axiom,leq(v640,v1280) & leq(v1280,v1920) & leq(v480,v720) & leq(v720,v1080)).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
