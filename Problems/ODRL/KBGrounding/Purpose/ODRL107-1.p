%--------------------------------------------------------------------------
% File     : ODRL107-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Counterintuitive: hasPart(marketing) ⊆ hasPart(advertising)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 7 (hasPart contravariance)
% Category : subsumption
%
% ODRL Policy (Turtle):
%   c1: hasPart(marketing), c2: hasPart(advertising)
%
% Denotation analysis:
%   ⟦hasPart(mkt)⟧ = {mkt, purpose}
%   ⟦hasPart(adv)⟧ = {adv, mkt, purpose}
%   {mkt,purpose} ⊆ {adv,mkt,purpose} → Confirmed (counterintuitive!)
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl107, conjecture,
    ![X]: ( in_denotation(X, marketing, hasPart)
          => in_denotation(X, advertising, hasPart) )).
%--------------------------------------------------------------------------
