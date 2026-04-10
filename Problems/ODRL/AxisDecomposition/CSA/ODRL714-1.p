%--------------------------------------------------------------------------
% File     : ODRL714-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Completion: claim box(compatible,unknown)=conflict (wrong)
% Version  : 1.0
% English  : Flip of ODRL635: box_verdict(compatible,unknown)=unknown.
%           : Wrong claim: box_verdict(compatible,unknown)=conflict.
%           : Countermodel: box_conflict requires at least one conflict.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL714-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL714-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl714, conjecture,
    box_verdict(compatible, unknown) = conflict).
%--------------------------------------------------------------------------
