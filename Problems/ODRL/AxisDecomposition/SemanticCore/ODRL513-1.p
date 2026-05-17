%--------------------------------------------------------------------------
% File     : ODRL513-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Geometric consequence of def:profile (iii) -- gt at effective upper bound has empty denotation
% Version  : 1.0
% English  : Geometric consequence of def:profile (iii): when the effective
%           : upper bound is v600, a constraint (gt, v600) combined with the
%           : domain (v0, v600] has empty denotation, since no X satisfies
%           : less(v600, X) AND leq(X, v600).
%           : Note: see ODRL512 comment.  This tests the geometric consequence;
%           : WF000 / WellFormedness tests the WF predicate.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL513-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL513-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl513, conjecture,
    ![X]: ~(less(v600, X) & in_lopen(X, v0, v600))).
%--------------------------------------------------------------------------
