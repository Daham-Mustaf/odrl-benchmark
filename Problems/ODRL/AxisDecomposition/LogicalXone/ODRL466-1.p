%--------------------------------------------------------------------------
% File     : ODRL466-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 3-branch xone-A vs and-B: A_x branch alone compatible → Compatible
% Version  : 1.0
% English  : PolicyA: xone3(width lteq 600, height lteq 400, depth lteq 200)
%           : PolicyB: and(width lteq 400, height gteq 500, depth gteq 300)
%           : Branch (A_x&~A_y&~A_z): X∈(0,400], Y≥500>400→Y∉(0,400]✓, Z≥300>200→Z∉(0,200]✓
%           : Witness: X=v300, Y=v500, Z=v300. verdictXone=Compatible
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL466-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL466-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v400_v500, axiom, less(v400, v500)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(distinct, axiom, $distinct(v0, v200, v300, v400, v500, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl466, conjecture,
    ?[X,Y,Z]: (((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400)) & ~(in_lopen(Z, v0, v200))) |
              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400) & ~(in_lopen(Z, v0, v200))) |
              (~(in_lopen(X, v0, v600)) & ~(in_lopen(Y, v0, v400)) & in_lopen(Z, v0, v200))) &
          (in_lopen(X, v0, v400) & leq(v500, Y) & leq(v300, Z)))).
%--------------------------------------------------------------------------
