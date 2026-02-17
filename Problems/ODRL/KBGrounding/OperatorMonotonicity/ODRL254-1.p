%--------------------------------------------------------------------------
% File     : ODRL254-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Counterexample — neq Is Non-Monotone
% Expected : Theorem
% Verdict  : NonMonotone
% Paper    : Counterexample — neq Is Non-Monotone
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:neq ;
%   %         odrl:rightOperand geo:bavaria ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:neq ;
%   %         odrl:rightOperand geo:germany ] ] .
%
% Formal test:
%   neq is non-monotone: leq(bav, de) but neq(bav) ⊄ neq(de).
%   %   Positive: in_den(germany, bavaria, neq) [den_neq_if: de ≠ bav by UNA]
%   %   Negative: ~in_den(germany, germany, neq) [den_neq_onlyif: de ≠ de → ⊥]
%   %   Tests: neq non-monotonicity via UNA-based positive + self-equality negative.
%
% One-liner : neq non-monotone: de ∈ neq(bav) ∧ de ∉ neq(de) despite bav ≤ de
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl254, conjecture,
    ?[X]: ( in_denotation(X, bavaria, neq)
          & ~in_denotation(X, germany, neq) )).

%--------------------------------------------------------------------------