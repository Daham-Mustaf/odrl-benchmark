%--------------------------------------------------------------------------
% File     : ODRL037-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption refuted: neq(germany) ⊄ isPartOf(westernEurope)
% Expected : CounterSatisfiable
% Verdict  : Refuted
% Paper    : Definition 7
%
% ODRL Policy (Turtle):
%   c1: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:neq ;
%     odrl:rightOperand geo:germany ] .
%
%   c2: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isPartOf ;
%     odrl:rightOperand geo:westernEurope ] .
%
% Formal:
%   Counterexample: poland
%   poland ≠ germany  [UNA]           → poland ∈ ⟦neq(germany)⟧
%   ¬leq(poland,wE)  [GEO axiom]      → poland ∉ ⟦isPartOf(wE)⟧
%
% Notes    : Paired with ODRL036: neq is much broader than isPartOf.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl037, conjecture,
    ![X]: ( in_denotation(X, germany, neq)
          => in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
