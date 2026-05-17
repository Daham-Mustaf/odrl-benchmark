%--------------------------------------------------------------------------
% File     : ODRL364-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Mixed operators across 4 axes → box Compatible
% Version  : 1.0
% English  : Width:  eq 600 ∩ lteq 800 = {600} ≠ ∅  Compatible
%           : Height: gt 100 ∩ lt 500  = (100,500) ≠ ∅  Compatible
%           : Depth:  gteq 8 ∩ lteq 32 = [8,32] ≠ ∅    Compatible
%           : Alt:    gteq 150 ∩ lteq 300 = [150,300] ≠ ∅ Compatible
%           : Existential conjecture; prover finds witnesses in chain (e.g., X=v600, Y=v300, Z=v8, W=v300). No density needed.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL364-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL364-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/COMP000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v100, axiom, val(v100)).
fof(val_v150, axiom, val(v150)).
fof(val_v300, axiom, val(v300)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v150, axiom, less(v8, v150)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v500, axiom, less(v8, v500)).
fof(ord_v8_v600, axiom, less(v8, v600)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v100, axiom, less(v32, v100)).
fof(ord_v32_v150, axiom, less(v32, v150)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v500, axiom, less(v32, v500)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v100_v150, axiom, less(v100, v150)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v150_v300, axiom, less(v150, v300)).
fof(ord_v150_v500, axiom, less(v150, v500)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v800, axiom, less(v150, v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v100, v150, v300, v500, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl364, conjecture,
    ?[X,Y,Z,W]: (in_closed(X, v600, v600) & in_lopen(X, v0, v800) &
             less(v100, Y) & in_open(Y, v0, v500) &
             leq(v8,   Z) & in_lopen(Z, v0, v32)  &
             in_lopen(W, v0, v300) & leq(v150, W))).
%--------------------------------------------------------------------------
