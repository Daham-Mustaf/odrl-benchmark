%--------------------------------------------------------------------------
% File     : ODRL761-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : intra-policy: lteq 600 AND gteq 800 gives empty denotation
% Version  : 1.0
% English  : Remark 3.4 intra-policy self-contradiction.
%           : width lteq 600: (0,600]; width gteq 800: [800,∞).
%           : (0,600] ∩ [800,∞) = ∅ — no request satisfies both.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL761-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : UNS — Remark 3.4 intra-policy self-contradiction.
%           : Empty denotation: no request satisfies the constraint.
%           : Policy source: Policies/ODRL761-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
% ─── Contradiction axioms ──────────────────────────────────────────────
fof(constraint, axiom, in_lopen(v0,v0,v600) & leq(v800,v0)).
%--------------------------------------------------------------------------
