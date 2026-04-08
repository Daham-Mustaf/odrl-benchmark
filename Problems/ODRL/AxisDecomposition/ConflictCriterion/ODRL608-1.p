%--------------------------------------------------------------------------
% File     : ODRL608-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : disjoint symmetry: disjoint(A,B) iff disjoint(B,A)
% Version  : 1.0
% English  : thm:criterion symmetry: disjoint is symmetric.
%           : disjoint(L1,U1,CL1,CU1,L2,U2,CL2,CU2) <=> disjoint(L2,U2,CL2,CU2,L1,U1,CL1,CU1)
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL608-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL608-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl608, conjecture,
    ![L1,U1,CL1,CU1,L2,U2,CL2,CU2]:
    (disjoint(L1,U1,CL1,CU1,L2,U2,CL2,CU2) <=>
     disjoint(L2,U2,CL2,CU2,L1,U1,CL1,CU1))).
%--------------------------------------------------------------------------
