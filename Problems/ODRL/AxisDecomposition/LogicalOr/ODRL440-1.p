%--------------------------------------------------------------------------
% File     : ODRL440-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : PolicyA or-branches: any branch overlaps PolicyB → Compatible
% Version  : 1.0
% English  : PolicyA: width lteq 400 OR height lteq 800 (odrl:or)
%           : PolicyB: width gteq 600 AND height gteq 200 (odrl:and)
%           : Branch pair (A2,B): Y∈(0,800]∩[200,∞)=[200,800] ≠ ∅ → Compatible
%           : verdictOr=Compatible [thm:composition-soundness]
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL440-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL440-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

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
fof(odrl440, conjecture,
    ?[X,Y]: ((in_lopen(X, v0, v400) | in_lopen(Y, v0, v800)) &
           (leq(v600, X) & leq(v200, Y)))).
%--------------------------------------------------------------------------
