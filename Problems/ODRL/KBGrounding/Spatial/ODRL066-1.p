%--------------------------------------------------------------------------
% File     : ODRL066-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Partial overlap: hasPart(germany) ∩≠ isPartOf(westernEurope)
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Refinement Conflict (hasPart vs isPartOf)
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:hasPart ; odrl:rightOperand geo:germany ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] ] .
%
% Formal:
%   ⟦hasPart(germany)⟧  = {X | leq(germany,X)} = {germany, wE, europe}
%   ⟦isPartOf(wE)⟧    = ↓wE = {wE, austria, belgium, france, de, ...}
%   X=germany: leq(germany,germany) ∧ leq(germany,wE)    ✓  [intersection]
%   Y=europe:  leq(germany,europe)  ∧ ¬leq(europe,wE)    ✓  [c1 only]
%   Z=france:  leq(france,wE)       ∧ ¬leq(germany,france) ✓  [c2 only]
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl066, conjecture,
    ( ?[X]: ( in_denotation(X, germany, hasPart)
           & in_denotation(X, westernEurope, isPartOf) )
    & ?[Y]: ( in_denotation(Y, germany, hasPart)
           & ~in_denotation(Y, westernEurope, isPartOf) )
    & ?[Z]: ( in_denotation(Z, westernEurope, isPartOf)
           & ~in_denotation(Z, germany, hasPart) ) )).
%--------------------------------------------------------------------------
