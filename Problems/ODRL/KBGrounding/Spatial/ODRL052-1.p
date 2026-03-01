%--------------------------------------------------------------------------
% File     : ODRL052-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Common ancestor: hasPart(germany) ∩ hasPart(france) ≠ ∅
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
%       odrl:constraint [ odrl:leftOperand odrl:spatial ; odrl:operator odrl:hasPart ; odrl:rightOperand geo:france ] ] .
%
% Formal:
%   ⟦hasPart(germany)⟧ = {X | leq(germany,X)} ∋ westernEurope
%   ⟦hasPart(france)⟧  = {X | leq(france,X)}  ∋ westernEurope
%   Witness: westernEurope  [leq(germany,wE) ∧ leq(france,wE)]
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl052, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, france, hasPart) )).
%--------------------------------------------------------------------------
