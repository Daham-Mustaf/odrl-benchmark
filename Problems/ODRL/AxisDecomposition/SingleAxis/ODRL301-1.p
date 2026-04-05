%--------------------------------------------------------------------------
% File     : ODRL301-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : width = 600 vs width = 800: distinct points
% Version  : 1.0
% English  : width eq 600 → {600}
%           : width eq 800 → {800}
%           : {600} ∩ {800} = ∅ → Conflict
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL301-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL301-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct,      axiom, $distinct(v0, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl301, conjecture,
    ~?[X]: (in_closed(X, v600, v600) & in_closed(X, v800, v800))).
%--------------------------------------------------------------------------
