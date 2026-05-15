%--------------------------------------------------------------------------
% File     : ODRL420-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : cc: lteq ∩ gteq — shared boundary point Compatible
% Version  : 1.0
% English  : thm:criterion cc: (0,600]∩[600,∞)={600}≠∅ Compatible
%           : Witness: X=v600 (named constant). Tightest possible overlap.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL420-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL420-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl420, conjecture,
    ?[X]: (in_lopen(X, v0, v600) & leq(v600, X))).
%--------------------------------------------------------------------------
