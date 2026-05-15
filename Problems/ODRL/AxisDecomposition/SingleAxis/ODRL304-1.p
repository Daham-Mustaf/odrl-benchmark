%--------------------------------------------------------------------------
% File     : ODRL304-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : width ≤ 600 vs width ≥ 200: overlapping intervals
% Version  : 1.0
% English  : width lteq 600 → (0, 600]   [def:interval-denotation, lteq]
%           : width gteq 200 → [200, ∞)   [def:interval-denotation, gteq]
%           : (0, 600] ∩ [200, ∞) = [200, 600] ≠ ∅
%           : Witness: X = v200 (named constant, no density needed).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL304-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL304-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% v0 = domain lower bound (excluded); v200, v600 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0, v200)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl304, conjecture,
    ?[X]: (in_lopen(X, v0, v600) & leq(v200, X))).
%--------------------------------------------------------------------------
