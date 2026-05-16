%--------------------------------------------------------------------------
% File     : ODRL664-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : negative: upper_tag(gteq,c) is NOT derivable
% Version  : 1.0
% English  : Negative existence test: upper_tag(gteq, c) must NOT be derivable
%           : from PREC000-0.ax v1.1, because gteq does not constrain the
%           : upper side of the interval.  Regression test for the previous
%           : version's bug.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL664-1.p
%
% Status   : CounterSatisfiable
% Verdict  : Unknown
% Relation : conflict
% SPC      : FOF_CSA_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL664-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PREC000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl664, conjecture,
    upper_tag(gteq, c)).
%--------------------------------------------------------------------------
