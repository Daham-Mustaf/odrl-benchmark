%--------------------------------------------------------------------------
% File     : ODRL416-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 4D all-touch single point Compatible (5 constants)
% Version  : 1.0
% English  : Width:  lteq 600 ∩ gteq 600 = {600} ≠ ∅ Compatible
%           : Height: lteq 480 ∩ gteq 480 = {480} ≠ ∅ Compatible
%           : Depth:  lteq 16  ∩ gteq 16  = {16}  ≠ ∅ Compatible
%           : Alt:    lteq 72  ∩ gteq 72  = {72}  ≠ ∅ Compatible
%           : Box intersection is a single point in R⁴.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL416-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL416-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v72, axiom, val(v72)).
fof(val_v480, axiom, val(v480)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v72, axiom, less(v0, v72)).
fof(ord_v0_v480, axiom, less(v0, v480)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v480, axiom, less(v16, v480)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v72_v480, axiom, less(v72, v480)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v480_v600, axiom, less(v480, v600)).
fof(distinct, axiom, $distinct(v0, v16, v72, v480, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl416, conjecture,
    ?[X,Y,Z,W]: (in_lopen(X, v0, v600) & leq(v600, X) &
           in_lopen(Y, v0, v480) & leq(v480, Y) &
           in_lopen(Z, v0, v16)  & leq(v16,  Z) &
           in_lopen(W, v0, v72)  & leq(v72,  W))).
%--------------------------------------------------------------------------
