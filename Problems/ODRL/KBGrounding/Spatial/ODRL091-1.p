%--------------------------------------------------------------------------
% File     : ODRL091-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Runtime witness: Compatible verdict → satisfying context
% Expected : Theorem
% Verdict  : Sound
% Paper    : Definition 10 — Runtime Witness for Compatible Verdict
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:europe ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:germany ] ] .
%
% Denotation analysis:
%   Static: Compatible (witness: germany ∈ both denotations).
%   Runtime: assigns(ω, germany) → denotation_to_satisfaction
%   → satisfies(ω, europe, isPartOf) ∧ satisfies(ω, germany, eq).
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').

fof(runtime_context_091, axiom, assigns(omega091, germany)).

fof(odrl091, conjecture,
    ( satisfies(omega091, europe, isPartOf)
    & satisfies(omega091, germany, eq) )).
%--------------------------------------------------------------------------
