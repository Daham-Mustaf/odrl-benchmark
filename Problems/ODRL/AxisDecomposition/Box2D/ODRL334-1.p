%--------------------------------------------------------------------------
% File     : ODRL334-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : box_verdict(conflict, compatible) = conflict: Kleene Rule 1 direct
% Version  : 1.0
% English  : box_verdict(conflict, compatible) = conflict  [def:box-verdict Rule 1]
%           : Forces Vampire to fire Section D axiom box_conflict directly.
%           : No ordering constants needed — pure verdict algebra test.
%           : SMT2: Kleene min encoding — min(0,2)=0 → negation unsat.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL334-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL334-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl334, conjecture,
    box_verdict(conflict, compatible) = conflict).
%--------------------------------------------------------------------------
