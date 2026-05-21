%--------------------------------------------------------------------------
% File     : ODRL771-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Runtime deny: request width 2400 violates lteq 1920
% Version  : 1.0
% English  : Def 24 satisfaction: BnF request rho(width)=2400 against BSB
%           : width constraint lteq 1920 -> (0,1920].  2400 not in (0,1920],
%           : so rho fails the constraint and the Evaluator state is deny.
%           : FOL proves the non-membership; SMT shows x=2400 & x in (0,1920]
%           : is unsatisfiable.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL771-1.p
%
% Status   : Theorem
% Verdict  : Deny
% Relation : runtime
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL771-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v1920, axiom, val(v1920)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v0_v1920,    axiom, less(v0, v1920)).
fof(ord_v1920_v2400, axiom, less(v1920, v2400)).
fof(distinct, axiom, $distinct(v0, v1920, v2400)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl771, conjecture,
    ~in_lopen(v2400, v0, v1920)).
%--------------------------------------------------------------------------
