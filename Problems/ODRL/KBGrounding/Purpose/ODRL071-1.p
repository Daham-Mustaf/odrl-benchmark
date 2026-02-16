%--------------------------------------------------------------------------
% File     : ODRL071-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict: hasPart(advertising) ∩ eq(fraudPrevention) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3, Definition 5, Lemma 1
% Category : basic
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:hasPart ;
%         odrl:rightOperand dpv:Advertising ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand dpv:FraudPreventionAndDetection ] ] .
%
% Denotation analysis:
%   ⟦hasPart(adv)⟧={adv,marketing,purpose}
%   fraudPrevention ≤ enforceSecurity, disjoint(enforceSecurity, marketing)
%   fraudPrevention ∉ {adv, marketing, purpose}… but purpose is root!
%   Actually: purpose IS in hasPart(adv), and eq(fraud)={fraud}.
%   fraud ∉ {adv, mkt, purpose} → ∅ (needs UNA for distinct from purpose)
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl071, conjecture,
    ![X]: ~( in_denotation(X, advertising, hasPart)
           & in_denotation(X, fraudPreventionAndDetection, eq) )).
%--------------------------------------------------------------------------
