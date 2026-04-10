%--------------------------------------------------------------------------
% File     : ODRL636-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : completion_compat at InfD: V=InfD is valid for eq completion
% Version  : 1.0
% English  : def:completion: V=InfD is in [InfD,SupD] so completion_compatible holds.
%           : completion_compatible(v0, v0, v1200) — infimum as eq value.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL636-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL636-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMPL000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(distinct, axiom, $distinct(v0, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl636, conjecture,
    completion_compatible(v0, v0, v1200)).
%--------------------------------------------------------------------------
