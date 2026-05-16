%--------------------------------------------------------------------------
% File     : ODRL761-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : intra-policy: lteq 600 AND gteq 800 gives empty denotation
% Version  : 1.0
% English  : Remark 3.4 intra-policy self-contradiction.
%           : width lteq 600: denotation is (v0, v600].
%           : width gteq 800: denotation is [v800, ∞).
%           : (v0, v600] ∩ [v800, ∞) = ∅ — no request satisfies both.
%           : Encoded by asserting a witness in both denotations (via in_lopen
%           : and leq from AXIS000/ORD000), which forces leq(v800, v600) and
%           : contradicts the declared ord chain less(v600, v800).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL761-1.p
%
% Status   : Unsatisfiable
% Verdict  : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
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
fof(witness_in_lteq, axiom, in_lopen(witness, v0, v600)).
fof(witness_in_gteq, axiom, leq(v800, witness)).
% (No conjecture: prover refutes/satisfies the axiom set.)
%--------------------------------------------------------------------------
