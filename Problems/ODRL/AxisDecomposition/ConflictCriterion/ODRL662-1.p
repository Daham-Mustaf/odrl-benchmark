%--------------------------------------------------------------------------
% File     : ODRL662-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : prec_co at strict less: less(a,b) implies prec(a,b,c,o)
% Version  : 1.0
% English  : thm:criterion prec_co strict: less(a,b) => prec(a,b,c,o)
%           : Tests prec_co at strict separation, complementing ODRL603.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL662-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL662-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PREC000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_a,     axiom, val(a)).
fof(val_b,     axiom, val(b)).
fof(ord_a_b,   axiom, less(a, b)).
fof(distinct,  axiom, $distinct(a, b)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl662, conjecture,
    prec(a, b, c, o)).
%--------------------------------------------------------------------------
