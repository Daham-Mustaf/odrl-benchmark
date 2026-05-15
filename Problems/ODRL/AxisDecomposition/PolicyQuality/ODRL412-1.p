%--------------------------------------------------------------------------
% File     : ODRL412-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 4D fractional bounds Conflict (12 constants)
% Version  : 1.0
% English  : Width: lt 599.5 (lb=1) ∩ gteq 600 → X<599.5 AND X≥600 = ∅ Conflict
%           : Domain lower bounds: v1,v2,v3,v4 (not v0).
%           : Fractional threshold: tests sub-integer precision.
%           : 66 ordering axioms — maximum difficulty.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL412-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL412-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v1, axiom, val(v1)).
fof(val_v2, axiom, val(v2)).
fof(val_v3, axiom, val(v3)).
fof(val_v4, axiom, val(v4)).
fof(val_v15_5, axiom, val(v15_5)).
fof(val_v16, axiom, val(v16)).
fof(val_v71_5, axiom, val(v71_5)).
fof(val_v72, axiom, val(v72)).
fof(val_v479_5, axiom, val(v479_5)).
fof(val_v480, axiom, val(v480)).
fof(val_v599_5, axiom, val(v599_5)).
fof(val_v600, axiom, val(v600)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v1_v3, axiom, less(v1, v3)).
fof(ord_v1_v4, axiom, less(v1, v4)).
fof(ord_v1_v15_5, axiom, less(v1, v15_5)).
fof(ord_v1_v16, axiom, less(v1, v16)).
fof(ord_v1_v71_5, axiom, less(v1, v71_5)).
fof(ord_v1_v72, axiom, less(v1, v72)).
fof(ord_v1_v479_5, axiom, less(v1, v479_5)).
fof(ord_v1_v480, axiom, less(v1, v480)).
fof(ord_v1_v599_5, axiom, less(v1, v599_5)).
fof(ord_v1_v600, axiom, less(v1, v600)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v2_v4, axiom, less(v2, v4)).
fof(ord_v2_v15_5, axiom, less(v2, v15_5)).
fof(ord_v2_v16, axiom, less(v2, v16)).
fof(ord_v2_v71_5, axiom, less(v2, v71_5)).
fof(ord_v2_v72, axiom, less(v2, v72)).
fof(ord_v2_v479_5, axiom, less(v2, v479_5)).
fof(ord_v2_v480, axiom, less(v2, v480)).
fof(ord_v2_v599_5, axiom, less(v2, v599_5)).
fof(ord_v2_v600, axiom, less(v2, v600)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v3_v15_5, axiom, less(v3, v15_5)).
fof(ord_v3_v16, axiom, less(v3, v16)).
fof(ord_v3_v71_5, axiom, less(v3, v71_5)).
fof(ord_v3_v72, axiom, less(v3, v72)).
fof(ord_v3_v479_5, axiom, less(v3, v479_5)).
fof(ord_v3_v480, axiom, less(v3, v480)).
fof(ord_v3_v599_5, axiom, less(v3, v599_5)).
fof(ord_v3_v600, axiom, less(v3, v600)).
fof(ord_v4_v15_5, axiom, less(v4, v15_5)).
fof(ord_v4_v16, axiom, less(v4, v16)).
fof(ord_v4_v71_5, axiom, less(v4, v71_5)).
fof(ord_v4_v72, axiom, less(v4, v72)).
fof(ord_v4_v479_5, axiom, less(v4, v479_5)).
fof(ord_v4_v480, axiom, less(v4, v480)).
fof(ord_v4_v599_5, axiom, less(v4, v599_5)).
fof(ord_v4_v600, axiom, less(v4, v600)).
fof(ord_v15_5_v16, axiom, less(v15_5, v16)).
fof(ord_v15_5_v71_5, axiom, less(v15_5, v71_5)).
fof(ord_v15_5_v72, axiom, less(v15_5, v72)).
fof(ord_v15_5_v479_5, axiom, less(v15_5, v479_5)).
fof(ord_v15_5_v480, axiom, less(v15_5, v480)).
fof(ord_v15_5_v599_5, axiom, less(v15_5, v599_5)).
fof(ord_v15_5_v600, axiom, less(v15_5, v600)).
fof(ord_v16_v71_5, axiom, less(v16, v71_5)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v479_5, axiom, less(v16, v479_5)).
fof(ord_v16_v480, axiom, less(v16, v480)).
fof(ord_v16_v599_5, axiom, less(v16, v599_5)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v71_5_v72, axiom, less(v71_5, v72)).
fof(ord_v71_5_v479_5, axiom, less(v71_5, v479_5)).
fof(ord_v71_5_v480, axiom, less(v71_5, v480)).
fof(ord_v71_5_v599_5, axiom, less(v71_5, v599_5)).
fof(ord_v71_5_v600, axiom, less(v71_5, v600)).
fof(ord_v72_v479_5, axiom, less(v72, v479_5)).
fof(ord_v72_v480, axiom, less(v72, v480)).
fof(ord_v72_v599_5, axiom, less(v72, v599_5)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v479_5_v480, axiom, less(v479_5, v480)).
fof(ord_v479_5_v599_5, axiom, less(v479_5, v599_5)).
fof(ord_v479_5_v600, axiom, less(v479_5, v600)).
fof(ord_v480_v599_5, axiom, less(v480, v599_5)).
fof(ord_v480_v600, axiom, less(v480, v600)).
fof(ord_v599_5_v600, axiom, less(v599_5, v600)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v15_5, v16, v71_5, v72, v479_5, v480, v599_5, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl412, conjecture,
    ![X,Y,Z,W]: ~(in_open(X, v1, v599_5) & leq(v600, X) &
             less(v479_5, Y) & in_open(Y, v2, v480) &
             less(v15_5,  Z) & in_open(Z, v3, v16)  &
             in_open(W, v4, v71_5) & leq(v72, W))).
%--------------------------------------------------------------------------
