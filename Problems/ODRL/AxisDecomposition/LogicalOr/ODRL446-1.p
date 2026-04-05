%--------------------------------------------------------------------------
% File     : ODRL446-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 3-branch or: depth branch overlaps → Compatible
% Version  : 1.0
% English  : PolicyA: width lteq 200 OR height lteq 100 OR depth lteq 200 (odrl:or)
%           : PolicyB: width gteq 400 AND height gteq 200 AND depth gteq 100 (odrl:and)
%           : Branch (A3,B): Z∈(0,200]∩[100,∞)=[100,200] ≠ ∅ → Compatible
%           : Witness: X=400, Y=200, Z=100 (named constants).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL446-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL446-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(distinct, axiom, $distinct(v0, v100, v200, v400)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl446, conjecture,
    ?[X,Y,Z]: ((in_lopen(X, v0, v200) | in_lopen(Y, v0, v100) | in_lopen(Z, v0, v200)) &
           (leq(v400, X) & leq(v200, Y) & leq(v100, Z)))).
%--------------------------------------------------------------------------
