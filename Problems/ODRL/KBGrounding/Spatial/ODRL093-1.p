%--------------------------------------------------------------------------
% File     : ODRL093-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Permissive ⊤: ungrounded constraint → satisfy by default
% Expected : Theorem
% Verdict  : Permissive
% Paper    : Definition 10 (⊤ case) — Permissive Satisfaction
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand <unknownConcept> ] ] .
%
%   ω(spatial) = germany (grounded), constraint value = unknownConcept (ungrounded)
%
% Denotation analysis:
%   Def. 10 disjunction case 1: ⟦c⟧ = ⊤ → any grounded context satisfies.
%   permissive_satisfaction: assigns(ω, germany) ∧ ungrounded(unknownConcept)
%   → satisfies(ω, unknownConcept, isPartOf).
%   Backward bridge blocked: concept(unknownConcept) fails → no in_denotation.
%   NOTE: Enforcement policies may override with default-deny.
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').

fof(runtime_context_093, axiom, assigns(omega093, germany)).
fof(unknown_ungrounded, axiom, ungrounded(unknownConcept)).

fof(odrl093, conjecture,
    satisfies(omega093, unknownConcept, isPartOf)).
%--------------------------------------------------------------------------
