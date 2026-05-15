%--------------------------------------------------------------------------
% File     : ODRL623-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : thm:projection 3D: point outside box3 on axis 2
% Version  : 1.0
% English  : thm:projection: v800 NOT in [v0,v600] on axis 2
%           : => (v300,v800,v200) NOT in box3.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL623-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL623-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200,   axiom, less(v0, v200)).
fof(ord_v0_v300,   axiom, less(v0, v300)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v200, v300, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl623, conjecture,
    ~in_box3(v300, v800, v200, v0, v600, v0, v600, v0, v600)).
%--------------------------------------------------------------------------
