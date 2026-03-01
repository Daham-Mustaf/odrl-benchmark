%--------------------------------------------------------------------------
% File     : ODRL145-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Edge Case — Query on Non-Existent Concept
% Expected : CounterSatisfiable
% Verdict  : Unknown
% Paper    : Edge Case — Query on Non-Existent Concept
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:phantomConcept ] ] .
%
% Formal test:
%   phantomConcept is NOT declared as concept/1 in any KB.
%   %   den_isPartOf_if requires concept(G) — won't fire.
%   %   No axiom produces in_denotation(_, phantomConcept, _).
%   %   Prover cannot prove or refute → Unknown.
%
% One-liner : Non-existent concept: no concept/1 → satisfaction unknown
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl145, conjecture,
    ?[X]: in_denotation(X, phantomConcept, isPartOf)).

%--------------------------------------------------------------------------