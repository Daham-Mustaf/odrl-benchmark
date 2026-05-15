%--------------------------------------------------------------------------
% File     : ODRL712-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA WellFormedness: claim wf(eq) not well-formed (wrong)
% Version  : 1.0
% English  : Flip of ODRL610: wf(eq,v600,v0,v1200) holds.
%           : Wrong claim: ~wf(eq,v600,v0,v1200).
%           : Countermodel: v600 in [v0,v1200] so wf holds — negation impossible.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL712-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL712-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/WF000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl712, conjecture,
    ~wf(eq, v600, v0, v1200)).
%--------------------------------------------------------------------------
