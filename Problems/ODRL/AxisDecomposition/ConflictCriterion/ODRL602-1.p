%--------------------------------------------------------------------------
% File     : ODRL602-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : prec_oc: leq(U,L) implies prec(U,L,o,c)
% Version  : 1.0
% English  : thm:criterion prec_oc: leq(v5,v5) => prec(v5,v5,o,c)
%           : Open upper v5 (excluded), closed lower v5: equal is sufficient.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL602-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL602-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PREC000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v5, axiom, val(v5)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl602, conjecture,
    prec(v5, v5, o, c)).
%--------------------------------------------------------------------------
