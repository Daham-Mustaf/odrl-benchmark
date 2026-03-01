%--------------------------------------------------------------------------
% File     : ODRL035-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict propagation: c1⊑c2 ∧ conflict(c2,c3) → conflict(c1,c3)
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Lemma 2 (Conflict Propagation)
%
% ODRL Policy (Turtle):
%   c1: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isPartOf ;
%     odrl:rightOperand geo:germany ] .
%
%   c2: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isPartOf ;
%     odrl:rightOperand geo:easternEurope ] .
%
% Formal:
%   ODRL030: isPartOf(germany) ⊆ isPartOf(westernEurope)  [c1⊑c2]
%   ODRL013: conflict(isPartOf(wE), isPartOf(eE))       [c2 conflict c3]
%   Lemma 2: c1⊑c2 ∧ conflict(c2,c3) → conflict(c1,c3)
%   → isPartOf(germany) ∩ isPartOf(easternEurope) = ∅
%
% Notes    : Combines ODRL030 (subsumption) and ODRL013 (conflict) in one proof.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl035, conjecture,
    ![X]: ~( in_denotation(X, germany, isPartOf)
           & in_denotation(X, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
