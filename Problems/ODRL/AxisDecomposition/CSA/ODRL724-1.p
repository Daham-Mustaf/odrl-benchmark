%--------------------------------------------------------------------------
% File     : ODRL724-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA ConflictCriterion: claim upper_tag(eq,o) (wrong - eq has closed upper)
% Version  : 1.0
% English  : upper_tag(eq,c) holds - eq has closed upper boundary.
%           : Wrong claim: upper_tag(eq,o).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL724-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% Relation : verdict_algebra
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL724-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl724, conjecture,
    upper_tag(eq, o)).
%--------------------------------------------------------------------------
