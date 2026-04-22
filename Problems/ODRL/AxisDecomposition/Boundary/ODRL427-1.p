%--------------------------------------------------------------------------
% File     : ODRL427-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : eq ∩ gt — eq value at boundary excluded by gt → Conflict
% Version  : 1.0
% English  : thm:criterion eq∩gt: {600}∩(600,∞)=∅ Conflict
%           : Proof: X=600 AND X>600 is order contradiction.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL427-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL427-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl427, conjecture,
    ![X]: ~(in_closed(X, v600, v600) & less(v600, X))).
%--------------------------------------------------------------------------
