%--------------------------------------------------------------------------
% File     : ODRL733-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA BoxContainment: claim box_subs(unknown,compatible)=compatible (wrong)
% Version  : 1.0
% English  : box_subs(unknown,compatible)=unknown.
%           : Wrong claim: =compatible.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL733-1.p
%
% Status   : CounterSatisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL733-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/SUBS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl733, conjecture,
    box_subs(unknown, compatible) = compatible).
%--------------------------------------------------------------------------
