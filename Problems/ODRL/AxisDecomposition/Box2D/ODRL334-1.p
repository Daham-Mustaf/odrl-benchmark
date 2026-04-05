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
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL334-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL334-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl334, conjecture,
    box_verdict(conflict, compatible) = conflict).
%--------------------------------------------------------------------------
