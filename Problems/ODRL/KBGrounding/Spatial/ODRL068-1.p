%--------------------------------------------------------------------------
% File     : ODRL068-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Partial overlap: isNoneOf({eE}) ∩≠ hasPart(poland)
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Refinement Conflict (isNoneOf vs hasPart)
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isNoneOf ; odrl:rightOperand geo:easternEurope ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [ odrl:action odrl:use ;
%       odrl:constraint [ odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:hasPart ; odrl:rightOperand geo:poland ] ] .
%
% Formal:
%   ⟦isNoneOf({eE})⟧   = C \ ↓eE = {europe, wE, nE, sE, france, ...}
%   ⟦hasPart(poland)⟧ = {X | leq(poland,X)} = {poland, eE, europe}
%   X=europe: ¬leq(europe,eE) ∧ leq(poland,europe)  ✓  [intersection]
%   Y=france: ¬leq(france,eE) ∧ ¬leq(poland,france)  ✓  [c1 only]
%   Z=poland: leq(poland,poland) ∧ leq(poland,eE) → poland ≤ eE → not in isNoneOf ✓ [c2 only]
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(list_excl068_1, axiom, in_value_list(easternEurope, excl068)).
fof(list_excl068_closed, axiom,
    ![G]: (in_value_list(G, excl068) => (G = easternEurope))).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl068, conjecture,
    ( ?[X]: ( in_denotation_set(X, excl068, isNoneOf)
           & in_denotation(X, poland, hasPart) )
    & ?[Y]: ( in_denotation_set(Y, excl068, isNoneOf)
           & ~in_denotation(Y, poland, hasPart) )
    & ?[Z]: ( in_denotation(Z, poland, hasPart)
           & ~in_denotation_set(Z, excl068, isNoneOf) ) )).
%--------------------------------------------------------------------------
