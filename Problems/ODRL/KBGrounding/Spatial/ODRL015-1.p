%--------------------------------------------------------------------------
% File     : ODRL015-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: hasPart(germany) ∩ eq(poland) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3, Definition 5, Lemma 1
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:hasPart ;
%         odrl:rightOperand geo:germany ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:poland ] ] .
%
% Denotation analysis:
%   disj(eE,wE) → disj(poland,germany) → poland ∉ ⟦hasPart(de)⟧ → ∅
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl015, conjecture,
    ![X]: ~( in_denotation(X, germany, hasPart)
           & in_denotation(X, poland, eq) )).
%--------------------------------------------------------------------------
