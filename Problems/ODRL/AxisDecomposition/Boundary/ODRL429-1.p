%--------------------------------------------------------------------------
% File     : ODRL429-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : gt ∩ gteq — open superset of closed → Compatible (sentinel)
% Version  : 1.0
% English  : thm:criterion gt∩gteq: (600,∞)∩[600,∞)=(600,∞)≠∅ Compatible
%           : Witness must be above v600 — adds sentinel v1200 with less(v600,v1200).
%           : X=v1200 satisfies less(v600,X) AND leq(v600,X).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL429-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL429-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl429, conjecture,
    ?[X]: (less(v600, X) & leq(v600, X))).
%--------------------------------------------------------------------------
