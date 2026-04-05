%--------------------------------------------------------------------------
% File     : ODRL311-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : [800,∞) ⊆ [400,∞): higher lower-bound subsumes
% Version  : 1.0
% English  : width gteq 800 → [800, ∞)
%           : width gteq 400 → [400, ∞)
%           : [800, ∞) ⊆ [400, ∞) → Compatible (subsumption)
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL311-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL311-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct,      axiom, $distinct(v0, v400, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl311, conjecture,
    ![X]: (leq(v800, X) => leq(v400, X))).
%--------------------------------------------------------------------------
