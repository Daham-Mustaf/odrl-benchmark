%--------------------------------------------------------------------------
% File     : ODRL308-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : width > 200 vs width < 800: open overlap
% Version  : 1.0
% English  : width gt 200 → (200, ∞)     [def:interval-denotation, gt]
%           : width lt 800 → (0, 800)     [def:interval-denotation, lt; D_k=(0,∞)]
%           : (200, ∞) ∩ (0, 800) = (200, 800) ≠ ∅
%           : Witness must lie strictly inside open interval (200,800).
%           : Requires ORD001-0.ax: density guarantees ∃Z. v200 < Z < v800.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL308-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL308-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/ORD001-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% v0 = domain lower bound (excluded); v200, v800 = constraint values
% in_open(X,v0,v800) encodes (0,800) = sem(lt 800) over D_k=(0,inf)
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v200,   axiom, less(v0, v200)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(distinct,      axiom, $distinct(v0, v200, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl308, conjecture,
    ?[X]: (less(v200, X) & in_open(X, v0, v800))).
%--------------------------------------------------------------------------
