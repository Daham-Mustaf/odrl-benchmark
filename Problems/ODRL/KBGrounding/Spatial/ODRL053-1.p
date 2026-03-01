%--------------------------------------------------------------------------
% File     : ODRL053-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-branch hasPart: hasPart(germany) ∩ hasPart(poland) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (hasPart)
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ; odrl:operator odrl:hasPart ; odrl:rightOperand geo:germany ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ; odrl:operator odrl:hasPart ; odrl:rightOperand geo:poland ] ] .
%
% Formal:
%   NOTE: isPartOf(germany) ∩ isPartOf(poland) = ∅  [disj(wE,eE)]
%   BUT hasPart goes UPWARD — cross-branch ancestors exist!
%   leq(germany,wE) → leq(germany,europe)  [leq_trans]
%   leq(poland,eE)  → leq(poland,europe)   [leq_trans]
%   Witness: europe ∈ both hasPart sets
%
% Notes    : Directional reversal: conflict in isPartOf becomes compatible in hasPart.
% Difficulty: Medium-Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl053, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, poland, hasPart) )).
%--------------------------------------------------------------------------
