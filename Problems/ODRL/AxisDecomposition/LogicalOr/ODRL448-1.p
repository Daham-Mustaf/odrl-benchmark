%--------------------------------------------------------------------------
% File     : ODRL448-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : or-subsumption: B_or ⊄ A_and escape witness → Conflict
% Version  : 1.0
% English  : PolicyA: width lteq 800 OR height lteq 600 (odrl:or) [wider]
%           : PolicyB: width lteq 600 AND height lteq 400 (odrl:and) [narrower]
%           : Escape: X=700 ∈ (0,800] but X∉(0,600] → A ⊄ B Conflict
%           : or-subsumption Conflict [def:box-containment escape]
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL448-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : subsumption
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL448-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/COMP000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v400, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl448, conjecture,
    ?[X,Y]: ((in_lopen(X, v0, v800) | in_lopen(Y, v0, v600)) &
           ~(in_lopen(X, v0, v600) & in_lopen(Y, v0, v400)))).
%--------------------------------------------------------------------------
