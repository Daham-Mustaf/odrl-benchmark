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
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL465-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL465-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

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
    ~?[X,Y,Z]: (((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400)) & ~(in_lopen(Z, v0, v200))) |
              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400) & ~(in_lopen(Z, v0, v200))) |
              (~(in_lopen(X, v0, v600)) & ~(in_lopen(Y, v0, v400)) & in_lopen(Z, v0, v200))) &
          (in_lopen(X, v0, v400) & in_lopen(Y, v0, v200) & in_lopen(Z, v0, v100)))).
%--------------------------------------------------------------------------
