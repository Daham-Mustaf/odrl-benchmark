%--------------------------------------------------------------------------
% File     : ODRL660-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : prec_cc backward: prec(u,l,c,c) implies less(u,l)
% Version  : 1.0
% English  : thm:criterion prec_cc backward: prec(u_c,l_c,c,c) => less(u_c,l_c)
%           : Directly tests the backward direction of the prec_cc biconditional.
%           : Fails under a forward-only axiom.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL660-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL660-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PREC000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_u_c,     axiom, val(u_c)).
fof(val_l_c,     axiom, val(l_c)).
fof(prec_assumed, axiom, prec(u_c, l_c, c, c)).
fof(distinct,    axiom, $distinct(u_c, l_c)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl660, conjecture,
    less(u_c, l_c)).
%--------------------------------------------------------------------------
