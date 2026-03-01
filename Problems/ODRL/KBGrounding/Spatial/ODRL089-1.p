%--------------------------------------------------------------------------
% File     : ODRL089-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Upward asymmetry: alignment data without theory is inert
% Expected : Theorem
% Verdict  : Unknown
% Paper    : Proposition 2(2) — Upward Asymmetry: Data Without Theory
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand iso:dE ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand iso:pL ] ] .
%
% Denotation analysis:
%   Both KBs loaded + ground alignment data, but NO alignment theory.
%   GEO: disjoint(germany, poland) derivable via disj_downward.
%   ALIGN-GEO-ISO: align(germany, dE), align(poland, pL) present.
%   MISSING: ALIGN000-0.ax (align_disj_forward rule).
%   Without the theory, align/2 facts cannot bridge GEO→ISO.
%   disjoint(dE, pL) is NOT derivable → Unknown.
%   Compare ODRL081 (adds ALIGN_THEORY → Conflict in 0.1s).
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl089, conjecture,
    ?[X]: ( in_denotation(X, dE, isPartOf)
          & in_denotation(X, pL, isPartOf) )).
%--------------------------------------------------------------------------
