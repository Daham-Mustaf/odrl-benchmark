%--------------------------------------------------------------------------
% File     : ODRL401-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 1D Compatible (3 constants)
% Version  : 1.0
% English  : Width: lteq 800 → (0,800] ∩ gteq 200 → [200,∞) = [200,800] ≠ ∅ Compatible
%           : Witness: X=v200.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL401-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL401-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(distinct, axiom, $distinct(v0, v200, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl401, conjecture,
    ?[X]: (in_lopen(X, v0, v800) & leq(v200, X))).
%--------------------------------------------------------------------------
