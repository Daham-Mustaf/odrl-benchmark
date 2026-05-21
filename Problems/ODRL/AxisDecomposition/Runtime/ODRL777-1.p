%--------------------------------------------------------------------------
% File     : ODRL777-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Runtime xone-permit: request width 1200 satisfies exactly one branch
% Version  : 1.0
% English  : Def 24 xone-satisfaction: rho |= xone(B1,B2) iff rho satisfies
%           : exactly one branch.  BnF request is xone(width eq 1200,
%           : width eq 2400).  rho(width)=1200 satisfies the first branch and
%           : not the second (1200 != 2400), so exactly one holds and the
%           : xone-policy permits.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL777-1.p
%
% Status   : Theorem
% Verdict  : Permit
% Relation : runtime
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL777-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v1200, axiom, val(v1200)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v1200_v2400, axiom, less(v1200, v2400)).
fof(distinct, axiom, $distinct(v1200, v2400)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl777, conjecture,
    (in_closed(v1200, v1200, v1200) & ~in_closed(v1200, v2400, v2400))).
%--------------------------------------------------------------------------
