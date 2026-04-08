%--------------------------------------------------------------------------
% File     : ODRL367-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : HD video width conflict → box Conflict
% Version  : 1.0
% English  : Width:  lteq 640  ∩ gteq 1920 = ∅  Conflict
%           : Height/Depth/Alt: same as ODRL366, all compatible
%           : box_verdict(Conflict,box_verdict(C,box_verdict(C,C)))=Conflict
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL367-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL367-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v48, axiom, val(v48)).
fof(val_v150, axiom, val(v150)).
fof(val_v480, axiom, val(v480)).
fof(val_v600, axiom, val(v600)).
fof(val_v640, axiom, val(v640)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v48, axiom, less(v0, v48)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v480, axiom, less(v0, v480)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v640, axiom, less(v0, v640)).
fof(ord_v0_v1080, axiom, less(v0, v1080)).
fof(ord_v0_v1920, axiom, less(v0, v1920)).
fof(ord_v16_v48, axiom, less(v16, v48)).
fof(ord_v16_v150, axiom, less(v16, v150)).
fof(ord_v16_v480, axiom, less(v16, v480)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v640, axiom, less(v16, v640)).
fof(ord_v16_v1080, axiom, less(v16, v1080)).
fof(ord_v16_v1920, axiom, less(v16, v1920)).
fof(ord_v48_v150, axiom, less(v48, v150)).
fof(ord_v48_v480, axiom, less(v48, v480)).
fof(ord_v48_v600, axiom, less(v48, v600)).
fof(ord_v48_v640, axiom, less(v48, v640)).
fof(ord_v48_v1080, axiom, less(v48, v1080)).
fof(ord_v48_v1920, axiom, less(v48, v1920)).
fof(ord_v150_v480, axiom, less(v150, v480)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v640, axiom, less(v150, v640)).
fof(ord_v150_v1080, axiom, less(v150, v1080)).
fof(ord_v150_v1920, axiom, less(v150, v1920)).
fof(ord_v480_v600, axiom, less(v480, v600)).
fof(ord_v480_v640, axiom, less(v480, v640)).
fof(ord_v480_v1080, axiom, less(v480, v1080)).
fof(ord_v480_v1920, axiom, less(v480, v1920)).
fof(ord_v600_v640, axiom, less(v600, v640)).
fof(ord_v600_v1080, axiom, less(v600, v1080)).
fof(ord_v600_v1920, axiom, less(v600, v1920)).
fof(ord_v640_v1080, axiom, less(v640, v1080)).
fof(ord_v640_v1920, axiom, less(v640, v1920)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(distinct, axiom, $distinct(v0, v16, v48, v150, v480, v600, v640, v1080, v1920)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl367, conjecture,
    ~?[X,Y,Z,W]: (in_lopen(X, v0, v640)  & leq(v1920, X) &            in_lopen(Y, v0, v1080) & leq(v480,  Y) &
            in_lopen(Z, v0, v48)   & leq(v16,   Z) &
            in_lopen(W, v0, v600)  & leq(v150,  W))).
%--------------------------------------------------------------------------
