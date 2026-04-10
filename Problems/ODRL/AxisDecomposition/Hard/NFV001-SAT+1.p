%--------------------------------------------------------------------------
% File     : NFV001-SAT+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : axis_conflict hypothesis set is self-consistent (SAT companion)
% Version  : 1.0
% English  : The ordering n0<n5<n10<n15 with axis_conflict(n0,n5,n10,n15)
%           : is satisfiable — the hypotheses of NFV001 do not self-contradict.
%           : This is the SAT companion of NFV001+1.p (THM).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : NFV001-SAT+1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : SAT companion for NFV001+1.p.
%           : Confirms axis_conflict hypothesis is consistent before THM proof.
%           : Policy source: Policies/NFV001-policy.ttl
%--------------------------------------------------------------------------

include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').
fof(order_0_5,   axiom, less(n0,n5)).
fof(order_5_10,  axiom, less(n5,n10)).
fof(order_10_15, axiom, less(n10,n15)).
fof(conflict_hyp, axiom, axis_conflict(n0,n5,n10,n15)).
% No conjecture — model finder confirms consistency.
fof(sat_witness, axiom, less(n0,n15)).
