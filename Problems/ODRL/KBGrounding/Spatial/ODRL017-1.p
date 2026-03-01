%--------------------------------------------------------------------------
% File     : ODRL017-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: neq(germany) ∩ eq(germany) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3 (eq/neq), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:neq ;
%         odrl:rightOperand geo:germany ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:germany ] ] .
%
% Formal:
%   ⟦neq(germany)⟧ = C \ {germany},  ⟦eq(germany)⟧ = {germany}
%   X=germany ∧ X≠germany  →  direct contradiction  →  ∅
%
% Notes    : Self-negation pattern. Purely propositional — no KB needed.
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl017, conjecture,
    ![X]: ~( in_denotation(X, germany, neq)
           & in_denotation(X, germany, eq) )).
%--------------------------------------------------------------------------
