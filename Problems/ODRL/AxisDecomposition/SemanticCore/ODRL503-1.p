%--------------------------------------------------------------------------
% File     : ODRL503-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : lem:totality -- gt denotation is non-empty
% Version  : 1.0
% English  : lem:totality applied to gt: denotation (v200, +inf) is non-empty.
%           : Witness: any X with less(v200, X); e.g., X = v600.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL503-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL503-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl503, conjecture,
    ?[X]: less(v200, X)).
%--------------------------------------------------------------------------
