%--------------------------------------------------------------------------
% File     : ODRL073-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: hasPart(advertising) ∩ hasPart(directMarketing) — common ancestor
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
%         odrl:operator odrl:hasPart ;
%         odrl:rightOperand dpv:Advertising ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:hasPart ;
%         odrl:rightOperand dpv:DirectMarketing ] ] .
%
% Denotation analysis:
%   Common ancestor: marketing, purpose. Witness: marketing
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl073, conjecture,
    ?[X]: ( in_denotation(X, advertising, hasPart)
          & in_denotation(X, directMarketing, hasPart) )).
%--------------------------------------------------------------------------
