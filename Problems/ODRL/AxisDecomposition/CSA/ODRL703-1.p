%--------------------------------------------------------------------------
% File     : ODRL703-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Boundary oc: claim lt∩gteq compatible (wrong)
% Version  : 1.0
% English  : Flip of ODRL422: lt 600 vs gteq 600.
%           : (0,600) ∩ [600,∞) = ∅ — Conflict.
%           : Wrong claim: overlap ?[X]: X<600 & X≥600.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL703-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL703-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl703, conjecture,
    ?[X]: (in_open(X,v0,v600) & leq(v600,X))).
%--------------------------------------------------------------------------
