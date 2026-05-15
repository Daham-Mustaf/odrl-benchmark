%--------------------------------------------------------------------------
% File     : ODRL467-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : or-subsumption: and-A ⊆ xone-B → Compatible
% Version  : 1.0
% English  : PolicyA: and(width gteq 800, height lteq 200)
%           : PolicyB: xone(width lteq 600, height lteq 400)
%           : For A: X≥800>600 → X∉(0,600] → ~B_x; Y∈(0,200]⊆(0,400] → B_y
%           : Exactly one B-branch true → xone holds  [~B_x & B_y]
%           : or-subsumption Compatible
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL467-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : subsumption
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL467-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/COMP000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl467, conjecture,
    ![X,Y]: ((leq(v800, X) & in_lopen(Y, v0, v200)) =>
          ((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400))) |
              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400))))).
%--------------------------------------------------------------------------
