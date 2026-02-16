%--------------------------------------------------------------------------
% File     : ODRL090-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Runtime soundness: Conflict → no ω satisfies both
% Expected : Theorem
% Verdict  : Sound
% Paper    : Theorem 3 — Runtime Soundness (Conflict → no context)
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
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:easternEurope ] ] .
%
% Denotation analysis:
%   Static: ⟦isPartOf(wE)⟧ ∩ ⟦isPartOf(eE)⟧ = ∅ (Conflict)
%   6-step refutation proof:
%     1. satisfies_needs_assignment → assigns(ω_sk, X)
%     2. satisfaction_to_denotation → in_den(X, wE/eE, isPartOf)
%     3. context_functional → same X for both
%     4. den_isPartOf_onlyif → leq(X, wE) ∧ leq(X, eE)
%     5. disj_downward(wE ⊥ eE) → disjoint(X, X)
%     6. disj_irrefl → contradiction
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').

fof(odrl090, conjecture,
    ![Omega]: ~( satisfies(Omega, westernEurope, isPartOf)
              & satisfies(Omega, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
