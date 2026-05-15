%--------------------------------------------------------------------------
% File     : ODRL752-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : PREC000 endpoint precedence is satisfiable
% Version  : 1.0
% English  : The PREC000 endpoint precedence axioms are consistent.
%           : Witness: prec(v5,v6,c,c) holds since less(v5,v6).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL752-1.p
%
% Status   : Satisfiable
% Verdict  : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL752-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v5, axiom, val(v5)).
fof(val_v6, axiom, val(v6)).
fof(ord_v5_v6, axiom, less(v5, v6)).
fof(distinct, axiom, $distinct(v5, v6)).
fof(prec_witness, axiom, prec(v5, v6, c, c)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl752, conjecture,
    None).
%--------------------------------------------------------------------------
