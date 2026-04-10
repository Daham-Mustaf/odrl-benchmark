%--------------------------------------------------------------------------
% File     : ODRL726-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Composition: claim or(unknown,unknown)=compatible (wrong)
% Version  : 1.0
% English  : or_verdict(unknown,unknown)=unknown.
%           : Wrong claim: =compatible.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL726-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL726-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl726, conjecture,
    or_verdict(unknown, unknown) = compatible).
%--------------------------------------------------------------------------
