%--------------------------------------------------------------------------
% File     : ODRL031-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption refuted: isPartOf(europe) ⊄ isPartOf(germany)
% Expected : CounterSatisfiable
% Verdict  : Refuted
% Paper    : Definition 7
%
% ODRL Policy (Turtle):
%   c1: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isPartOf ;
%     odrl:rightOperand geo:europe ] .
%
%   c2: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isPartOf ;
%     odrl:rightOperand geo:germany ] .
%
% Formal:
%   Counterexample: france
%   leq(france, westernEurope) → leq(france, europe)  → france ∈ ⟦c1⟧
%   leq(france, germany) is NOT derivable              → france ∉ ⟦c2⟧
%   (france and germany are distinct siblings under wE)
%
% Notes    : Paired with ODRL030: subsumption is strictly one-directional.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl031, conjecture,
    ![X]: ( in_denotation(X, europe, isPartOf)
          => in_denotation(X, germany, isPartOf) )).
%--------------------------------------------------------------------------
