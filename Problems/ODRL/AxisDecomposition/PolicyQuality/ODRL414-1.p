%--------------------------------------------------------------------------
% File     : ODRL414-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 4D fractional subsumption Conflict — alt escape (11 constants)
% Version  : 1.0
% English  : Width: {600} ∈ A_w; A_w ⊆ B_w=(1,1920] Compatible
%           : Height: A_h=(300,∞) ⊄ B_h=(2,1080) via Y≥1080
%           : Depth: A_d=[16,∞) ⊄ B_d=(3,48] via Z>48
%           : Alt: A_w=(4,300) ⊄ B_W=[72,∞) via W<72 (escape)
%           : Witness: X=600, Y=1080, Z=72, W=16.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL414-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL414-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v1, axiom, val(v1)).
fof(val_v2, axiom, val(v2)).
fof(val_v3, axiom, val(v3)).
fof(val_v4, axiom, val(v4)).
fof(val_v16, axiom, val(v16)).
fof(val_v48, axiom, val(v48)).
fof(val_v72, axiom, val(v72)).
fof(val_v300, axiom, val(v300)).
fof(val_v600, axiom, val(v600)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v1_v3, axiom, less(v1, v3)).
fof(ord_v1_v4, axiom, less(v1, v4)).
fof(ord_v1_v16, axiom, less(v1, v16)).
fof(ord_v1_v48, axiom, less(v1, v48)).
fof(ord_v1_v72, axiom, less(v1, v72)).
fof(ord_v1_v300, axiom, less(v1, v300)).
fof(ord_v1_v600, axiom, less(v1, v600)).
fof(ord_v1_v1080, axiom, less(v1, v1080)).
fof(ord_v1_v1920, axiom, less(v1, v1920)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v2_v4, axiom, less(v2, v4)).
fof(ord_v2_v16, axiom, less(v2, v16)).
fof(ord_v2_v48, axiom, less(v2, v48)).
fof(ord_v2_v72, axiom, less(v2, v72)).
fof(ord_v2_v300, axiom, less(v2, v300)).
fof(ord_v2_v600, axiom, less(v2, v600)).
fof(ord_v2_v1080, axiom, less(v2, v1080)).
fof(ord_v2_v1920, axiom, less(v2, v1920)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v3_v16, axiom, less(v3, v16)).
fof(ord_v3_v48, axiom, less(v3, v48)).
fof(ord_v3_v72, axiom, less(v3, v72)).
fof(ord_v3_v300, axiom, less(v3, v300)).
fof(ord_v3_v600, axiom, less(v3, v600)).
fof(ord_v3_v1080, axiom, less(v3, v1080)).
fof(ord_v3_v1920, axiom, less(v3, v1920)).
fof(ord_v4_v16, axiom, less(v4, v16)).
fof(ord_v4_v48, axiom, less(v4, v48)).
fof(ord_v4_v72, axiom, less(v4, v72)).
fof(ord_v4_v300, axiom, less(v4, v300)).
fof(ord_v4_v600, axiom, less(v4, v600)).
fof(ord_v4_v1080, axiom, less(v4, v1080)).
fof(ord_v4_v1920, axiom, less(v4, v1920)).
fof(ord_v16_v48, axiom, less(v16, v48)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v300, axiom, less(v16, v300)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v1080, axiom, less(v16, v1080)).
fof(ord_v16_v1920, axiom, less(v16, v1920)).
fof(ord_v48_v72, axiom, less(v48, v72)).
fof(ord_v48_v300, axiom, less(v48, v300)).
fof(ord_v48_v600, axiom, less(v48, v600)).
fof(ord_v48_v1080, axiom, less(v48, v1080)).
fof(ord_v48_v1920, axiom, less(v48, v1920)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v72_v1080, axiom, less(v72, v1080)).
fof(ord_v72_v1920, axiom, less(v72, v1920)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v1080, axiom, less(v300, v1080)).
fof(ord_v300_v1920, axiom, less(v300, v1920)).
fof(ord_v600_v1080, axiom, less(v600, v1080)).
fof(ord_v600_v1920, axiom, less(v600, v1920)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v16, v48, v72, v300, v600, v1080, v1920)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl414, conjecture,
    in_closed(v600, v600, v600) &
    less(v300, v1080) &
    leq(v16, v16) &
    in_open(v16, v4, v300) &
    ~in_open(v1080, v2, v1080)).
%--------------------------------------------------------------------------
