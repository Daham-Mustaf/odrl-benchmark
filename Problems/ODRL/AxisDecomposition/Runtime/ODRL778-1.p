%--------------------------------------------------------------------------
% File     : ODRL778-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Runtime soundness (box): no request satisfies both BSB and BnF
% Version  : 1.0
% English  : Thm 6 across the box: BSB and(width lteq 1920, height lteq 1080)
%           : vs BnF and(width eq 2400, height eq 800).  The width axis
%           : conflicts (2400 not in (0,1920]), so by Thm 6 no request (W,H)
%           : satisfies both policies regardless of the compatible height.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL778-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : runtime
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL778-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v0_v800,     axiom, less(v0, v800)).
fof(ord_v800_v1080,  axiom, less(v800, v1080)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(ord_v1920_v2400, axiom, less(v1920, v2400)).
fof(distinct, axiom, $distinct(v0, v800, v1080, v1920, v2400)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl778, conjecture,
    ![W,H]: ~(in_lopen(W, v0, v1920) & in_closed(W, v2400, v2400) &
          in_lopen(H, v0, v1080) & in_closed(H, v800, v800))).
%--------------------------------------------------------------------------
