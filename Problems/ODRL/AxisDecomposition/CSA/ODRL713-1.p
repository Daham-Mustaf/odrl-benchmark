%--------------------------------------------------------------------------
% File     : ODRL713-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Projection: claim v400 in point interval [v600,v600] (wrong)
% Version  : 1.0
% English  : Flip of ODRL626: in_closed(v600,v600,v600) holds but in_closed(v400,v600,v600) does not.
%           : Wrong claim: in_closed(v400,v600,v600).
%           : Countermodel: v400 != v600 so v400 not in {v600}.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL713-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL713-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PROJ000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl713, conjecture,
    in_closed(v400, v600, v600)).
%--------------------------------------------------------------------------
