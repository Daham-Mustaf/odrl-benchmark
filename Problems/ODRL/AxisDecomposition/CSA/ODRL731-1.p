%--------------------------------------------------------------------------
% File     : ODRL731-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Completion: claim sharpness_compat holds without less(U,V) (wrong)
% Version  : 1.0
% English  : sharpness_compat requires less(U,V). V=U so fails.
%           : Wrong: claim completion_compatible(v800,v0,v600) without V in domain.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL731-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL731-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMPL000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v600,axiom,val(v600)).
fof(val_v800,axiom,val(v800)).
fof(ord_v0_v600,axiom,less(v0,v600)).
fof(ord_v600_v800,axiom,less(v600,v800)).
fof(distinct,axiom,$distinct(v0,v600,v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl731, conjecture,
    completion_compatible(v800, v0, v600)).
%--------------------------------------------------------------------------
