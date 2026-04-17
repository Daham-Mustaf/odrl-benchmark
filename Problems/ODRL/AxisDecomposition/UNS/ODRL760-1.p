%--------------------------------------------------------------------------
% File     : ODRL760-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : intra-policy: eq 600 AND gteq 700 gives empty denotation
% Version  : 1.0
% English  : Remark 3.4 intra-policy self-contradiction.
%           : width eq 600: denotation is {v600}.
%           : width gteq 700: denotation is [v700, ∞).
%           : {v600} ∩ [v700, ∞) = ∅ — no request satisfies both.
%           : Encoded by asserting a witness X in both denotations (via in_closed
%           : and leq from AXIS000/ORD000), which forces leq(v700, v600) and
%           : contradicts the declared ord chain less(v600, v700).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL760-1.p
%
% Status   : Unsatisfiable
% Rating   : 0.00 v9.0.0
% SPC      : FOF_UNS_RFN
%
% Comments : UNS — Remark 3.4 intra-policy self-contradiction.
%           : Empty denotation: no request satisfies the constraint.
%           : Policy source: Policies/ODRL760-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v700, axiom, val(v700)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v600_v700, axiom, less(v600, v700)).
fof(distinct, axiom, $distinct(v0, v600, v700)).
fof(witness_in_eq,   axiom, in_closed(witness, v600, v600)).
fof(witness_in_gteq, axiom, leq(v700, witness)).
% ─── No conjecture — contradiction in axioms ─────────────────────────
%--------------------------------------------------------------------------
