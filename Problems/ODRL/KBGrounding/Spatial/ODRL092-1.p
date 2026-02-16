%--------------------------------------------------------------------------
% File     : ODRL092-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Contrapositive: runtime witness → verdict ≠ Conflict
% Expected : Theorem
% Verdict  : Sound
% Paper    : Theorem 3 (contrapositive) — Runtime Witness → Static Compatible
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:westernEurope ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:neq ;
%         odrl:rightOperand geo:germany ] ] .
%
% Denotation analysis:
%   Contrapositive of Theorem 3: ∃ω:(ω ⊨ c1 ∧ ω ⊨ c2) → verdict ≠ Conflict.
%   Runtime witness: assigns(ω, france).
%   france ∈ ⟦isPartOf(wE)⟧ ∧ france ∈ ⟦neq(de)⟧ → static overlap.
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').

fof(runtime_context_092, axiom, assigns(omega092, france)).

fof(odrl092, conjecture,
    ?[X]: ( in_denotation(X, westernEurope, isPartOf)
          & in_denotation(X, germany, neq) )).
%--------------------------------------------------------------------------
