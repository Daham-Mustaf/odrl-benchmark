%--------------------------------------------------------------------------
% File     : ODRL329-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Narrow width strip × wide height → box Compatible
% Version  : 1.0
% English  : Width:  gteq 500 → [500,∞)  ∩  lteq 510 → (0,510] = [500,510] ≠ ∅  Compatible
%           : Height: gteq 100 → [100,∞)  ∩  lteq 900 → (0,900] = [100,900] ≠ ∅  Compatible
%           : box_verdict(Compatible, Compatible) = Compatible  [def:box-verdict Rule 2]
%           : Witnesses: (X=v500, Y=v100). Tests narrow but non-empty intersection.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL329-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL329-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v100,      axiom, val(v100)).
fof(val_v500,      axiom, val(v500)).
fof(val_v510,      axiom, val(v510)).
fof(val_v900,      axiom, val(v900)).
fof(ord_v0_v100,   axiom, less(v0,   v100)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v510,   axiom, less(v0,   v510)).
fof(ord_v0_v900,   axiom, less(v0,   v900)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v510, axiom, less(v100, v510)).
fof(ord_v100_v900, axiom, less(v100, v900)).
fof(ord_v500_v510, axiom, less(v500, v510)).
fof(ord_v500_v900, axiom, less(v500, v900)).
fof(ord_v510_v900, axiom, less(v510, v900)).
fof(distinct,      axiom, $distinct(v0, v100, v500, v510, v900)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl329, conjecture,
    ?[X,Y]: (leq(v500, X) & in_lopen(X, v0, v510) &
          leq(v100, Y) & in_lopen(Y, v0, v900))).
%--------------------------------------------------------------------------
