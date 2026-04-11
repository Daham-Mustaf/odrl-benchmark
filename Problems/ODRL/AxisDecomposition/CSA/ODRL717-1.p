%--------------------------------------------------------------------------
% File     : ODRL717-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA SingleAxis: claim eq∩eq compatible for different values (wrong)
% Version  : 1.0
% English  : eq 400 vs eq 600: {400}∩{600}=∅.
%           : Wrong: claim overlap.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL717-1.p
%
% Status   : CounterSatisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL717-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v400,axiom,val(v400)).
fof(val_v600,axiom,val(v600)).
fof(ord_v400_v600,axiom,less(v400,v600)).
fof(distinct,axiom,$distinct(v400,v600)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl717, conjecture,
    ?[X]: (in_closed(X,v400,v400) & in_closed(X,v600,v600))).
%--------------------------------------------------------------------------
