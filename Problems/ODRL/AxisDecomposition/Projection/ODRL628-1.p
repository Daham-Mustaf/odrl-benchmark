%--------------------------------------------------------------------------
% File     : ODRL628-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : thm:aabb shape_open: in_open(X,v400,v600)
% Version  : 1.0
% English  : thm:aabb shape_open (shape 9): open bounded (v400,v600).
%           : Witness must be strictly between v400 and v600 -- requires ORD001 density.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL628-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL628-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/ORD001-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl628, conjecture,
    ?[X]: in_open(X, v400, v600)).
%--------------------------------------------------------------------------
