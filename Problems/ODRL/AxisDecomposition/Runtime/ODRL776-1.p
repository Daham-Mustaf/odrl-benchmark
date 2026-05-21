%--------------------------------------------------------------------------
% File     : ODRL776-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Runtime or-permit: request width 1200 satisfies the archival branch
% Version  : 1.0
% English  : Def 24 or-satisfaction: rho |= or(B1,B2) iff rho satisfies some
%           : branch.  BnF request is or(kiosk: width eq 2400, archival:
%           : width eq 1200).  rho(width)=1200 satisfies the archival branch
%           : (not the kiosk branch), so the or-policy permits.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL776-1.p
%
% Status   : Theorem
% Verdict  : Permit
% Relation : runtime
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL776-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v1200, axiom, val(v1200)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v1200_v2400, axiom, less(v1200, v2400)).
fof(distinct, axiom, $distinct(v1200, v2400)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl776, conjecture,
    (in_closed(v1200, v1200, v1200) | in_closed(v1200, v2400, v2400))).
%--------------------------------------------------------------------------
