%--------------------------------------------------------------------------
% File     : ODRL650-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 1-axis containment: lteq 600 subsumes lteq 800 → Compatible
% Version  : 1.0
% English  : Width: (0,600] ⊆ (0,800]  →  axis_subsumes(v0,v600,v0,v800)
%           : subs_verdict(v0,v600,present,v0,v800,present) = compatible
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL650-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL650-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/SUBS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl650, conjecture,
    subs_verdict(v0,v600,present,v0,v800,present) = compatible).
%--------------------------------------------------------------------------
