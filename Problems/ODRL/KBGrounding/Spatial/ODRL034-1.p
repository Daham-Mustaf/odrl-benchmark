%--------------------------------------------------------------------------
% File     : ODRL034-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Redundancy: eq(germany) ⊆ isPartOf(westernEurope)
% Expected : Theorem
% Verdict  : Subsumption
% Paper    : Definition 7, policy simplification
%
% ODRL Policy (Turtle):
%   c1: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:eq ;
%     odrl:rightOperand geo:germany ] .
%
%   c2: [
%     odrl:leftOperand odrl:spatial ;
%     odrl:operator    odrl:isPartOf ;
%     odrl:rightOperand geo:westernEurope ] .
%
% Formal:
%   ⟦eq(germany)⟧ = {germany}
%   leq(germany, westernEurope)  [direct edge in GEO]
%   → germany ∈ ⟦isPartOf(westernEurope)⟧
%   → isPartOf(wE) is redundant in ∧-conjunction with eq(germany)
%
% Notes    : The stricter eq constraint makes the weaker isPartOf constraint redundant.
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl034, conjecture,
    ![X]: ( in_denotation(X, germany, eq)
          => in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
