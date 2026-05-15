%--------------------------------------------------------------------------
% File     : ODRL301-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : width = 600 vs width = 800: distinct points
% Version  : 1.0
% English  : width eq 600 → {600}         [def:interval-denotation, eq]
%           : width eq 800 → {800}         [def:interval-denotation, eq]
%           : {600} ∩ {800} = ∅            by $distinct(v600, v800)
%           : Conflict Criterion (cc): u1=600, l2=800, both closed → 600 < 800.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL301-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL301-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% v0 = domain lower bound (excluded); v600, v800 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct,      axiom, $distinct(v0, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl301, conjecture,
    ![X]:~(in_closed(X, v600, v600) & in_closed(X, v800, v800))).
%--------------------------------------------------------------------------
