%--------------------------------------------------------------------------
% File     : ODRL087-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Aligned compatible: isAnyOf({dE, fR}) ∩ isPartOf(europe) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf), Proposition 2(1)
%
% ODRL Policy (Turtle):
%   Dataspace A (GEO): permission spatial isAnyOf (germany france)
%   Dataspace B (ISO): prohibition spatial isPartOf europe
%   Via alignment: isAnyOf({dE, fR}) tested against isPartOf(europe)
%
% Denotation analysis:
%   ⟦isAnyOf({dE,fR})⟧ = ↓dE ∪ ↓fR ⊆ ↓europe = ⟦isPartOf(europe)⟧
%   Witness: dE ∈ ↓dE ∩ ↓europe.
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').

fof(list_087_1, axiom, in_value_list(dE, isoRegions087)).
fof(list_087_2, axiom, in_value_list(fR, isoRegions087)).
fof(list_isoRegions087_closed, axiom,
    ![G]: (in_value_list(G, isoRegions087) => (G = dE | G = fR))).

fof(odrl087, conjecture,
    ?[X]: ( in_denotation_set(X, isoRegions087, isAnyOf)
          & in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
