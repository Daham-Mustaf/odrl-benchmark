%--------------------------------------------------------------------------
% File     : ODRL609-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : operator tags: lt has open upper, gt has open lower
% Version  : 1.0
% English  : Operator tags: lt => upper_tag(lt,o), gt => lower_tag(gt,o)
%           : These capture the open-boundary semantics of strict operators.
%           : SMT is an indirect sanity check (lt/gt contradictory at same value);
%           : the tag axioms themselves have no direct SMT encoding.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL609-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : conflict
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL609-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PREC000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl609, conjecture,
    upper_tag(lt, o) & lower_tag(gt, o)).
%--------------------------------------------------------------------------
