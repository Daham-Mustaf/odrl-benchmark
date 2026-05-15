%--------------------------------------------------------------------------
% File     : ODRL421-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : co: lteq ∩ gt — boundary excluded on right → Conflict
% Version  : 1.0
% English  : thm:criterion co: (0,600]∩(600,∞)=∅ Conflict
%           : Proof: X≤600 AND X>600 is order contradiction.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL421-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL421-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl421, conjecture,
    ![X]: ~(in_lopen(X, v0, v600) & less(v600, X))).
%--------------------------------------------------------------------------
