%--------------------------------------------------------------------------
% File     : ODRL608-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : disjoint symmetry: disjoint(A,B) iff disjoint(B,A)
% Version  : 1.0
% English  : thm:criterion symmetry: disjoint is symmetric.
%           : disjoint(L1,U1,CL1,CU1,L2,U2,CL2,CU2) <=> disjoint(L2,U2,CL2,CU2,L1,U1,CL1,CU1)
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL608-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL608-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PREC000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl608, conjecture,
    ![L1,U1,CL1,CU1,L2,U2,CL2,CU2]:
    (disjoint(L1,U1,CL1,CU1,L2,U2,CL2,CU2) <=>
     disjoint(L2,U2,CL2,CU2,L1,U1,CL1,CU1))).
%--------------------------------------------------------------------------
