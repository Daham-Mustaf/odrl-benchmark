%--------------------------------------------------------------------------
% File     : ODRL756-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT SingleAxis: gteq constraint is satisfiable
% Version  : 1.0
% English  : width gteq 200: [200,inf) is non-empty. Witness: v400.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL756-1.p
%
% Status   : Satisfiable
% Verdict  : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL756-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(distinct, axiom, $distinct(v200, v400)).
fof(witness,  axiom, leq(v200, v400)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl756, conjecture,
    None).
%--------------------------------------------------------------------------
