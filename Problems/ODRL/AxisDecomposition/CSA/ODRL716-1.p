%--------------------------------------------------------------------------
% File     : ODRL716-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA SingleAxis: claim lt∩lt conflict when compatible (wrong)
% Version  : 1.0
% English  : lt 800 vs lt 600: (0,800)∩(0,600)=(0,600)≠∅ — Compatible.
%           : Wrong claim: no overlap.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL716-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL716-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v600,axiom,val(v600)).
fof(val_v800,axiom,val(v800)).
fof(ord_v0_v600,axiom,less(v0,v600)).
fof(ord_v600_v800,axiom,less(v600,v800)).
fof(distinct,axiom,$distinct(v0,v600,v800)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl716, conjecture,
    ~?[X]: (in_open(X,v0,v800) & in_open(X,v0,v600))).
%--------------------------------------------------------------------------
