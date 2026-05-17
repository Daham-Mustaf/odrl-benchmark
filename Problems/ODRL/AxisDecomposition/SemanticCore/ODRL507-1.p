%--------------------------------------------------------------------------
% File     : ODRL507-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : thm:projection -- box <=> per-axis membership (concrete instance)
% Version  : 1.0
% English  : thm:projection at concrete point (v200, v200) over box
%           : [v0, v600] x [v0, v400]:
%           : in_box2(v200, v200, v0, v600, v0, v400)
%           : <=> (in_closed(v200, v0, v600) & in_closed(v200, v0, v400)).
%           : Tests both directions of the paper's biconditional.
%           : FOL closes via in_box2_def (PROJ000) + in_closed_def (AXIS000).
%           : SMT: negation of the iff is empty.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL507-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL507-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl507, conjecture,
    in_box2(v200, v200, v0, v600, v0, v400)
  <=> (in_closed(v200, v0, v600) & in_closed(v200, v0, v400))).
%--------------------------------------------------------------------------
