%--------------------------------------------------------------------------
% File     : ODRL095-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Runtime propagation: subsumption + conflict → no ω
% Expected : Theorem
% Verdict  : Sound
% Paper    : Lemma 2 + Theorem 3 — Runtime Conflict Propagation
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:germany ] ] .
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
%   Lemma 2: isPartOf(de) ⊑ isPartOf(wE) ∧ conflict(wE,eE) → conflict(de,eE).
%   Theorem 3: conflict(de,eE) → ¬∃ω: (ω ⊨ isPartOf(de) ∧ ω ⊨ isPartOf(eE)).
%   7-step proof (ODRL090 + one leq_trans step):
%     1. satisfies_needs_assignment → assigns(ω_sk, X)
%     2. satisfaction_to_denotation → in_den(X, de/eE, isPartOf)
%     3. context_functional → same X
%     4. den_onlyif → leq(X, de) ∧ leq(X, eE)
%     5. leq_trans: leq(X, de) ∧ leq(de, wE) → leq(X, wE)
%     6. disj_downward(wE ⊥ eE) → disjoint(X, X)
%     7. disj_irrefl → contradiction
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').

fof(odrl095, conjecture,
    ![Omega]: ~( satisfies(Omega, germany, isPartOf)
              & satisfies(Omega, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
