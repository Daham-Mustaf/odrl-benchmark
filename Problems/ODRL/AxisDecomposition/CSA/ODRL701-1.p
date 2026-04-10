%--------------------------------------------------------------------------
% File     : ODRL701-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA SingleAxis: claim eq values compatible when distinct (wrong)
% Version  : 1.0
% English  : width eq 600 vs eq 800: {600} ∩ {800} = ∅ — Conflict.
%           : Wrong claim: ?[X]: X=v600 & X=v800. Countermodel: v600≠v800.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL701-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL701-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v600, v800)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl701, conjecture,
    ?[X]: (in_closed(X,v600,v600) & in_closed(X,v800,v800))).
%--------------------------------------------------------------------------
