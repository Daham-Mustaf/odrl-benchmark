%--------------------------------------------------------------------------
% File     : ODRL727-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Composition: claim xone(conflict,conflict)=compatible (wrong)
% Version  : 1.0
% English  : xone_verdict(conflict,conflict)=conflict.
%           : Wrong claim: =compatible.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL727-1.p
%
% Status   : CounterSatisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL727-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl727, conjecture,
    xone_verdict(conflict, conflict) = compatible).
%--------------------------------------------------------------------------
