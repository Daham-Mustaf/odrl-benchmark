%--------------------------------------------------------------------------
% File     : ODRL654-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : C1 absent on width axis -> Unknown
% Version  : 1.0
% English  : C1 does not constrain width (P1=absent).
%           : Unknown-when-absent: intended scope of C1 not known.
%           : subs_verdict(v0,v600,absent,v0,v800,present) = unknown
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL654-1.p
%
% Status   : Theorem
% Verdict  : Unknown
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL654-policy.ttl
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
fof(odrl654, conjecture,
    subs_verdict(v0,v600,absent,v0,v800,present) = unknown).
%--------------------------------------------------------------------------
