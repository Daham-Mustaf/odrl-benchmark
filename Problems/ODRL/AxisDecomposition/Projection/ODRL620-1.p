%--------------------------------------------------------------------------
% File     : ODRL620-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : thm:projection 2D: point inside box2
% Version  : 1.0
% English  : thm:projection: (v300,v400) in [v0,v600]x[v0,v600]
%           : iff v300 in [v0,v600] AND v400 in [v0,v600].
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL620-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL620-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PROJ000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v300,   axiom, less(v0, v300)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v300, v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl620, conjecture,
    in_box2(v300, v400, v0, v600, v0, v600)).
%--------------------------------------------------------------------------
