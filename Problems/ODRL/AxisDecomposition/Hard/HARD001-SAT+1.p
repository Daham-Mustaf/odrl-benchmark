%--------------------------------------------------------------------------
% File     : HARD001-SAT+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Hypothesis set of HARD001 is self-consistent (SAT companion)
% Version  : 1.0
% English  : The ordering chain n0<n3<n5<n10<n20 with universal domain bounds
%           : is satisfiable — the hypotheses of HARD001 do not self-contradict.
%           : This is the SAT companion of HARD001+1.p (THM).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : HARD001-SAT+1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : SAT companion for HARD001+1.p.
%           : No conjecture — prover finds a model of the hypothesis set.
%           : Policy source: Policies/HARD001-policy.ttl
%--------------------------------------------------------------------------

include('Axioms/ORD000-0.ax').
include('Axioms/ORD001-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/COMPL000-0.ax').
% Ordering chain: n0 < n3 < n5 < n10 < n20
fof(h_0_3,    axiom, less(n0,n3)).
fof(h_3_5,    axiom, less(n3,n5)).
fof(h_5_10,   axiom, less(n5,n10)).
fof(h_10_20,  axiom, less(n10,n20)).
% Domain bounds
fof(h_inf_lb, axiom, ![X]: leq(ninf,X)).
fof(h_sup_ub, axiom, ![X]: leq(X,nsup)).
% SAT witness: the ordering chain is satisfiable in any dense total order.
% No conjecture — model finder confirms consistency.
fof(sat_witness, axiom, less(n0,n20)).
