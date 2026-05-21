%--------------------------------------------------------------------------
% File     : ODRL773-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Runtime joint permit: a request satisfies both lteq 1080 and eq 800
% Version  : 1.0
% English  : Height axis is compatible: BSB lteq 1080 -> (0,1080] and BnF
%           : eq 800 -> {800} share the value 800.  A request rho(height)=800
%           : satisfies both, so a joint permit exists (existential witness).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL773-1.p
%
% Status   : Theorem
% Verdict  : Permit
% Relation : runtime
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL773-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1080, axiom, val(v1080)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v800_v1080, axiom, less(v800, v1080)).
fof(distinct, axiom, $distinct(v0, v800, v1080)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl773, conjecture,
    ?[W]: (in_lopen(W, v0, v1080) & in_closed(W, v800, v800))).
%--------------------------------------------------------------------------
