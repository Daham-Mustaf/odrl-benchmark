%--------------------------------------------------------------------------
% File     : ODRL430-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 2D cc×cc — both axes touch → Compatible
% Version  : 1.0
% English  : Width:  (0,600]∩[600,∞)={600}≠∅ Compatible (cc)
%           : Height: (0,400]∩[400,∞)={400}≠∅ Compatible (cc)
%           : Witnesses: X=v600, Y=v400.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL430-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL430-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v400, v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl430, conjecture,
    ?[X,Y]: (in_lopen(X, v0, v600) & leq(v600, X) &
           in_lopen(Y, v0, v400) & leq(v400, Y))).
%--------------------------------------------------------------------------
