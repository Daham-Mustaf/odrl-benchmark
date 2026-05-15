%--------------------------------------------------------------------------
% File     : ODRL737-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Projection: claim box2_compatible when axis 2 conflicts (wrong)
% Version  : 1.0
% English  : Axis2: [v0,v300]∩[v600,v800]=∅. Axis1 ok.
%           : Wrong claim: box2_compatible.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL737-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL737-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PROJ000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v300,axiom,val(v300)).
fof(val_v400,axiom,val(v400)).
fof(val_v600,axiom,val(v600)).
fof(val_v800,axiom,val(v800)).
fof(ord_v0_v300,axiom,less(v0,v300)).
fof(ord_v300_v400,axiom,less(v300,v400)).
fof(ord_v400_v600,axiom,less(v400,v600)).
fof(ord_v600_v800,axiom,less(v600,v800)).
fof(distinct,axiom,$distinct(v0,v300,v400,v600,v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl737, conjecture,
    box2_compatible(v0,v800,v0,v300,v0,v800,v600,v800)).
%--------------------------------------------------------------------------
