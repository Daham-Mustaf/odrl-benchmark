%--------------------------------------------------------------------------
% File     : ODRL069-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : NOT partial overlap: eq(germany) ⊆ isPartOf(wE) → full subsumption
% Expected : Theorem
% Verdict  : Full-Subsumption
% Paper    : Refinement Conflict Refuted
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:germany ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:westernEurope ] ] .
%
% Denotation analysis:
%   ⟦eq(de)⟧ = {de} ⊆ ↓wE = ⟦isPartOf(wE)⟧
%   Three-part test fails at part 2:
%     X: eq(de) ∩ isPartOf(wE) → germany ✓
%     Y: eq(de) \ isPartOf(wE) → NO witness! (de ≤ wE by h_0017)
%     Z: isPartOf(wE) \ eq(de) → france ✓
%   → NOT partial overlap; this is full subsumption (cf. ODRL034)
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl069, conjecture,
    ~( ?[Y]: ( in_denotation(Y, germany, eq)
            & ~in_denotation(Y, westernEurope, isPartOf) ) )).
%--------------------------------------------------------------------------
