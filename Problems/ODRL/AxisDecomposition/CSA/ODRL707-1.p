%--------------------------------------------------------------------------
% File     : ODRL707-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Boundary: claim eq∩gt compatible (wrong — boundary excluded)
% Version  : 1.0
% English  : eq 600 vs gt 600: {600} ∩ (600,∞) = ∅ — Conflict.
%           : Wrong claim: ?[X]: X=600 & X>600. Countermodel: irreflexive.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL707-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL707-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl707, conjecture,
    ?[X]: (in_closed(X,v600,v600) & less(v600,X))).
%--------------------------------------------------------------------------
