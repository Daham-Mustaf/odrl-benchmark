%--------------------------------------------------------------------------
% File     : ODRL764-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT SemanticCore: verdict algebra constants are consistent
% Version  : 1.0
% English  : conflict, compatible, unknown are distinct is_verdict constants.
%           : Axioms consistent.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL764-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : SAT — axiom layer consistency witness.
%           : No conjecture; model finder confirms satisfiability.
%           : Policy source: Policies/ODRL764-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and witness axioms ────────────────────────────────
fof(v_distinct,axiom,conflict != compatible & compatible != unknown & conflict != unknown).
% ─── No conjecture — satisfiability check ───────────────────────────
%--------------------------------------------------------------------------
