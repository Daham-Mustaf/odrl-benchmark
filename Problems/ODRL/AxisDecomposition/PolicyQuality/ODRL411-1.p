%--------------------------------------------------------------------------
% File     : ODRL411-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 3D eq conflict via distinctness (7 constants)
% Version  : 1.0
% English  : Width: eq 600 ∩ eq 601 = {600}∩{601} = ∅ Conflict (distinct)
%           : Height: gt 300 ∩ lt 500 = (300,500) Compatible
%           : Depth: gteq 16 ∩ lteq 32 = [16,32] Compatible
%           : Conflict proved by X distinctness — no density needed.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL411-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL411-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v32, axiom, val(v32)).
fof(val_v300, axiom, val(v300)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(val_v601, axiom, val(v601)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v601, axiom, less(v0, v601)).
fof(ord_v16_v32, axiom, less(v16, v32)).
fof(ord_v16_v300, axiom, less(v16, v300)).
fof(ord_v16_v500, axiom, less(v16, v500)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v601, axiom, less(v16, v601)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v500, axiom, less(v32, v500)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v601, axiom, less(v32, v601)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v601, axiom, less(v300, v601)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v601, axiom, less(v500, v601)).
fof(ord_v600_v601, axiom, less(v600, v601)).
fof(distinct, axiom, $distinct(v0, v16, v32, v300, v500, v600, v601)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl411, conjecture,
    ![X,Y,Z]: ~(in_closed(X, v600, v600) & in_closed(X, v601, v601) &
            less(v300, Y) & in_open(Y, v0, v500) &
            leq(v16, Z) & in_lopen(Z, v0, v32))).
%--------------------------------------------------------------------------
