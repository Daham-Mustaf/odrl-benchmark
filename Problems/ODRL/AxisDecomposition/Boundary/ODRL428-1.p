%--------------------------------------------------------------------------
% File     : ODRL428-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : lt ∩ lteq — open subset of closed → Compatible (density)
% Version  : 1.0
% English  : thm:criterion lt∩lteq: (0,600)∩(0,600]=(0,600)≠∅ Compatible
%           : Witness must be strictly inside (0,600) — no named constant.
%           : Requires ORD001-0.ax (density) for Vampire to find witness.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL428-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL428-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD001-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl428, conjecture,
    ?[X]: (in_open(X, v0, v600) & in_lopen(X, v0, v600))).
%--------------------------------------------------------------------------
