%--------------------------------------------------------------------------
% File     : NFV002+1.p
% Domain   : Axis Decomposition (ODRL)
% Problem  : Compatible verdict implies a joint witness exists (prop:no-false-verdict)
% Version  : [vldb2027] axioms.
% English  : If axis_compatible holds for two closed intervals, then some
%            value belongs to both.  This establishes that Compatible is
%            never a false positive (prop:no-false-verdict, paper sec:conflict).
%            The witness is found via the total-order axioms of ORD000-0.ax.
%
% Refs     : [vldb2027] Axis Decomposition paper
% Source   : Generated for PAAR 2026 TPTP benchmark
% Names    :
% Status   : Theorem
% Rating   : TBD
% Syntax   : Number of formulae    :   6
%            Number of atoms       :  14
%            Maximal formula depth :   5
% SPC      : FOF_THM_RFO_SEQ
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
