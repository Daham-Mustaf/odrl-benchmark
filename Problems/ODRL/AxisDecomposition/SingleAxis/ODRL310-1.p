%--------------------------------------------------------------------------
% File     : ODRL310-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : (0,1200] ⊄ (0,600]: wider does not subsume tighter
% Version  : 1.0
% English  : width lteq 1200 → (0, 1200]  [def:interval-denotation, lteq]
%           : width lteq 600  → (0, 600]   [def:interval-denotation, lteq]
%           : (0, 1200] ⊄ (0, 600]         [def:box-containment, Conflict]
%           : Counterexample: X = v800 ∈ (0,1200] but v800 ∉ (0,600]
%           : since less(v600, v800) and less(v800, v1200).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL310-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : subsumption
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL310-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% v0 = domain lower bound (excluded); v600, v800, v1200 = constraint/witness values
% v800 witnesses X ∈ A \ B
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v0_v1200,   axiom, less(v0, v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v800, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl310, conjecture,
    ?[X]: (in_lopen(X, v0, v1200) & ~in_lopen(X, v0, v600))).
%--------------------------------------------------------------------------
