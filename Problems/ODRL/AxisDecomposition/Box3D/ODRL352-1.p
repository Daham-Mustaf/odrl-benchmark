%--------------------------------------------------------------------------
% File     : ODRL352-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Associativity: both nestings of box_verdict give Conflict
% Version  : 1.0
% English  : Tests def:box-verdict associativity:
%           : box_verdict(conflict, box_verdict(compatible, compatible)) = conflict
%           : AND
%           : box_verdict(box_verdict(conflict, compatible), compatible) = conflict
%           : Both nestings produce the same result (conflict dominates).
%           : Forces Section D axioms directly — no interval arithmetic.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL352-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL352-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl352, conjecture,
    box_verdict(conflict, box_verdict(compatible, compatible)) = conflict &
box_verdict(box_verdict(conflict, compatible), compatible) = conflict).
%--------------------------------------------------------------------------
