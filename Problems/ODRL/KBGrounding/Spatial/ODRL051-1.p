%--------------------------------------------------------------------------
% File     : ODRL051-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Root reachability: hasPart(germany) ∩ eq(world) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (hasPart)
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
%         odrl:rightOperand geo:world ] ] .
%
% Denotation analysis:
%   Witness: world (3 transitivity steps: de→wE→eu→world)
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl051, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, world, eq) )).
%--------------------------------------------------------------------------
