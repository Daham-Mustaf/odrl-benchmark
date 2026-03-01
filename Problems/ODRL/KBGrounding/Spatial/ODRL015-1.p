%--------------------------------------------------------------------------
% File     : ODRL015-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: hasPart(germany) ∩ eq(poland) = ∅ [Lemma 1]
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3, Definition 5, Lemma 1
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:hasPart ;
%         odrl:rightOperand geo:germany ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:poland ] ] .
%
% Formal:
%   disj(easternEurope, westernEurope)  +  disj_downward
%   → disj(poland, germany)         [de ≤ wE, pl ≤ eE]
%   disj_order_consistency: leq(germany, poland) → ¬disj(germany,poland)
%   But disj(germany,poland) holds  → ¬leq(germany,poland)
%   → poland ∉ ⟦hasPart(germany)⟧  → ∅
%
% Notes    : Requires Lemma 1 (disj_order_consistency). Harder than ODRL012.
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl015, conjecture,
    ![X]: ~( in_denotation(X, germany, hasPart)
           & in_denotation(X, poland, eq) )).
%--------------------------------------------------------------------------
