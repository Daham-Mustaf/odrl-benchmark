%--------------------------------------------------------------------------
% File     : NFV001+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Conflict verdict implies no joint witness (prop:no-false-verdict)
% Version  : 1.0
% English  : If axis_conflict holds for two closed intervals then no value
%           : belongs to both. Establishes Conflict is never a false positive
%           : (prop:no-false-verdict, Conflict direction).
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R.,
%          :          Quix, C., Decker, S. Axis Decomposition for ODRL.
%          :          arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : NFV001+1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Hard tier — prop:no-false-verdict Conflict direction.
%           : axis_conflict given as hypothesis; prover derives emptiness.
%           : Policy source: Policies/NFV001-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').

% Domain constants: n0 < n5 < n10 < n15
fof(order_0_5,   hypothesis, less(n0,n5)).
fof(order_5_10,  hypothesis, less(n5,n10)).
fof(order_10_15, hypothesis, less(n10,n15)).

% The two intervals [n0,n5] and [n10,n15] are disjoint on this axis.
% axis_conflict is defined in AXIS000 Section B as the absence of a
% shared witness; we assert it here directly as a ground hypothesis to
% exercise the no-false-verdict claim independently of the criterion proof.
fof(conflict_hyp, hypothesis,
    axis_conflict(n0,n5,n10,n15)).

% Conjecture: no value lies in both intervals.
% This is prop:no-false-verdict (Conflict direction):
%   Conflict => no request simultaneously satisfies both constraint sets.
fof(no_false_conflict, conjecture,
    ~?[X]: (in_closed(X,n0,n5) & in_closed(X,n10,n15))).
%--------------------------------------------------------------------------
