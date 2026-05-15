%--------------------------------------------------------------------------
% File     : ODRL651-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 1-axis containment: lteq 800 does not subsume lteq 600 → Conflict
% Version  : 1.0
% English  : Width: (0,800] ⊄ (0,600]  →  ~axis_subsumes(v0,v800,v0,v600)
%           : subs_verdict(v0,v800,present,v0,v600,present) = conflict
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL651-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : subsumption
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL651-policy.ttl
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
fof(odrl651, conjecture,
    subs_verdict(v0,v800,present,v0,v600,present) = conflict).
%--------------------------------------------------------------------------
