%--------------------------------------------------------------------------
% File     : ODRL065-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Non-redundant: isPartOf(europe) ⊄ neq(germany)
% Expected : Theorem
% Verdict  : Non-Redundant
% Paper    : Redundancy Refuted
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:rule a odrl:Permission ;
%     odrl:constraint [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] ;
%     odrl:constraint [ odrl:operator odrl:neq ; odrl:rightOperand geo:germany ] .
%
% Denotation analysis:
%   ⟦isPartOf(eu)⟧ ⊄ ⟦neq(de)⟧: germany ∈ ⟦isPartOf(eu)⟧ but germany ∉ ⟦neq(de)⟧
%   → neq(germany) is NOT redundant; it genuinely restricts the rule
%   (removes exactly germany from the europe scope)
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl065, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & ~in_denotation(X, germany, neq) )).
%--------------------------------------------------------------------------
