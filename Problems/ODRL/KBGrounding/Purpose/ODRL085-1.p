%--------------------------------------------------------------------------
% File     : ODRL085-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: isAllOf × isAnyOf with overlap
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAllOf/isAnyOf), Definition 5
% Category : set
%
% ODRL Policy (Turtle):
%   isAllOf({marketing, advertising}) ∩ isAnyOf({advertising, directMarketing})
%
% Denotation analysis:
%   ⟦isAllOf⟧=↓adv, ⟦isAnyOf⟧=↓adv∪↓directMkt. Witness: advertising
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(l085a_1, axiom, in_value_list(marketing, all085)).
fof(l085a_2, axiom, in_value_list(advertising, all085)).
fof(l085b_1, axiom, in_value_list(advertising, any085)).
fof(l085b_2, axiom, in_value_list(directMarketing, any085)).

fof(odrl085, conjecture,
    ?[X]: ( in_denotation_set(X, all085, isAllOf)
          & in_denotation_set(X, any085, isAnyOf) )).
%--------------------------------------------------------------------------
