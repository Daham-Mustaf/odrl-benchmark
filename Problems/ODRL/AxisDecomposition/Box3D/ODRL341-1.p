%--------------------------------------------------------------------------
% File     : ODRL341-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Width conflict × height+depth compatible → box Conflict
% Version  : 1.0
% English  : Width:  lteq 600  → (0,600]  ∩  gteq 1200 → [1200,∞) = ∅  Conflict
%           : Height: lteq 800  → (0,800]  ∩  gteq 200  → [200,∞)  ≠ ∅  Compatible
%           : Depth:  lteq 32   → (0,32]   ∩  gteq 8    → [8,∞)    ≠ ∅  Compatible
%           : box_verdict(Conflict, box_verdict(Compatible, Compatible)) = Conflict
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL341-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL341-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,         axiom, val(v0)).
fof(val_v8,         axiom, val(v8)).
fof(val_v32,        axiom, val(v32)).
fof(val_v200,       axiom, val(v200)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v8,      axiom, less(v0,   v8)).
fof(ord_v0_v32,     axiom, less(v0,   v32)).
fof(ord_v0_v200,    axiom, less(v0,   v200)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v800,    axiom, less(v0,   v800)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v8_v32,     axiom, less(v8,   v32)).
fof(ord_v8_v200,    axiom, less(v8,   v200)).
fof(ord_v8_v600,    axiom, less(v8,   v600)).
fof(ord_v8_v800,    axiom, less(v8,   v800)).
fof(ord_v8_v1200,   axiom, less(v8,   v1200)).
fof(ord_v32_v200,   axiom, less(v32,  v200)).
fof(ord_v32_v600,   axiom, less(v32,  v600)).
fof(ord_v32_v800,   axiom, less(v32,  v800)).
fof(ord_v32_v1200,  axiom, less(v32,  v1200)).
fof(ord_v200_v600,  axiom, less(v200, v600)).
fof(ord_v200_v800,  axiom, less(v200, v800)).
fof(ord_v200_v1200, axiom, less(v200, v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v8, v32, v200, v600, v800, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl341, conjecture,
    ![X,Y,Z]: ~(in_lopen(X, v0, v600)  & leq(v1200, X) &
            in_lopen(Y, v0, v800)  & leq(v200,  Y) &
            in_lopen(Z, v0, v32)   & leq(v8,    Z))).
%--------------------------------------------------------------------------
