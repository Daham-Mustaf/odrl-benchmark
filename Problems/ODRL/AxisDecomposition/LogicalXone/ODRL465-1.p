%--------------------------------------------------------------------------
% File     : ODRL465-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 3-branch xone-A vs and-B: B implies 2+ branches → Conflict
% Version  : 1.0
% English  : PolicyA: xone3(width lteq 600, height lteq 400, depth lteq 200)
%           : PolicyB: and(width lteq 400, height lteq 200, depth lteq 100)
%           : For B: X∈(0,400]⊆(0,600]→A_x true; Y∈(0,200]⊆(0,400]→A_y true
%           : Two branches simultaneously true → xone3 fails → Conflict
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL465-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL465-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/COMP000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v100, v200, v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl465, conjecture,
    ![X,Y,Z]: ~(((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400)) & ~(in_lopen(Z, v0, v200))) |
             (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400) & ~(in_lopen(Z, v0, v200))) |
             (~(in_lopen(X, v0, v600)) & ~(in_lopen(Y, v0, v400)) & in_lopen(Z, v0, v200))) &
          (in_lopen(X, v0, v400) & in_lopen(Y, v0, v200) & in_lopen(Z, v0, v100)))).
%--------------------------------------------------------------------------
