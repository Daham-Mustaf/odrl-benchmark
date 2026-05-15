%--------------------------------------------------------------------------
% File     : ODRL764-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : SAT SemanticCore: verdict algebra constants are consistent
% Version  : 1.0
% English  : AXIS000 verdict algebra: conflict, compatible, unknown are three
%           : distinct is_verdict constants. Axioms are consistent, no contradiction.
%           : Meta-level consistency check; TTL is a minimal Set placeholder since
%           : the scenario is about the verdict ontology itself, not a concrete policy.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL764-1.p
%
% Status   : Satisfiable
% Verdict  : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL764-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(v_distinct, axiom, conflict != compatible & compatible != unknown & conflict != unknown).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl764, conjecture,
    None).
%--------------------------------------------------------------------------
