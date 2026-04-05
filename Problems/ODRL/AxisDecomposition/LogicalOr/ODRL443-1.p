%--------------------------------------------------------------------------
% File     : ODRL443-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : PolicyA and: all PolicyB or-branches conflict → Conflict
% Version  : 1.0
% English  : PolicyA: width lteq 400 AND height lteq 100 (odrl:and)
%           : PolicyB: width gteq 800 OR height gteq 200 (odrl:or)
%           : (A,B1): (0,400]∩[800,∞)=∅ Conflict; (A,B2): (0,100]∩[200,∞)=∅ Conflict
%           : All branch pairs Conflict → verdictOr=Conflict
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Names    : ODRL443-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. PAAR 2026 benchmark.
%           : Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).
%           : Policy source: Policies/ODRL443-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct, axiom, $distinct(v0, v100, v200, v400, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl443, conjecture,
    ~?[X,Y]: ((in_lopen(X, v0, v400) & in_lopen(Y, v0, v100)) &
            (leq(v800, X) | leq(v200, Y)))).
%--------------------------------------------------------------------------
