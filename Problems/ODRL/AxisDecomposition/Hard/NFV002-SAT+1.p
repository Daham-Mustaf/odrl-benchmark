%--------------------------------------------------------------------------
% File     : NFV002-SAT+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : axis_compatible hypothesis set is self-consistent (SAT companion)
% Version  : 1.0
% English  : The ordering n0<n5<n10 with axis_compatible(n0,n10,n5,n10)
%           : is satisfiable — the hypotheses of NFV002 do not self-contradict.
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
% Comments : SAT companion for NFV002+1.p.
%           : Confirms axis_compatible hypothesis is consistent before THM proof.
%           : Policy source: Policies/NFV002-policy.ttl
%--------------------------------------------------------------------------

include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').
fof(order_0_5,  axiom, less(n0,n5)).
fof(order_5_10, axiom, less(n5,n10)).
fof(compatible_hyp, axiom, axis_compatible(n0,n10,n5,n10)).
% No conjecture — model finder confirms consistency.
fof(sat_witness, axiom, less(n0,n10)).
