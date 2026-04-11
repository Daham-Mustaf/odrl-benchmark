%--------------------------------------------------------------------------
% File     : ODRL762-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : intra-policy: lt InfD violates wf condition (ii) — empty denotation
% Version  : 1.0
% English  : Remark 3.4 intra-policy self-contradiction via wf_lt condition (ii).
%           : width lt v0 (infimum): [infD, v0) with v0=InfD => empty.
%           : def:profile condition (ii): op=lt => V != InfD.
%           : Violated: denotation is empty, policy is ill-formed.
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL762-1.p
%
% Status   : Unsatisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_UNS_RFN
%
% Comments : UNS — Remark 3.4 intra-policy self-contradiction.
%           : Empty denotation: no request satisfies the constraint.
%           : Policy source: Policies/ODRL762-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/WF000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(distinct, axiom, $distinct(v0, v1200)).
fof(contradiction, axiom, less(v0,v0)).
% ─── No conjecture — contradiction in axioms ─────────────────────────
%--------------------------------------------------------------------------
