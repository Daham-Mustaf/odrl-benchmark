%--------------------------------------------------------------------------
% File     : NFV002+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Compatible verdict implies joint witness exists (prop:no-false-verdict)
% Version  : 1.0
% English  : If axis_compatible holds for two closed intervals then some
%           : value belongs to both. Establishes Compatible is never a
%           : false positive (prop:no-false-verdict, Compatible direction).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R.,
%          :          Quix, C., Decker, S. Axis Decomposition for ODRL.
%          :          arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : NFV002+1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Hard tier — prop:no-false-verdict Compatible direction.
%           : axis_compatible given as hypothesis; prover finds witness.
%           : Policy source: Policies/NFV002-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').

% Domain constants: n0 < n5 < n10
fof(order_0_5,  hypothesis, less(n0,n5)).
fof(order_5_10, hypothesis, less(n5,n10)).

% The two intervals [n0,n10] and [n5,n10] overlap (n5 is in both).
% axis_compatible is defined in AXIS000 Section B as the existence of a
% shared witness; we assert it here directly as a ground hypothesis to
% exercise the no-false-verdict claim independently of the criterion proof.
fof(compatible_hyp, hypothesis,
    axis_compatible(n0,n10,n5,n10)).

% Conjecture: some value lies in both intervals.
% This is prop:no-false-verdict (Compatible direction):
%   Compatible => every axis was examined and admits overlap.
fof(no_false_compatible, conjecture,
    ?[X]: (in_closed(X,n0,n10) & in_closed(X,n5,n10))).
%--------------------------------------------------------------------------
