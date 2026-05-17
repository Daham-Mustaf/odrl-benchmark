%--------------------------------------------------------------------------
% File     : ODRL705-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA ConflictCriterion: claim NOT disjoint cc (wrong)
% Version  : 1.0
% English  : Flip of ODRL605: [v0,v5] vs [v6,v10] strictly separated
%           : (since less(v5, v6) in the named chain).
%           : Wrong claim: ~disjoint(v0,v5,c,c,v6,v10,c,c).
%           : Countermodel: less(v5,v6) => disjoint holds, so its negation fails.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL705-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL705-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,  axiom, val(v0)).
fof(val_v5,  axiom, val(v5)).
fof(val_v6,  axiom, val(v6)).
fof(val_v10, axiom, val(v10)).
fof(ord_v0_v5,  axiom, less(v0, v5)).
fof(ord_v5_v6,  axiom, less(v5, v6)).
fof(ord_v6_v10, axiom, less(v6, v10)).
fof(distinct, axiom, $distinct(v0, v5, v6, v10)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl705, conjecture,
    ~disjoint(v0, v5, closed, closed, v6, v10, closed, closed)).
%--------------------------------------------------------------------------
