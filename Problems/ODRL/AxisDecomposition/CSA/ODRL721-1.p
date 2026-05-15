%--------------------------------------------------------------------------
% File     : ODRL721-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA ConflictCriterion: claim prec(v5,v5,c,c) holds (wrong)
% Version  : 1.0
% English  : prec(v5,v5,c,c) requires less(v5,v5) — impossible by irreflexivity.
%           : Wrong claim.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL721-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL721-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v5,axiom,val(v5)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl721, conjecture,
    prec(v5, v5, c, c)).
%--------------------------------------------------------------------------
