%--------------------------------------------------------------------------
% File     : ODRL347-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : All three axes open overlap → box Compatible (density)
% Version  : 1.0
% English  : Width:  intervals gt 200 and lt 800 share open (200, 800)        Compatible
%           : Height: intervals gt 100 and lt 500 share open (100, 500)        Compatible
%           : Depth:  intervals gt 8   and lt 32  share open (8, 32)           Compatible
%           : All three conjuncts are existentials over open intervals with no
%           : named interior witness; genuinely requires ORD001-0.ax (density).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL347-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : compatible
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL347-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/ORD001-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% Minimal named-constant chain: no named point lies strictly between any
% adjacent pair, so all three open-interval witnesses must come from ORD001
% (density). Do NOT add v16, v300, or other intermediate constants here —
% they would let the existentials be discharged without density and
% defeat the test.
fof(val_v0,        axiom, val(v0)).
fof(val_v8,        axiom, val(v8)).
fof(val_v32,       axiom, val(v32)).
fof(val_v100,      axiom, val(v100)).
fof(val_v200,      axiom, val(v200)).
fof(val_v500,      axiom, val(v500)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v8,     axiom, less(v0,   v8)).
fof(ord_v8_v32,    axiom, less(v8,   v32)).
fof(ord_v32_v100,  axiom, less(v32,  v100)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(distinct,      axiom, $distinct(v0, v8, v32, v100, v200, v500, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl347, conjecture,
    ?[X,Y,Z]: (in_open(X, v200, v800) & in_open(Y, v100, v500) & in_open(Z, v8,   v32))).
%--------------------------------------------------------------------------
