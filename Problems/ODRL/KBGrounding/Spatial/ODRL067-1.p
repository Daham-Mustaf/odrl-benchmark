%--------------------------------------------------------------------------
% File     : ODRL067-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Partial overlap: neq(germany) ∩≠ isPartOf(westernEurope)
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Refinement Conflict (neq vs isPartOf)
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:neq ; odrl:rightOperand geo:germany ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] ] .
%
% Formal:
%   ⟦neq(germany)⟧  = C \ {germany}  (25 concepts)
%   ⟦isPartOf(wE)⟧ = ↓wE            (10 concepts)
%   X=france:   france≠germany ∧ leq(france,wE)   ✓  [intersection]
%   Y=poland:   poland≠germany ∧ ¬leq(poland,wE)  ✓  [c1 only]
%   Z=germany:  leq(germany,wE) ∧ germany=germany  ✓  [c2 only]
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl067, conjecture,
    ( ?[X]: ( in_denotation(X, germany, neq)
           & in_denotation(X, westernEurope, isPartOf) )
    & ?[Y]: ( in_denotation(Y, germany, neq)
           & ~in_denotation(Y, westernEurope, isPartOf) )
    & ?[Z]: ( in_denotation(Z, westernEurope, isPartOf)
           & ~in_denotation(Z, germany, neq) ) )).
%--------------------------------------------------------------------------
