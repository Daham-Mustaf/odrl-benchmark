%--------------------------------------------------------------------------
% File     : ODRL755-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT SingleAxis: lteq constraint is satisfiable
% Version  : 1.0
% English  : width lteq 800: (0,800] is non-empty. Witness: v400.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL755-1.p
%
% Status   : Satisfiable
% Verdict  : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL755-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct, axiom, $distinct(v0, v400, v800)).
fof(witness,  axiom, in_lopen(v400, v0, v800)).
% (No conjecture: prover refutes/satisfies the axiom set.)
%--------------------------------------------------------------------------
