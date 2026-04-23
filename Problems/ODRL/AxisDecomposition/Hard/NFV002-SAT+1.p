%--------------------------------------------------------------------------
% File     : NFV002-SAT+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : axis_compatible hypothesis set is self-consistent (SAT companion)
% Version  : 1.0
% English  : The ordering n0<n5<n10 with axis_compatible(n0,n10,n5,n10)
%           : is satisfiable — the intervals [n0,n10] and [n5,n10] overlap
%           : in [n5,n10], so a witness exists (X=n5 or X=n10).
%           : This is the SAT companion of NFV002+1.p (THM).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : NFV002-SAT+1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : SAT companion for NFV002+1.p. No conjecture.
%           : Policy source: Policies/NFV002-policy.ttl
%--------------------------------------------------------------------------

include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').
fof(order_0_5,  axiom, less(n0,n5)).
fof(order_5_10, axiom, less(n5,n10)).
fof(distinct,   axiom, $distinct(n0,n5,n10)).
fof(compatible_hyp, axiom, axis_compatible(n0,n10,n5,n10)).
