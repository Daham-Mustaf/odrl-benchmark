%--------------------------------------------------------------------------
% File     : ODRL775-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Runtime and-deny: request (2400,900) fails width, so box denied
% Version  : 1.0
% English  : Def 24 and-satisfaction: a single failing branch breaks the
%           : conjunction.  Request rho(width)=2400 fails width lteq 1920
%           : even though rho(height)=900 satisfies height lteq 1080, so
%           : rho does not satisfy the and-policy and is denied.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL775-1.p
%
% Status   : Theorem
% Verdict  : Deny
% Relation : runtime
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL775-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v900,  axiom, val(v900)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v0_v900,     axiom, less(v0, v900)).
fof(ord_v900_v1080,  axiom, less(v900, v1080)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(ord_v1920_v2400, axiom, less(v1920, v2400)).
fof(distinct, axiom, $distinct(v0, v900, v1080, v1920, v2400)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl775, conjecture,
    ~(in_lopen(v2400, v0, v1920) & in_lopen(v900, v0, v1080))).
%--------------------------------------------------------------------------
