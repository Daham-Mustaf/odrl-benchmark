%--------------------------------------------------------------------------
% File     : ODRL089-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict: isAllOf({mkt,adv}) ⊆ ↓mkt, isNoneOf({mkt}) excludes ↓mkt
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3, Definition 5
% Category : set
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   isAllOf({marketing, advertising}) ∩ isNoneOf({marketing})
%
% Denotation analysis:
%   ⟦isAllOf⟧=↓adv ⊆ ↓mkt, isNoneOf excludes ↓mkt → ∅
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(l089a_1, axiom, in_value_list(marketing, all089)).
fof(l089a_2, axiom, in_value_list(advertising, all089)).
fof(l089b_1, axiom, in_value_list(marketing, none089)).

fof(odrl089, conjecture,
    ![X]: ~( in_denotation_set(X, all089, isAllOf)
           & in_denotation_set(X, none089, isNoneOf) )).
%--------------------------------------------------------------------------
