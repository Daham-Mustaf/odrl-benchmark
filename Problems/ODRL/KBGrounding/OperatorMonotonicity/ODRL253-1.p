%--------------------------------------------------------------------------
% File     : ODRL253-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Counterexample — eq Is Non-Monotone
% Expected : Theorem
% Verdict  : NonMonotone
% Paper    : Counterexample — eq Is Non-Monotone
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand geo:bavaria ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand geo:germany ] ] .
%
% Formal test:
%   eq is non-monotone: leq(bavaria, germany) but eq(bav) ⊄ eq(de).
%   %   Positive: in_den(bavaria, bavaria, eq) [den_eq_if: bav = bav]
%   %   Negative: ~in_den(bavaria, germany, eq) [den_eq_onlyif: bav = de → ⊥ by UNA]
%   %   Tests: proof by contradiction using UNA ($distinct) for negative membership.
%
% One-liner : eq non-monotone: bav ∈ eq(bav) ∧ bav ∉ eq(de) despite bav ≤ de
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl253, conjecture,
    ?[X]: ( in_denotation(X, bavaria, eq)
          & ~in_denotation(X, germany, eq) )).

%--------------------------------------------------------------------------