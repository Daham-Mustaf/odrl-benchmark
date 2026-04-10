%--------------------------------------------------------------------------
% File     : ODRL708-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Composition: claim or(conflict,conflict)=compatible (wrong)
% Version  : 1.0
% English  : Flip of ODRL641: or_verdict(conflict,conflict)=conflict.
%           : Wrong claim: or_verdict(conflict,conflict)=compatible.
%           : Countermodel: violates or_conflict axiom.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL708-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL708-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl708, conjecture,
    or_verdict(conflict, conflict) = compatible).
%--------------------------------------------------------------------------
