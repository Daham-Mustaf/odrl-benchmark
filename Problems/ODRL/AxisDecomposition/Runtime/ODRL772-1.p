%--------------------------------------------------------------------------
% File     : ODRL772-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Runtime soundness: no request satisfies both lteq 1920 and eq 2400
% Version  : 1.0
% English  : Thm 6 (Runtime Soundness): the width axis conflicts between BSB
%           : (lteq 1920 -> (0,1920]) and BnF (eq 2400 -> {2400}).  Therefore
%           : no request value W satisfies both constraints, i.e. the static
%           : Conflict verdict guarantees no joint permit at runtime.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL772-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% Relation : runtime
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL772-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v1920, axiom, val(v1920)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v0_v1920,    axiom, less(v0, v1920)).
fof(ord_v1920_v2400, axiom, less(v1920, v2400)).
fof(distinct, axiom, $distinct(v0, v1920, v2400)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl772, conjecture,
    ![W]: ~(in_lopen(W, v0, v1920) & in_closed(W, v2400, v2400))).
%--------------------------------------------------------------------------
