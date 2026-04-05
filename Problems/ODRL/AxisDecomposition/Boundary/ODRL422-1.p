%--------------------------------------------------------------------------
% File     : ODRL422-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : oc: lt ∩ gteq — boundary excluded on left → Conflict
% Version  : 1.0
% English  : thm:criterion oc: (0,600)∩[600,∞)=∅ Conflict
%           : Proof: X<600 AND X≥600 is order contradiction.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL422-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL422-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl422, conjecture,
    ~?[X]: (in_open(X, v0, v600) & leq(v600, X))).
%--------------------------------------------------------------------------
