%--------------------------------------------------------------------------
% File     : ODRL451-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 3-branch or with mixed ops: all branches conflict → Conflict
% Version  : 1.0
% English  : PolicyA: width eq 600 OR height lt 200 OR depth gt 100 (odrl:or)
%           : PolicyB: width gt 800 AND height gteq 400 AND depth lteq 50 (odrl:and)
%           : (A1,B): {600}∩(800,∞)=∅; (A2,B): (0,200)∩[400,∞)=∅; (A3,B): (100,∞)∩(0,50]=∅
%           : All 3 branch pairs Conflict → verdictOr=Conflict
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL451-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL451-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/COMP000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v50, axiom, val(v50)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v50, axiom, less(v0, v50)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v50_v100, axiom, less(v50, v100)).
fof(ord_v50_v200, axiom, less(v50, v200)).
fof(ord_v50_v400, axiom, less(v50, v400)).
fof(ord_v50_v600, axiom, less(v50, v600)).
fof(ord_v50_v800, axiom, less(v50, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v50, v100, v200, v400, v600, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl451, conjecture,
    ![X,Y,Z]: ~((in_closed(X, v600, v600) | in_open(Y, v0, v200) | less(v100, Z)) &
            (less(v800, X) & leq(v400, Y) & in_lopen(Z, v0, v50)))).
%--------------------------------------------------------------------------
