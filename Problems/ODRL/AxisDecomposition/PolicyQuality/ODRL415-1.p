%--------------------------------------------------------------------------
% File     : ODRL415-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 4D fractional subsumption Compatible — maximum difficulty (12 constants, 66 orderings)
% Version  : 1.0
% English  : Width:  (1,599.5] ⊆ (1,600.5] Compatible (599.5<600.5)
%           : Height: (2,479.5] ⊆ (2,480.5] Compatible (479.5<480.5)
%           : Depth:  (3,15.5]  ⊆ (3,16.5]  Compatible (15.5<16.5)
%           : Alt:    (4,71.5]  ⊆ (4,72.5]  Compatible (71.5<72.5)
%           : Maximum difficulty: 12 constants, C(12,2)=66 ordering axioms.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL415-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : subsumption
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL415-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v1, axiom, val(v1)).
fof(val_v2, axiom, val(v2)).
fof(val_v3, axiom, val(v3)).
fof(val_v4, axiom, val(v4)).
fof(val_v15_5, axiom, val(v15_5)).
fof(val_v16_5, axiom, val(v16_5)).
fof(val_v71_5, axiom, val(v71_5)).
fof(val_v72_5, axiom, val(v72_5)).
fof(val_v479_5, axiom, val(v479_5)).
fof(val_v480_5, axiom, val(v480_5)).
fof(val_v599_5, axiom, val(v599_5)).
fof(val_v600_5, axiom, val(v600_5)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v1_v3, axiom, less(v1, v3)).
fof(ord_v1_v4, axiom, less(v1, v4)).
fof(ord_v1_v15_5, axiom, less(v1, v15_5)).
fof(ord_v1_v16_5, axiom, less(v1, v16_5)).
fof(ord_v1_v71_5, axiom, less(v1, v71_5)).
fof(ord_v1_v72_5, axiom, less(v1, v72_5)).
fof(ord_v1_v479_5, axiom, less(v1, v479_5)).
fof(ord_v1_v480_5, axiom, less(v1, v480_5)).
fof(ord_v1_v599_5, axiom, less(v1, v599_5)).
fof(ord_v1_v600_5, axiom, less(v1, v600_5)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v2_v4, axiom, less(v2, v4)).
fof(ord_v2_v15_5, axiom, less(v2, v15_5)).
fof(ord_v2_v16_5, axiom, less(v2, v16_5)).
fof(ord_v2_v71_5, axiom, less(v2, v71_5)).
fof(ord_v2_v72_5, axiom, less(v2, v72_5)).
fof(ord_v2_v479_5, axiom, less(v2, v479_5)).
fof(ord_v2_v480_5, axiom, less(v2, v480_5)).
fof(ord_v2_v599_5, axiom, less(v2, v599_5)).
fof(ord_v2_v600_5, axiom, less(v2, v600_5)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v3_v15_5, axiom, less(v3, v15_5)).
fof(ord_v3_v16_5, axiom, less(v3, v16_5)).
fof(ord_v3_v71_5, axiom, less(v3, v71_5)).
fof(ord_v3_v72_5, axiom, less(v3, v72_5)).
fof(ord_v3_v479_5, axiom, less(v3, v479_5)).
fof(ord_v3_v480_5, axiom, less(v3, v480_5)).
fof(ord_v3_v599_5, axiom, less(v3, v599_5)).
fof(ord_v3_v600_5, axiom, less(v3, v600_5)).
fof(ord_v4_v15_5, axiom, less(v4, v15_5)).
fof(ord_v4_v16_5, axiom, less(v4, v16_5)).
fof(ord_v4_v71_5, axiom, less(v4, v71_5)).
fof(ord_v4_v72_5, axiom, less(v4, v72_5)).
fof(ord_v4_v479_5, axiom, less(v4, v479_5)).
fof(ord_v4_v480_5, axiom, less(v4, v480_5)).
fof(ord_v4_v599_5, axiom, less(v4, v599_5)).
fof(ord_v4_v600_5, axiom, less(v4, v600_5)).
fof(ord_v15_5_v16_5, axiom, less(v15_5, v16_5)).
fof(ord_v15_5_v71_5, axiom, less(v15_5, v71_5)).
fof(ord_v15_5_v72_5, axiom, less(v15_5, v72_5)).
fof(ord_v15_5_v479_5, axiom, less(v15_5, v479_5)).
fof(ord_v15_5_v480_5, axiom, less(v15_5, v480_5)).
fof(ord_v15_5_v599_5, axiom, less(v15_5, v599_5)).
fof(ord_v15_5_v600_5, axiom, less(v15_5, v600_5)).
fof(ord_v16_5_v71_5, axiom, less(v16_5, v71_5)).
fof(ord_v16_5_v72_5, axiom, less(v16_5, v72_5)).
fof(ord_v16_5_v479_5, axiom, less(v16_5, v479_5)).
fof(ord_v16_5_v480_5, axiom, less(v16_5, v480_5)).
fof(ord_v16_5_v599_5, axiom, less(v16_5, v599_5)).
fof(ord_v16_5_v600_5, axiom, less(v16_5, v600_5)).
fof(ord_v71_5_v72_5, axiom, less(v71_5, v72_5)).
fof(ord_v71_5_v479_5, axiom, less(v71_5, v479_5)).
fof(ord_v71_5_v480_5, axiom, less(v71_5, v480_5)).
fof(ord_v71_5_v599_5, axiom, less(v71_5, v599_5)).
fof(ord_v71_5_v600_5, axiom, less(v71_5, v600_5)).
fof(ord_v72_5_v479_5, axiom, less(v72_5, v479_5)).
fof(ord_v72_5_v480_5, axiom, less(v72_5, v480_5)).
fof(ord_v72_5_v599_5, axiom, less(v72_5, v599_5)).
fof(ord_v72_5_v600_5, axiom, less(v72_5, v600_5)).
fof(ord_v479_5_v480_5, axiom, less(v479_5, v480_5)).
fof(ord_v479_5_v599_5, axiom, less(v479_5, v599_5)).
fof(ord_v479_5_v600_5, axiom, less(v479_5, v600_5)).
fof(ord_v480_5_v599_5, axiom, less(v480_5, v599_5)).
fof(ord_v480_5_v600_5, axiom, less(v480_5, v600_5)).
fof(ord_v599_5_v600_5, axiom, less(v599_5, v600_5)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v15_5, v16_5, v71_5, v72_5, v479_5, v480_5, v599_5, v600_5)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl415, conjecture,
    ![X,Y,Z,W]: ((in_lopen(X, v1, v599_5) & in_lopen(Y, v2, v479_5) & in_lopen(Z, v3, v15_5) & in_lopen(W, v4, v71_5)) =>
              (in_lopen(X, v1, v600_5) & in_lopen(Y, v2, v480_5) & in_lopen(Z, v3, v16_5) & in_lopen(W, v4, v72_5)))).
%--------------------------------------------------------------------------
