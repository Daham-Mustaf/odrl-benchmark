%--------------------------------------------------------------------------
% File     : ODRL060-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: eq(marketing) ∩ eq(marketing) — identity
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
%         odrl:operator odrl:eq ;
%         odrl:rightOperand dpv:Marketing ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand dpv:Marketing ] ] .
%
% Denotation analysis:
%   ⟦eq(marketing)⟧={marketing} ∩ ⟦eq(marketing)⟧={marketing} = {marketing} ≠ ∅
%
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl060, conjecture,
    ?[X]: ( in_denotation(X, marketing, eq)
          & in_denotation(X, marketing, eq) )).
%--------------------------------------------------------------------------
