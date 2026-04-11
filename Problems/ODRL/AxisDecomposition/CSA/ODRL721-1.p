%--------------------------------------------------------------------------
% File     : ODRL721-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA ConflictCriterion: claim prec(v5,v5,c,c) holds (wrong)
% Version  : 1.0
% English  : prec(v5,v5,c,c) requires less(v5,v5) — impossible by irreflexivity.
%           : Wrong claim.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL721-1.p
%
% Status   : CounterSatisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL721-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v5,axiom,val(v5)).
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl721, conjecture,
    prec(v5, v5, c, c)).
%--------------------------------------------------------------------------
