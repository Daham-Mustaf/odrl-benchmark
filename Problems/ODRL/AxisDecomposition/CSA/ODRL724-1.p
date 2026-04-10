%--------------------------------------------------------------------------
% File     : ODRL724-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA ConflictCriterion: claim upper_tag(eq,o) (wrong — eq has closed upper)
% Version  : 1.0
% English  : upper_tag(eq,c) holds — eq has closed upper boundary.
%           : Wrong claim: upper_tag(eq,o).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL724-1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : CSA — wrong verdict claim, countermodel exists.
%           : Flip of corresponding THM problem.
%           : Policy source: Policies/ODRL724-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture (WRONG — countermodel exists) ──────────────────────
fof(odrl724, conjecture,
    upper_tag(eq, o)).
%--------------------------------------------------------------------------
