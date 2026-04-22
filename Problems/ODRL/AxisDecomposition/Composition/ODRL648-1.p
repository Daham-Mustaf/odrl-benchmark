%--------------------------------------------------------------------------
% File     : ODRL648-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : or_sound_2branch: all axis pairs conflict implies no shared point
% Version  : 1.0
% English  : thm:composition-soundness disjunction case (or_sound_2branch):
%           : A1=[v0,v400], A2=[v0,v300]; B1=[v600,v800], B2=[v500,v800].
%           : All 4 cross-pairs conflict (v400<v500, v300<v500)
%           : => no point in (A1∪A2) ∩ (B1∪B2).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL648-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL648-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMP000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v400_v500, axiom, less(v400, v500)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v300, v400, v500, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl648, conjecture,
    ![X]: ~(
    (in_closed(X,v0,v400) | in_closed(X,v0,v300)) &
    (in_closed(X,v600,v800) | in_closed(X,v500,v800)))).
%--------------------------------------------------------------------------
