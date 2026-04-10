%--------------------------------------------------------------------------
% File     : ODRL710-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Completion: claim conflict completion holds when U=V (wrong)
% Version  : 1.0
% English  : Flip of ODRL637: ~completion_conflict(v600,v600,v0,v1200).
%           : Wrong claim: completion_conflict(v600,v600,...) holds.
%           : Requires less(v600,v600) — contradicts irreflexivity.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL710-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL710-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMPL000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl710, conjecture,
    completion_conflict(v600, v600, v0, v1200)).
%--------------------------------------------------------------------------
