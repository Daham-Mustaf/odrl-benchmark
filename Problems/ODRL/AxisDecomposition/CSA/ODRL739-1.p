%--------------------------------------------------------------------------
% File     : ODRL739-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Boundary: claim gteq∩lt compatible when equal (wrong)
% Version  : 1.0
% English  : gteq 600 vs lt 600: [600,∞)∩(0,600)=∅.
%           : Wrong claim: overlap.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL739-1.p
%
% Status   : CounterSatisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL739-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v600,axiom,val(v600)).
fof(ord_v0_v600,axiom,less(v0,v600)).
fof(distinct,axiom,$distinct(v0,v600)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl739, conjecture,
    ?[X]: (leq(v600,X) & in_open(X,v0,v600))).
%--------------------------------------------------------------------------
