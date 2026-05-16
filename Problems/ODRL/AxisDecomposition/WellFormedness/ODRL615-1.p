%--------------------------------------------------------------------------
% File     : ODRL615-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : wf_gt: V strictly below SupD is well-formed
% Version  : 1.0
% English  : def:well-formed wf_gt: V in [InfD,SupD] & V != SupD => wf(gt,V,InfD,SupD)
%           : v600 != v1200 and v600 in [v0,v1200] => wf(gt,v600,v0,v1200).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL615-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL615-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/WF000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl615, conjecture,
    wf(gt, v600, v0, v1200)).
%--------------------------------------------------------------------------
