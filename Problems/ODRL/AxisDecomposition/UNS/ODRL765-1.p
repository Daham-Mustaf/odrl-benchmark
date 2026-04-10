%--------------------------------------------------------------------------
% File     : ODRL765-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : intra-policy Box2D: width lteq 600 AND gteq 800 empty
% Version  : 1.0
% English  : Remark 3.4: width (0,600] ∩ [800,∞) = ∅.
%           : Single policy asserts width ≤ 600 AND ≥ 800 simultaneously.
%           : Contradiction via fresh witness w: in_lopen(w,v0,v600) forces
%           : leq(w,v600), and leq(v800,w) with less(v600,v800) gives less(w,v800)
%           : and less(v800,w) — irreflexivity closes the proof.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL765-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : UNS — Remark 3.4 intra-policy self-contradiction.
%           : Empty denotation: no request satisfies the constraint.
%           : Policy source: Policies/ODRL765-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
fof(wit_val,      axiom, val(w)).
fof(wit_in_lopen, axiom, in_lopen(w, v0, v600)).
fof(wit_leq,      axiom, leq(v800, w)).
% ─── No conjecture — contradiction in axioms ─────────────────────────
%--------------------------------------------------------------------------
