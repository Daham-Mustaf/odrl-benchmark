%--------------------------------------------------------------------------
% File     : ODRL774-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Runtime and-permit: request (1500,900) satisfies width&height box
% Version  : 1.0
% English  : Def 24 and-satisfaction: rho |= and(B1,B2) iff rho satisfies
%           : every branch.  Request rho(width)=1500, rho(height)=900 against
%           : BSB and(width lteq 1920, height lteq 1080): 1500 in (0,1920] and
%           : 900 in (0,1080], so both branches hold and rho permits.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL774-1.p
%
% Status   : Theorem
% Verdict  : Permit
% Relation : runtime
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL774-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v900,  axiom, val(v900)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1500, axiom, val(v1500)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v0_v900,     axiom, less(v0, v900)).
fof(ord_v0_v1500,    axiom, less(v0, v1500)).
fof(ord_v900_v1080,  axiom, less(v900, v1080)).
fof(ord_v1080_v1500, axiom, less(v1080, v1500)).
fof(ord_v1500_v1920, axiom, less(v1500, v1920)).
fof(distinct, axiom, $distinct(v0, v900, v1080, v1500, v1920)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl774, conjecture,
    (in_lopen(v1500, v0, v1920) & in_lopen(v900, v0, v1080))).
%--------------------------------------------------------------------------
