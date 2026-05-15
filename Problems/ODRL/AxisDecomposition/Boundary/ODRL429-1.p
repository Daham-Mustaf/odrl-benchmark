%--------------------------------------------------------------------------
% File     : ODRL429-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : gt ∩ gteq — open superset of closed → Compatible (sentinel)
% Version  : 1.0
% English  : thm:criterion gt∩gteq: (600,∞)∩[600,∞)=(600,∞)≠∅ Compatible
%           : Witness must be above v600 — adds sentinel v1200 with less(v600,v1200).
%           : X=v1200 satisfies less(v600,X) AND leq(v600,X).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL429-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL429-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl429, conjecture,
    ?[X]: (less(v600, X) & leq(v600, X))).
%--------------------------------------------------------------------------
