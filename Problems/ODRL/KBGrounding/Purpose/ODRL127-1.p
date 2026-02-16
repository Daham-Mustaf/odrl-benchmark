%--------------------------------------------------------------------------
% File     : ODRL127-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Sibling leaves: hasPart upward finds common parent sellProducts
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (leaf eq × leaf eq siblings)
% Category : edge
%
% ODRL Policy (Turtle):
%   Two leaves under same parent — but using hasPart (upward).
%
% Denotation analysis:
%   ⟦hasPart(sellDataToThirdParties)⟧ ∩ ⟦hasPart(sellInsightsFromData)⟧
%   Both under sellProducts. Witness: sellProducts
%
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl127, conjecture,
    ?[X]: ( in_denotation(X, sellDataToThirdParties, hasPart)
          & in_denotation(X, sellInsightsFromData, hasPart) )).
%--------------------------------------------------------------------------
