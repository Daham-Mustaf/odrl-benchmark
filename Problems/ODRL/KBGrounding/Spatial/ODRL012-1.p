%--------------------------------------------------------------------------
% File     : ODRL012-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: eq(germany) ∩ eq(france) = ∅ [UNA]
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3, Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:germany ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:france ] ] .
%
% Formal:
%   ⟦eq(germany)⟧ = {germany},  ⟦eq(france)⟧ = {france}
%   germany ≠ france  [UNA: $distinct in GEO000-0.ax]
%   → intersection = ∅ → Conflict
%
% Notes    : Simplest conflict: two distinct singleton denotations.
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl012, conjecture,
    ![X]: ~( in_denotation(X, germany, eq)
           & in_denotation(X, france, eq) )).
%--------------------------------------------------------------------------
