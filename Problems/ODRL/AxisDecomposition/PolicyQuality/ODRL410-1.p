%--------------------------------------------------------------------------
% File     : ODRL410-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 4D subsumption Compatible — scaling (8 constants)
% Version  : 1.0
% English  : Width:  (0,600]  ⊆ (0,1920]  Compatible
%           : Height: (0,400]  ⊆ (0,1080]  Compatible
%           : Depth:  (0,16]   ⊆ (0,48]    Compatible
%           : Alt:    (0,150]  ⊆ (0,600]   Compatible
%           : 28 ordering axioms, HD video scaling scenario.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL410-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : subsumption
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL410-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v48, axiom, val(v48)).
fof(val_v150, axiom, val(v150)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v48, axiom, less(v0, v48)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v1080, axiom, less(v0, v1080)).
fof(ord_v0_v1920, axiom, less(v0, v1920)).
fof(ord_v16_v48, axiom, less(v16, v48)).
fof(ord_v16_v150, axiom, less(v16, v150)).
fof(ord_v16_v400, axiom, less(v16, v400)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v1080, axiom, less(v16, v1080)).
fof(ord_v16_v1920, axiom, less(v16, v1920)).
fof(ord_v48_v150, axiom, less(v48, v150)).
fof(ord_v48_v400, axiom, less(v48, v400)).
fof(ord_v48_v600, axiom, less(v48, v600)).
fof(ord_v48_v1080, axiom, less(v48, v1080)).
fof(ord_v48_v1920, axiom, less(v48, v1920)).
fof(ord_v150_v400, axiom, less(v150, v400)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v1080, axiom, less(v150, v1080)).
fof(ord_v150_v1920, axiom, less(v150, v1920)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v1080, axiom, less(v400, v1080)).
fof(ord_v400_v1920, axiom, less(v400, v1920)).
fof(ord_v600_v1080, axiom, less(v600, v1080)).
fof(ord_v600_v1920, axiom, less(v600, v1920)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(distinct, axiom, $distinct(v0, v16, v48, v150, v400, v600, v1080, v1920)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl410, conjecture,
    ![X,Y,Z,W]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400) & in_lopen(Z, v0, v16) & in_lopen(W, v0, v150)) =>
              (in_lopen(X, v0, v1920) & in_lopen(Y, v0, v1080) & in_lopen(Z, v0, v48) & in_lopen(W, v0, v600)))).
%--------------------------------------------------------------------------
