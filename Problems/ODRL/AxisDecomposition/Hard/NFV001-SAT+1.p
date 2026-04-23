%--------------------------------------------------------------------------
% File     : NFV001-SAT+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : axis_conflict hypothesis set is self-consistent (SAT companion)
% Version  : 1.0
% English  : The ordering n0<n5<n10<n15 with axis_conflict(n0,n5,n10,n15)
%           : is satisfiable — the disjointness of [n0,n5] and [n10,n15]
%           : is consistent with the strict chain (since less(n5,n10) holds).
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
% Comments : SAT companion for NFV001+1.p. No conjecture.
%           : Run with Mace4 -n 4 -N 6, Paradox, or Vampire-FMB.
%           : Policy source: Policies/NFV001-policy.ttl
%--------------------------------------------------------------------------

include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').
fof(order_0_5,   axiom, less(n0,n5)).
fof(order_5_10,  axiom, less(n5,n10)).
fof(order_10_15, axiom, less(n10,n15)).
fof(distinct,    axiom, $distinct(n0,n5,n10,n15)).
fof(conflict_hyp, axiom, axis_conflict(n0,n5,n10,n15)).
