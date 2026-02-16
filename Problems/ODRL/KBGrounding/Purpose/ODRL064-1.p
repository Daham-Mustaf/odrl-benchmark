%--------------------------------------------------------------------------
% File     : ODRL064-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: neq(marketing) ∩ neq(customerManagement) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3, Definition 5
% Category : basic
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:neq ;
%         odrl:rightOperand dpv:Marketing ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:neq ;
%         odrl:rightOperand dpv:CustomerManagement ] ] .
%
% Denotation analysis:
%   C\{mkt} ∩ C\{cm} = C\{mkt,cm} ≠ ∅ (|C|=95)
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl064, conjecture,
    ?[X]: ( in_denotation(X, marketing, neq)
          & in_denotation(X, customerManagement, neq) )).
%--------------------------------------------------------------------------
