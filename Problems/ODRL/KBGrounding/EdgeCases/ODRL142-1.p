%--------------------------------------------------------------------------
% File     : ODRL142-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Edge Case — Root-Level Conflict (Large KB Loaded)
% Expected : CounterSatisfiable
% Verdict  : Conflict
% Paper    : Edge Case — Root-Level Conflict (Large KB Loaded)
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand geo:europe ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:neq ;
%   %         odrl:rightOperand geo:europe ] ] .
%
% Formal test:
%   eq(europe) ∩ neq(europe) = ∅ — trivial even with 24-concept KB.
%   %   Tests: loading many concepts doesn't disrupt simple reasoning.
%
% One-liner : Root-level eq/neq conflict with full KB loaded
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl142, conjecture,
    ?[X]: ( in_denotation(X, europe, eq)
          & in_denotation(X, europe, neq) )).

%--------------------------------------------------------------------------