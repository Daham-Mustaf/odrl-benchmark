%--------------------------------------------------------------------------
% File     : ODRL442-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : PolicyA and-constraints: any PolicyB or-branch overlaps → Compatible
% Version  : 1.0
% English  : PolicyA: width lteq 800 AND height lteq 600 (odrl:and)
%           : PolicyB: width gteq 1000 OR height gteq 200 (odrl:or)
%           : (A,B2): Y∈(0,600]∩[200,∞)=[200,600] ≠ ∅ → Compatible
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL442-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL442-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(val_v1000, axiom, val(v1000)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v0_v1000, axiom, less(v0, v1000)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v200_v1000, axiom, less(v200, v1000)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(ord_v600_v1000, axiom, less(v600, v1000)).
fof(ord_v800_v1000, axiom, less(v800, v1000)).
fof(distinct, axiom, $distinct(v0, v200, v600, v800, v1000)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl442, conjecture,
    ?[X,Y]: ((in_lopen(X, v0, v800) & in_lopen(Y, v0, v600)) &
           (leq(v1000, X) | leq(v200, Y)))).
%--------------------------------------------------------------------------
