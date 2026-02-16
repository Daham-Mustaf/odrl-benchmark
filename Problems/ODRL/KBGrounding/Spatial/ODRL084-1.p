%--------------------------------------------------------------------------
% File     : ODRL084-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption preservation: isPartOf(dE) ⊆ isPartOf(europe)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Corollary 1 — Subsumption Preservation
%
% ODRL Policy (Turtle):
%   c1: [ odrl:operator odrl:isPartOf ; odrl:rightOperand iso:dE ] .
%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .
%
% Denotation analysis:
%   ⟦isPartOf(dE)⟧ ⊆ ⟦isPartOf(europe)⟧ in ISO3166
%   leq(dE, europe) [ISO3166] → transitivity → subsumption
%   Tests Corollary 1: subsumption preserved under alignment.
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').

fof(odrl084, conjecture,
    ![X]: ( in_denotation(X, dE, isPartOf)
          => in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
