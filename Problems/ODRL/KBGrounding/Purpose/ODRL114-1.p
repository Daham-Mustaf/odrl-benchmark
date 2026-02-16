%--------------------------------------------------------------------------
% File     : ODRL114-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : AND-Compatible: purpose ✓ ∧ spatial ✓ → Compatible
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 6 (AND)
% Category : composition
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:Marketing ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:Europe ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand dpv:Advertising ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:Germany ] ] .
%
% Denotation analysis:
%   V_purpose=Compatible(adv≤mkt), V_spatial=Compatible(de≤eu) → AND=Compatible
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl114, conjecture,
    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)
             & in_denotation(Xp, advertising, eq) )
    & ?[Xs]: ( in_denotation(Xs, europe, isPartOf)
             & in_denotation(Xs, germany, eq) ) )).
%--------------------------------------------------------------------------
