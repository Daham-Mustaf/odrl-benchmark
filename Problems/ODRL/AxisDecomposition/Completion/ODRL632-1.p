%--------------------------------------------------------------------------
% File     : ODRL632-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : sharpness_compat: U<V in domain implies compatible completion exists
% Version  : 1.0
% English  : thm:unknown-sound sharpness_compat:
%           : leq(v0,v400) & less(v400,v800) & leq(v800,v1200)
%           : => completion_compatible(v400, v0, v1200).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL632-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL632-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMPL000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v400,  axiom, val(v400)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v400,    axiom, less(v0, v400)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v400, v800, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl632, conjecture,
    completion_compatible(v400, v0, v1200)).
%--------------------------------------------------------------------------
