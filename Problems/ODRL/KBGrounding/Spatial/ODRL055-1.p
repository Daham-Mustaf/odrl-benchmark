%--------------------------------------------------------------------------
% File     : ODRL055-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption refuted: hasPart(germany) ⊄ hasPart(europe)
% Expected : CounterSatisfiable
% Verdict  : Refuted
% Paper    : Definition 7
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:germany ] .
%   c2: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] .
%
% Formal:
%   Counterexample: germany
%   leq(germany,germany)  [reflexivity] → germany ∈ ⟦hasPart(germany)⟧
%   leq(europe,germany)   is NOT in KB   → germany ∉ ⟦hasPart(europe)⟧
%   → ⟦c1⟧ ⊄ ⟦c2⟧  →  Refuted
%
% Notes    : Paired with ODRL054: hasPart subsumption is strictly one-directional.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl055, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & ~in_denotation(X, europe, hasPart) )).
%--------------------------------------------------------------------------
