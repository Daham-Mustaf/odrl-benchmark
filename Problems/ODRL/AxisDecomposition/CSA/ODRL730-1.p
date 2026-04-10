%--------------------------------------------------------------------------
% File     : ODRL730-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Completion: claim box_verdict(unknown,compatible)=conflict (wrong)
% Version  : 1.0
% English  : box_verdict(unknown,compatible)=unknown.
%           : Wrong claim: =conflict.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL730-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL730-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl730, conjecture,
    box_verdict(unknown, compatible) = conflict).
%--------------------------------------------------------------------------
