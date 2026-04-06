%--------------------------------------------------------------------------
% File     : ODRL468-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : xone-subsumption Conflict: A_and ⊄ B_xone — both branches simultaneously true
% Version  : 1.0
% English  : PolicyA: and(width lteq 400, height lteq 200)
%           : PolicyB: xone(width lteq 600, height lteq 400)
%           : For A: X∈(0,400]⊆(0,600]→B_x true AND Y∈(0,200]⊆(0,400]→B_y true
%           : Both B-branches true → xone fails → ~xone → escape witness exists
%           : Conflict: A ⊄ B_xone
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL468-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL468-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl468, conjecture,
    ?[X,Y]: ((in_lopen(X, v0, v400) & in_lopen(Y, v0, v200)) &
          ~((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400))) |
              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400))))).
%--------------------------------------------------------------------------
