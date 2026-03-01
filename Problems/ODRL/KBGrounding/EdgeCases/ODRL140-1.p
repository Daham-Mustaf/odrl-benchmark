%--------------------------------------------------------------------------
% File     : ODRL140-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Definition 5 — Tautological Self-Conflict (eq ∩ neq)
% Expected : CounterSatisfiable
% Verdict  : Conflict
% Paper    : Definition 5 — Tautological Self-Conflict (eq ∩ neq)
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand geo:germany ] ] .
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
%   eq(de) = {de}, neq(de) = {X ≠ de} → intersection = ∅.
%   %   Tautological conflict: same concept with contradictory operators.
%
% One-liner : Tautological conflict: eq(de) ∩ neq(de) = ∅
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl140, conjecture,
    ?[X]: ( in_denotation(X, germany, eq)
          & in_denotation(X, germany, neq) )).

%--------------------------------------------------------------------------