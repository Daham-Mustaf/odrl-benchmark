%--------------------------------------------------------------------------
% File     : ODRL512-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Geometric consequence of def:profile (ii) -- lt at domain inf has empty denotation
% Version  : 1.0
% English  : Geometric consequence of def:profile (ii): a constraint (lt, v0)
%           : on domain (v0, +inf) has empty denotation, since no X satisfies
%           : less(v0, X) AND less(X, v0).  Closes via in_open unfold +
%           : less irreflexivity (transitivity gives less(v0, v0)).
%           : Note: def:profile (ii) rejects this constraint as ill-formed.
%           : WF000 / WellFormedness category tests the WF predicate directly.
%           : This problem tests the geometric consequence (empty denotation).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL512-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL512-policy.ttl
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
fof(odrl512, conjecture,
    ![X]: ~in_open(X, v0, v0)).
%--------------------------------------------------------------------------
