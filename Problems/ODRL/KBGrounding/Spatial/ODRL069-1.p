%--------------------------------------------------------------------------
% File     : ODRL069-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : NOT partial overlap: eq(germany) ⊆ isPartOf(wE) — full subsumption
% Expected : Theorem
% Verdict  : Subsumption
% Paper    : Refinement Conflict Refuted
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ; odrl:rightOperand geo:germany ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] ] .
%
% Formal:
%   Three-part test fails at part 2:
%   X: eq(de) ∩ isPartOf(wE) → germany ✓  (de=de ∧ leq(de,wE))
%   Y: eq(de) \ isPartOf(wE) → NO WITNESS  (de ≤ wE directly)
%   Z: isPartOf(wE) \ eq(de)  → france ✓
%   → Not partial overlap; this is FULL SUBSUMPTION (cf. ODRL034)
%
% Notes    : flip_conj proves the missing witness Y doesn't exist.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
% NOT partial overlap — prove part 2 witness cannot exist
fof(odrl069, conjecture,
    ~( ?[Y]: ( in_denotation(Y, germany, eq)
            & ~in_denotation(Y, westernEurope, isPartOf) ) )).
%--------------------------------------------------------------------------
