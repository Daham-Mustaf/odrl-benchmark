%--------------------------------------------------------------------------
% File     : ODRL141-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Edge Case — Single-Concept KB (Degenerate)
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Edge Case — Single-Concept KB (Degenerate)
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand min:universe ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand min:universe ] ] .
%
% Formal test:
%   Degenerate KB: only concept is universe, leq(universe, universe).
%   %   isPartOf(universe) = {universe}, eq(universe) = {universe}.
%   %   → trivially Compatible. Tests boundary case.
%
% One-liner : Degenerate: single-concept KB → trivially compatible
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
% --- Minimal KB: single concept "universe" ---
fof(min_root, axiom, concept(universe)).
fof(min_refl, axiom, leq(universe, universe)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl141, conjecture,
    ?[X]: ( in_denotation(X, universe, isPartOf)
          & in_denotation(X, universe, eq) )).

%--------------------------------------------------------------------------