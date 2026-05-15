%--------------------------------------------------------------------------
% File     : ODRL325-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Both axes touch at boundary → single-point box Compatible
% Version  : 1.0
% English  : Width:  lteq 600 → (0,600]  ∩  gteq 600 → [600,∞) = {600} ≠ ∅  Compatible
%           : Height: lteq 400 → (0,400]  ∩  gteq 400 → [400,∞) = {400} ≠ ∅  Compatible
%           : box_verdict(Compatible, Compatible) = Compatible  [def:box-verdict Rule 2]
%           : Witness: (X=v600, Y=v400). Box intersection is a single point.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL325-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL325-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl325, conjecture,
    ?[X,Y]: (in_lopen(X, v0, v600) & leq(v600, X) &
          in_lopen(Y, v0, v400) & leq(v400, Y))).
%--------------------------------------------------------------------------
