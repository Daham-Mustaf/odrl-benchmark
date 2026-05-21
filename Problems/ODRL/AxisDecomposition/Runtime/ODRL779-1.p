%--------------------------------------------------------------------------
% File     : ODRL779-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Runtime permit at boundary: request width 1920 satisfies lteq 1920
% Version  : 1.0
% English  : Boundary satisfaction: lteq 1920 -> (0,1920] is closed at the
%           : upper end, so the request rho(width)=1920 lies exactly on the
%           : boundary and is permitted (1920 in (0,1920]).  Confirms the
%           : endpoint-inclusion of lteq at runtime.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL779-1.p
%
% Status   : Theorem
% Verdict  : Permit
% Relation : runtime
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL779-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v0_v1920, axiom, less(v0, v1920)).
fof(distinct, axiom, $distinct(v0, v1920)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl779, conjecture,
    in_lopen(v1920, v0, v1920)).
%--------------------------------------------------------------------------
