%--------------------------------------------------------------------------
% File     : ODRL061-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict: eq(marketing) ∩ eq(customerManagement) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3, Definition 5
% Category : basic
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand dpv:Marketing ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand dpv:CustomerManagement ] ] .
%
% Denotation analysis:
%   ⟦eq(mkt)⟧={marketing}, ⟦eq(cm)⟧={customerManagement}
%   disjoint(marketing, customerManagement) [d_0083] → ∅
%
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl061, conjecture,
    ![X]: ~( in_denotation(X, marketing, eq)
           & in_denotation(X, customerManagement, eq) )).
%--------------------------------------------------------------------------
