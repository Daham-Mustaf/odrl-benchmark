%--------------------------------------------------------------------------
% File     : ODRL753-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : WF000 well-formedness axioms are satisfiable
% Version  : 1.0
% English  : The WF000 well-formedness axioms are consistent.
%           : Witness: wf(eq,v600,v0,v1200) holds — v600 in [v0,v1200].
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL753-1.p
%
% Status   : Satisfiable
% Verdict  : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL753-policy.ttl
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
fof(wf_witness, axiom, wf(eq, v600, v0, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl753, conjecture,
    None).
%--------------------------------------------------------------------------
