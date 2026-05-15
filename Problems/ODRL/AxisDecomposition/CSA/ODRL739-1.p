%--------------------------------------------------------------------------
% File     : ODRL739-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : CSA Boundary: claim gteq∩lt compatible when equal (wrong)
% Version  : 1.0
% English  : gteq 600 vs lt 600: [600,∞)∩(0,600)=∅.
%           : Wrong claim: overlap.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL739-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL739-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,axiom,val(v0)).
fof(val_v600,axiom,val(v600)).
fof(ord_v0_v600,axiom,less(v0,v600)).
fof(distinct,axiom,$distinct(v0,v600)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl739, conjecture,
    ?[X]: (leq(v600,X) & in_open(X,v0,v600))).
%--------------------------------------------------------------------------
