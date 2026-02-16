%--------------------------------------------------------------------------
% File     : ODRL012-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: eq(germany) ∩ eq(france) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3, Definition 5
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
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:france ] ] .
%
% Denotation analysis:
%   ⟦eq(germany)⟧={germany}, ⟦eq(france)⟧={france}, germany≠france (UNA) → ∅
%
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl012, conjecture,
    ![X]: ~( in_denotation(X, germany, eq)
           & in_denotation(X, france, eq) )).
%--------------------------------------------------------------------------
