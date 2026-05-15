%--------------------------------------------------------------------------
% File     : ODRL616-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : wf_gt violation: V=SupD implies not wf(gt)
% Version  : 1.0
% English  : def:profile condition (iii): V=SupD => ~wf(gt,V,InfD,SupD)
%           : gt at the supremum gives empty denotation — not well-formed.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL616-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL616-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/WF000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(distinct, axiom, $distinct(v0, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl616, conjecture,
    ~wf(gt, v1200, v0, v1200)).
%--------------------------------------------------------------------------
